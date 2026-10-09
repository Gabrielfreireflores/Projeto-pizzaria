from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from app.routes.categoria_routes import categoria_bp
from app.routes.auth_routes import auth_bp
from app.routes.produto_routes import produto_bp
from app.routes.pedido_routes import pedido_bp
from app.routes.cardapio_routes import cardapio_bp
from app.exceptions.custom_exceptions import AppBaseException

def create_app():
    # Cria a instância principal do servidor Flask
    load_dotenv()

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Registra o Blueprint contendo todas as rotas de categoria
    app.register_blueprint(categoria_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(cardapio_bp)
    app.register_blueprint(pedido_bp)   

    return app
    @app.errorhandler(AppBaseException)
    def handle_app_base_exception(error):
        """
        Captura QUALQUER exceção que herde de AppBaseException
        e devolve um JSON limpo e padronizado para a API.
        """
        response = {
            "erro": error.message
        }
        return jsonify(response), error.status_code

    # (Opcional) Tratador genérico para erros 500 não previstos (ex: Python sintaxe/bugs)
    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):
        # Log do erro no terminal para depuração
        app.logger.error(f"Erro não tratado: {str(error)}")
        
        response = {
            "erro": "Ocorreu um erro interno inesperado no servidor."
        }
        return jsonify(response), 500

    return app
