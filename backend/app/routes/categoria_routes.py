from flask import Blueprint, request, jsonify
from app.controllers import criar_categoria_controller

categoria_bp = Blueprint('categoria_bp', __name__)

@categoria_bp.route('/categorias', methods=['POST'])
def criar_categoria():
    return criar_categoria_controller()

@categoria_bp.route('/categorias', methods=['GET'])
def listar_categoria():
    return listar_categorias_controller()
