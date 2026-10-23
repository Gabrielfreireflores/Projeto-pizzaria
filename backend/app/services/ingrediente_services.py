from app.repositories.funcionario_repository import buscar_funcionario_por_usuario
from app.repositories.ingrediente_repository import listar_ingredientes as listar_ingredientes_repository


def listar_ingredientes(id_usuario: int):
    # Mesma regra de permissão do cadastro de produto: funcionário ativo.
    funcionario = buscar_funcionario_por_usuario(id_usuario)
    if (funcionario is None or not funcionario[0]
            or funcionario[1].strip().casefold() not in ('funcionario', 'funcionário')
            or funcionario[2] is None):
        raise PermissionError('Acesso exclusivo de funcionário ativo.')

    return [
        {
            'id_ingrediente': linha[0],
            'nome': linha[1],
            'quantidade_estoque': linha[2],
            'unidade_medida': linha[3],
        }
        for linha in listar_ingredientes_repository()
    ]