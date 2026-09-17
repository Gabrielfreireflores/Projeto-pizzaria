import os
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

import psycopg
import pytest
from psycopg import sql
from psycopg.conninfo import make_conninfo

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app
from app.schemas.produto_schema import validar_produto


@pytest.fixture
def payload():
    return dict(nome='Pizza teste', tamanho='Grande', preco='49.90', id_categoria=1,
                ingredientes=[dict(id_ingrediente=1, quantidade_necessaria='1.000'),
                              dict(id_ingrediente=2, quantidade_necessaria='0.200')])


@pytest.mark.parametrize('campo,valor', [
    ('nome', None), ('nome', '  '), ('nome', 'x' * 121),
    ('tamanho', None), ('tamanho', 'x' * 31), ('preco', None),
    ('preco', '-0.01'), ('preco', True), ('preco', 'NaN'),
    ('preco', 'Infinity'), ('preco', '1.001'), ('preco', '100000000'),
    ('id_categoria', None), ('id_categoria', True), ('id_categoria', 0),
    ('id_categoria', 2147483648), ('ingredientes', []), ('ingredientes', None),
    ('ingredientes', [1]), ('disponivel', 'true'),
])
def test_campos_invalidos(payload, campo, valor):
    payload[campo] = valor
    with pytest.raises(ValueError):
        validar_produto(payload)


@pytest.mark.parametrize('valor', ['0', '-1', '0.0001', 'NaN', '1000000000', True, None])
def test_quantidade_invalida(payload, valor):
    payload['ingredientes'][0]['quantidade_necessaria'] = valor
    with pytest.raises(ValueError):
        validar_produto(payload)


def test_ingrediente_repetido(payload):
    payload['ingredientes'].append(deepcopy(payload['ingredientes'][0]))
    with pytest.raises(ValueError):
        validar_produto(payload)


def test_preco_zero_e_normalizacao(payload):
    payload.update(preco=0, nome='  Pizza  ')
    produto = validar_produto(payload)
    assert str(produto['preco']) == '0.00'
    assert produto['nome'] == 'Pizza'


def test_sem_autenticacao(payload):
    app = create_app()
    app.config.update(TESTING=True, SECRET_KEY='teste')
    client = app.test_client()
    assert client.post('/api/produtos', json=payload).status_code == 401


def test_json_invalido():
    app = create_app()
    app.config.update(TESTING=True, SECRET_KEY='teste')
    client = app.test_client()
    with client.session_transaction() as sess:
        sess['id_usuario'] = 2
    for body in ['{', '[]', 'null']:
        assert client.post('/api/produtos', data=body,
                           content_type='application/json').status_code == 400


@pytest.fixture
def banco():
    url = os.getenv('TEST_DATABASE_URL')
    if not url:
        pytest.skip('Defina TEST_DATABASE_URL para executar integração PostgreSQL.')
    schema = 'teste_produtos_' + uuid4().hex
    with psycopg.connect(url, autocommit=True) as conn:
        conn.execute(sql.SQL('CREATE SCHEMA {}').format(sql.Identifier(schema)))
    dsn = make_conninfo(url, options=f'-c search_path={schema}')
    try:
        with psycopg.connect(dsn, autocommit=True) as conn:
            arquivo = Path(__file__).resolve().parents[2] / 'db' / 'schema.sql'
            conn.execute(arquivo.read_text(encoding='utf-8'))
        yield dsn
    finally:
        with psycopg.connect(url, autocommit=True) as conn:
            conn.execute(sql.SQL('DROP SCHEMA {} CASCADE').format(sql.Identifier(schema)))


