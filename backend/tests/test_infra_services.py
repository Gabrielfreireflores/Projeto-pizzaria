"""Integrações de infraestrutura sem conexão ou upload externo real."""
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import json
from threading import Lock
from unittest.mock import Mock
from urllib.error import HTTPError, URLError
from types import SimpleNamespace

import pytest
from PIL import Image

from app import create_app, database, login_rate_limit, provider_http, blob_storage
from app.controllers import auth_controller
from app.image_storage import get_image_storage
from app.repositories import pedido_repository
from app.services import auth_services, permissoes, produto_services
from . import api_client


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv('APP_ENV', 'development')
    monkeypatch.setenv('VERCEL', '0')
    monkeypatch.setenv('APP_ORIGINS', 'http://127.0.0.1:3000')
    monkeypatch.setenv('SECRET_KEY', 'chave-apenas-testes-nao-utilizar-em-producao')
    monkeypatch.setenv('IMAGE_STORAGE', 'local')
    monkeypatch.setenv('LOGIN_RATE_LIMITER', 'disabled')
    return create_app()


def enable_limits(app):
    app.config.update(LOGIN_RATE_LIMITER='upstash', LOGIN_RATE_LIMIT=3,
                      LOGIN_GLOBAL_LIMIT=100, LOGIN_WINDOW_SECONDS=60,
                      UPSTASH_REDIS_REST_URL='https://fake.upstash.io',
                      UPSTASH_REDIS_REST_TOKEN='token-apenas-testes')


class FakeAtomicRedis:
    """Modelo do contrato EVAL, com relógio e mutex; não substitui teste em Redis real."""
    def __init__(self):
        self.lock = Lock()
        self.now = 0
        self.values = {}
        self.commands = []

    def __call__(self, url, body, headers):
        command = json.loads(body)
        assert command[:3] == ['EVAL', login_rate_limit.LOGIN_SCRIPT, 2]
        assert headers['Authorization'].startswith('Bearer ')
        with self.lock:
            self.commands.append(command)
            keys, window, limits = command[3:5], command[5], command[6:8]
            retry = 0
            for key, limit in zip(keys, limits):
                count, expiry = self.values.get(key, (0, self.now + window))
                if expiry <= self.now:
                    count, expiry = 0, self.now + window
                self.values[key] = (count, expiry)
                if count >= limit:
                    retry = max(retry, expiry - self.now)
            if retry:
                return {'result': [0, retry]}
            for key in keys:
                count, expiry = self.values[key]
                self.values[key] = (count + 1, expiry)
            return {'result': [1, 0]}


def test_distributed_limit_expiry_and_private_keys(app, monkeypatch):
    enable_limits(app)
    redis = FakeAtomicRedis()
    monkeypatch.setattr(login_rate_limit, 'post_json_response', redis)
    with app.app_context():
        assert [login_rate_limit.check_login_rate('  CLIENTE@example.com ') for _ in range(4)] == [0, 0, 0, 60]
        assert login_rate_limit.check_login_rate('cliente@example.com') == 60
        redis.now = 61
        assert login_rate_limit.check_login_rate('cliente@example.com') == 0
    encoded = json.dumps(redis.commands)
    assert 'CLIENTE@example.com' not in encoded and 'cliente@example.com' not in encoded
    assert 'redis.call' in redis.commands[0][1]
    assert redis.commands[0][3].startswith('pizzaria:{login}:account:')


def test_concurrent_instances_use_one_atomic_eval_per_attempt(app, monkeypatch):
    enable_limits(app)
    redis = FakeAtomicRedis()
    monkeypatch.setattr(login_rate_limit, 'post_json_response', redis)
    def attempt(_):
        with app.app_context():
            return login_rate_limit.check_login_rate('same@example.com')
    with ThreadPoolExecutor(max_workers=12) as workers:
        results = list(workers.map(attempt, range(30)))
    assert results.count(0) == 3 and results.count(60) == 27
    assert len(redis.commands) == 30  # Não há GET/INCR/EXPIRE separados pela rede.


