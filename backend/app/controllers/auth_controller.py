from flask import request, jsonify
from app.services import auth_services # serviço de autenticação/usuários

def cadastrar_usuario_controller(perfil_padrao: str):
    data = request.get_json() or {}

    email = data.get('email', '')
    senha = data.get('senha', '')
    descricao = data.get('descricao', f"Cadastro do perfil {perfil_padrao}")

    if not email or not senha:
        return jsonify({"erro": "E-mail e senha são campos obrigatórios."}), 400

    try:
        usuario = auth_services.cadastrar_usuario(
            email=email,
            senha=senha,
            nome_perfil=perfil_padrao, # <-- "Funcionário" ou "Cliente"
            descricao_perfil=descricao
        )

        return jsonify({
            "mensagem": f"Usuário do perfil '{perfil_padrao}' cadastrado com sucesso.",
            "usuario": {
                "id": usuario[0],
                "email": usuario[1]
            }
        }), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400