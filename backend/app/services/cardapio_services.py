from app.repositories.cardapio_repository import listar_cardapio as listar_cardapio_repository


def listar_cardapio():
    categorias = {}
    for linha in listar_cardapio_repository():
        id_categoria = linha[0]
        if id_categoria not in categorias:
            categorias[id_categoria] = {
                'id_categoria': id_categoria,
                'nome': linha[1],
                'produtos': [],
            }
        categorias[id_categoria]['produtos'].append({
            'id_produto': linha[2],
            'nome': linha[3],
            'tamanho': linha[4],
            'preco': format(linha[5], '.2f'),
            'foto': linha[6],
            'descricao': linha[7],
        })
    return list(categorias.values())