def test_global_limit_covers_rotating_accounts_without_trusting_ip_headers(app, monkeypatch):
    enable_limits(app)
    app.config['LOGIN_GLOBAL_LIMIT'] = 2
    redis = FakeAtomicRedis()
    monkeypatch.setattr(login_rate_limit, 'post_json_response', redis)
    monkeypatch.setattr(auth_services, 'autenticar_usuario', lambda **kwargs: (7, kwargs['email']))
    client = api_client(app)
    for number, status in enumerate((200, 200, 429)):
        response = client.post('/api/v1/login', json={'email': f'{number}@example.com', 'senha': 'teste'},
                               headers={'X-Forwarded-For': f'1.2.3.{number}'})
        assert response.status_code == status
    assert response.headers['Retry-After'] == '60'
    assert '1.2.3.' not in json.dumps(redis.commands)


@pytest.mark.parametrize('provider_result', [None, [], [0, 0], [2, 0], [False, 0], [1, -1], [1, 10]])
def test_invalid_limiter_response_fails_closed(app, monkeypatch, provider_result):
    enable_limits(app)
    monkeypatch.setattr(login_rate_limit, 'post_json_response', lambda *args: {'result': provider_result})
    auth = Mock()
    monkeypatch.setattr(auth_services, 'autenticar_usuario', auth)
    response = api_client(app).post('/api/v1/login', json={'email': 'a@example.com', 'senha': 'segredo'})
    assert response.status_code == 503
    auth.assert_not_called()


def test_limiter_outage_does_not_leak_or_authenticate(app, monkeypatch, caplog):
    enable_limits(app)
    def fail(*args):
        raise RuntimeError('token-privado-do-provedor')
    monkeypatch.setattr(login_rate_limit, 'post_json_response', fail)
    auth = Mock()
    monkeypatch.setattr(auth_services, 'autenticar_usuario', auth)
    response = api_client(app).post('/api/v1/login', json={'email': 'a@example.com', 'senha': 'senha-secreta'})
    assert response.status_code == 503
    assert 'token-privado' not in response.get_data(as_text=True) + caplog.text
    assert 'senha-secreta' not in caplog.text
    auth.assert_not_called()


@pytest.mark.parametrize('mode', ['disabled', 'upstash'])
def test_production_cannot_silently_disable_distributed_limit(app, monkeypatch, mode):
    app.config.update(PRODUCTION=True, LOGIN_RATE_LIMITER=mode,
                      UPSTASH_REDIS_REST_URL='', UPSTASH_REDIS_REST_TOKEN='')
    auth = Mock()
    monkeypatch.setattr(auth_services, 'autenticar_usuario', auth)
    assert api_client(app).post('/api/v1/login', json={'email': 'a@example.com', 'senha': 'teste'}).status_code == 503
    auth.assert_not_called()


def test_legitimate_login_keeps_session_with_limiter(app, monkeypatch):
    enable_limits(app)
    monkeypatch.setattr(login_rate_limit, 'post_json_response', FakeAtomicRedis())
    monkeypatch.setattr(auth_services, 'autenticar_usuario', lambda **kwargs: (7, kwargs['email']))
    client = api_client(app)
    assert client.post('/api/v1/login', json={'email': 'a@example.com', 'senha': 'teste'}).status_code == 200
    with client.session_transaction() as sess:
        assert sess['id_usuario'] == 7


@pytest.mark.parametrize('url,production,expected_ssl', [
    ('postgresql://test:fake@localhost:5432/pizzaria', False, None),
    ('postgresql://test:fake@db-pooler.test.neon.tech/db?sslmode=require', True, 'require'),
    ('postgresql://test:fake@db.example/db?sslmode=verify-full', True, 'verify-full'),
])
def test_database_direct_and_pooled_connections_use_timeout_without_local_pool(monkeypatch, url, production, expected_ssl):
    monkeypatch.setenv('DATABASE_URL', url)
    monkeypatch.setenv('APP_ENV', 'production' if production else 'development')
    monkeypatch.setenv('VERCEL', '0')
    monkeypatch.setenv('DB_CONNECT_TIMEOUT', '7')
    connect = Mock()
    monkeypatch.setattr(database.psycopg, 'connect', connect)
    assert database.get_connection() is connect.return_value
    params = connect.call_args.kwargs
    assert params['connect_timeout'] == 7 and params['prepare_threshold'] is None
    assert params.get('sslmode') == expected_ssl
    if '.neon.tech' in url:
        assert params['channel_binding'] == 'require'


@pytest.mark.parametrize('sslmode', ['disable', 'allow', 'prefer'])
def test_database_rejects_plaintext_production_connections(monkeypatch, sslmode):
    monkeypatch.setenv('APP_ENV', 'production')
    monkeypatch.setenv('DATABASE_URL', f'postgresql://test:fake@db.example/db?sslmode={sslmode}')
    connect = Mock()
    monkeypatch.setattr(database.psycopg, 'connect', connect)
    with pytest.raises(RuntimeError, match='TLS'):
        database.get_connection()
    connect.assert_not_called()


