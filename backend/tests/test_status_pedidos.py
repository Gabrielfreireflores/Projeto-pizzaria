from contextlib import contextmanager
from unittest.mock import MagicMock, Mock

import pytest

from app import create_app
from app.services import pedido_services


@pytest.fixture
def fluxo(monkeypatch):
    app = create_app()
    app.config.update(TESTING=True, SECRET_KEY='somente-testes')
    client = app.test_client()
    with client.session_transaction() as sess:
        sess['id_usuario'] = 2

    conn = MagicMock()
    cursor = conn.cursor.return_value.__enter__.return_value

    @contextmanager
    def transacao():
        yield conn

    funcionario = Mock(return_value=(True, 'Funcionário', 7))
    atualizar = Mock()
    monkeypatch.setattr(pedido_services, 'transacao_pedido_repository', transacao)
    monkeypatch.setattr(pedido_services, 'buscar_funcionario_por_usuario', funcionario)
    monkeypatch.setattr(pedido_services, 'buscar_status_repository', lambda conn, nome: (8,))
    monkeypatch.setattr(pedido_services, 'atualizar_status_repository', atualizar)
    return client, cursor, atualizar, funcionario


def test_aceite_atribui_funcionario_autenticado(fluxo):
    client, cursor, atualizar, _ = fluxo
    cursor.fetchone.return_value = (1, 'Recebido')
    resposta = client.post('/api/v1/pedidos/42/aceitar')
    assert resposta.status_code == 200
    assert resposta.json == {
        'id_pedido': 42, 'status': 'Em preparação', 'id_funcionario': 7,
    }
    assert atualizar.call_args.args[1:] == (42, 8, 7)


def test_pedido_ja_aceito_retorna_conflito(fluxo):
    client, cursor, atualizar, _ = fluxo
    cursor.fetchone.return_value = (8, 'Em preparação')
    assert client.post('/api/v1/pedidos/42/aceitar').status_code == 409
    atualizar.assert_not_called()


@pytest.mark.parametrize('atual,novo', [
    ('Em preparação', 'Saiu para entrega'),
    ('Saiu para entrega', 'Entregue'),
])
def test_transicao_valida_preserva_responsavel(fluxo, atual, novo):
    client, cursor, atualizar, _ = fluxo
    cursor.fetchone.return_value = (atual, 3)
    resposta = client.put('/api/v1/pedidos/42/status', json={'status': novo})
    assert resposta.status_code == 200
    assert resposta.json['status'] == novo
    assert resposta.json['id_funcionario'] == 3
    assert atualizar.call_args.args[1:] == (42, 8, 3)


@pytest.mark.parametrize('atual,novo', [
    ('Recebido', 'Entregue'),
    ('Recebido', 'Em preparação'),
    ('Em preparação', 'Entregue'),
    ('Saiu para entrega', 'Em preparação'),
    ('Entregue', 'Saiu para entrega'),
])
def test_transicao_invalida_retorna_409_sem_atualizar(fluxo, atual, novo):
    client, cursor, atualizar, _ = fluxo
    cursor.fetchone.return_value = (atual, 3)
    resposta = client.put('/api/v1/pedidos/42/status', json={'status': novo})
    assert resposta.status_code == 409
    assert 'erro' in resposta.json
    atualizar.assert_not_called()


@pytest.mark.parametrize('rota,metodo', [('aceitar', 'post'), ('status', 'put')])
def test_pedido_inexistente(fluxo, rota, metodo):
    client, cursor, atualizar, _ = fluxo
    cursor.fetchone.return_value = None
    resposta = getattr(client, metodo)(f'/api/v1/pedidos/42/{rota}', json={'status': 'Entregue'})
    assert resposta.status_code == 404
    atualizar.assert_not_called()


@pytest.mark.parametrize('rota,metodo', [('aceitar', 'post'), ('status', 'put')])
@pytest.mark.parametrize('usuario', ['anonimo', 'cliente', 'inativo'])
def test_alteracao_exige_funcionario_ativo(fluxo, rota, metodo, usuario):
    client, _, atualizar, funcionario = fluxo
    if usuario == 'anonimo':
        with client.session_transaction() as sess:
            sess.clear()
    else:
        funcionario.return_value = (
            (True, 'Cliente', None) if usuario == 'cliente' else (False, 'Funcionário', 7)
        )
    resposta = getattr(client, metodo)(f'/api/v1/pedidos/42/{rota}', json={'status': 'Entregue'})
    assert resposta.status_code == (401 if usuario == 'anonimo' else 403)
    atualizar.assert_not_called()
