"""Testes estáticos e de transação simulada. Nenhum SQL chega a um banco."""
from contextlib import contextmanager
from copy import deepcopy
import importlib
import json
from pathlib import Path
import re
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

import db_admin as admin

HOST = 'ep-test.region.aws.neon.tech'


class Rows:
    def __init__(self, rows=()):
        self.rows = list(rows)

    def fetchone(self):
        return self.rows[0] if self.rows else None

    def fetchall(self):
        return self.rows


class FakeCursor:
    def __init__(self, conn):
        self.conn = conn

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def execute(self, sql, params):
        self.result = self.conn.execute(sql, params)

    def fetchone(self):
        return self.result.fetchone()


class FakeConnection:
    """Modelo limitado do contrato psycopg; não interpreta nem executa scripts SQL."""
    def __init__(self, plan, applied=False):
        self.plan = plan
        self.info = SimpleNamespace(host=HOST)
        self.pgconn = SimpleNamespace(ssl_in_use=True)
        self.target = ('neondb', 150000, True, True, True, 'public')
        self.relations = {}
        self.history = []
        self.commands = []
        self.users = []
        self.staff = []
        self.hashes = []
        self.closed = False
        self.rollbacks = 0
        self.commits = 0
        self.fail_file = None
        self.fail_staff = False
        self.lock_available = True
        if applied:
            self.relations = {name: 'r' for name in admin.APP_TABLES | {admin.JOURNAL}}
            self.relations.update({name: 'S' for name in admin.SEQUENCES})
            self.history = [(item.name, item.sha256, position, 'data-simulada')
                            for position, item in enumerate(plan, 1)]

    @contextmanager
    def transaction(self):
        snapshot = deepcopy((self.relations, self.history, self.users, self.staff))
        try:
            yield
        except BaseException:
            self.relations, self.history, self.users, self.staff = snapshot
            self.rollbacks += 1
            raise
        else:
            self.commits += 1

    def close(self):
        self.closed = True

    def cursor(self):
        return FakeCursor(self)

    def execute(self, source, params=None, **kwargs):
        self.commands.append((source, params))
        sql = ' '.join(source.split())
        if sql.startswith('SELECT current_database()'):
            return Rows([self.target])
        if sql.startswith('SELECT c.relname'):
            return Rows(self.relations.items())
        if sql.startswith('SELECT name, sha256'):
            return Rows(self.history)
        if sql.startswith('CREATE TABLE IF NOT EXISTS public._pizzaria_migrations'):
            self.relations[admin.JOURNAL] = 'r'
            return Rows()
        if sql.startswith('INSERT INTO public._pizzaria_migrations'):
            self.history.append((*params, 'data-simulada'))
            return Rows()
        for item in self.plan:
            if source == item.body:
                if item.name == self.fail_file:
                    raise RuntimeError('Falha SQL simulada: valor-sensivel')
                if item.name == 'db/schema.sql':
                    self.relations.update({name: 'r' for name in admin.BASE_TABLES})
                    self.relations.update({name: 'S' for name in admin.SEQUENCES})
                if item.name.endswith('005_bordas_por_item.sql'):
                    self.relations['item_pedido_borda'] = 'r'
                return Rows()
        if sql.startswith('SELECT has_table_privilege'):
            return Rows([(True, True, True, True)])
        if sql.startswith('SELECT 1 FROM public.usuario'):
            return Rows([(1,)] if any(user['email'].strip().lower() == params[0] for user in self.users) else [])
        if sql.startswith('SELECT 1 FROM public.funcionario'):
            return Rows([(1,)] if any(re.sub(r'\D', '', member['cpf']) == params[0] for member in self.staff) else [])
        if sql.startswith('SELECT u.senha'):
            return Rows([(value,) for value in self.hashes])
        if sql.startswith('INSERT INTO usuario '):
            self.users.append({'email': params[0], 'hash': params[1]})
            return Rows([(10, params[0])])
        if sql.startswith('INSERT INTO public.funcionario'):
            if self.fail_staff:
                raise RuntimeError('Falha simulada no funcionário')
            self.staff.append({'id_usuario': params[0], 'cpf': params[2]})
            return Rows([(20,)])
        if sql.startswith('SELECT pg_try_advisory_xact_lock'):
            return Rows([(self.lock_available,)])
        if sql.startswith(('SET ', 'LOCK TABLE ')):
            return Rows()
        raise AssertionError('Operação não prevista no fake: ' + sql[:70])


