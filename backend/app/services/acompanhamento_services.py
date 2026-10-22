from datetime import datetime, timedelta, timezone

from app.models.status_pedido import StatusPedido
from app.repositories.acompanhamento_repository import buscar_acompanhamento as buscar_acompanhamento_repository
from app.repositories.cliente_repository import buscar_cliente_por_usuario as buscar_cliente_repository
from app.repositories.pedido_repository import transacao_pedido as transacao_pedido_repository


class PedidoNaoEncontrado(LookupError):
    """Pedido inexistente ou pertencente a outro cliente."""


def consultar_acompanhamento(id_pedido: int, id_usuario: int, prazo_minutos=60):
    if type(id_usuario) is not int or id_usuario <= 0:
        raise PermissionError('Cliente autenticado obrigatório.')
    with transacao_pedido_repository() as conn:
        cliente = buscar_cliente_repository(conn, id_usuario)
        if cliente is None or not cliente[1] or cliente[2].strip().casefold() != 'cliente':
            raise PermissionError('É necessário ter um cadastro de cliente ativo.')
        pedido = buscar_acompanhamento_repository(conn, id_pedido, cliente[0])
    if pedido is None:
        raise PedidoNaoEncontrado('Pedido não encontrado.')
    try:
        status = StatusPedido(pedido[1])
    except ValueError:
        raise RuntimeError('Status do pedido não reconhecido.') from None
    finalizado = status in (StatusPedido.ENTREGUE, StatusPedido.CANCELADO)
    estimativa = None
    if not finalizado:
        # Aceita configuração inteira ou string de inteiro do ambiente.
        if type(prazo_minutos) is int:
            prazo = prazo_minutos
        elif isinstance(prazo_minutos, str) and prazo_minutos.isascii() and prazo_minutos.isdecimal():
            prazo = int(prazo_minutos)
        else:
            raise RuntimeError('Prazo estimado de entrega inválido.')
        if not 1 <= prazo <= 1440:
            raise RuntimeError('Prazo estimado de entrega inválido.')
        previsao = pedido[2] + timedelta(minutes=prazo)
        estimativa = {
            'prazo_minutos': prazo,
            'previsao_entrega': previsao.isoformat(),
            'atrasada': datetime.now(timezone.utc) > previsao,
        }
    return {
        'id_pedido': pedido[0],
        'status': status.name,
        'status_descricao': status.value,
        'data_hora_pedido': pedido[2].isoformat(),
        'estimativa_entrega': estimativa,
        'finalizado': finalizado,
        'atualizar_em_segundos': None if finalizado else 10,
    }
