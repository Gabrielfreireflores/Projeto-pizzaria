import re


def _texto(valor, campo, limite):
    if not isinstance(valor, str) or not valor.strip() or len(valor.strip()) > limite:
        raise ValueError(f'{campo} é obrigatório e deve ter até {limite} caracteres.')
    return valor.strip()


def validar_pedido(data: dict):
    if not isinstance(data, dict):
        raise ValueError('Envie um objeto JSON.')
    contato = data.get('contato')
    endereco = data.get('endereco')
    if not isinstance(contato, dict) or not isinstance(endereco, dict):
        raise ValueError('Informe os objetos contato e endereco.')
    nome = _texto(contato.get('nome'), 'nome', 120)
    telefone = _texto(contato.get('telefone'), 'telefone', 20)
    if (not re.fullmatch(r'[+()\d .-]+', telefone)
            or not 10 <= len(re.sub(r'\D', '', telefone)) <= 15):
        raise ValueError('Telefone inválido.')
    entrega = {campo: _texto(endereco.get(campo), campo, limite)
               for campo, limite in [('cep', 9), ('logradouro', 160), ('numero', 20),
                                     ('bairro', 100), ('cidade', 100), ('uf', 2)]}
    if not re.fullmatch(r'\d{5}-?\d{3}', entrega['cep']):
        raise ValueError('CEP inválido.')
    entrega['uf'] = entrega['uf'].upper()
    if not re.fullmatch(r'[A-Z]{2}', entrega['uf']):
        raise ValueError('UF deve ter duas letras.')
    complemento = endereco.get('complemento')
    if complemento is not None and (not isinstance(complemento, str) or len(complemento) > 100):
        raise ValueError('Complemento deve ter até 100 caracteres.')
    entrega['complemento'] = complemento.strip() if complemento else None
    itens = data.get('itens')
    if not isinstance(itens, list) or not 1 <= len(itens) <= 100:
        raise ValueError('Informe de 1 a 100 itens.')
    normalizados = []
    ids = set()
    for item in itens:
        if not isinstance(item, dict):
            raise ValueError('Cada item deve ser um objeto.')
        identificador = item.get('id_produto')
        quantidade = item.get('quantidade')
        if type(identificador) is not int or not 0 < identificador <= 2147483647:
            raise ValueError('id_produto deve ser um inteiro positivo válido.')
        if type(quantidade) is not int or not 0 < quantidade <= 2147483647:
            raise ValueError('Quantidade deve ser um inteiro positivo válido.')
        if identificador in ids:
            raise ValueError('Não repita produtos; informe a quantidade em um único item.')
        ids.add(identificador)
        observacao = item.get('observacao')
        if observacao is not None and (not isinstance(observacao, str) or len(observacao) > 500):
            raise ValueError('Observação deve ter até 500 caracteres.')
        normalizados.append({'id_produto': identificador, 'quantidade': quantidade,
                             'observacao': observacao})
    return {'contato': {'nome': nome, 'telefone': telefone}, 'endereco': entrega,
            'forma_pagamento': _texto(data.get('forma_pagamento'), 'forma_pagamento', 40),
            'itens': normalizados}