@pytest.fixture(autouse=True)
def no_database(monkeypatch):
    blocked = Mock(side_effect=AssertionError('Conexões reais são proibidas nestes testes.'))
    monkeypatch.setattr(admin, 'get_connection', blocked)
    return blocked


@pytest.fixture
def plan():
    return admin.load_plan()


@pytest.fixture
def data():
    return {'nome': 'Equipe Teste', 'email': 'equipe@example.test', 'cpf': '12345678901',
            'cargo': 'Atendente', 'telefone': None, 'senha': 'Senha-somente-testes-123'}


def test_manifest_exact_order_both_005_and_no_destructive_scripts(plan):
    assert tuple(item.name for item in plan) == (
        'db/schema.sql', 'db/migrations/001_pedido_contato.sql',
        'db/migrations/002_produto_cardapio.sql', 'db/migrations/003_checkout_convidado_retirada.sql',
        'db/migrations/004_seed_cardapio_v2.sql', 'db/migrations/005_bordas_por_item.sql',
        'db/migrations/005_cliente_cpf_opcional.sql',
    )
    assert len({item.name for item in plan}) == 7
    assert not any('/008_' in item.name or '/006_' in item.name or '/007_' in item.name for item in plan)
    assert (admin.ROOT / 'db/migrations/008_remover_produtos_legados.sql').is_file()


def test_schema_explicit_transaction_and_executor_owns_commit(plan):
    for item in plan:
        assert len(re.findall(r'^BEGIN;$', item.source, re.M)) == 1
        assert len(re.findall(r'^COMMIT;$', item.source, re.M)) == 1
        assert not re.search(r'^(?:BEGIN|COMMIT);$', item.body, re.M)
        assert admin.checksum(item.source) == item.sha256


def test_checksum_is_portable_between_windows_and_linux():
    assert admin.checksum('linha\r\n') == admin.checksum('linha\n')
    assert admin.checksum('linha\n') != admin.checksum('linha modificada\n')


def copy_plan(tmp_path):
    for name in (*admin.INITIAL_FILES, 'db/migrations/manifest.json'):
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((admin.ROOT / name).read_bytes())


def test_modified_sql_rejected_before_connection(tmp_path, no_database):
    copy_plan(tmp_path)
    target = tmp_path / admin.INITIAL_FILES[4]
    target.write_bytes(target.read_bytes() + b'\n-- changed\n')
    with pytest.raises(admin.AdminError, match='Checksum'):
        admin.load_plan(tmp_path)
    no_database.assert_not_called()


@pytest.mark.parametrize('change', ['swap_005', 'remove_005', 'add_008'])
def test_changed_manifest_order_or_extra_file_rejected(tmp_path, change):
    copy_plan(tmp_path)
    path = tmp_path / 'db/migrations/manifest.json'
    manifest = json.loads(path.read_text(encoding='utf-8'))
    if change == 'swap_005':
        manifest['files'][5:7] = reversed(manifest['files'][5:7])
    elif change == 'remove_005':
        manifest['files'].pop()
    else:
        manifest['files'].append({'name': 'db/migrations/008_remover_produtos_legados.sql'})
    path.write_text(json.dumps(manifest), encoding='utf-8')
    with pytest.raises(admin.AdminError, match='ordem'):
        admin.load_plan(tmp_path)


@pytest.mark.parametrize('source', ['CREATE TABLE test();\nCOMMIT;\n',
    'BEGIN;\nCOMMIT;\nCOMMIT;\n', 'BEGIN;\nROLLBACK;\nCOMMIT;\n',
    'BEGIN;\nCOMMIT;\nSELECT 1;\n'])
