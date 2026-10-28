import os
import re
import sys
from pathlib import Path
from uuid import uuid4

import psycopg
import pytest
from psycopg import sql
from werkzeug.security import generate_password_hash

from app import create_app
from app.database import get_connection


@pytest.fixture
def ambiente(monkeypatch):
    url = os.getenv('TEST_DATABASE_URL')
    if not url:
        pytest.skip('Defina TEST_DATABASE_URL para testar SQL em transação isolada.')
    conn = psycopg.connect(url)
    schema = 'teste_cliente_borda_' + uuid4().hex

    class ConexaoIsolada:
        def cursor(self, *args, **kwargs):
            return conn.cursor(*args, **kwargs)

        def commit(self):
            pass

        def rollback(self):
            pass

        def close(self):
            pass

    try:
        conn.execute(sql.SQL('CREATE SCHEMA {}').format(sql.Identifier(schema)))
        conn.execute(sql.SQL('SET LOCAL search_path TO {}').format(sql.Identifier(schema)))
        raiz = Path(__file__).resolve().parents[2]
        for arquivo in [raiz / 'db/schema.sql', *sorted((raiz / 'db/migrations').glob('*.sql'))]:
            conteudo = re.sub(r'^\s*(?:BEGIN|COMMIT);\s*$', '', arquivo.read_text(encoding='utf-8'), flags=re.M)
            conn.execute(conteudo)
        # Também verifica a reaplicação das duas migrations novas.
        for nome in ('005_bordas_por_item.sql', '005_cliente_cpf_opcional.sql', '006_desativar_refrigerante_legado.sql'):
            conteudo = (raiz / 'db/migrations' / nome).read_text(encoding='utf-8')
            conn.execute(re.sub(r'^\s*(?:BEGIN|COMMIT);\s*$', '', conteudo, flags=re.M))
        conn.execute('UPDATE usuario SET senha = %s WHERE id_usuario = 2', (generate_password_hash('teste'),))
        app = create_app()
        app.config.update(TESTING=True, SECRET_KEY='teste-isolado', TAXA_ENTREGA='5.00')
        proxy = ConexaoIsolada()
        for modulo in list(sys.modules.values()):
            if modulo and getattr(modulo, '__name__', '').startswith('app.'):
                if getattr(modulo, 'get_connection', None) is get_connection:
                    monkeypatch.setattr(modulo, 'get_connection', lambda: proxy)
        yield app, conn
    finally:
        conn.rollback()
        assert conn.execute('SELECT to_regnamespace(%s)', (schema,)).fetchone()[0] is None
        conn.rollback()
        conn.close()


def produtos(conn):
    def buscar(categoria, tamanho):
        return conn.execute('''SELECT p.id_produto, p.preco FROM produto p
            JOIN categoria c USING (id_categoria) WHERE c.nome = %s AND p.tamanho = %s
            ORDER BY p.id_produto LIMIT 1''', (categoria, tamanho)).fetchone()
    return buscar('Pizzas Salgadas', 'Grande'), buscar('Bordas', 'Grande')


def payload(conn):
    pizza, borda = produtos(conn)
    return {'contato': {'nome': 'Cliente Teste', 'telefone': '16999999999'},
            'tipo_entrega': 'retirada', 'forma_pagamento': 'Pix',
            'itens': [{'id_produto': pizza[0], 'quantidade': 2,
                       'bordas': [{'id_produto': borda[0], 'quantidade': 2}]}]}


def cadastrar(client, cpf='52998224725', email='cliente@teste.local'):
    resposta = client.post('/api/v1/clientes', json={
        'nome': 'Cliente Teste', 'cpf': cpf, 'telefone': '16999999999',
        'email': email, 'senha': 'teste',
    })
    assert resposta.status_code == 201, resposta.json
    assert client.post('/api/v1/login', json={'email': email, 'senha': 'teste'}).status_code == 200
    return resposta.json


def test_borda_vinculada_preco_do_banco_e_historico(ambiente):
    app, conn = ambiente
    client = app.test_client()
    corpo = payload(conn)
    corpo['itens'][0]['bordas'][0]['preco_unitario'] = '0.01'
    resposta = client.post('/api/v1/pedidos', json=corpo)
    assert resposta.status_code == 201, resposta.json
    pizza, borda = produtos(conn)
    assert resposta.json['valor_total'] == str((pizza[1] + borda[1]) * 2)
    registro = conn.execute('''SELECT b.id_produto, b.quantidade, b.preco_unitario,
        ip.id_produto, p.id_funcionario FROM item_pedido_borda b
        JOIN item_pedido ip USING (id_item_pedido) JOIN pedido p USING (id_pedido)
        WHERE p.id_pedido = %s''', (resposta.json['id_pedido'],)).fetchone()
    assert registro == (borda[0], 2, borda[1], pizza[0], None)
    assert client.post('/api/v1/login', json={'email': 'funcionario.exemplo@email.com', 'senha': 'teste'}).status_code == 200
    lista = client.get('/api/v1/pedidos')
    assert lista.status_code == 200
    pedido = next(p for p in lista.json if p['id_pedido'] == resposta.json['id_pedido'])
    assert pedido['itens'][0]['bordas'][0]['id_produto'] == borda[0]
    legado = conn.execute("SELECT id_produto FROM produto WHERE nome = 'Refrigerante'").fetchone()
    assert legado is not None
    assert conn.execute('SELECT count(*) FROM item_pedido WHERE id_produto = %s', legado).fetchone()[0] > 0
    cardapio = client.get('/api/v1/cardapio').json
    assert not any(p['nome'] == 'Refrigerante' for c in cardapio['categorias'] for p in c['produtos'])


