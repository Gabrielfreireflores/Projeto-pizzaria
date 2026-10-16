
from flask import Blueprint
from app.controllers import auth_controller

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/auth/api/cadastro/funcionario', methods=['POST'])
def cadastrar_funcionario():
    return auth_controller.cadastrar_usuario_controller(
        perfil_padrao="Funcionário"
    )


@auth_bp.route('/auth/api/cadastro/cliente', methods=['POST'])
def cadastrar_cliente_legado():
    return auth_controller.cadastrar_usuario_controller(
        perfil_padrao="Cliente"
    )


# Rotas atuais da API
@auth_bp.route('/api/v1/clientes', methods=['POST'])
def cadastrar_cliente():
    return auth_controller.cadastrar_cliente_controller()


@auth_bp.route('/api/v1/login', methods=['POST'])
def login():
    return auth_controller.login_controller()


@auth_bp.route('/api/v1/me', methods=['GET'])
def usuario_logado():
    return auth_controller.usuario_logado_controller()


@auth_bp.route('/api/v1/logout', methods=['POST'])
def logout():
    return auth_controller.logout_controller()