def test_unreviewed_transaction_wrapper_rejected(source):
    with pytest.raises(admin.AdminError):
        admin.transaction_body(source)


def test_preflight_only_reads_and_never_creates_journal(plan):
    conn = FakeConnection(plan)
    assert admin.check_target(conn, plan, 'neondb', HOST) == 'empty'
    assert not conn.history and not conn.relations
    assert all(sql.lstrip().startswith(('SELECT ', 'SET TRANSACTION READ ONLY')) for sql, _ in conn.commands)


@pytest.mark.parametrize('problem', ['database', 'host', 'version', 'permission', 'schema',
                                     'tls', 'pooler', 'unexpected', 'untracked', 'view'])
def test_preflight_rejects_wrong_or_unsafe_target(plan, problem):
    conn = FakeConnection(plan)
    if problem == 'database':
        conn.target = ('other', *conn.target[1:])
    elif problem == 'host':
        conn.info.host = 'other.region.aws.neon.tech'
    elif problem == 'version':
        conn.target = ('neondb', 140000, *conn.target[2:])
    elif problem == 'permission':
        conn.target = (*conn.target[:4], False, 'public')
    elif problem == 'schema':
        conn.target = (*conn.target[:5], 'other')
    elif problem == 'tls':
        conn.pgconn.ssl_in_use = False
    elif problem == 'pooler':
        conn.info.host = HOST.replace('ep-test', 'ep-test-pooler')
    elif problem == 'unexpected':
        conn.relations['other_table'] = 'r'
    elif problem == 'untracked':
        conn.relations['usuario'] = 'r'
    else:
        conn.relations['usuario'] = 'v'
    with pytest.raises(admin.AdminError):
        admin.apply_initial(conn, plan, 'neondb', HOST, confirmed=True, free_confirmed=True)
    assert not any(sql.startswith('CREATE ') for sql, _ in conn.commands)


def test_initialization_journal_and_entire_plan_are_atomic_and_reapply_is_noop(plan):
    conn = FakeConnection(plan)
    applied = admin.apply_initial(conn, plan, 'neondb', HOST, confirmed=True, free_confirmed=True)
    assert applied == admin.INITIAL_FILES
    assert [(row[0], row[1], row[2]) for row in conn.history] == [
        (item.name, item.sha256, position) for position, item in enumerate(plan, 1)]
    assert all(row[3] for row in conn.history)
    assert conn.commits == 1
    count = len(conn.commands)
    assert admin.apply_initial(conn, plan, 'neondb', HOST, confirmed=True, free_confirmed=True) == ()
    assert not any(sql.startswith(('INSERT ', 'CREATE ')) for sql, _ in conn.commands[count:])


def test_concurrent_admin_operation_is_refused_before_any_write(plan):
    conn = FakeConnection(plan)
    conn.lock_available = False
    with pytest.raises(admin.AdminError, match='andamento'):
        admin.apply_initial(conn, plan, 'neondb', HOST, confirmed=True, free_confirmed=True)
    assert len(conn.commands) == 1


@pytest.mark.parametrize('position', [0, 3, 6])
def test_first_error_stops_later_files_and_rolls_back_schema_seed_and_journal(plan, position):
    conn = FakeConnection(plan)
    conn.fail_file = plan[position].name
    with pytest.raises(RuntimeError):
        admin.apply_initial(conn, plan, 'neondb', HOST, confirmed=True, free_confirmed=True)
    assert conn.rollbacks == 1 and conn.commits == 0
    assert not conn.relations and not conn.history
    executed = [sql for sql, _ in conn.commands]
    assert all(item.body not in executed for item in plan[position + 1:])


