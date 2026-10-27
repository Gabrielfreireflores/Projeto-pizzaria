import psycopg
from flask import Blueprint, current_app, jsonify, session

from app.services import ingrediente_services

ingrediente_bp = Blueprint('ingrediente_bp', __name__)


@ingrediente_bp.route('/api/v1/ingredientes', methods=['GET'])
def listar_ingredientes():
    id_usuario = session.get('id_usuario')
    if type(id_usuario) is not int or id_usuario <= 0:
        return jsonify({'erro': 'Autenticação necessária.'}), 401

    try:
        ingredientes = ingrediente_services.listar_ingredientes(id_usuario)
        return jsonify({'ingredientes': ingredientes}), 200
    except PermissionError as e:
        return jsonify({'erro': str(e)}), 403
    except (psycopg.Error, RuntimeError):
        current_app.logger.error('Falha de banco ao listar ingredientes.')
        return jsonify({'erro': 'Não foi possível listar os ingredientes.'}), 503