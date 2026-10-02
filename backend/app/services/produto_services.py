from psycopg.errors import ForeignKeyViolation, UniqueViolation

from app.repositories.funcionario_repository import buscar_funcionario_por_usuario as buscar_funcionario_repository
from app.repositories.produto_repository import criar_produto as criar_produto_repository
from app.repositories.produto_repository import listar_produtos as listar_produtos_repository
from app.schemas.produto_schema import validar_produto as validar_produto_schema


class ProdutoDuplicado(ValueError):
    """Já existe um produto com o mesmo nome e tamanho."""


def listar_produtos():
    produtos = {}
    for linha in listar_produtos_repository():
        identificador = linha[0]
        if identificador not in produtos:
            produtos[identificador] = {
                'id_produto': identificador, 'nome': linha[1], 'tamanho': linha[2],
                'preco': linha[3], 'disponivel': linha[4],
                'categoria': {'id_categoria': linha[5], 'nome': linha[6]},
                'ingredientes': [],
            }
        if linha[7] is not None:
            produtos[identificador]['ingredientes'].append({
                'id_ingrediente': linha[7], 'nome': linha[8],
                'quantidade_necessaria': linha[9], 'unidade_medida': linha[10],
            })
    return list(produtos.values())


def criar_produto(data: dict, id_usuario: int):
    funcionario = buscar_funcionario_repository(id_usuario)
    if (funcionario is None or not funcionario[0]
            or funcionario[1].strip().casefold() not in ('funcionario', 'funcionário')
            or funcionario[2] is None):
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
