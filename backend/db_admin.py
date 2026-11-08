"""Administração explícita do banco. Importar este módulo nunca abre conexão.

Uso local sem banco: python db_admin.py plan
Check/apply/bootstrap exigem opt-in; senhas são lidas apenas por getpass.
"""
import argparse
from dataclasses import dataclass
from getpass import getpass, GetPassWarning
import hashlib
import json
from pathlib import Path
import re
import warnings

from app.database import get_connection
from app.repositories.usuario_repository import criar_usuario
from app.schemas.equipe_schema import validar_funcionario
from werkzeug.security import check_password_hash, generate_password_hash


ROOT = Path(__file__).resolve().parents[1]
INITIAL_FILES = (
    'db/schema.sql',
    'db/migrations/001_pedido_contato.sql',
    'db/migrations/002_produto_cardapio.sql',
    'db/migrations/003_checkout_convidado_retirada.sql',
    'db/migrations/004_seed_cardapio_v2.sql',
    'db/migrations/005_bordas_por_item.sql',
    'db/migrations/005_cliente_cpf_opcional.sql',
)
BASE_TABLES = frozenset(('usuario', 'categoria', 'ingrediente', 'status', 'funcionario',
                         'cliente', 'endereco', 'produto', 'ingrediente_produto',
                         'pedido', 'item_pedido'))
APP_TABLES = BASE_TABLES | {'item_pedido_borda'}
SEQUENCES = {f'{table}_id_{table}_seq' for table in BASE_TABLES}
JOURNAL = '_pizzaria_migrations'
LOCK_ID = 884217301


class AdminError(Exception):
    """Mensagem administrativa segura, sem parâmetros ou exceções do banco."""


@dataclass(frozen=True)
class Migration:
    name: str
    sha256: str
    source: str
    body: str


