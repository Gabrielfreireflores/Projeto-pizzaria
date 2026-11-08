"""Configuração de sessão e proteção CSRF para a API usada pelo proxy Next."""
import os
from urllib.parse import urlsplit

from flask import jsonify, request


def _origin(value):
    parsed = urlsplit(value)
    if (parsed.scheme not in ('http', 'https') or not parsed.netloc
            or parsed.username or parsed.password or parsed.query or parsed.fragment
            or parsed.path not in ('', '/')):
        raise ValueError('Origem inválida em APP_ORIGINS.')
    return f'{parsed.scheme}://{parsed.netloc}'.lower()


def configure_security(app):
    production = os.getenv('APP_ENV') == 'production' or os.getenv('VERCEL') == '1'
    secret = os.getenv('SECRET_KEY', '')
    if production and (len(secret) < 32 or len(set(secret)) < 12):
        raise RuntimeError('Configure SECRET_KEY forte e estável (ao menos 32 caracteres).')

    origins = os.getenv('APP_ORIGINS', '')
    if production and not origins.strip():
        raise RuntimeError('Configure APP_ORIGINS com a origem HTTPS do frontend.')
    allowed = {_origin(value.strip()) for value in origins.split(',') if value.strip()}
    if production and any(not value.startswith('https://') for value in allowed):
        raise RuntimeError('APP_ORIGINS deve usar HTTPS em produção.')
    if not production:
        allowed.update(('http://localhost:3000', 'http://127.0.0.1:3000'))

    app.config.update(
        PRODUCTION=production, SECRET_KEY=secret or None,
        SESSION_COOKIE_SECURE=production, SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax', SESSION_COOKIE_DOMAIN=None,
        SESSION_COOKIE_PATH='/', APP_ORIGINS=allowed,
    )

    @app.before_request
    def protect_api():
        if request.url_rule is None or request.method in ('GET', 'HEAD', 'OPTIONS'):
            return None
        # Cabeçalho não simples: formulários externos não conseguem enviá-lo.
        # Não habilitar CORS para origens arbitrárias nem permitir este header via CORS.
        if request.headers.get('X-CSRF-Protection') != '1':
            return jsonify({'erro': 'Requisição sem proteção CSRF.'}), 403
        if request.headers.get('Sec-Fetch-Site') == 'cross-site':
            return jsonify({'erro': 'Origem da requisição não permitida.'}), 403
        origin = request.headers.get('Origin')
        if origin:
            try:
                origin = _origin(origin)
            except ValueError:
                origin = None
            permitted = app.config['APP_ORIGINS']
            # Apenas desenvolvimento direto; não confiar no Host como origem em produção.
            local_origin = request.host_url.rstrip('/').lower()
            if origin not in permitted and not (not production and origin == local_origin):
                return jsonify({'erro': 'Origem da requisição não permitida.'}), 403

    @app.after_request
    def private_api_responses(response):
        if request.path.startswith(('/api/', '/auth/')):
            response.headers['Cache-Control'] = 'no-store'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
