import importlib.util
from io import BytesIO
from pathlib import Path
from unittest.mock import Mock

import psycopg
import pytest
from PIL import Image

from app import create_app
from app import image_storage
from app.controllers import auth_controller
from app.services import auth_services, categoria_services, equipe_services, permissoes, produto_services
from . import api_client


@pytest.fixture
def app(monkeypatch, tmp_path):
    monkeypatch.setenv('APP_ENV', 'development')
    monkeypatch.setenv('VERCEL', '0')
    monkeypatch.setenv('SECRET_KEY', 'chave-exclusiva-dos-testes-locais')
    monkeypatch.setenv('APP_ORIGINS', 'http://127.0.0.1:3000')
    monkeypatch.setenv('IMAGE_STORAGE', 'local')
    app = create_app()
    app.config.update(TESTING=True, UPLOAD_FOLDER=str(tmp_path / 'uploads'))
    return app


def logged_in(app):
    client = api_client(app)
    with client.session_transaction() as sess:
        sess['id_usuario'] = 7
    return client


@pytest.mark.parametrize('method,path', [
    ('post', '/api/v1/login'), ('post', '/api/v1/logout'),
    ('post', '/api/categorias'), ('post', '/api/v1/produtos'),
    ('put', '/api/v1/produtos/1'), ('delete', '/api/v1/funcionarios/1'),
])
def test_csrf_header_required_even_without_origin(app, method, path):
    response = getattr(app.test_client(), method)(path, json={})
    assert response.status_code == 403
    assert 'CSRF' in response.json['erro']


@pytest.mark.parametrize('origin', ['https://evil.example', 'null',
                                      'http://127.0.0.1:3000.evil.example'])
def test_csrf_rejects_untrusted_origins(app, origin):
    response = api_client(app).post('/api/v1/logout', headers={'Origin': origin})
    assert response.status_code == 403


def test_csrf_rejects_cross_site_and_does_not_enable_cors(app):
    client = api_client(app)
    assert client.post('/api/v1/logout', headers={'Sec-Fetch-Site': 'cross-site'}).status_code == 403
    response = client.options('/api/v1/logout', headers={
        'Origin': 'https://evil.example', 'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'X-CSRF-Protection',
    })
    assert 'Access-Control-Allow-Origin' not in response.headers
    assert 'Access-Control-Allow-Headers' not in response.headers


def test_csrf_allows_frontend_and_local_http(app):
    response = api_client(app).post('/api/v1/logout', headers={
        'Origin': 'http://127.0.0.1:3000', 'Sec-Fetch-Site': 'same-origin',
    })
    assert response.status_code == 200
    assert response.headers['Cache-Control'] == 'no-store'
    assert app.config['SESSION_COOKIE_SECURE'] is False


@pytest.mark.parametrize('role', [None, (False, 'funcionario', 3),
                                  (True, 'cliente', None), (True, 'funcionario', None)])
def test_category_requires_active_staff(app, monkeypatch, role):
    monkeypatch.setattr(permissoes, 'buscar_funcionario_por_usuario', lambda _: role)
    create = Mock()
    monkeypatch.setattr(categoria_services, 'criar_categoria', create)
    assert logged_in(app).post('/api/categorias', json={'nome': 'Teste'}).status_code == 403
    create.assert_not_called()


def test_category_requires_session_and_preserves_authorized_creation(app, monkeypatch):
    client = api_client(app)
    assert client.post('/api/categorias', json={'nome': 'Teste'}).status_code == 401
    monkeypatch.setattr(permissoes, 'buscar_funcionario_por_usuario', lambda _: (True, 'funcionário', 3))
    monkeypatch.setattr(categoria_services, 'criar_categoria', lambda name: (4, name))
    client = logged_in(app)
    assert client.post('/api/categorias', json=[]).status_code == 400
    assert client.post('/api/categorias', json={'nome': 10}).status_code == 400
    response = client.post('/api/categorias', json={'nome': 'Teste'})
    assert response.status_code == 201
    assert response.json['categoria']['id_categoria'] == 4


