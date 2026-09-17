from flask import Flask
from app.routes.categoria_routes import categoria_bp
from app.routes.produto_routes import produto_bp

def create_app():
    # Cria a instância principal do servidor Flask
    app = Flask(__name__)

    # Registra o Blueprint contendo todas as rotas de categoria
    app.register_blueprint(categoria_bp)
    app.register_blueprint(produto_bp)

    return app