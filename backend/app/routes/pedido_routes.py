from flask import Blueprint
from app.controllers import pedido_controller

pedido_bp = Blueprint('pedido_bp', __name__, url_prefix='/api/v1/pedidos')


@pedido_bp.route('', methods=['POST'])
def criar_pedido():
    return pedido_controller.criar_pedido_controller()
