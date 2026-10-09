import os

import psycopg
from flask import current_app, jsonify, session

from app.services import acompanhamento_services


def consultar_acompanhamento_controller(id_pedido: int):
    id_usuario = session.get('id_usuario')
    if type(id_usuario) is not int or id_usuario <= 0:
        resposta = jsonify({'erro': 'Autenticação necessária.'})
        status = 401
    else:
        try:
            prazo = current_app.config.get(
                'PRAZO_ESTIMADO_ENTREGA_MINUTOS',
                os.getenv('PRAZO_ESTIMADO_ENTREGA_MINUTOS', '60'),
            )
            resposta = jsonify(acompanhamento_services.consultar_acompanhamento(
                id_pedido, id_usuario, prazo,
            ))
            status = 200
        except PermissionError as erro:
            resposta, status = jsonify({'erro': str(erro)}), 403
        except acompanhamento_services.PedidoNaoEncontrado as erro:
            resposta, status = jsonify({'erro': str(erro)}), 404
        except (psycopg.Error, RuntimeError):
            current_app.logger.error('Falha ao consultar acompanhamento do pedido.')
            resposta = jsonify({'erro': 'Não foi possível consultar o pedido.'})
            status = 503
    resposta.headers['Cache-Control'] = 'no-store'
    return resposta, status
