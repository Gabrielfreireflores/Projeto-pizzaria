import os
import sys
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

import psycopg
import pytest
from psycopg import sql
from psycopg.conninfo import make_conninfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from app.services import cardapio_services


@pytest.fixture
def http():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_publico_vazio(http, monkeypatch):
    monkeypatch.setattr(cardapio_services, 'listar_cardapio_repository', lambda: [])
    resposta = http.get('/api/v1/cardapio')
    assert resposta.status_code == 200
    assert resposta.json == {'categorias': []}


def test_agrupa_por_id_e_serializa_campos(http, monkeypatch):
    linhas = [
        (1, 'Pizzas', 4, 'Mussarela', 'Grande', Decimal('49.90'), '/pizza.jpg', 'Queijo'),
        (1, 'Pizzas', 5, 'Calabresa', 'Grande', Decimal('50'), None, None),
        (2, 'Bebidas', 6, 'Água', '500ml', Decimal('0'), None, ''),
    ]
    monkeypatch.setattr(cardapio_services, 'listar_cardapio_repository', lambda: linhas)
    resposta = http.get('/api/v1/cardapio')
    assert resposta.status_code == 200
    categorias = resposta.json['categorias']
    assert len(categorias) == 2
    assert categorias[0]['id_categoria'] == 1
    assert len(categorias[0]['produtos']) == 2
    assert categorias[0]['produtos'][0] == {
        'id_produto': 4, 'nome': 'Mussarela', 'tamanho': 'Grande',
        'preco': '49.90', 'foto': '/pizza.jpg', 'descricao': 'Queijo',
    }
    assert categorias[0]['produtos'][1]['foto'] is None
    assert categorias[0]['produtos'][1]['descricao'] is None
    assert categorias[0]['produtos'][1]['preco'] == '50.00'
    assert categorias[1]['produtos'][0]['preco'] == '0.00'


@pytest.mark.parametrize('erro', [psycopg.OperationalError('segredo'), RuntimeError('segredo')])
def test_falha_banco_sem_expor_detalhes(http, monkeypatch, erro):
    def falhar():
        raise erro
    monkeypatch.setattr(cardapio_services, 'listar_cardapio_repository', falhar)
    resposta = http.get('/api/v1/cardapio')
    assert resposta.status_code == 503
    assert resposta.json == {'erro': 'Não foi possível consultar o cardápio.'}


@pytest.fixture
def banco(monkeypatch):
    url = os.getenv('TEST_DATABASE_URL')
    if not url:
        pytest.skip('Defina TEST_DATABASE_URL para integração PostgreSQL.')
    schema = 'teste_cardapio_' + uuid4().hex
    raiz = Path(__file__).resolve().parents[2]
    with psycopg.connect(url, autocommit=True) as conn:
        conn.execute(sql.SQL('CREATE SCHEMA {}').format(sql.Identifier(schema)))
    dsn = make_conninfo(url, options=f'-c search_path={schema}')
    try:
        with psycopg.connect(dsn, autocommit=True) as conn:
            conn.execute((raiz / 'db/schema.sql').read_text(encoding='utf-8'))
            migracao = (raiz / 'db/migrations/002_produto_cardapio.sql').read_text(encoding='utf-8')
            conn.execute(migracao)
            conn.execute(migracao)
        monkeypatch.setenv('DATABASE_URL', dsn)
        yield dsn
    finally:
        with psycopg.connect(url, autocommit=True) as conn:
            conn.execute(sql.SQL('DROP SCHEMA {} CASCADE').format(sql.Identifier(schema)))


def test_banco_filtra_disponiveis_e_preserva_legados(http, banco):
    with psycopg.connect(banco) as conn:
        conn.execute("UPDATE produto SET disponivel = FALSE WHERE nome = 'Refrigerante'")
        conn.execute("UPDATE produto SET foto = '/pizza.jpg', descricao = 'Pizza tradicional' WHERE nome = 'Pizza de Muçarela'")
    resposta = http.get('/api/v1/cardapio')
    assert resposta.status_code == 200
    assert len(resposta.json['categorias']) == 1
    categoria = resposta.json['categorias'][0]
    assert categoria['nome'] == 'Pizzas'
    assert len(categoria['produtos']) == 1
    assert categoria['produtos'][0]['foto'] == '/pizza.jpg'
    assert categoria['produtos'][0]['descricao'] == 'Pizza tradicional'
    assert categoria['produtos'][0]['preco'] == '49.90'
    with psycopg.connect(banco) as conn:
        assert conn.execute('SELECT count(*) FROM produto').fetchone()[0] == 2
        conn.execute('UPDATE produto SET disponivel = FALSE')
    assert http.get('/api/v1/cardapio').json == {'categorias': []}


def test_banco_campos_opcionais_e_ordem(http, banco):
    resposta = http.get('/api/v1/cardapio')
    assert resposta.status_code == 200
    assert [c['nome'] for c in resposta.json['categorias']] == ['Bebidas', 'Pizzas']
    for categoria in resposta.json['categorias']:
        for produto in categoria['produtos']:
            assert produto['foto'] is None
            assert produto['descricao'] is None