def test_authorized_team_registration_remains_available(app, monkeypatch):
    monkeypatch.setattr(permissoes, 'buscar_funcionario_por_usuario', lambda _: (True, 'funcionario', 3))
    monkeypatch.setattr(equipe_services, 'validar_funcionario', lambda data, criando: data)
    monkeypatch.setattr(equipe_services, 'generate_password_hash', lambda _: 'hash-teste')
    monkeypatch.setattr(equipe_services.repo, 'criar_membro', lambda *args:
                        (8, 'Novo Funcionário', '123', 'Atendente', '16999999999', 'staff@example.com', True))
    assert logged_in(app).post('/api/v1/funcionarios', json={'senha': 'teste'}).status_code == 201


@pytest.mark.parametrize('route', ['/api/v1/pedidos', '/api/categorias', '/api/v1/login'])
def test_internal_errors_never_expose_sql_or_credentials(app, monkeypatch, caplog, route):
    def fail(*args, **kwargs):
        raise psycopg.OperationalError('SELECT segredo password=nao-expor')
    from app.services import pedido_services
    monkeypatch.setattr(pedido_services, 'criar_pedido', fail)
    monkeypatch.setattr(categoria_services, 'criar_categoria', fail)
    monkeypatch.setattr(auth_services, 'autenticar_usuario', fail)
    monkeypatch.setattr(permissoes, 'buscar_funcionario_por_usuario', lambda _: (True, 'funcionario', 3))
    response = logged_in(app).post(route, json={'nome': 'Teste', 'email': 'teste@example.com', 'senha': 'teste'})
    assert response.status_code in (500, 503)
    assert 'segredo' not in response.get_data(as_text=True)
    assert 'nao-expor' not in caplog.text


@pytest.mark.parametrize('body', [[], None, {'email': [], 'senha': 'teste'},
                                    {'email': 'teste@example.com', 'senha': {}}])
def test_invalid_login_input_is_client_error(app, body):
    response = api_client(app).post('/api/v1/login', json=body)
    assert response.status_code == 400


def production(monkeypatch):
    monkeypatch.setenv('APP_ENV', 'production')
    monkeypatch.setenv('SECRET_KEY', 'somente-testes-A7c9e2f4b6d8g0h1j3k5m7n9')
    monkeypatch.setenv('APP_ORIGINS', 'https://frontend.example')
    monkeypatch.setenv('IMAGE_STORAGE', 'disabled')


@pytest.mark.parametrize('key,value', [('SECRET_KEY', ''), ('SECRET_KEY', 'x' * 40),
    ('APP_ORIGINS', ''), ('APP_ORIGINS', '*'), ('APP_ORIGINS', 'http://frontend.example'),
    ('IMAGE_STORAGE', 'local')])
def test_production_rejects_unsafe_configuration(monkeypatch, key, value):
    production(monkeypatch)
    monkeypatch.setenv(key, value)
    with pytest.raises((RuntimeError, ValueError)):
        create_app()


def test_vercel_preview_also_uses_production_security(monkeypatch):
    production(monkeypatch)
    monkeypatch.setenv('APP_ENV', 'development')
    monkeypatch.setenv('VERCEL', '1')
    assert create_app().config['SESSION_COOKIE_SECURE'] is True


