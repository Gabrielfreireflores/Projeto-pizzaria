from psycopg.errors import ForeignKeyViolation, UniqueViolation

from app.repositories.funcionario_repository import buscar_funcionario_por_usuario as buscar_funcionario_repository
from app.repositories.produto_repository import criar_produto as criar_produto_repository
from app.repositories.produto_repository import listar_produtos as listar_produtos_repository
from app.schemas.produto_schema import validar_produto as validar_produto_schema

from app.repositories.produto_repository import atualizar_produto as atualizar_produto_repository
from app.repositories.produto_repository import excluir_produto as excluir_produto_repository


class ProdutoDuplicado(ValueError):
    """Já existe um produto com o mesmo nome e tamanho."""


def listar_produtos():
    produtos = {}

    for linha in listar_produtos_repository():
        identificador = linha[0]

        if identificador not in produtos:
            produtos[identificador] = {
                'id_produto': identificador,
                'nome': linha[1],
                'tamanho': linha[2],
                'preco': linha[3],
                'disponivel': linha[4],
                'foto': linha[5],
                'descricao': linha[12],
                'categoria': {
                    'id_categoria': linha[6],
                    'nome': linha[7],
                },
                'ingredientes': [],
            }

        if linha[8] is not None:
            produtos[identificador]['ingredientes'].append({
                'id_ingrediente': linha[8],
                'nome': linha[9],
                'quantidade_necessaria': linha[10],
                'unidade_medida': linha[11],
            })

    return list(produtos.values())


def criar_produto(data: dict, id_usuario: int):
    funcionario = buscar_funcionario_repository(id_usuario)
    if (funcionario is None or not funcionario[0]
            or funcionario[1].strip().casefold() not in ('funcionario', 'funcionário')
            or funcionario[2] is None):
        raise PermissionError('Acesso exclusivo de funcionário ativo.')

    produto = validar_produto_schema(data)

    if data.get("foto"):
        produto["foto"] = data["foto"]

    try:
        resultado = criar_produto_repository(produto)
    except ForeignKeyViolation:
        raise ValueError('Categoria ou ingrediente inexistente.') from None
    except UniqueViolation:
        raise ProdutoDuplicado('Já existe produto com esse nome e tamanho.') from None

    return {
        'id_produto': resultado[0],
        'nome': resultado[1],
        'tamanho': resultado[2],
        'preco': resultado[3],
        'id_categoria': resultado[4],
        'disponivel': resultado[5],
        "foto": resultado[6],
        'descricao': resultado[7],
        'ingredientes': produto['ingredientes'],
    }

class ProdutoNaoEncontrado(LookupError):
    """O produto informado não existe."""


class ProdutoEmUso(ValueError):
    """O produto já aparece em pedidos e não pode ser excluído."""

def _exigir_funcionario(id_usuario: int):
    funcionario = buscar_funcionario_repository(id_usuario)
    if (funcionario is None or not funcionario[0]
            or funcionario[1].strip().casefold() not in ('funcionario', 'funcionário')
            or funcionario[2] is None):
        raise PermissionError('Acesso exclusivo de funcionário ativo.')


def atualizar_produto(id_produto: int, data: dict, id_usuario: int):
    _exigir_funcionario(id_usuario)
    produto = validar_produto_schema(data)
    if data.get("foto"):
        produto["foto"] = data["foto"]

    try:
        resultado = atualizar_produto_repository(id_produto, produto)
    except ForeignKeyViolation:
        raise ValueError('Categoria ou ingrediente inexistente.') from None
    except UniqueViolation:
        raise ProdutoDuplicado('Já existe produto com esse nome e tamanho.') from None
    if resultado is None:
        raise ProdutoNaoEncontrado('Produto não encontrado.')

    return {
        'id_produto': resultado[0],
        'nome': resultado[1],
        'tamanho': resultado[2],
        'preco': resultado[3],
        'id_categoria': resultado[4],
        'disponivel': resultado[5],
        "foto": resultado[6],
        'descricao': resultado[7],
        'ingredientes': produto['ingredientes'],
    }


def excluir_produto(id_produto: int, id_usuario: int):
    _exigir_funcionario(id_usuario)
    try:
        removido = excluir_produto_repository(id_produto)
    except ForeignKeyViolation:
        raise ProdutoEmUso(
            'Este produto já foi usado em pedidos e não pode ser excluído. '
            'Marque-o como indisponível.'
        ) from None
    if not removido:
        raise ProdutoNaoEncontrado('Produto não encontrado.')
