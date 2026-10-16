from flask import Blueprint
from app.controllers import pedido_controller

pedido_bp = Blueprint('pedido_bp', __name__, url_prefix='/api/v1/pedidos')


@pedido_bp.route('', methods=['POST'])
def criar_pedido():
    return pedido_controller.criar_pedido_controller()

@pedido_bp.route('', methods=['GET'])
def listar_pedidos():
    return pedido_controller.listar_pedidos_controller()


@pedido_bp.route('/<int:id_pedido>/aceitar', methods=['POST'])
def aceitar_pedido(id_pedido):
    return pedido_controller.aceitar_pedido_controller(id_pedido)