def test_secure_cookie_is_stable_between_instances_and_host_only(monkeypatch):
    production(monkeypatch)
    # Este teste isola cookies; o limitador real é coberto por test_infra_services.
    monkeypatch.setattr(auth_controller, 'check_login_rate', lambda _: 0)
    monkeypatch.setattr(auth_services, 'autenticar_usuario', lambda **kwargs: (7, 'test@example.com'))
    monkeypatch.setattr(auth_controller, 'buscar_usuario_por_id', lambda _: (7, 'test@example.com', True,
                        'cliente', '', 'Cliente Teste', '16999999999', None))
    first = api_client(create_app())
    response = first.post('/api/v1/login', base_url='https://frontend.example',
                          headers={'Origin': 'https://frontend.example'},
                          json={'email': 'test@example.com', 'senha': 'teste'})
    assert response.status_code == 200
    cookie = response.headers['Set-Cookie']
    assert all(flag in cookie for flag in ('Secure', 'HttpOnly', 'SameSite=Lax', 'Path=/'))
    assert 'Domain=' not in cookie
    second = api_client(create_app())
    second.set_cookie('session', first.get_cookie('session', domain='frontend.example').value,
                      domain='frontend.example')
    assert second.get('/api/v1/me', base_url='https://frontend.example').json['usuario']['id'] == 7


def image_bytes(fmt='PNG'):
    stream = BytesIO()
    Image.new('RGB', (16, 16), 'red').save(stream, format=fmt)
    return stream.getvalue()


def upload(app, content, name='pizza.png', mimetype='image/png'):
    from werkzeug.datastructures import FileStorage
    with app.app_context():
        return image_storage.save_product_image(FileStorage(
            stream=BytesIO(content), filename=name, content_type=mimetype))


@pytest.mark.parametrize('fmt,extension,mimetype', [('PNG', '.png', 'image/png'),
    ('JPEG', '.jpg', 'image/jpeg'), ('WEBP', '.webp', 'image/webp')])
def test_local_storage_validates_real_image_and_uses_safe_name(app, fmt, extension, mimetype):
    url, key = upload(app, image_bytes(fmt), '../../pizza' + extension, mimetype)
    assert Path(key).parent == Path(app.config['UPLOAD_FOLDER'])
    assert url.startswith('/static/uploads/produtos/')
    assert Path(key).name != 'pizza' + extension
    assert Path(key).read_bytes() == image_bytes(fmt)


@pytest.mark.parametrize('content,name,mimetype', [
    (b'<script>bad</script>', 'pizza.png', 'image/png'),
    (b'', 'pizza.png', 'image/png'),
    (image_bytes(), 'pizza.jpg', 'image/jpeg'),
    (image_bytes(), 'pizza.png', 'text/html'),
    (image_bytes()[:40], 'pizza.png', 'image/png'),
])
def test_invalid_uploads_do_not_write_files(app, content, name, mimetype):
    with pytest.raises(ValueError):
        upload(app, content, name, mimetype)
    assert not Path(app.config['UPLOAD_FOLDER']).exists()


def test_upload_rejects_size_and_dimensions(app, monkeypatch):
    monkeypatch.setattr(image_storage, 'MAX_BYTES', 8)
    with pytest.raises(ValueError, match='3 MiB'):
        upload(app, image_bytes())
    monkeypatch.setattr(image_storage, 'MAX_BYTES', 3 * 1024 * 1024)
    monkeypatch.setattr(image_storage, 'MAX_PIXELS', 10)
    with pytest.raises(ValueError, match='dimensões'):
        upload(app, image_bytes())


@pytest.mark.parametrize('extra,expected', [(0, 201), (1, 400)])
def test_production_multipart_image_limit(monkeypatch, extra, expected):
    production(monkeypatch)
    monkeypatch.setenv('IMAGE_STORAGE', 'blob')
    app = create_app()
    app.config['TESTING'] = True
    monkeypatch.setattr(permissoes, 'buscar_funcionario_por_usuario',
                        lambda _: (True, 'funcionario', 3))
    save = Mock(return_value=('https://store.example/test.png', 'test-key'))
    monkeypatch.setattr(image_storage.BlobImageStorage, 'save', save)
    create = Mock(return_value={'id_produto': 10})
    monkeypatch.setattr(produto_services, 'criar_produto', create)
    content = image_bytes()
    content += b'\0' * (3 * 1024 * 1024 + extra - len(content))
    response = logged_in(app).post('/api/v1/produtos', data={
        'id_categoria': '1', 'foto': (BytesIO(content), 'pizza.png'),
    })
    assert response.status_code == expected
    assert save.call_count == create.call_count == (expected == 201)