def checksum(source):
    # Canonicalização explícita torna o checksum igual em checkout Windows/Linux.
    return hashlib.sha256(source.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def transaction_body(source):
    """Só aceita os wrappers dos sete arquivos auditados; não é executor SQL genérico.

    Retira BEGIN/COMMIT apenas em memória para o executor controlar uma única
    transação, incluindo schema, seeds e registro. Os arquivos são preservados.
    """
    lines = source.splitlines(keepends=True)
    controls = [(index, line.strip().upper()) for index, line in enumerate(lines)
                if re.fullmatch(r'\s*(?:BEGIN|COMMIT|ROLLBACK|SAVEPOINT|END)\s*;\s*', line, re.I)]
    if [value for _, value in controls] != ['BEGIN;', 'COMMIT;']:
        raise AdminError('Arquivo sem wrapper transacional auditado.')
    final = [line.strip() for line in lines if line.strip() and not line.lstrip().startswith('--')]
    if not final or final[-1].upper() != 'COMMIT;':
        raise AdminError('COMMIT deve encerrar o arquivo auditado.')
    omitted = {index for index, _ in controls}
    return ''.join(line for index, line in enumerate(lines) if index not in omitted)


def load_plan(root=ROOT):
    manifest = json.loads((root / 'db/migrations/manifest.json').read_text(encoding='utf-8'))
    entries = manifest.get('files', [])
    if (manifest.get('format') != 'sha256-utf8-lf-v1'
            or tuple(entry.get('name') for entry in entries) != INITIAL_FILES):
        raise AdminError('Manifesto inicial fora da ordem autorizada.')
    result = []
    for entry in entries:
        source = (root / entry['name']).read_bytes().decode('utf-8').replace('\r\n', '\n')
        digest = checksum(source)
        if entry.get('sha256') != digest:
            raise AdminError('Checksum divergente: ' + entry['name'])
        result.append(Migration(entry['name'], digest, source, transaction_body(source)))
    return tuple(result)


def inspect_target(conn, plan, expected_database, expected_host, schema='public'):
    """Somente SELECT: não cria tabela de histórico nem adota banco preexistente."""
    if schema != 'public':
        raise AdminError('O backend atual exige o schema public.')
    target = conn.execute("""SELECT current_database(), current_setting('server_version_num')::int,
        has_database_privilege(current_database(), 'CONNECT'),
        has_schema_privilege('public', 'USAGE'), has_schema_privilege('public', 'CREATE'),
        current_schema()""").fetchone()
    if target[0] != expected_database or target[1] < 150000:
        raise AdminError('Banco de destino ou versão PostgreSQL incompatível.')
    if not all(target[2:5]) or target[5] != schema:
        raise AdminError('Permissões CONNECT/USAGE/CREATE insuficientes.')
    if not expected_host or conn.info.host.lower() != expected_host.lower():
        raise AdminError('Host não corresponde ao projeto explicitamente autorizado.')
    if not conn.pgconn.ssl_in_use:
        raise AdminError('Conexão administrativa exige TLS.')
    if '-pooler' in conn.info.host.split('.')[0]:
        raise AdminError('Use a URL direta para administração, sem pooler.')
    relations = dict(conn.execute("""SELECT c.relname, c.relkind
        FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = 'public' AND c.relkind IN ('r','p','v','m','f','S')""").fetchall())
    allowed = APP_TABLES | SEQUENCES | {JOURNAL}
    if set(relations) - allowed:
        raise AdminError('Há objetos inesperados no schema de destino.')
    if any(kind != ('S' if name in SEQUENCES else 'r') for name, kind in relations.items()):
        raise AdminError('Tipo de objeto incompatível no schema de destino.')
    rows = []
    if JOURNAL in relations:
        rows = conn.execute('SELECT name, sha256, position, applied_at FROM public._pizzaria_migrations ORDER BY position').fetchall()
    if rows:
        expected = [(item.name, item.sha256, position) for position, item in enumerate(plan, 1)]
        actual = [(row[0], row[1], row[2]) for row in rows]
        if actual != expected or any(row[3] is None for row in rows):
            raise AdminError('Histórico incompleto, desconhecido ou checksum aplicado divergente.')
        if set(relations) != allowed:
            raise AdminError('Estrutura ausente apesar do histórico aplicado.')
        return 'applied'
    if set(relations) - {JOURNAL}:
        raise AdminError('Banco com objetos existentes sem histórico completo; não reinicializar.')
    return 'empty'


def check_target(conn, plan, expected_database, expected_host, schema='public'):
    # Autocommit garante que o context manager seja dono da transação, não um savepoint.
    conn.autocommit = True
    with conn.transaction():
        conn.execute('SET TRANSACTION READ ONLY')
        return inspect_target(conn, plan, expected_database, expected_host, schema)


def _lock_admin(conn):
    if not conn.execute('SELECT pg_try_advisory_xact_lock(%s)', (LOCK_ID,)).fetchone()[0]:
        raise AdminError('Outra operação administrativa está em andamento.')
    conn.execute("SET LOCAL lock_timeout = '5s'")
    conn.execute("SET LOCAL statement_timeout = '60s'")


def apply_initial(conn, plan, expected_database, expected_host, *, confirmed=False, free_confirmed=False):
    if not confirmed or not free_confirmed:
        raise AdminError('Confirmação explícita do destino e plano Free obrigatória.')
    conn.autocommit = True
    with conn.transaction():
        _lock_admin(conn)
        state = inspect_target(conn, plan, expected_database, expected_host)
        if state == 'applied':
            return ()
        conn.execute("""CREATE TABLE IF NOT EXISTS public._pizzaria_migrations (
            name TEXT PRIMARY KEY, sha256 CHAR(64) NOT NULL,
            position INTEGER NOT NULL UNIQUE,
            applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")
        conn.execute('SET LOCAL search_path TO public')
        applied = []
        for position, item in enumerate(plan, 1):
            # Falha interrompe imediatamente; o context manager desfaz também o histórico.
            conn.execute(item.body, prepare=False)
            conn.execute('INSERT INTO public._pizzaria_migrations (name, sha256, position) VALUES (%s, %s, %s)',
                         (item.name, item.sha256, position))
            applied.append(item.name)
        if inspect_target(conn, plan, expected_database, expected_host) != 'applied':
            raise AdminError('Verificação final de estrutura/histórico falhou; inicialização desfeita.')
        return tuple(applied)


def _supported_hash(value):
    if not isinstance(value, str) or len(value.split('$')) != 3:
        return False
    try:
        # Verifica compatibilidade do formato, não tenta descobrir a senha existente.
        check_password_hash(value, 'bootstrap-format-probe')
    except (ValueError, TypeError):
        return False
    return True


def bootstrap_staff(conn, plan, expected_database, expected_host, data, *, confirmed=False, free_confirmed=False):
    if not confirmed or not free_confirmed:
        raise AdminError('Confirmação explícita do bootstrap e plano Free obrigatória.')
    validated = validar_funcionario(data, criando=True)
    conn.autocommit = True
    with conn.transaction():
        _lock_admin(conn)
        if inspect_target(conn, plan, expected_database, expected_host) != 'applied':
            raise AdminError('Inicialize e registre todo o manifesto antes do bootstrap.')
        privileges = conn.execute("""SELECT
            has_table_privilege('public.usuario', 'SELECT') AND has_table_privilege('public.usuario', 'INSERT'),
            has_table_privilege('public.funcionario', 'SELECT') AND has_table_privilege('public.funcionario', 'INSERT'),
            has_sequence_privilege('public.usuario_id_usuario_seq', 'USAGE'),
            has_sequence_privilege('public.funcionario_id_funcionario_seq', 'USAGE')""").fetchone()
        if not all(privileges):
            raise AdminError('Permissões de bootstrap insuficientes.')
        conn.execute('SET LOCAL search_path TO public')
        conn.execute('LOCK TABLE public.usuario, public.funcionario IN SHARE ROW EXCLUSIVE MODE')
        # Também reconhece e-mail/CPF legados com caixa ou pontuação diferentes.
        if conn.execute('SELECT 1 FROM public.usuario WHERE lower(trim(email)) = %s LIMIT 1',
                        (validated['email'],)).fetchone():
            raise AdminError('E-mail já cadastrado; o bootstrap não altera contas existentes.')
        if conn.execute("SELECT 1 FROM public.funcionario WHERE regexp_replace(cpf, '[^0-9]', '', 'g') = %s LIMIT 1",
                        (validated['cpf'],)).fetchone():
            raise AdminError('CPF já cadastrado; o bootstrap não altera contas existentes.')
        hashes = conn.execute("""SELECT u.senha FROM public.usuario u
            JOIN public.funcionario f ON f.id_usuario = u.id_usuario
            WHERE u.ativo AND lower(trim(u.nome_perfil)) IN ('funcionario', 'funcionário')""").fetchall()
        if any(_supported_hash(row[0]) for row in hashes):
            raise AdminError('Já existe funcionário ativo com hash compatível; utilize a gestão da equipe.')
        password_hash = generate_password_hash(validated['senha'])
        user = criar_usuario(conn, validated['email'], password_hash, 'funcionario',
                             'Primeiro funcionário criado por comando administrativo')
        staff = conn.execute("""INSERT INTO public.funcionario (id_usuario, nome, cpf, cargo, telefone)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_funcionario""",
            (user[0], validated['nome'], validated['cpf'], validated['cargo'], validated['telefone'])).fetchone()
        return staff[0]


def _host_argument(value):
    if not re.fullmatch(r'[A-Za-z0-9.-]{1,253}', value) or '..' in value:
        raise argparse.ArgumentTypeError('Informe somente host DNS, sem URL ou credenciais.')
    return value


def _database_argument(value):
    if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_-]{0,62}', value):
        raise argparse.ArgumentTypeError('Informe somente o nome do banco, sem URL ou credenciais.')
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('plan', help='Valida manifesto/checksums localmente, sem banco.')
    for command in ('check', 'apply', 'bootstrap'):
        child = sub.add_parser(command)
        child.add_argument('--database', required=True, type=_database_argument, help='Nome esperado, nunca URL ou senha.')
        child.add_argument('--host', required=True, type=_host_argument, help='Host direto esperado do projeto, sem URL ou credenciais.')
        child.add_argument('--schema', choices=['public'], default='public')
        child.add_argument('--confirm-free-plan', action='store_true', required=True,
                           help='Confirmação manual do plano Free/cotas no painel; SQL não comprova cobrança.')
        child.add_argument('--connect' if command == 'check' else '--execute', action='store_true', required=True)
    args = parser.parse_args(argv)
    connection = None
    try:
        plan = load_plan()
        if args.command == 'plan':
            for position, item in enumerate(plan, 1):
                print(f'{position}. {item.name} SHA-256={item.sha256}')
            return 0
        data = None
        if args.command != 'check':
            phrase = f'CONFIRMO {args.command.upper()} {args.host}/{args.database}/public'
            if input(f'Para autorizar este banco, digite exatamente: {phrase}\n') != phrase:
                raise AdminError('Operação cancelada antes de abrir conexão.')
            if args.command == 'bootstrap':
                data = {key: input(label).strip() for key, label in (
                    ('nome', 'Nome: '), ('email', 'E-mail: '), ('cpf', 'CPF: '),
                    ('cargo', 'Cargo: '), ('telefone', 'Telefone (opcional): '))}
                with warnings.catch_warnings():
                    # Sem terminal seguro, recusa o fallback que exibiria a senha.
                    warnings.simplefilter('error', GetPassWarning)
                    data['senha'] = getpass('Senha: ')
                    if getpass('Confirme a senha: ') != data['senha']:
                        raise AdminError('As senhas não coincidem.')
                validar_funcionario(data, criando=True)
        connection = get_connection()
        if args.command == 'check':
            print('Destino verificado: ' + check_target(connection, plan, args.database, args.host))
        elif args.command == 'apply':
            applied = apply_initial(connection, plan, args.database, args.host, confirmed=True, free_confirmed=True)
            print(f'Inicialização concluída: {len(applied)} arquivos aplicados; nenhum seed reaplicado se já registrado.')
        else:
            bootstrap_staff(connection, plan, args.database, args.host, data, confirmed=True, free_confirmed=True)
            print('Primeiro funcionário criado. Credenciais não serão exibidas.')
        return 0
    except (AdminError, ValueError, OSError) as error:
        # Somente mensagens de validação controladas; erros de infraestrutura são genéricos.
        if isinstance(error, AdminError):
            print(str(error))
        else:
            print('Validação ou leitura local inválida; nenhuma conclusão de sucesso.')
        return 1
    except Exception:
        print('Falha administrativa. Transação interrompida; verifique o destino sem reaplicar arquivos.')
        return 1
    finally:
        if connection is not None:
            connection.close()


if __name__ == '__main__':
    raise SystemExit(main())
