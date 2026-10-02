import os
import sys
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

import psycopg
import pytest
from psycopg import sql
from psycopg.conninfo import make_conninfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from app.schemas.pedido_schema import validar_pedido
from app.services import pedido_services, produto_services


@pytest.fixture
def payload():
    return {
        'contato': {'nome': 'Ana Teste', 'telefone': '(16) 99999-0001'},
        'endereco': {'cep': '14150-000', 'logradouro': 'Rua Teste', 'numero': '12',
                     'bairro': 'Centro', 'cidade': 'Serrana', 'uf': 'sp'},
        'forma_pagamento': 'PIX',
        'itens': [{'id_produto': 1, 'quantidade': 2}, {'id_produto': 2, 'quantidade': 1}],
    }


@pytest.mark.parametrize('campo,valor', [
    ('contato', None), ('contato', []), ('endereco', None), ('endereco', 'Rua'),
    ('forma_pagamento', None), ('forma_pagamento', ' '),
    ('itens', None), ('itens', []), ('itens', [None]), ('itens', [{}]),
])
def test_payload_invalido(payload, campo, valor):
    payload[campo] = valor
    with pytest.raises(ValueError):
        validar_pedido(payload)


@pytest.mark.parametrize('quantidade', [0, -1, True, '2', 1.5, 2147483648])
def test_quantidade_invalida(payload, quantidade):
    payload['itens'][0]['quantidade'] = quantidade
    with pytest.raises(ValueError):
        validar_pedido(payload)


@pytest.mark.parametrize('grupo,campo,valor', [
    ('contato', 'nome', ' '), ('contato', 'telefone', '123'),
    ('contato', 'telefone', 'abc16999990001'), ('endereco', 'cep', '000'),
    ('endereco', 'uf', 'ABC'), ('endereco', 'logradouro', ''),
    ('endereco', 'complemento', 123),
])
def test_contato_endereco_invalidos(payload, grupo, campo, valor):
    payload[grupo][campo] = valor
    with pytest.raises(ValueError):
        validar_pedido(payload)


def test_produto_duplicado(payload):
    payload['itens'].append(deepcopy(payload['itens'][0]))
    with pytest.raises(ValueError):
        validar_pedido(payload)


def test_normalizacao_sem_mutar_payload(payload):
    original = deepcopy(payload)
    normalizado = validar_pedido(payload)
    assert normalizado['endereco']['uf'] == 'SP'
    assert normalizado['endereco']['complemento'] is None
    assert payload == original


@pytest.fixture
def http():
    app = create_app()
    app.config.update(TESTING=True, SECRET_KEY='somente-testes', TAXA_ENTREGA='5.00')
    return app.test_client()


def test_sem_sessao(http, payload):
    assert http.post('/api/v1/pedidos', json=payload).status_code == 401


@pytest.mark.parametrize('corpo', ['{', '[]', 'null', '"texto"'])
def test_json_invalido(http, corpo):
    with http.session_transaction() as sess:
        sess['id_usuario'] = 1
    assert http.post('/api/v1/pedidos', data=corpo,
                     content_type='application/json').status_code == 400


@pytest.mark.parametrize('rota', ['/produtos', '/api/produtos', '/api/v1/produtos'])
def test_lista_vazia(http, monkeypatch, rota):
    monkeypatch.setattr(produto_services, 'listar_produtos_repository', lambda: [])
    resposta = http.get(rota)
    assert resposta.status_code == 200
    assert resposta.json == {'produtos': []}


def test_erro_banco_sem_detalhes(http, monkeypatch):
    def falha():
        raise psycopg.OperationalError('detalhe interno')
    monkeypatch.setattr(produto_services, 'listar_produtos_repository', falha)
    resposta = http.get('/api/v1/produtos')
    assert resposta.status_code == 503
    assert 'detalhe interno' not in resposta.get_data(as_text=True)


@pytest.fixture
def banco(monkeypatch):
    url = os.getenv('TEST_DATABASE_URL')
    if not url:
        pytest.skip('Defina TEST_DATABASE_URL para integração PostgreSQL.')
    schema = 'teste_h06_' + uuid4().hex
    with psycopg.connect(url, autocommit=True) as conn:
        conn.execute(sql.SQL('CREATE SCHEMA {}').format(sql.Identifier(schema)))
    dsn = make_conninfo(url, options=f'-c search_path={schema}')
    try:
        raiz = Path(__file__).resolve().parents[2]
        with psycopg.connect(dsn, autocommit=True) as conn:
            conn.execute((raiz / 'db/schema.sql').read_text(encoding='utf-8'))
            migration = (raiz / 'db/migrations/001_pedido_contato.sql').read_text(encoding='utf-8')
            conn.execute(migration)
            conn.execute(migration)  # Migração pode ser reaplicada.
        monkeypatch.setenv('DATABASE_URL', dsn)
        yield dsn
    finally:
        with psycopg.connect(url, autocommit=True) as conn:
            conn.execute(sql.SQL('DROP SCHEMA {} CASCADE').format(sql.Identifier(schema)))


@pytest.fixture
def client(http, banco):
    with http.session_transaction() as sess:
        sess['id_usuario'] = 1
    return http


def contagens(banco):
    with psycopg.connect(banco) as conn:
        return tuple(conn.execute(f'SELECT count(*) FROM {tabela}').fetchone()[0]
                     for tabela in ('pedido', 'item_pedido', 'endereco'))


