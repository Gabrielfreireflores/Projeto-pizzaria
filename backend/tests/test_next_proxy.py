"""Teste opt-in do proxy real, sem banco e sem serviços externos.

Requer `npm run build` com BACKEND_URL=http://127.0.0.1:5000.
Executar: TEST_NEXT_PROXY=1 python -m pytest tests/test_next_proxy.py -q
Usa exclusivamente portas locais 5000 e 3107, sem parar processos existentes.
"""
from http.cookiejar import CookieJar
from io import BytesIO
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
from threading import Thread
import time
from urllib.error import HTTPError, URLError
from urllib.request import HTTPCookieProcessor, Request, build_opener

from PIL import Image
import pytest
from werkzeug.serving import make_server

from app import create_app
from app.controllers import auth_controller
from app.services import auth_services, cardapio_services, categoria_services, permissoes, produto_services


@pytest.mark.skipif(os.getenv('TEST_NEXT_PROXY') != '1', reason='Requer build e TEST_NEXT_PROXY=1.')
def test_next_proxy_cookies_methods_headers_json_and_multipart(monkeypatch, tmp_path):
    for port in (5000, 3107):
        with socket.socket() as probe:
            if probe.connect_ex(('127.0.0.1', port)) == 0:
                pytest.skip(f'Porta {port} já está ocupada; nenhum processo será interrompido.')
    frontend = Path(__file__).resolve().parents[2] / 'frontend'
    assert (frontend / '.next/BUILD_ID').is_file(), 'Execute npm run build primeiro.'
    monkeypatch.setenv('APP_ENV', 'development')
    monkeypatch.setenv('VERCEL', '0')
    monkeypatch.setenv('APP_ORIGINS', 'http://127.0.0.1:3107')
    monkeypatch.setenv('SECRET_KEY', 'chave-apenas-para-teste-do-proxy')
    monkeypatch.setenv('IMAGE_STORAGE', 'local')
    monkeypatch.setattr(auth_services, 'autenticar_usuario', lambda **kwargs: (7, 'proxy@example.com'))
    monkeypatch.setattr(auth_controller, 'buscar_usuario_por_id', lambda _: (
        7, 'proxy@example.com', True, 'funcionario', '', 'Teste Proxy', None, 'Atendente'))
    monkeypatch.setattr(permissoes, 'buscar_funcionario_por_usuario', lambda _: (True, 'funcionario', 3))
    monkeypatch.setattr(cardapio_services, 'listar_cardapio', lambda: [])
    monkeypatch.setattr(categoria_services, 'criar_categoria', lambda name: (9, name))
    monkeypatch.setattr(produto_services, 'criar_produto', lambda data, user: dict(data, id_produto=10))
    monkeypatch.setattr(produto_services, 'atualizar_produto', lambda identifier, data, user: dict(
        data, id_produto=identifier))
    deleted = []
    monkeypatch.setattr(produto_services, 'excluir_produto', lambda identifier, user: deleted.append((identifier, user)))
    app = create_app()
    app.config['UPLOAD_FOLDER'] = str(tmp_path / 'uploads')
    server = make_server('127.0.0.1', 5000, app)
    worker = Thread(target=server.serve_forever, daemon=True)
    process = None
    log = (tmp_path / 'next.log').open('w', encoding='utf-8')
    worker.start()
    try:
        env = dict(os.environ, BACKEND_URL='http://127.0.0.1:5000')
        process = subprocess.Popen([
            shutil.which('node'), str(frontend / 'node_modules/next/dist/bin/next'),
            'start', '--hostname', '127.0.0.1', '--port', '3107',
        ], cwd=frontend, env=env, stdout=log, stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        cookies = CookieJar()
        browser = build_opener(HTTPCookieProcessor(cookies))

        def request(path, method='GET', data=None, headers=None):
            supplied = {'X-CSRF-Protection': '1', 'Origin': 'http://127.0.0.1:3107'}
            supplied.update(headers or {})
            if isinstance(data, dict):
                data = json.dumps(data).encode()
                supplied['Content-Type'] = 'application/json'
            req = Request('http://127.0.0.1:3107' + path, data=data, method=method, headers=supplied)
            try:
                return browser.open(req, timeout=3)
            except HTTPError as error:
                return error

        deadline = time.monotonic() + 45
        while True:
            assert process.poll() is None, 'Next encerrou antes de iniciar.'
            try:
                response = request('/api/v1/cardapio')
                if response.status == 200:
                    break
            except (URLError, TimeoutError):
                pass
            assert time.monotonic() < deadline, 'Next não iniciou no prazo.'
            time.sleep(0.2)

        assert json.load(response) == {'categorias': []}
        assert request('/api/categorias', 'POST', {'nome': 'Teste'}).status == 401
        login = request('/api/v1/login', 'POST', {'email': 'proxy@example.com', 'senha': 'teste'})
        assert login.status == 200
        assert 'HttpOnly' in login.headers['Set-Cookie']
        assert json.load(request('/api/v1/me'))['usuario']['id'] == 7
        assert request('/api/categorias', 'POST', {'nome': 'Teste'}).status == 201
        assert request('/api/categorias', 'POST', {'nome': 'Teste'}, {
            'X-CSRF-Protection': '',
        }).status == 403
        assert request('/api/categorias', 'POST', {'nome': 'Teste'}, {
            'Origin': 'https://evil.example',
        }).status == 403
        assert request('/api/v1/produtos/10', 'PUT', {'nome': 'Editado'}).status == 200

        image = BytesIO()
        Image.new('RGB', (16, 16), 'red').save(image, format='PNG')
        boundary = 'test-proxy-boundary'
        body = (f'--{boundary}\r\nContent-Disposition: form-data; name="id_categoria"\r\n\r\n1\r\n'
                f'--{boundary}\r\nContent-Disposition: form-data; name="foto"; filename="pizza.png"\r\n'
                'Content-Type: image/png\r\n\r\n').encode() + image.getvalue() + f'\r\n--{boundary}--\r\n'.encode()
        response = request('/api/v1/produtos', 'POST', body, {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
        })
        assert response.status == 201
        assert json.load(response)['foto'].startswith('/static/uploads/produtos/')
        assert len(list((tmp_path / 'uploads').glob('*.png'))) == 1
        assert request('/api/v1/produtos/10', 'DELETE').status == 204
        assert deleted == [(10, 7)]
        assert request('/api/v1/logout', 'POST').status == 200
        assert request('/api/v1/me').status == 401
    finally:
        if process is not None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        server.shutdown()
        worker.join(timeout=5)
        server.server_close()
        log.close()
