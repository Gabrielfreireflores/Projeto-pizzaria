from enum import Enum


class StatusPedido(str, Enum):
    RECEBIDO = 'Recebido'
    EM_PREPARACAO = 'Em preparação'
    SAIU_PARA_ENTREGA = 'Saiu para entrega'
    ENTREGUE = 'Entregue'
    CANCELADO = 'Cancelado'
