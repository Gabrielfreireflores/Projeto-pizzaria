"""Validação dos campos da equipe."""

import re

_EMAIL = re.compile(r'[^@\s]+@[^@\s]+\.[^@\s]+')


def _texto(valor, campo, limite, obrigatorio=True):
    if valor is None or (isinstance(valor, str) and not valor.strip()):
        if obrigatorio:
            raise ValueError(f'{campo} é obrigatório.')
        return None
    if not isinstance(valor, str) or len(valor.strip()) > limite:
        raise ValueError(f'{campo} deve ter até {limite} caracteres.')
    return valor.strip()


# def validar_funcionario(dados, criando):
#     if not isinstance(dados, dict):
#         raise ValueError('Envie um objeto JSON.')

#     email = _texto(dados.get('email'), 'E-mail', 120).lower()
#     if not _EMAIL.fullmatch(email):
#         raise ValueError('Informe um e-mail válido.')

#     funcionario = {
#         'nome': _texto(dados.get('nome'), 'Nome', 100),
#         'cpf': _texto(dados.get('cpf'), 'Cpf', 9),
#         'cargo': _texto(dados.get('cargo'), 'Cargo', 50),
#         'telefone': _texto(dados.get('telefone'), 'Telefone', 20, obrigatorio=False),
#         'email': email,
#     }

#     # Na criação a senha é obrigatória; na edição só é trocada se for enviada.
#     senha = dados.get('senha')
#     if criando or senha:
#         if not isinstance(senha, str) or not 8 <= len(senha) <= 128:
#             raise ValueError('A senha deve ter entre 8 e 128 caracteres.')
#         funcionario['senha'] = senha

#     if not criando:
#         ativo = dados.get('ativo', True)
#         if type(ativo) is not bool:
#             raise ValueError('ativo deve ser booleano.')
#         funcionario['ativo'] = ativo

#     return funcionario

def validar_funcionario(dados, criando):
    if not isinstance(dados, dict):
        raise ValueError('Envie um objeto JSON.')

    email = _texto(dados.get('email'), 'E-mail', 160).lower()
    if not _EMAIL.fullmatch(email):
        raise ValueError('Informe um e-mail válido.')

    cpf = _texto(dados.get('cpf'), 'CPF', 14)
    cpf_digitos = re.sub(r'\D', '', cpf)

    if len(cpf_digitos) != 11:
        raise ValueError('O CPF deve conter 11 dígitos.')

    funcionario = {
        'nome': _texto(dados.get('nome'), 'Nome', 120),
        'cpf': cpf_digitos,
        'cargo': _texto(dados.get('cargo'), 'Cargo', 80),
        'telefone': _texto(
            dados.get('telefone'), 'Telefone', 20,
            obrigatorio=False
        ),
        'email': email,
    }

    # Na criação a senha é obrigatória; na edição só é trocada se for enviada.
    senha = dados.get('senha')
    if criando or senha:
        if not isinstance(senha, str) or not 8 <= len(senha) <= 128:
            raise ValueError('A senha deve ter entre 8 e 128 caracteres.')
        funcionario['senha'] = senha

    if not criando:
        ativo = dados.get('ativo', True)
        if type(ativo) is not bool:
            raise ValueError('ativo deve ser booleano.')
        funcionario['ativo'] = ativo

    return funcionario
