import re


def validar_cadastro_cliente(email, senha, nome, telefone):
    if not isinstance(nome, str) or len(nome.strip().split()) < 2 or len(nome.strip()) > 120:
        raise ValueError('Informe nome e sobrenome com até 120 caracteres.')
    if (not isinstance(email, str) or len(email.strip()) > 160
            or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email.strip())):
        raise ValueError('Informe um e-mail válido com até 160 caracteres.')
    if (not isinstance(telefone, str) or len(telefone.strip()) > 20
            or not re.fullmatch(r'[+()\d .-]+', telefone.strip())
            or not 10 <= len(re.sub(r'\D', '', telefone)) <= 15):
        raise ValueError('Informe um celular válido com DDD, de 10 a 15 dígitos.')
    # Mantém a regra existente: senha textual não vazia, sem mínimo novo.
    if not isinstance(senha, str) or senha == '':
        raise ValueError('A senha não pode ser vazia.')
    return {'email': email.strip().lower(), 'senha': senha,
            'nome': nome.strip(), 'telefone': telefone.strip()}