@pytest.mark.parametrize('problem', ['checksum', 'partial', 'extra', 'missing_table'])
def test_history_drift_is_never_adopted_or_reapplied(plan, problem):
    conn = FakeConnection(plan, applied=True)
    if problem == 'checksum':
        name, _, position, date = conn.history[0]
        conn.history[0] = (name, '0' * 64, position, date)
    elif problem == 'partial':
        conn.history.pop()
    elif problem == 'extra':
        conn.history.append(('db/migrations/008_remover_produtos_legados.sql', '0' * 64, 8, 'date'))
    else:
        del conn.relations['item_pedido_borda']
    with pytest.raises(admin.AdminError):
        admin.apply_initial(conn, plan, 'neondb', HOST, confirmed=True, free_confirmed=True)
    assert not any(sql.startswith(('INSERT ', 'CREATE ')) for sql, _ in conn.commands)


@pytest.mark.parametrize('confirm,free', [(False, True), (True, False), (False, False)])
def test_mutations_require_both_confirmations_before_any_query(plan, data, confirm, free):
    conn = FakeConnection(plan)
    for action in (
        lambda: admin.apply_initial(conn, plan, 'neondb', HOST, confirmed=confirm, free_confirmed=free),
        lambda: admin.bootstrap_staff(conn, plan, 'neondb', HOST, data, confirmed=confirm, free_confirmed=free),
    ):
        with pytest.raises(admin.AdminError):
            action()
    assert not conn.commands


def test_bootstrap_hashes_password_and_creates_both_rows_in_one_transaction(plan, data):
    conn = FakeConnection(plan, applied=True)
    conn.hashes = ['!', 'invalid-seed-marker']
    result = admin.bootstrap_staff(conn, plan, 'neondb', HOST, data, confirmed=True, free_confirmed=True)
    assert result == 20 and conn.commits == 1
    assert len(conn.users) == len(conn.staff) == 1
    assert conn.users[0]['hash'] != data['senha']
    assert admin.check_password_hash(conn.users[0]['hash'], data['senha'])
    assert all(data['senha'] not in str(params) for _, params in conn.commands)


def test_bootstrap_rolls_back_user_when_staff_insert_fails(plan, data):
    conn = FakeConnection(plan, applied=True)
    conn.fail_staff = True
    with pytest.raises(RuntimeError):
        admin.bootstrap_staff(conn, plan, 'neondb', HOST, data, confirmed=True, free_confirmed=True)
    assert not conn.users and not conn.staff and conn.rollbacks == 1


@pytest.mark.parametrize('duplicate', ['email', 'cpf'])
def test_bootstrap_detects_legacy_normalized_duplicates(plan, data, duplicate):
    conn = FakeConnection(plan, applied=True)
    if duplicate == 'email':
        conn.users = [{'email': 'EQUIPE@EXAMPLE.TEST'}]
    else:
        conn.staff = [{'cpf': '123.456.789-01'}]
    with pytest.raises(admin.AdminError, match='já cadastrado'):
        admin.bootstrap_staff(conn, plan, 'neondb', HOST, data, confirmed=True, free_confirmed=True)
    assert not any(sql.lstrip().startswith('INSERT INTO usuario ') for sql, _ in conn.commands)


def test_bootstrap_refuses_existing_authorized_staff(plan, data):
    conn = FakeConnection(plan, applied=True)
    conn.hashes = [admin.generate_password_hash('senha-de-outro-teste')]
    with pytest.raises(admin.AdminError, match='Já existe funcionário'):
        admin.bootstrap_staff(conn, plan, 'neondb', HOST, data, confirmed=True, free_confirmed=True)
    assert not conn.users


def test_bootstrap_requires_completed_initialization(plan, data):
    conn = FakeConnection(plan)
    with pytest.raises(admin.AdminError, match='Inicialize'):
        admin.bootstrap_staff(conn, plan, 'neondb', HOST, data, confirmed=True, free_confirmed=True)
    assert not conn.users


def test_plan_command_never_connects(no_database, capsys):
    assert admin.main(['plan']) == 0
    assert '005_bordas_por_item' in capsys.readouterr().out
    no_database.assert_not_called()


