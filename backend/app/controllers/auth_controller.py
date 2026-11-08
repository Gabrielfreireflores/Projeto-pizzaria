from app.error_logging import log_internal_error
from flask import request, jsonify, session
from werkzeug.exceptions import BadRequest, UnsupportedMediaType
from app.repositories.usuario_repository import buscar_usuario_por_id

from app.services import auth_services
from app.login_rate_limit import check_login_rate

def logout_controller():
    session.clear()

    return jsonify({
        "mensagem": "Logout realizado com sucesso."
    }), 200


def usuario_logado_controller():
    id_usuario = session.get("id_usuario")

    if type(id_usuario) is not int or id_usuario <= 0:
        return jsonify({
            "erro": "Usuário não autenticado."
        }), 401

    usuario = buscar_usuario_por_id(id_usuario)

    if usuario is None or not usuario[2]:
        session.clear()
        return jsonify({
            "erro": "Usuário não encontrado."
        }), 401

    return jsonify({
        "usuario": {
            "id": usuario[0],
            "email": usuario[1],
            "ativo": usuario[2],
            "perfil": usuario[3],
            "nome": usuario[5],
            "telefone": usuario[6],
            "cargo": usuario[7]
        }
    }), 200

def cadastrar_usuario_controller(perfil_padrao: str):
    try:
        data = request.get_json()
    except (BadRequest, UnsupportedMediaType):
        return jsonify({'erro': 'Envie um objeto JSON válido.'}), 400
    if not isinstance(data, dict):
        return jsonify({'erro': 'Envie um objeto JSON válido.'}), 400

    email = data.get("email", "")
    senha = data.get("senha", "")
    descricao = data.get(
        "descricao",
        f"Cadastro do perfil {perfil_padrao}"
    )

    if not isinstance(email, str) or not isinstance(senha, str) or not email.strip() or not senha:
        return jsonify({
            "erro": "E-mail e senha são campos obrigatórios."
        }), 400

    try:
        usuario = auth_services.cadastrar_usuario(
            email=email,
            senha=senha,
            nome_perfil=perfil_padrao,
            descricao_perfil=descricao
        )

        return jsonify({
            "mensagem": (
                f"Usuário do perfil '{perfil_padrao}' "
                "cadastrado com sucesso."
            ),
            "usuario": {
                "id": usuario[0],
                "email": usuario[1]
            }
        }), 201

    except ValueError as e:
        return jsonify({
            "erro": str(e)
        }), 400

def cadastrar_cliente_controller():
    try:
        data = request.get_json()
    except (BadRequest, UnsupportedMediaType):
        return jsonify({'erro': 'Envie um objeto JSON válido.'}), 400
    if not isinstance(data, dict):
        return jsonify({'erro': 'Envie um objeto JSON válido.'}), 400

    email = data.get("email", "")
    senha = data.get("senha", "")
    nome = data.get("nome", "")
    telefone = data.get("telefone")

    if not email or not senha or not nome or not telefone:
        return jsonify({
            "erro": "Nome completo, e-mail, celular e senha são obrigatórios."
        }), 400

    try:
        usuario, cliente = auth_services.cadastrar_cliente(
            email=email,
            senha=senha,
            nome=nome,
            telefone=telefone
        )

        return jsonify({
            "mensagem": "Cliente cadastrado com sucesso.",
            "usuario": {
                "id": usuario[0],
                "email": usuario[1]
            },
            "cliente": {
                "id": cliente[0],
                "nome": cliente[2],
                "cpf": cliente[3],
                "telefone": cliente[4]
            }
        }), 201

    except ValueError as e:
        return jsonify({
            "erro": str(e)
        }), 400

    except Exception:
        log_internal_error('Falha ao cadastrar cliente.')
        return jsonify({'erro': 'Não foi possível criar sua conta. Tente novamente.'}), 503


def login_controller():
    try:
        data = request.get_json()
    except (BadRequest, UnsupportedMediaType):
        return jsonify({'erro': 'Envie um objeto JSON válido.'}), 400
    if not isinstance(data, dict):
        return jsonify({'erro': 'Envie um objeto JSON válido.'}), 400

    email = data.get("email", "")
    senha = data.get("senha", "")

    if not isinstance(email, str) or not isinstance(senha, str) or not email.strip() or not senha:
        return jsonify({
            "erro": "E-mail e senha são obrigatórios."
        }), 400

    try:
        retry_after = check_login_rate(email)
    except (RuntimeError, ValueError):
        log_internal_error('Falha no limitador de login.')
        return jsonify({'erro': 'Login temporariamente indisponível. Tente novamente.'}), 503
    if retry_after:
        return jsonify({'erro': 'Muitas tentativas. Aguarde antes de tentar novamente.'}), 429, {
            'Retry-After': str(retry_after),
        }

    try:
        usuario = auth_services.autenticar_usuario(
            email=email,
            senha=senha
        )

        session.clear()
        session["id_usuario"] = usuario[0]

        return jsonify({
            "mensagem": "Login realizado com sucesso.",
            "usuario": {
                "id": usuario[0],
                "email": usuario[1]
            }
        }), 200

    except ValueError as e:
        return jsonify({
            "erro": str(e)
        }), 401
