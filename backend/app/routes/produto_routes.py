from flask import Blueprint
from app.controllers import produto_controller

produto_bp = Blueprint('produto_bp', __name__)


@produto_bp.route('/produtos', methods=['POST'])
@produto_bp.route('/api/produtos', methods=['POST'])
@produto_bp.route('/api/v1/produtos', methods=['POST'])
def criar_produto():
    return produto_controller.criar_produto_controller()


@produto_bp.route('/produtos', methods=['GET'])
@produto_bp.route('/api/produtos', methods=['GET'])
@produto_bp.route('/api/v1/produtos', methods=['GET'])
def listar_produtos():
    return produto_controller.listar_produtos_controller()