@pytest.mark.parametrize('timeout', ['0', '31', 'abc'])
def test_database_rejects_invalid_timeout(monkeypatch, timeout):
    monkeypatch.setenv('DATABASE_URL', 'postgresql://test:fake@localhost/db')
    monkeypatch.setenv('DB_CONNECT_TIMEOUT', timeout)
    with pytest.raises(RuntimeError):
        database.get_connection()


@pytest.mark.parametrize('error', [False, True])
def test_order_transaction_still_closes_and_commits_or_rolls_back(monkeypatch, error):
    connection = Mock()
    monkeypatch.setattr(pedido_repository, 'get_connection', lambda: connection)
    try:
        with pedido_repository.transacao_pedido():
            if error:
                raise ValueError('teste')
    except ValueError:
        pass
    connection.close.assert_called_once()
    (connection.rollback if error else connection.commit).assert_called_once()


@pytest.fixture
def blob_store(app, monkeypatch):
    app.config['IMAGE_STORAGE'] = 'blob'
    monkeypatch.setenv('BLOB_READ_WRITE_TOKEN', 'token-apenas-testes')
    monkeypatch.setenv('BLOB_STORE_ID', 'store_teststore')
    return blob_storage.BlobImageStorage()


def successful_blob(key, *args, **kwargs):
    return SimpleNamespace(pathname=key,
        url=f'https://teststore.public.blob.vercel-storage.com/{key}')


def test_blob_official_sync_sdk_no_overwrite_and_safe_delete(app, blob_store, monkeypatch):
    put = Mock(side_effect=successful_blob)
    delete = Mock()
    monkeypatch.setattr(blob_storage.blob, 'put_blob', put)
    monkeypatch.setattr(blob_storage.blob, 'delete_blob', delete)
    with app.app_context():
        assert isinstance(get_image_storage(), blob_storage.BlobImageStorage)
        url, key = blob_store.save(b'image-already-validated', '.png')
        blob_store.delete(key)
    assert url.startswith('https://teststore.public.blob.vercel-storage.com/pizzaria/produtos/')
    assert put.call_args.kwargs == dict(access='public', content_type='image/png',
                                        add_random_suffix=False, allow_overwrite=False)
    delete.assert_called_once_with(key)
    with pytest.raises(ValueError):
        blob_store.delete('../existing-image')
    assert delete.call_count == 1


def test_blob_requires_configuration_without_network(app, blob_store, monkeypatch):
    monkeypatch.setenv('BLOB_READ_WRITE_TOKEN', '')
    put = Mock()
    monkeypatch.setattr(blob_storage.blob, 'put_blob', put)
    with pytest.raises(RuntimeError, match='não configurado'):
        blob_store.save(b'image', '.png')
    put.assert_not_called()


def test_official_blob_sdk_upload_over_mock_http_transport(blob_store, monkeypatch):
    """Exercita o SDK instalado e serialização real, sem abrir sockets."""
    import httpx2
    from vercel.api import session as sdk_session
    monkeypatch.setenv('BLOB_READ_WRITE_TOKEN', 'vercel_blob_rw_teststore_fake-secret')
    requests = []
    def handler(request):
        requests.append(request)
        key = request.url.params.get('pathname')
        url = f'https://teststore.public.blob.vercel-storage.com/{key}'
        return httpx2.Response(200, json={
            'url': url, 'downloadUrl': url + '?download=1', 'pathname': key,
            'contentType': 'image/png', 'contentDisposition': 'inline', 'etag': 'etag-test',
        })
    monkeypatch.setattr(blob_storage, 'session', lambda **kwargs: sdk_session(
        service_options=kwargs['service_options'],
        httpx_client_factory=lambda: httpx2.Client(transport=httpx2.MockTransport(handler)),
    ))
    url, key = blob_store.save(b'image-bytes', '.png')
    assert url.endswith(key)
    assert len(requests) == 1
    assert requests[0].content == b'image-bytes'
    assert requests[0].url.host == 'vercel.com'


@pytest.mark.parametrize('failure', [RuntimeError('token-privado'),
    blob_storage.blob.BlobAccessError('token-privado')])
