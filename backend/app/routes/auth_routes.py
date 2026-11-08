
from flask import Blueprint, jsonify
from app.controllers import auth_controller
from app.controllers import pedido_controller

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/auth/api/cadastro/funcionario', methods=['POST'])
def cadastrar_funcionario():
    # O cadastro legítimo permanece em /api/v1/funcionarios, com funcionário ativo.
    return jsonify({'erro': 'Utilize o cadastro autorizado da equipe.'}), 403


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


@auth_bp.route('/api/v1/meus-pedidos', methods=['GET'])
def meus_pedidos():
    return pedido_controller.listar_meus_pedidos_controller()
