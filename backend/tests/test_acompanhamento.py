import os
import sys
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

import psycopg
import pytest
from psycopg import sql
from psycopg.conninfo import make_conninfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from app.services import acompanhamento_services as service


@pytest.fixture
def http():
    app = create_app()
    app.config.update(TESTING=True, SECRET_KEY='teste', PRAZO_ESTIMADO_ENTREGA_MINUTOS=60)
    return app.test_client()


def login(http, usuario=1):
    with http.session_transaction() as sessao:
        sessao['id_usuario'] = usuario


@pytest.fixture
def simulado(monkeypatch):
    @contextmanager
    def transacao():
        yield None
    monkeypatch.setattr(service, 'transacao_pedido_repository', transacao)
    monkeypatch.setattr(service, 'buscar_cliente_repository', lambda *args: (3, True, 'Cliente'))
    criado = datetime.now(timezone.utc).replace(microsecond=0)
    monkeypatch.setattr(service, 'buscar_acompanhamento_repository', lambda *args: (7, 'Recebido', criado))
    return criado


@pytest.mark.parametrize('usuario', [None, True, '1', 0, -1])
def test_exige_sessao_valida(http, usuario):
    login(http, usuario)
    resposta = http.get('/api/v1/pedidos/7/acompanhamento')
    assert resposta.status_code == 401
    assert resposta.headers['Cache-Control'] == 'no-store'


@pytest.mark.parametrize('cliente', [None, (1, False, 'Cliente'), (1, True, 'Funcionário')])
def test_exige_cliente_ativo(http, simulado, monkeypatch, cliente):
    login(http)
    monkeypatch.setattr(service, 'buscar_cliente_repository', lambda *args: cliente)
    assert http.get('/api/v1/pedidos/7/acompanhamento').status_code == 403


def test_prazo_estavel_e_contrato(http, simulado):
    login(http)
    resposta = http.get('/api/v1/pedidos/7/acompanhamento')
    assert resposta.status_code == 200
    assert resposta.headers['Cache-Control'] == 'no-store'
    assert resposta.json == {
        'id_pedido': 7, 'status': 'RECEBIDO', 'status_descricao': 'Recebido',
        'data_hora_pedido': simulado.isoformat(), 'finalizado': False,
        'atualizar_em_segundos': 10,
        'estimativa_entrega': {'prazo_minutos': 60,
            'previsao_entrega': (simulado + timedelta(minutes=60)).isoformat(), 'atrasada': False},
    }
    assert http.get('/api/v1/pedidos/7/acompanhamento').json == resposta.json


@pytest.mark.parametrize('status,codigo', [('Em preparação', 'EM_PREPARACAO'), ('Saiu para entrega', 'SAIU_PARA_ENTREGA'), ('Entregue', 'ENTREGUE'), ('Cancelado', 'CANCELADO')])
def test_estados(http, simulado, monkeypatch, status, codigo):
    login(http)
    monkeypatch.setattr(service, 'buscar_acompanhamento_repository', lambda *args: (7, status, simulado))
    resposta = http.get('/api/v1/pedidos/7/acompanhamento')
    assert resposta.status_code == 200
    assert resposta.json['status'] == codigo
    final = codigo in ('ENTREGUE', 'CANCELADO')
    assert resposta.json['finalizado'] is final
    assert (resposta.json['estimativa_entrega'] is None) is final
    assert resposta.json['atualizar_em_segundos'] == (None if final else 10)


def test_atraso_sem_mudar_status(http, simulado, monkeypatch):
    login(http)
    antigo = simulado - timedelta(hours=2)
    monkeypatch.setattr(service, 'buscar_acompanhamento_repository', lambda *args: (7, 'Recebido', antigo))
    resposta = http.get('/api/v1/pedidos/7/acompanhamento')
    assert resposta.json['estimativa_entrega']['atrasada'] is True
    assert resposta.json['status'] == 'RECEBIDO'


