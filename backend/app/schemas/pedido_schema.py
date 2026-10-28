import re

# Valores usados quando o checkout simplificado não envia o campo.
# CEP_PADRAO é um marcador: trocar pelo CEP real da pizzaria, se houver.
CIDADE_PADRAO = 'Jardinópolis'
UF_PADRAO = 'SP'
CEP_PADRAO = '00000-000'
NUMERO_PADRAO = 'S/N'
TIPOS_ENTREGA = ('entrega', 'retirada')


def _texto(valor, campo, limite):
    if not isinstance(valor, str) or not valor.strip() or len(valor.strip()) > limite:
        raise ValueError(f'{campo} é obrigatório e deve ter até {limite} caracteres.')
    return valor.strip()


def _validar_endereco(endereco):
    """Obrigatórios: logradouro e bairro. Os demais campos, se vierem, são validados;
    se não vierem, usam os valores padrão da pizzaria (entrega local)."""
    if not isinstance(endereco, dict):
        raise ValueError('Informe o objeto endereco para entrega.')
    entrega = {'logradouro': _texto(endereco.get('logradouro'), 'logradouro', 160),
               'bairro': _texto(endereco.get('bairro'), 'bairro', 100)}
    entrega['numero'] = (_texto(endereco['numero'], 'numero', 20)
                         if endereco.get('numero') not in (None, '') else NUMERO_PADRAO)
    entrega['cep'] = (_texto(endereco['cep'], 'cep', 9)
                      if endereco.get('cep') is not None else CEP_PADRAO)
    if not re.fullmatch(r'\d{5}-?\d{3}', entrega['cep']):
        raise ValueError('CEP inválido.')
    entrega['cidade'] = (_texto(endereco['cidade'], 'cidade', 100)
                         if endereco.get('cidade') is not None else CIDADE_PADRAO)
    entrega['uf'] = (_texto(endereco['uf'], 'uf', 2)
                     if endereco.get('uf') is not None else UF_PADRAO).upper()
    if not re.fullmatch(r'[A-Z]{2}', entrega['uf']):
        raise ValueError('UF deve ter duas letras.')
    complemento = endereco.get('complemento')
    if complemento is not None and (not isinstance(complemento, str) or len(complemento) > 100):
        raise ValueError('Complemento deve ter até 100 caracteres.')
    entrega['complemento'] = complemento.strip() if complemento else None
    return entrega


def validar_pedido(data: dict):
    if not isinstance(data, dict):
        raise ValueError('Envie um objeto JSON.')
    contato = data.get('contato')
    if not isinstance(contato, dict):
        raise ValueError('Informe o objeto contato.')
    tipo_entrega = data.get('tipo_entrega', 'entrega')
    if tipo_entrega not in TIPOS_ENTREGA:
        raise ValueError('tipo_entrega deve ser "entrega" ou "retirada".')
    nome = _texto(contato.get('nome'), 'nome', 120)
    if len(nome.split()) < 2:
        raise ValueError('Informe nome e sobrenome.')
    telefone = _texto(contato.get('telefone'), 'telefone', 20)
    if (not re.fullmatch(r'[+()\d .-]+', telefone)
            or not 10 <= len(re.sub(r'\D', '', telefone)) <= 15):
        raise ValueError('Telefone inválido.')
    entrega = _validar_endereco(data.get('endereco')) if tipo_entrega == 'entrega' else None
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
        bordas = item.get('bordas', [])
        if not isinstance(bordas, list) or len(bordas) > 100:
            raise ValueError('Informe uma lista de até 100 bordas por item.')
        bordas_normalizadas = []
        ids_bordas = set()
        for borda in bordas:
            if not isinstance(borda, dict):
                raise ValueError('Cada borda deve ser um objeto.')
            id_borda, qtd_borda = borda.get('id_produto'), borda.get('quantidade')
            if type(id_borda) is not int or not 0 < id_borda <= 2147483647:
                raise ValueError('Produto da borda inválido.')
            if type(qtd_borda) is not int or not 0 < qtd_borda <= quantidade:
                raise ValueError('Quantidade da borda inválida.')
            if id_borda in ids_bordas:
                raise ValueError('Não repita a mesma borda no item.')
            ids_bordas.add(id_borda)
            bordas_normalizadas.append({'id_produto': id_borda, 'quantidade': qtd_borda})
        if sum(b['quantidade'] for b in bordas_normalizadas) > quantidade:
            raise ValueError('Selecione no máximo uma borda por pizza.')
        normalizados.append({'id_produto': identificador, 'quantidade': quantidade,
                             'observacao': observacao, 'bordas': bordas_normalizadas})
    return {'contato': {'nome': nome, 'telefone': telefone}, 'tipo_entrega': tipo_entrega,
            'endereco': entrega,
            'forma_pagamento': _texto(data.get('forma_pagamento'), 'forma_pagamento', 40),
            'itens': normalizados}
