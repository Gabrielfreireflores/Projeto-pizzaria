import psycopg
from flask import request, jsonify, session, current_app
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

from app.services import produto_services


def listar_produtos_controller():
    try:
        return jsonify({'produtos': produto_services.listar_produtos()}), 200
    except (psycopg.Error, RuntimeError):
        current_app.logger.error('Falha de banco ao listar produtos.')
        return jsonify({'erro': 'Não foi possível listar os produtos.'}), 503


def criar_produto_controller():
    id_usuario = session.get('id_usuario')
    if type(id_usuario) is not int or id_usuario <= 0:
        return jsonify({'erro': 'Autenticação necessária.'}), 401

    try:
        data = request.get_json()
    except (BadRequest, UnsupportedMediaType):
        return jsonify({'erro': 'Envie um objeto JSON válido.'}), 400
    if not isinstance(data, dict):
        return jsonify({'erro': 'Envie um objeto JSON.'}), 400

    try:
        produto = produto_services.criar_produto(data, id_usuario)
        return jsonify(produto), 201
    except PermissionError as e:
        return jsonify({'erro': str(e)}), 403
    except produto_services.ProdutoDuplicado as e:
        return jsonify({'erro': str(e)}), 409
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except (psycopg.Error, RuntimeError):
        current_app.logger.error('Falha de banco ao cadastrar produto.')
        return jsonify({'erro': 'Não foi possível cadastrar o produto.'}), 503