def test_blob_provider_errors_do_not_expose_details(app, blob_store, monkeypatch, failure):
    def fail(*args, **kwargs):
        raise failure
    monkeypatch.setattr(blob_storage.blob, 'put_blob', fail)
    if isinstance(failure, blob_storage.blob.BlobError):
        with pytest.raises(RuntimeError) as error:
            blob_store.save(b'image', '.png')
        assert 'token-privado' not in str(error.value)
    else:
        # Falha técnica inesperada continua sendo serializada genericamente pelo controller.
        with pytest.raises(RuntimeError):
            blob_store.save(b'image', '.png')


def test_blob_rejects_unexpected_delivery_host(blob_store, monkeypatch):
    monkeypatch.setattr(blob_storage.blob, 'put_blob', lambda key, *args, **kwargs:
                        SimpleNamespace(pathname=key, url='https://evil.example/image.png'))
    with pytest.raises(RuntimeError, match='Resposta inválida'):
        blob_store.save(b'image', '.png')


def test_blob_cleanup_after_database_failure_preserves_database_contract(app, blob_store, monkeypatch):
    put = Mock(side_effect=successful_blob)
    delete = Mock()
    monkeypatch.setattr(blob_storage.blob, 'put_blob', put)
    monkeypatch.setattr(blob_storage.blob, 'delete_blob', delete)
    monkeypatch.setattr(permissoes, 'buscar_funcionario_por_usuario', lambda _: (True, 'funcionario', 1))
    def fail(*args):
        raise ValueError('Categoria inválida.')
    monkeypatch.setattr(produto_services, 'criar_produto', fail)
    image = BytesIO()
    Image.new('RGB', (16, 16), 'red').save(image, format='PNG')
    image.seek(0)
    client = api_client(app)
    with client.session_transaction() as sess:
        sess['id_usuario'] = 7
    response = client.post('/api/v1/produtos', data={'id_categoria': '1', 'foto': (image, 'pizza.png')})
    assert response.status_code == 400
    delete.assert_called_once_with(put.call_args.args[0])


def test_blob_delete_outage_keeps_original_error_without_deleting_existing_assets(app, blob_store, monkeypatch, caplog):
    monkeypatch.setattr(blob_storage.blob, 'put_blob', successful_blob)
    delete = Mock(side_effect=blob_storage.blob.BlobAccessError('token-privado'))
    monkeypatch.setattr(blob_storage.blob, 'delete_blob', delete)
    monkeypatch.setattr(permissoes, 'buscar_funcionario_por_usuario', lambda _: (True, 'funcionario', 1))
    def fail(*args):
        raise ValueError('Categoria inválida.')
    monkeypatch.setattr(produto_services, 'criar_produto', fail)
    image = BytesIO()
    Image.new('RGB', (16, 16)).save(image, format='PNG')
    image.seek(0)
    client = api_client(app)
    with client.session_transaction() as sess:
        sess['id_usuario'] = 7
    response = client.post('/api/v1/produtos', data={'id_categoria': '1', 'foto': (image, 'pizza.png')})
    assert response.status_code == 400
    assert response.json == {'erro': 'Categoria inválida.'}
    assert delete.call_count == 1
    assert 'token-privado' not in caplog.text


def test_invalid_image_is_rejected_before_blob_call(app, blob_store, monkeypatch):
    put = Mock()
    monkeypatch.setattr(blob_storage.blob, 'put_blob', put)
    monkeypatch.setattr(permissoes, 'buscar_funcionario_por_usuario', lambda _: (True, 'funcionario', 1))
    client = api_client(app)
    with client.session_transaction() as sess:
        sess['id_usuario'] = 7
    response = client.post('/api/v1/produtos', data={
        'id_categoria': '1', 'foto': (BytesIO(b'not an image'), 'pizza.png'),
    })
    assert response.status_code == 400
    put.assert_not_called()


@pytest.mark.parametrize('failure', [URLError('token-sensivel'), HTTPError('https://fake', 429, 'segredo', {}, None)])
def test_http_provider_errors_are_generic(monkeypatch, failure):
    opener = Mock()
    opener.open.side_effect = failure
    monkeypatch.setattr(provider_http, 'build_opener', lambda *args: opener)
    with pytest.raises(RuntimeError) as error:
        provider_http.post_json_response('https://fake.example', b'{}', {})
    assert 'token' not in str(error.value) and 'segredo' not in str(error.value)