@pytest.fixture
def client(banco, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", banco)
    app = create_app()
    app.config.update(TESTING=True, SECRET_KEY='somente-testes')
    client = app.test_client()
    with client.session_transaction() as sess:
        sess['id_usuario'] = 2
    return client


def test_cadastro_e_relacao_nn(client, banco, payload):
    for nome in ['Pizza A', 'Pizza B']:
        payload['nome'] = nome
        resposta = client.post('/api/produtos', json=payload)
        assert resposta.status_code == 201
        assert resposta.json['preco'] == '49.90'
        with psycopg.connect(banco) as conn:
            linhas = conn.execute('''SELECT id_ingrediente, quantidade_necessaria
                FROM ingrediente_produto WHERE id_produto = %s ORDER BY id_ingrediente''',
                (resposta.json['id_produto'],)).fetchall()
            assert [linha[0] for linha in linhas] == [1, 2]
            assert [str(linha[1]) for linha in linhas] == ['1.000', '0.200']


@pytest.mark.parametrize('alvo', ['categoria', 'ingrediente'])
def test_referencia_inexistente_desfaz_tudo(client, banco, payload, alvo):
    if alvo == 'categoria':
        payload['id_categoria'] = 99999
    else:
        payload['ingredientes'][1]['id_ingrediente'] = 99999
    assert client.post('/api/produtos', json=payload).status_code == 400
    with psycopg.connect(banco) as conn:
        assert conn.execute('SELECT count(*) FROM produto').fetchone()[0] == 2
        assert conn.execute('SELECT count(*) FROM ingrediente_produto').fetchone()[0] == 3


def test_duplicidade(client, payload):
    assert client.post('/api/produtos', json=payload).status_code == 201
    assert client.post('/api/produtos', json=payload).status_code == 409
    payload['tamanho'] = 'Pequena'
    assert client.post('/api/produtos', json=payload).status_code == 201


@pytest.mark.parametrize('usuario', [1, 99999, 2])
def test_apenas_funcionario_ativo(client, banco, payload, usuario):
    if usuario == 2:
        with psycopg.connect(banco) as conn:
            conn.execute('UPDATE usuario SET ativo = FALSE WHERE id_usuario = 2')
    with client.session_transaction() as sess:
        sess['id_usuario'] = usuario
    assert client.post('/api/produtos', json=payload).status_code == 403


def test_categorias_e_produtos_na_mesma_aplicacao(monkeypatch):
    from app.services import categoria_services
    monkeypatch.setattr(categoria_services, 'listar_categorias', lambda: [[1, 'Pizzas']])
    app = create_app()
    app.config.update(TESTING=True, SECRET_KEY='teste')
    client = app.test_client()
    assert client.get('/categorias').json == [[1, 'Pizzas']]
    assert client.post('/produtos', json={}).status_code == 401
    assert client.post('/api/produtos', json={}).status_code == 401


@pytest.mark.parametrize('funcionario', [None, (False, 'funcionario', 1),
                                       (True, 'cliente', None), (True, 'funcionario', None)])
def test_servico_impede_cadastro_sem_permissao(monkeypatch, payload, funcionario):
    from app.services import produto_services
    from unittest.mock import Mock
    inserir = Mock()
    monkeypatch.setattr(produto_services, 'buscar_funcionario_repository', lambda _: funcionario)
    monkeypatch.setattr(produto_services, 'criar_produto_repository', inserir)
    with pytest.raises(PermissionError):
        produto_services.criar_produto(payload, 2)
    inserir.assert_not_called()


def test_servico_valida_antes_de_inserir(monkeypatch, payload):
    from app.services import produto_services
    from unittest.mock import Mock
    inserir = Mock()
    monkeypatch.setattr(produto_services, 'buscar_funcionario_repository', lambda _: (True, 'funcionario', 1))
    monkeypatch.setattr(produto_services, 'criar_produto_repository', inserir)
    payload['preco'] = '-1'
    with pytest.raises(ValueError):
        produto_services.criar_produto(payload, 2)
    inserir.assert_not_called()


def test_repository_desfaz_e_fecha_conexao(monkeypatch, payload):
    from app.repositories import produto_repository
    from unittest.mock import MagicMock
    conn = MagicMock()
    cursor = conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = (10, 'Pizza teste', 'Grande', 49.90, 1, True)
    cursor.executemany.side_effect = psycopg.errors.ForeignKeyViolation('ingrediente ausente')
    monkeypatch.setattr(produto_repository, 'get_connection', lambda: conn)
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        produto_repository.criar_produto(validar_produto(payload))
    conn.commit.assert_not_called()
    conn.rollback.assert_called_once()
    conn.close.assert_called_once()