def test_production_rejects_total_multipart_before_storage(monkeypatch):
    production(monkeypatch)
    app = create_app()
    app.config['TESTING'] = True
    save = Mock()
    create = Mock()
    monkeypatch.setattr(image_storage.BlobImageStorage, 'save', save)
    monkeypatch.setattr(produto_services, 'criar_produto', create)
    response = logged_in(app).post('/api/v1/produtos', data={
        'id_categoria': '1',
        'foto': (BytesIO(b'x' * (4 * 1024 * 1024)), 'pizza.png'),
    })
    assert response.status_code == 413
    assert response.is_json
    save.assert_not_called()
    create.assert_not_called()


def test_storage_never_deletes_paths_outside_upload_directory(app, tmp_path):
    sentinel = tmp_path / 'existing.png'
    sentinel.write_bytes(image_bytes())
    with app.app_context(), pytest.raises(ValueError):
        image_storage.LocalImageStorage().delete(str(sentinel))
    assert sentinel.exists()


def test_disabled_storage_fails_without_creating_directory(app):
    app.config['IMAGE_STORAGE'] = 'disabled'
    with pytest.raises(RuntimeError, match='não configurado'):
        upload(app, image_bytes())
    assert not Path(app.config['UPLOAD_FOLDER']).exists()


def test_storage_permission_error_does_not_expose_path(app, monkeypatch):
    monkeypatch.setattr(permissoes, 'buscar_funcionario_por_usuario', lambda _: (True, 'funcionario', 3))
    def fail(*args, **kwargs):
        raise PermissionError('caminho-interno-confidencial')
    monkeypatch.setattr(Path, 'mkdir', fail)
    response = logged_in(app).post('/api/v1/produtos', data={
        'id_categoria': '1', 'foto': (BytesIO(image_bytes()), 'pizza.png'),
    })
    assert response.status_code == 503
    assert 'confidencial' not in response.get_data(as_text=True)


def test_failed_product_insert_cleans_only_new_upload(app, monkeypatch):
    monkeypatch.setattr(permissoes, 'buscar_funcionario_por_usuario', lambda _: (True, 'funcionario', 3))
    def fail(*args):
        raise ValueError('Categoria inválida.')
    monkeypatch.setattr(produto_services, 'criar_produto', fail)
    folder = Path(app.config['UPLOAD_FOLDER'])
    folder.mkdir()
    existing = folder / 'existing.png'
    existing.write_bytes(image_bytes())
    response = logged_in(app).post('/api/v1/produtos', data={
        'id_categoria': '1', 'foto': (BytesIO(image_bytes()), 'pizza.png'),
    })
    assert response.status_code == 400
    assert list(folder.iterdir()) == [existing]


def test_non_staff_cannot_store_upload(app, monkeypatch):
    monkeypatch.setattr(permissoes, 'buscar_funcionario_por_usuario', lambda _: None)
    response = logged_in(app).post('/api/v1/produtos', data={
        'id_categoria': '1', 'foto': (BytesIO(image_bytes()), 'pizza.png'),
    })
    assert response.status_code == 403
    assert not Path(app.config['UPLOAD_FOLDER']).exists()


def test_serverless_import_never_starts_server_or_creates_directory(app, monkeypatch):
    from flask import Flask
    server = Mock(side_effect=AssertionError('Servidor não deve iniciar.'))
    monkeypatch.setattr(Flask, 'run', server)
    connect = Mock(side_effect=AssertionError('Banco não deve conectar na importação.'))
    monkeypatch.setattr(psycopg, 'connect', connect)
    monkeypatch.setattr(Path, 'mkdir', Mock(side_effect=AssertionError('Escrita na importação.')))
    module_path = Path(__file__).resolve().parents[1] / 'main.py'
    spec = importlib.util.spec_from_file_location('vercel_entry_test', module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert isinstance(module.app, Flask)
    server.assert_not_called()
    connect.assert_not_called()