def test_cancelled_confirmation_never_connects(monkeypatch, no_database):
    monkeypatch.setattr('builtins.input', lambda _: 'não')
    assert admin.main(['apply', '--database', 'neondb', '--host', HOST,
                       '--execute', '--confirm-free-plan']) == 1
    no_database.assert_not_called()


def test_missing_execution_flag_never_connects(no_database):
    with pytest.raises(SystemExit) as error:
        admin.main(['apply', '--database', 'neondb', '--host', HOST, '--confirm-free-plan'])
    assert error.value.code == 2
    no_database.assert_not_called()


@pytest.mark.parametrize('field', ['--host', '--database'])
def test_secret_connection_urls_are_rejected_without_echo(field, no_database, capsys):
    args = ['check', '--host', HOST, '--database', 'neondb', '--connect', '--confirm-free-plan']
    args[args.index(field) + 1] = 'postgresql://user:nao-imprimir@host/db'
    with pytest.raises(SystemExit) as error:
        admin.main(args)
    assert error.value.code == 2
    captured = capsys.readouterr()
    assert 'nao-imprimir' not in captured.out + captured.err
    no_database.assert_not_called()


def test_cli_bootstrap_uses_hidden_confirmation_and_closes_connection(plan, data, monkeypatch, capsys):
    conn = FakeConnection(plan, applied=True)
    monkeypatch.setattr(admin, 'get_connection', lambda: conn)
    responses = iter([f'CONFIRMO BOOTSTRAP {HOST}/neondb/public', data['nome'], data['email'],
                      data['cpf'], data['cargo'], ''])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    monkeypatch.setattr(admin, 'getpass', lambda _: data['senha'])
    assert admin.main(['bootstrap', '--database', 'neondb', '--host', HOST,
                       '--execute', '--confirm-free-plan']) == 0
    assert conn.closed and len(conn.staff) == 1
    assert data['senha'] not in capsys.readouterr().out


def test_password_mismatch_never_connects(data, monkeypatch, no_database):
    responses = iter([f'CONFIRMO BOOTSTRAP {HOST}/neondb/public', data['nome'], data['email'],
                      data['cpf'], data['cargo'], ''])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    passwords = iter([data['senha'], 'diferente'])
    monkeypatch.setattr(admin, 'getpass', lambda _: next(passwords))
    assert admin.main(['bootstrap', '--database', 'neondb', '--host', HOST,
                       '--execute', '--confirm-free-plan']) == 1
    no_database.assert_not_called()


def test_unsafe_password_echo_fallback_never_connects(data, monkeypatch, no_database):
    import warnings
    responses = iter([f'CONFIRMO BOOTSTRAP {HOST}/neondb/public', data['nome'], data['email'],
                      data['cpf'], data['cargo'], ''])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    def unsafe_prompt(_):
        warnings.warn('Sem terminal seguro.', admin.GetPassWarning)
        raise AssertionError('Não deve continuar para leitura com echo.')
    monkeypatch.setattr(admin, 'getpass', unsafe_prompt)
    assert admin.main(['bootstrap', '--database', 'neondb', '--host', HOST,
                       '--execute', '--confirm-free-plan']) == 1
    no_database.assert_not_called()


def test_cli_connection_closed_and_sensitive_errors_not_printed(plan, monkeypatch, capsys):
    conn = FakeConnection(plan)
    conn.fail_file = plan[0].name
    monkeypatch.setattr(admin, 'get_connection', lambda: conn)
    monkeypatch.setattr('builtins.input', lambda _: f'CONFIRMO APPLY {HOST}/neondb/public')
    assert admin.main(['apply', '--database', 'neondb', '--host', HOST,
                       '--execute', '--confirm-free-plan']) == 1
    assert conn.closed and conn.rollbacks == 1
    assert 'valor-sensivel' not in capsys.readouterr().out


def test_importing_administration_module_does_not_connect(monkeypatch):
    import app.database
    connect = Mock(side_effect=AssertionError('Não abrir conexão ao importar.'))
    monkeypatch.setattr(app.database, 'get_connection', connect)
    importlib.reload(admin)
    connect.assert_not_called()
