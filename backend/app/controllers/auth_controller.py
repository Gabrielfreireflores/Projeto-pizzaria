from flask import request, jsonify, session
from app.repositories.usuario_repository import buscar_usuario_por_id

from app.services import auth_services

def logout_controller():
    session.clear()

    return jsonify({
        "mensagem": "Logout realizado com sucesso."
    }), 200


def usuario_logado_controller():
    id_usuario = session.get("id_usuario")

    if not id_usuario:
        return jsonify({
            "erro": "Usuário não autenticado."
        }), 401

    usuario = buscar_usuario_por_id(id_usuario)

    if usuario is None:
        session.clear()
        return jsonify({
            "erro": "Usuário não encontrado."
        }), 401

    return jsonify({
        "usuario": {
            "id": usuario[0],
            "email": usuario[1],
            "ativo": usuario[2],
            "perfil": usuario[3]
        }
    }), 200

def cadastrar_usuario_controller(perfil_padrao: str):
    data = request.get_json() or {}

    email = data.get("email", "")
    senha = data.get("senha", "")
    descricao = data.get(
        "descricao",
        f"Cadastro do perfil {perfil_padrao}"
    )

    if not email or not senha:
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
    data = request.get_json() or {}

    email = data.get("email", "")
    senha = data.get("senha", "")
    nome = data.get("nome", "")
    cpf = data.get("cpf", "")
    telefone = data.get("telefone")

    if not email or not senha or not nome or not cpf:
        return jsonify({
            "erro": "E-mail, senha, nome e CPF são obrigatórios."
        }), 400

    try:
        usuario, cliente = auth_services.cadastrar_cliente(
            email=email,
            senha=senha,
            nome=nome,
            cpf=cpf,
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

    except Exception as e:
        return jsonify({
            "erro": str(e)
        }), 400


def login_controller():
    data = request.get_json() or {}

    email = data.get("email", "")
    senha = data.get("senha", "")

    if not email or not senha:
        return jsonify({
            "erro": "E-mail e senha são obrigatórios."
        }), 400

    try:
        usuario = auth_services.autenticar_usuario(
            email=email,
            senha=senha
        )

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