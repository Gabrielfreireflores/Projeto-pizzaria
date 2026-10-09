from decimal import Decimal, InvalidOperation
import unicodedata

from app.models.status_pedido import StatusPedido
from app.repositories.cliente_repository import buscar_cliente_por_usuario as buscar_cliente_repository
from app.repositories.endereco_repository import criar_endereco as criar_endereco_repository
from app.repositories.produto_repository import buscar_produtos_para_pedido as buscar_produtos_repository
from app.repositories.pedido_repository import (
    transacao_pedido as transacao_pedido_repository,
    buscar_status_por_nome as buscar_status_repository,
    criar_pedido as criar_pedido_repository,
    criar_itens_pedido as criar_itens_repository,
)
from app.schemas.pedido_schema import validar_pedido as validar_pedido_schema
from app.repositories.funcionario_repository import (
    buscar_funcionario_por_usuario,
)
from app.repositories.pedido_repository import (
    listar_pedidos as listar_pedidos_repository,
    atualizar_status_pedido as atualizar_status_repository,
)


def criar_pedido(data: dict, id_usuario: int, taxa_entrega='0.00'):
    if type(id_usuario) is not int or id_usuario <= 0:
        raise PermissionError('Cliente autenticado obrigatório.')
    pedido = validar_pedido_schema(data)
    try:
        taxa = Decimal(str(taxa_entrega))
        if (not taxa.is_finite() or not 0 <= taxa <= Decimal('99999999.99')
                or taxa != taxa.quantize(Decimal('0.01'))):
            raise ValueError()
        taxa = taxa.quantize(Decimal('0.01'))
    except (InvalidOperation, ValueError):
        raise RuntimeError('Taxa de entrega do servidor inválida.') from None

    with transacao_pedido_repository() as conn:
        cliente = buscar_cliente_repository(conn, id_usuario)
        # O PR #11 usa "Cliente"; o seed existente usa "cliente".
        if cliente is None or not cliente[1] or cliente[2].strip().casefold() != 'cliente':
            raise PermissionError('É necessário ter um cadastro de cliente ativo.')
        ids = [item['id_produto'] for item in pedido['itens']]
        produtos = {linha[0]: linha for linha in buscar_produtos_repository(conn, ids)}
        total = taxa
        for item in pedido['itens']:
            produto = produtos.get(item['id_produto'])
            if produto is None:
                raise ValueError(f"Produto {item['id_produto']} inexistente.")
            if not produto[2]:
                raise ValueError(f"Produto {item['id_produto']} indisponível.")
            preco = produto[1]
            if not preco.is_finite() or preco < 0:
                raise RuntimeError('Preço inválido no cadastro do produto.')
            item['preco_unitario'] = preco
            item['subtotal'] = preco * item['quantidade']
            total += item['subtotal']
            if total > Decimal('9999999999.99'):
                raise ValueError('Valor total do pedido excede o limite permitido.')
        status = buscar_status_repository(conn, StatusPedido.RECEBIDO.value)
        if status is None:
            raise RuntimeError('Status inicial não configurado no banco.')
        pedido.update(id_cliente=cliente[0], id_status=status[0], taxa_entrega=taxa,
                      valor_total=total)
        pedido['id_endereco'] = criar_endereco_repository(conn, cliente[0], pedido['endereco'])
        resultado = criar_pedido_repository(conn, pedido)
        criar_itens_repository(conn, resultado[0], pedido['itens'])

    return {'id_pedido': resultado[0], 'status': StatusPedido.RECEBIDO.name,
            'id_status': status[0], 'data_hora_pedido': resultado[1].isoformat(),
            'contato': pedido['contato'], 'endereco': pedido['endereco'],
            'forma_pagamento': pedido['forma_pagamento'], 'taxa_entrega': taxa,
            'valor_total': total, 'itens': pedido['itens']}


def _obter_funcionario(id_usuario: int):
    if type(id_usuario) is not int or id_usuario <= 0:
        raise PermissionError("Autenticação necessária.")

    funcionario = buscar_funcionario_por_usuario(id_usuario)

    if (
        funcionario is None
        or not funcionario[0]
        or unicodedata.normalize(
            "NFKD",
            funcionario[1].strip().casefold()
        ).encode("ascii", "ignore").decode("ascii") != "funcionario"
        or funcionario[2] is None
    ):
        raise PermissionError("Acesso exclusivo para funcionários.")

    return funcionario[2]


def listar_pedidos(id_usuario: int):
    _obter_funcionario(id_usuario)

    with transacao_pedido_repository() as conn:
        return listar_pedidos_repository(conn)


def aceitar_pedido(id_pedido: int, id_usuario: int):
    id_funcionario = _obter_funcionario(id_usuario)

    with transacao_pedido_repository() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT p.id_status, s.nome_status
                FROM pedido p
                JOIN status s ON s.id_status = p.id_status
                WHERE p.id_pedido = %s
                FOR UPDATE OF p
                """,
                (id_pedido,),
            )
            pedido = cursor.fetchone()

        if pedido is None:
            raise LookupError("Pedido não encontrado.")

        if pedido[1].casefold() != "recebido":
            raise ValueError("Somente pedidos recebidos podem ser aceitos.")

        status = buscar_status_repository(conn, "Em preparação")
        if status is None:
            raise RuntimeError("Status 'Em preparação' não cadastrado.")

        atualizar_status_repository(
            conn, id_pedido, status[0], id_funcionario
        )

    return {
        "id_pedido": id_pedido,
        "status": "Em preparação",
        "id_funcionario": id_funcionario,
    }
