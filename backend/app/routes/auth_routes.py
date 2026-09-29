from flask import Blueprint
from app.controllers import auth_controller

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/cadastro/funcionario', methods=['POST'])
def cadastrar_funcionario():
    return auth_controller.cadastrar_usuario_controller(perfil_padrao="Funcionário")


@auth_bp.route('/cadastro/cliente', methods=['POST'])
def cadastrar_cliente():
    return auth_controller.cadastrar_usuario_controller(perfil_padrao="Cliente")