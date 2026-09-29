from flask import request, jsonify
from app.services import categoria_services

def criar_categoria_controller():
    data = request.get_json() or {}
    nome = data.get('nome','')

    if not nome:
        return jsonify({"erro": "O nome da categoria é obrigatório."}), 400

    try:
        categoria = categoria_services.criar_categoria(nome)
        
        resposta = {
            "id_categoria": categoria[0],
            "nome": categoria[1]
        }
        return jsonify(resposta), 201
    Except ValueError as e:
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
