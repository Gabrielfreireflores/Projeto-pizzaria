import psycopg
from flask import request, jsonify, session, current_app
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

from app.services import pedido_services


def criar_pedido_controller():
    id_usuario = session.get('id_usuario')
    if type(id_usuario) is not int or id_usuario <= 0:
        return jsonify({'erro': 'Autenticação necessária.'}), 401
    try:
        data = request.get_json()
    except (BadRequest, UnsupportedMediaType):
        return jsonify({'erro': 'Envie um objeto JSON válido.'}), 400
    try:
        pedido = pedido_services.criar_pedido(
            data, id_usuario, current_app.config.get('TAXA_ENTREGA', '0.00')
        )
        return jsonify(pedido), 201
    except PermissionError as e:
        return jsonify({'erro': str(e)}), 403
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except (psycopg.Error, RuntimeError) as e:
        current_app.logger.exception(
            'Falha de persistência/configuração ao criar pedido.'
        )
        return jsonify({
            'erro': str(e)
        }), 503