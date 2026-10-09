from flask import Blueprint, request, jsonify
from app.controllers.categoria_controller import criar_categoria_controller, listar_categorias_controller

categoria_bp = Blueprint('categoria_bp', __name__)

@categoria_bp.route('/api/categorias', methods=['POST'])
def criar_categoria():
    return criar_categoria_controller()

@categoria_bp.route('/api/categorias', methods=['GET'])
def listar_categoria():
    return listar_categorias_controller()
