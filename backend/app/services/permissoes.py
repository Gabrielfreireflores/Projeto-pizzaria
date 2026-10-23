from app.repositories.funcionario_repository import buscar_funcionario_por_usuario


def exigir_funcionario_ativo(id_usuario: int):
    funcionario = buscar_funcionario_por_usuario(id_usuario)
    if (funcionario is None or not funcionario[0]
            or funcionario[1].strip().casefold() not in ('funcionario', 'funcionário')
            or funcionario[2] is None):
        raise PermissionError('Acesso exclusivo de funcionário ativo.')
    return funcionario