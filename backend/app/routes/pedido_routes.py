from flask import Blueprint
from app.controllers import pedido_controller
from app.controllers import acompanhamento_controller

pedido_bp = Blueprint('pedido_bp', __name__, url_prefix='/api/v1/pedidos')


@pedido_bp.route('', methods=['POST'])
def criar_pedido():
    return pedido_controller.criar_pedido_controller()


@pedido_bp.route('/<int:id_pedido>/acompanhamento', methods=['GET'])
def consultar_acompanhamento(id_pedido):
    return acompanhamento_controller.consultar_acompanhamento_controller(id_pedido)
