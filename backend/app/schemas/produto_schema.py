"""Validação dos campos segundo db/schema.sql."""

from decimal import Decimal, InvalidOperation


def _texto(valor, campo, limite):
    if not isinstance(valor, str) or not valor.strip() or len(valor.strip()) > limite:
        raise ValueError(f'{campo} é obrigatório e deve ter até {limite} caracteres.')
    return valor.strip()


def _id(valor, campo):
    if type(valor) is not int or not 0 < valor <= 2147483647:
        raise ValueError(f'{campo} deve ser um inteiro positivo válido.')
    return valor


def _decimal(valor, campo, casas, maximo, permite_zero):
    if isinstance(valor, bool) or not isinstance(valor, (str, int, float, Decimal)):
        raise ValueError(f'{campo} deve ser um número válido.')
    try:
        numero = Decimal(str(valor))
        if not numero.is_finite() or numero < 0 or numero > Decimal(maximo):
            raise ValueError(f'{campo} está fora do intervalo permitido.')
        if not permite_zero and numero == 0:
            raise ValueError(f'{campo} deve ser maior que zero.')
        arredondado = numero.quantize(Decimal(1).scaleb(-casas))
        if arredondado != numero:
            raise ValueError(f'{campo} deve ter no máximo {casas} casas decimais.')
        return arredondado
    except InvalidOperation:
        raise ValueError(f'{campo} deve ser um número válido.') from None


def validar_produto(dados):
    if not isinstance(dados, dict):
        raise ValueError('Envie um objeto JSON.')
    produto = {
        'nome': _texto(dados.get('nome'), 'nome', 120),
        'tamanho': _texto(dados.get('tamanho'), 'tamanho', 30),
        'preco': _decimal(dados.get('preco'), 'preco', 2, '99999999.99', True),
        'id_categoria': _id(dados.get('id_categoria'), 'id_categoria'),
        'disponivel': dados.get('disponivel', True),
    }
    if type(produto['disponivel']) is not bool:
        raise ValueError('disponivel deve ser booleano.')
    ingredientes = dados.get('ingredientes')
    if not isinstance(ingredientes, list) or not ingredientes:
        raise ValueError('Informe ao menos um ingrediente.')
    vistos = set()
    produto['ingredientes'] = []
    for item in ingredientes:
        if not isinstance(item, dict):
            raise ValueError('Cada ingrediente deve ser um objeto.')
        identificador = _id(item.get('id_ingrediente'), 'id_ingrediente')
        if identificador in vistos:
            raise ValueError('Não repita ingredientes no mesmo produto.')
        vistos.add(identificador)
        produto['ingredientes'].append({
            'id_ingrediente': identificador,
            'quantidade_necessaria': _decimal(item.get('quantidade_necessaria'),
                'quantidade_necessaria', 3, '999999999.999', False),
        })
    return produto
