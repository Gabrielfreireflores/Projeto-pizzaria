from app.error_logging import log_internal_error
import psycopg
from flask import request, jsonify, session, current_app
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

from app.services import pedido_services


def criar_pedido_controller():
    id_usuario = session.get('id_usuario')
    if type(id_usuario) is not int or id_usuario <= 0:
        return jsonify({'erro': 'Faça login para finalizar o pedido.'}), 401
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
    except (psycopg.Error, RuntimeError):
        log_internal_error(
            'Falha de persistência/configuração ao criar pedido.'
        )
        return jsonify({
            'erro': 'Não foi possível criar o pedido. Tente novamente.'
        }), 503


def listar_pedidos_controller():
    id_usuario = session.get("id_usuario")

    if type(id_usuario) is not int or id_usuario <= 0:
        return jsonify({"erro": "Autenticação necessária."}), 401

    try:
        pedidos = pedido_services.listar_pedidos(id_usuario)
        return jsonify(pedidos), 200
    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403
    except (psycopg.Error, RuntimeError):
        log_internal_error("Falha ao listar pedidos.")
        return jsonify({"erro": "Não foi possível listar os pedidos."}), 500


def listar_meus_pedidos_controller():
    id_usuario = session.get('id_usuario')
    if type(id_usuario) is not int or id_usuario <= 0:
        return jsonify({'erro': 'Faça login para acompanhar seus pedidos.'}), 401
    try:
        return jsonify(pedido_services.listar_meus_pedidos(id_usuario)), 200
    except PermissionError as e:
        return jsonify({'erro': str(e)}), 403
    except (psycopg.Error, RuntimeError):
        log_internal_error('Falha ao consultar pedidos do cliente.')
        return jsonify({'erro': 'Não foi possível consultar seus pedidos.'}), 503


def aceitar_pedido_controller(id_pedido):
    id_usuario = session.get("id_usuario")

    if type(id_usuario) is not int or id_usuario <= 0:
        return jsonify({"erro": "Autenticação necessária."}), 401

    try:
        resultado = pedido_services.aceitar_pedido(
            id_pedido, id_usuario
        )
        return jsonify(resultado), 200
    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403
    except LookupError as e:
        return jsonify({"erro": str(e)}), 404
    except ValueError as e:
        return jsonify({"erro": str(e)}), 409
    except (psycopg.Error, RuntimeError):
        log_internal_error("Falha ao aceitar pedido.")
        return jsonify({"erro": "Não foi possível aceitar o pedido."}), 500

def alterar_status_pedido_controller(id_pedido):
    id_usuario = session.get("id_usuario")

    if type(id_usuario) is not int or id_usuario <= 0:
        return jsonify({"erro": "Autenticação necessária."}), 401

    try:
        data = request.get_json()
    except (BadRequest, UnsupportedMediaType):
        return jsonify({"erro": "Envie um objeto JSON válido."}), 400
    if not isinstance(data, dict):
        return jsonify({"erro": "Envie um objeto JSON."}), 400

    try:
        resultado = pedido_services.alterar_status_pedido(id_pedido, data, id_usuario)
        return jsonify(resultado), 200
    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403
    except LookupError as e:
        return jsonify({"erro": str(e)}), 404
    except pedido_services.TransicaoInvalida as e:
        return jsonify({"erro": str(e)}), 409
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except (psycopg.Error, RuntimeError):
        log_internal_error("Falha ao alterar status do pedido.")
        return jsonify({"erro": "Não foi possível atualizar o pedido."}), 500
