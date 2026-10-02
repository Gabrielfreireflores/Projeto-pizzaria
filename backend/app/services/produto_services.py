from psycopg.errors import ForeignKeyViolation, UniqueViolation

from app.repositories.funcionario_repository import buscar_funcionario_por_usuario as buscar_funcionario_repository
from app.repositories.produto_repository import criar_produto as criar_produto_repository
from app.schemas.produto_schema import validar_produto as validar_produto_schema


class ProdutoDuplicado(ValueError):
    """Já existe um produto com o mesmo nome e tamanho."""


def criar_produto(data: dict, id_usuario: int):
    funcionario = buscar_funcionario_repository(id_usuario)
    if (funcionario is None or not funcionario[0]
            or funcionario[1] != 'funcionario' or funcionario[2] is None):
        raise PermissionError('Acesso exclusivo de funcionário ativo.')

    produto = validar_produto_schema(data)
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
        'ingredientes': produto['ingredientes'],
    }
