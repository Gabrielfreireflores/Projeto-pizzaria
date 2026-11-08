from flask import request, jsonify, session
from app.services.permissoes import exigir_funcionario_ativo
from app.services import categoria_services
from app.exceptions.custom_exceptions import RequisicaoInvalidaError

def criar_categoria_controller():
    id_usuario = session.get('id_usuario')
    if type(id_usuario) is not int or id_usuario <= 0:
        return jsonify({'erro': 'Autenticação necessária.'}), 401
    try:
        exigir_funcionario_ativo(id_usuario)
    except PermissionError:
        return jsonify({'erro': 'Acesso exclusivo de funcionário ativo.'}), 403
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({'erro': 'Envie um objeto JSON válido.'}), 400
    nome = data.get('nome','')

    if not isinstance(nome, str) or not nome.strip() or len(nome.strip()) > 100:
        raise RequisicaoInvalidaError( "O nome da categoria é obrigatório.")

    try:
        categoria = categoria_services.criar_categoria(nome)
        
        return jsonify({
            "mensagem": f"Categoria '{nome}' criada com sucesso.",
            "categoria": {
                "id_categoria": categoria[0],
                "nome": categoria[1]
            }
        }), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

def listar_categorias_controller():
    try:
        lista_categorias = categoria_services.listar_categorias()
        resposta = {
            "categorias": lista_categorias
        }
        return jsonify(resposta), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
