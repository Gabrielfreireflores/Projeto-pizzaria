from flask import Blueprint, request, jsonify
from app.services import categoria_services

categoria_bp = Blueprint('categoria_bp', __name__)

@categoria_bp.route('/categorias', methods=['POST'])
def criar_categoria():
    data = request.get_json() or {}
    nome = data.get('nome', '')

    try:
        categoria = categoria_services.criar_categoria(nome)
        
        resposta = {
            "id_categoria": categoria[0],
            "nome": categoria[1]
        }
        return jsonify(resposta), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@categoria_bp.route('/categorias', methods=['GET'])
def listar_categoria():
    try:
        lista_categorias = categoria_services.listar_categorias()
        return jsonify(lista_categorias), 200
    except ValueError as e:
        return jsonify({"sem info"}, 400)
