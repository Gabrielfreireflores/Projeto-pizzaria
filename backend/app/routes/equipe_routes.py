from flask import Blueprint

from app.controllers import equipe_controller

equipe_bp = Blueprint('equipe_bp', __name__)


@equipe_bp.route('/api/v1/funcionarios', methods=['GET'])
def listar_equipe():
    return equipe_controller.listar_equipe_controller()


@equipe_bp.route('/api/v1/funcionarios', methods=['POST'])
def criar_membro():
    return equipe_controller.criar_membro_controller()


@equipe_bp.route('/api/v1/funcionarios/<int:id_funcionario>', methods=['PUT'])
def atualizar_membro(id_funcionario):
    return equipe_controller.atualizar_membro_controller(id_funcionario)


@equipe_bp.route('/api/v1/funcionarios/<int:id_funcionario>', methods=['DELETE'])
def excluir_membro(id_funcionario):
    return equipe_controller.excluir_membro_controller(id_funcionario)