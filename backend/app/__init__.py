from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from app.routes.categoria_routes import categoria_bp
from app.routes.auth_routes import auth_bp
from app.routes.produto_routes import produto_bp
from app.routes.auth_routes import auth_bp
from app.routes.pedido_routes import pedido_bp
from app.routes.cardapio_routes import cardapio_bp
from app.routes.ingrediente_routes import ingrediente_bp
from app.routes.equipe_routes import equipe_bp

from app.exceptions.custom_exceptions import AppBaseException
from werkzeug.exceptions import HTTPException
from app.security import configure_security
from app.login_rate_limit import configure_login_limits


def create_app():
    # Cria a instância principal do servidor Flask
    load_dotenv()

    app = Flask(__name__)

    configure_security(app)
    configure_login_limits(app)

    #Limite máximo da requisição: 10 MB
    # Em produção, inclui todo o multipart e fica abaixo dos 4,5 MB da Vercel.
    app.config["MAX_CONTENT_LENGTH"] = (4 if app.config['PRODUCTION'] else 10)*1024*1024

    #Diretório absoluto para salvar as fotos dos produtos
    app.config["UPLOAD_FOLDER"] = os.path.join(
        app.root_path,
        "static",
        "uploads",
        "produtos",
    )

    # A pasta é criada somente ao salvar localmente, sem escrita na importação.
    app.config['IMAGE_STORAGE'] = os.getenv(
        'IMAGE_STORAGE', 'disabled' if app.config['PRODUCTION'] else 'local'
    )
    if app.config['IMAGE_STORAGE'] not in ('local', 'disabled', 'blob'):
        raise RuntimeError('IMAGE_STORAGE não possui adaptador configurado.')
    if app.config['PRODUCTION'] and app.config['IMAGE_STORAGE'] == 'local':
        raise RuntimeError('Armazenamento local de uploads não é permitido em produção.')

    #Endereço público para exibir as fotos
    app.config["UPLOAD_URL"] = "/static/uploads/produtos"

    # Registra o Blueprint contendo todas as rotas de categoria
    app.register_blueprint(categoria_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(cardapio_bp)
    app.register_blueprint(pedido_bp)
    app.register_blueprint(ingrediente_bp)
    app.register_blueprint(equipe_bp)

    @app.errorhandler(AppBaseException)
    def handle_app_base_exception(error):
        """
        Captura QUALQUER exceção que herde de AppBaseException
        e devolve um JSON limpo e padronizado para a API.
        """
        response = {"erro": error.message if error.status_code < 500 else
                    "Não foi possível concluir a operação."}
        if error.status_code >= 500:
            app.logger.error('Falha interna da aplicação (%s).', type(error).__name__)
        return jsonify(response), error.status_code

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Erros HTTP normais (404, 405, 401...) mantêm o status original."""
        return jsonify({"erro": error.name}), error.code

    # (Opcional) Tratador genérico para erros 500 não previstos (ex: Python sintaxe/bugs)
    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):
        # Log do erro no terminal para depuração
        app.logger.error('Erro não tratado (%s).', type(error).__name__)
        
        response = {
            "erro": "Ocorreu um erro interno inesperado no servidor."
        }
        return jsonify(response), 500

    return app