@pytest.mark.parametrize('prazo', [0, -1, 1441, True, 1.5, 'abc', '2.5'])
def test_configuracao_invalida(http, simulado, prazo):
    login(http)
    http.application.config['PRAZO_ESTIMADO_ENTREGA_MINUTOS'] = prazo
    resposta = http.get('/api/v1/pedidos/7/acompanhamento')
    assert resposta.status_code == 503
    assert resposta.json == {'erro': 'Não foi possível consultar o pedido.'}


def test_prazo_configuravel(http, simulado):
    login(http)
    http.application.config['PRAZO_ESTIMADO_ENTREGA_MINUTOS'] = '45'
    resposta = http.get('/api/v1/pedidos/7/acompanhamento')
    assert resposta.json['estimativa_entrega']['prazo_minutos'] == 45


def test_erro_banco(http, simulado, monkeypatch):
    login(http)
    def falhar(*args):
        raise psycopg.OperationalError('detalhe privado')
    monkeypatch.setattr(service, 'buscar_acompanhamento_repository', falhar)
    resposta = http.get('/api/v1/pedidos/7/acompanhamento')
    assert resposta.status_code == 503
    assert 'privado' not in resposta.get_data(as_text=True)


@pytest.fixture
def banco(monkeypatch):
    url = os.getenv('TEST_DATABASE_URL')
    if not url:
        pytest.skip('Defina TEST_DATABASE_URL para integração PostgreSQL.')
    schema = 'teste_h09_' + uuid4().hex
    with psycopg.connect(url, autocommit=True) as conn:
        conn.execute(sql.SQL('CREATE SCHEMA {}').format(sql.Identifier(schema)))
    dsn = make_conninfo(url, options=f'-c search_path={schema}')
    try:
        with psycopg.connect(dsn, autocommit=True) as conn:
            raiz = Path(__file__).resolve().parents[2]
            conn.execute((raiz / 'db/schema.sql').read_text(encoding='utf-8'))
        monkeypatch.setenv('DATABASE_URL', dsn)
        yield dsn
    finally:
        with psycopg.connect(url, autocommit=True) as conn:
            conn.execute(sql.SQL('DROP SCHEMA {} CASCADE').format(sql.Identifier(schema)))


def test_banco_reflete_mudanca_e_preserva_previsao(http, banco):
    login(http)
    primeira = http.get('/api/v1/pedidos/1/acompanhamento')
    assert primeira.status_code == 200
    assert primeira.json['status'] == 'RECEBIDO'
    with psycopg.connect(banco) as conn:
        conn.execute("UPDATE pedido SET id_status = (SELECT id_status FROM status WHERE nome_status = 'Em preparação') WHERE id_pedido = 1")
    segunda = http.get('/api/v1/pedidos/1/acompanhamento')
    assert segunda.json['status'] == 'EM_PREPARACAO'
    assert segunda.json['estimativa_entrega'] == primeira.json['estimativa_entrega']
    assert datetime.fromisoformat(segunda.json['data_hora_pedido']).tzinfo is not None


def test_banco_nao_expoe_pedido_de_outro_cliente(http, banco):
    with psycopg.connect(banco) as conn:
        usuario = conn.execute("INSERT INTO usuario(email, senha, nome_perfil) VALUES ('outro@teste.com', 'teste', 'Cliente') RETURNING id_usuario").fetchone()[0]
        conn.execute("INSERT INTO cliente(id_usuario, nome, cpf) VALUES (%s, 'Outro', '000.000.000-00')", (usuario,))
    login(http, usuario)
    outro = http.get('/api/v1/pedidos/1/acompanhamento')
    ausente = http.get('/api/v1/pedidos/99999/acompanhamento')
    assert outro.status_code == ausente.status_code == 404
    assert outro.json == ausente.json == {'erro': 'Pedido não encontrado.'}
    login(http, 1)
    assert http.get('/api/v1/pedidos/1/acompanhamento').status_code == 200
    with psycopg.connect(banco) as conn:
        conn.execute('UPDATE usuario SET ativo = FALSE WHERE id_usuario = 1')
    assert http.get('/api/v1/pedidos/1/acompanhamento').status_code == 403
