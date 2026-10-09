from flask import Blueprint
from app.controllers import cardapio_controller

cardapio_bp = Blueprint('cardapio_bp', __name__)


@cardapio_bp.route('/api/v1/cardapio', methods=['GET'])
def listar_cardapio():
    return cardapio_controller.listar_cardapio_controller()