@pytest.mark.parametrize('erro', ['tamanho', 'categoria', 'quantidade', 'indisponivel'])
def test_borda_invalida_nao_cria_pedido(ambiente, erro):
    app, conn = ambiente
    corpo = payload(conn)
    borda = corpo['itens'][0]['bordas'][0]
    if erro == 'quantidade':
        borda['quantidade'] = 3
    elif erro == 'categoria':
        borda['id_produto'] = corpo['itens'][0]['id_produto']
    elif erro == 'tamanho':
        borda['id_produto'] = conn.execute("SELECT id_produto FROM produto WHERE nome LIKE 'Borda %' AND tamanho = 'Pequena' LIMIT 1").fetchone()[0]
    else:
        conn.execute('UPDATE produto SET disponivel = FALSE WHERE id_produto = %s', (borda['id_produto'],))
    antes = conn.execute('SELECT count(*) FROM pedido').fetchone()[0]
    resposta = app.test_client().post('/api/v1/pedidos', json=corpo)
    assert resposta.status_code == 400, resposta.json
    assert conn.execute('SELECT count(*) FROM pedido').fetchone()[0] == antes


def test_cadastro_login_pedido_e_isolamento_de_contas(ambiente):
    app, conn = ambiente
    primeiro, segundo, anonimo = (app.test_client() for _ in range(3))
    cadastrado = cadastrar(primeiro)
    cpf = conn.execute('SELECT cpf FROM cliente WHERE id_cliente = %s', (cadastrado['cliente']['id'],)).fetchone()[0]
    assert cpf is None
    resposta = primeiro.post('/api/v1/pedidos', json=payload(conn))
    assert resposta.status_code == 201
    assert [p['id_pedido'] for p in primeiro.get('/api/v1/meus-pedidos').json] == [resposta.json['id_pedido']]
    cadastrar(segundo, '11144477735', 'outro@teste.local')
    assert segundo.get('/api/v1/meus-pedidos?id_cliente=' + str(cadastrado['cliente']['id'])).json == []
    assert anonimo.get('/api/v1/meus-pedidos').status_code == 401
    assert anonimo.post('/api/v1/pedidos', json=payload(conn)).status_code == 201
    assert len(primeiro.get('/api/v1/meus-pedidos').json) == 1
    conn.execute('UPDATE usuario SET ativo = FALSE WHERE id_usuario = %s', (cadastrado['usuario']['id'],))
    assert primeiro.get('/api/v1/meus-pedidos').status_code == 403
    assert primeiro.get('/api/v1/me').status_code == 401


def test_email_duplicado_retorna_mensagem_publica(ambiente):
    app, _ = ambiente
    client = app.test_client()
    cadastrar(client)
    resposta = client.post('/api/v1/clientes', json={
        'nome': 'Outra Pessoa', 'telefone': '16999999999', 'email': 'cliente@teste.local', 'senha': 'teste',
    })
    assert resposta.status_code == 400
    assert resposta.json == {'erro': 'Usuário já cadastrado com este e-mail.'}


def test_cpf_enviado_e_ignorado_e_multiplos_clientes_sem_cpf(ambiente):
    app, conn = ambiente
    conn.execute("UPDATE cliente SET cpf = '52998224725' WHERE id_cliente = 1")
    resposta = app.test_client().post('/api/v1/clientes', json={
        'nome': 'Outra Pessoa', 'cpf': '529.982.247-25', 'telefone': '16999999999', 'email': 'novo@teste.local', 'senha': 'teste',
    })
    assert resposta.status_code == 201
    assert resposta.json['cliente']['cpf'] is None
    cadastrar(app.test_client(), email='segundo@teste.local')
    assert conn.execute('SELECT count(*) FROM cliente WHERE cpf IS NULL').fetchone()[0] == 2
    assert conn.execute("SELECT is_nullable FROM information_schema.columns WHERE table_schema = current_schema() AND table_name = 'funcionario' AND column_name = 'cpf'").fetchone()[0] == 'NO'