def test_listagem_completa(client, banco):
    with psycopg.connect(banco) as conn:
        conn.execute('UPDATE produto SET disponivel = FALSE WHERE id_produto = 2')
    resposta = client.get('/api/v1/produtos')
    assert resposta.status_code == 200
    pizza, bebida = resposta.json['produtos']
    assert pizza['categoria'] == {'id_categoria': 1, 'nome': 'Pizzas'}
    assert pizza['preco'] == '49.90'
    assert len(pizza['ingredientes']) == 3
    assert pizza['ingredientes'][0]['quantidade_necessaria'] == '1.000'
    assert pizza['ingredientes'][0]['unidade_medida'] == 'unidade'
    assert bebida['ingredientes'] == []
    assert bebida['disponivel'] is False


def test_pedido_recalcula_e_fixa_status(client, banco, payload):
    payload.update(valor_total='0.01', taxa_entrega='0', status='ENTREGUE', id_cliente=999, id_funcionario=999)
    payload['itens'][0].update(preco_unitario='0.01', subtotal='0.02')
    resposta = client.post('/api/v1/pedidos', json=payload)
    assert resposta.status_code == 201
    assert resposta.json['valor_total'] == '116.80'
    assert resposta.json['taxa_entrega'] == '5.00'
    assert resposta.json['status'] == 'RECEBIDO'
    with psycopg.connect(banco) as conn:
        registro = conn.execute('''SELECT p.id_cliente, p.id_funcionario, s.nome_status,
            p.nome_contato, p.telefone_contato, e.logradouro
            FROM pedido p JOIN status s USING (id_status)
            JOIN endereco e USING (id_endereco) WHERE id_pedido = %s''',
            (resposta.json['id_pedido'],)).fetchone()
        assert registro == (1, None, 'Recebido', 'Ana Teste', '(16) 99999-0001', 'Rua Teste')
        itens = conn.execute('''SELECT quantidade, preco_unitario, subtotal FROM item_pedido
            WHERE id_pedido = %s ORDER BY id_produto''', (resposta.json['id_pedido'],)).fetchall()
        assert str(itens[0][2]) == '99.80'
        assert len(itens) == 2


@pytest.mark.parametrize('problema', ['inexistente', 'indisponivel', 'total_excessivo'])
def test_produto_invalido_nao_grava(client, banco, payload, problema):
    antes = contagens(banco)
    if problema == 'inexistente':
        payload['itens'][0]['id_produto'] = 99999
    elif problema == 'indisponivel':
        with psycopg.connect(banco) as conn:
            conn.execute('UPDATE produto SET disponivel = FALSE WHERE id_produto = 1')
    else:
        payload['itens'][0]['quantidade'] = 2147483647
    assert client.post('/api/v1/pedidos', json=payload).status_code == 400
    assert contagens(banco) == antes


@pytest.mark.parametrize('usuario', [2, 99999, 1])
def test_cliente_invalido(client, banco, payload, usuario):
    antes = contagens(banco)
    if usuario == 1:
        with psycopg.connect(banco) as conn:
            conn.execute('UPDATE usuario SET ativo = FALSE WHERE id_usuario = 1')
    with client.session_transaction() as sess:
        sess['id_usuario'] = usuario
    assert client.post('/api/v1/pedidos', json=payload).status_code == 403
    assert contagens(banco) == antes


def test_perfil_cliente_do_pr11(client, banco, payload):
    with psycopg.connect(banco) as conn:
        conn.execute("UPDATE usuario SET nome_perfil = 'Cliente' WHERE id_usuario = 1")
    assert client.post('/api/v1/pedidos', json=payload).status_code == 201


def test_perfil_funcionario_do_pr11(client, banco):
    with psycopg.connect(banco) as conn:
        conn.execute("UPDATE usuario SET nome_perfil = 'Funcionário' WHERE id_usuario = 2")
    with client.session_transaction() as sess:
        sess['id_usuario'] = 2
    resposta = client.post('/api/v1/produtos', json={
        'nome': 'Produto PR11', 'tamanho': 'Grande', 'preco': '20.00', 'id_categoria': 1,
        'ingredientes': [{'id_ingrediente': 1, 'quantidade_necessaria': '1.000'}],
    })
    assert resposta.status_code == 201


def test_rollback_inclui_endereco(client, banco, payload, monkeypatch):
    antes = contagens(banco)
    def falha(conn, id_pedido, itens):
        with conn.cursor() as cursor:
            cursor.execute('''INSERT INTO item_pedido
                (id_pedido,id_produto,quantidade,preco_unitario,subtotal)
                VALUES (%s,1,0,1,1)''', (id_pedido,))
    monkeypatch.setattr(pedido_services, 'criar_itens_repository', falha)
    assert client.post('/api/v1/pedidos', json=payload).status_code == 503
    assert contagens(banco) == antes


def test_status_sem_id_fixo(client, banco, payload):
    with psycopg.connect(banco) as conn:
        conn.execute("UPDATE status SET nome_status = 'Legado' WHERE nome_status = 'Recebido'")
        id_status = conn.execute("INSERT INTO status (nome_status) VALUES ('Recebido') RETURNING id_status").fetchone()[0]
    resposta = client.post('/api/v1/pedidos', json=payload)
    assert resposta.status_code == 201
    assert resposta.json['id_status'] == id_status


def test_sem_status_configurado(client, banco, payload):
    antes = contagens(banco)
    with psycopg.connect(banco) as conn:
        conn.execute("UPDATE status SET nome_status = 'Legado' WHERE nome_status = 'Recebido'")
    assert client.post('/api/v1/pedidos', json=payload).status_code == 503
    assert contagens(banco) == antes
