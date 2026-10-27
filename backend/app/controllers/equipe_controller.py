import psycopg
from flask import current_app, jsonify, request, session
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

from app.services import equipe_services


def _usuario_logado():
    id_usuario = session.get('id_usuario')
    if type(id_usuario) is not int or id_usuario <= 0:
        return None
    return id_usuario


def _ler_json():
    try:
        data = request.get_json()
    except (BadRequest, UnsupportedMediaType):
        return None
    return data if isinstance(data, dict) else None


def _responder_erro(e):
    if isinstance(e, PermissionError):
        return jsonify({'erro': str(e)}), 403
    if isinstance(e, equipe_services.MembroNaoEncontrado):
        return jsonify({'erro': str(e)}), 404
    if isinstance(e, (equipe_services.EmailDuplicado, equipe_services.MembroEmUso)):
        return jsonify({'erro': str(e)}), 409
    return jsonify({'erro': str(e)}), 400


def listar_equipe_controller():
    id_usuario = _usuario_logado()
    if id_usuario is None:
        return jsonify({'erro': 'Autenticação necessária.'}), 401
    try:
        return jsonify({'equipe': equipe_services.listar_equipe(id_usuario)}), 200
    except PermissionError as e:
        return _responder_erro(e)
    except (psycopg.Error, RuntimeError):
        current_app.logger.error('Falha de banco ao listar a equipe.')
        return jsonify({'erro': 'Não foi possível listar a equipe.'}), 503


def criar_membro_controller():
    id_usuario = _usuario_logado()
    if id_usuario is None:
        return jsonify({'erro': 'Autenticação necessária.'}), 401
    data = _ler_json()
    if data is None:
        return jsonify({'erro': 'Envie um objeto JSON válido.'}), 400
    try:
        return jsonify(equipe_services.criar_membro(data, id_usuario)), 201
    except (PermissionError, ValueError) as e:
        return _responder_erro(e)
    except (psycopg.Error, RuntimeError):
        current_app.logger.exception(
            'Falha de banco ao cadastrar funcionário.'
        )
        return jsonify({
            'erro': 'Não foi possível cadastrar o funcionário.'
        }), 503


def atualizar_membro_controller(id_funcionario):
    id_usuario = _usuario_logado()
    if id_usuario is None:
        return jsonify({'erro': 'Autenticação necessária.'}), 401
    data = _ler_json()
    if data is None:
        return jsonify({'erro': 'Envie um objeto JSON válido.'}), 400
    try:
        return jsonify(equipe_services.atualizar_membro(id_funcionario, data, id_usuario)), 200
    # except (PermissionError, ValueError, equipe_services.MembroNaoEncontrado) as e:
    #     return _responder_erro(e)
    except (PermissionError, ValueError, equipe_services.MembroNaoEncontrado) as e:
        current_app.logger.warning(
            "Erro ao atualizar funcionário %s: %s: %s",
            id_funcionario,
            type(e).__name__,
            str(e),
        )
        return _responder_erro(e)
    except (psycopg.Error, RuntimeError):
        current_app.logger.error('Falha de banco ao atualizar funcionário.')
        return jsonify({'erro': 'Não foi possível atualizar o funcionário.'}), 503


def excluir_membro_controller(id_funcionario):
    id_usuario = _usuario_logado()
    if id_usuario is None:
        return jsonify({'erro': 'Autenticação necessária.'}), 401
    try:
        equipe_services.excluir_membro(id_funcionario, id_usuario)
        return '', 204
    except (PermissionError, ValueError, equipe_services.MembroNaoEncontrado) as e:
        return _responder_erro(e)
    except (psycopg.Error, RuntimeError):
        current_app.logger.error('Falha de banco ao excluir funcionário.')
        return jsonify({'erro': 'Não foi possível excluir o funcionário.'}), 503