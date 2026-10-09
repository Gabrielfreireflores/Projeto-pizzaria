import psycopg
from flask import current_app, jsonify

from app.services import cardapio_services


def listar_cardapio_controller():
    try:
        return jsonify({'categorias': cardapio_services.listar_cardapio()}), 200
    except (psycopg.Error, RuntimeError):
        current_app.logger.error('Falha de banco ao consultar cardápio.')
        return jsonify({'erro': 'Não foi possível consultar o cardápio.'}), 503
