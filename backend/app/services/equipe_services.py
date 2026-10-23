from psycopg.errors import ForeignKeyViolation, UniqueViolation
from werkzeug.security import generate_password_hash

from app.repositories import equipe_repository as repo
from app.schemas.equipe_schema import validar_funcionario
from app.services.permissoes import exigir_funcionario_ativo


class MembroNaoEncontrado(LookupError):
    """O funcionário informado não existe."""


class EmailDuplicado(ValueError):
    """Já existe um usuário com esse e-mail."""


class MembroEmUso(ValueError):
    """O funcionário já aceitou pedidos e não pode ser excluído."""


def _formatar(linha):
    return {
        'id_funcionario': linha[0], 'nome': linha[1], 'cpf': linha[2], 'cargo': linha[3],
        'telefone': linha[4], 'email': linha[5], 'ativo': linha[6],
    }


def listar_equipe(id_usuario: int):
    exigir_funcionario_ativo(id_usuario)
    return [_formatar(linha) for linha in repo.listar_equipe()]


def criar_membro(data: dict, id_usuario: int):
    exigir_funcionario_ativo(id_usuario)
    dados = validar_funcionario(data, criando=True)
    try:
        linha = repo.criar_membro(dados, generate_password_hash(dados['senha']))
    except UniqueViolation:
        raise EmailDuplicado('Já existe um usuário com esse e-mail.') from None
    return _formatar(linha)


def atualizar_membro(id_funcionario: int, data: dict, id_usuario: int):
    exigir_funcionario_ativo(id_usuario)
    dados = validar_funcionario(data, criando=False)

    alvo = repo.buscar_id_usuario(id_funcionario)
    if alvo is None:
        raise MembroNaoEncontrado('Funcionário não encontrado.')
    if alvo == id_usuario and not dados['ativo']:
        raise ValueError('Você não pode desativar a sua própria conta.')

    senha_hash = generate_password_hash(dados['senha']) if dados.get('senha') else None
    try:
        linha = repo.atualizar_membro(id_funcionario, dados, senha_hash)
    except UniqueViolation:
        raise EmailDuplicado('Já existe um usuário com esse e-mail.') from None
    if linha is None:
        raise MembroNaoEncontrado('Funcionário não encontrado.')
    return _formatar(linha)


def excluir_membro(id_funcionario: int, id_usuario: int):
    exigir_funcionario_ativo(id_usuario)

    alvo = repo.buscar_id_usuario(id_funcionario)
    if alvo is None:
        raise MembroNaoEncontrado('Funcionário não encontrado.')
    if alvo == id_usuario:
        raise ValueError('Você não pode excluir a sua própria conta.')

    try:
        removido = repo.excluir_membro(id_funcionario)
    except ForeignKeyViolation:
        raise MembroEmUso(
            'Este funcionário já aceitou pedidos e não pode ser excluído. '
            'Desative-o na edição.'
        ) from None
    if not removido:
        raise MembroNaoEncontrado('Funcionário não encontrado.')