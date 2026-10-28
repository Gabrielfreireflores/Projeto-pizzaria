from unittest.mock import Mock

import pytest
from werkzeug.security import check_password_hash

from app import create_app
from app.services import auth_services


@pytest.fixture
def cadastro(monkeypatch):
    conn = Mock()
    usuario = Mock(return_value=(77, 'ana@teste.local'))
    cliente = Mock(return_value=(88, 77, 'Ana Souza', None, '(16) 99999-0001'))
    monkeypatch.setattr(auth_services, 'get_connection', lambda: conn)
    monkeypatch.setattr(auth_services, 'buscar_usuario_por_email', lambda email: None)
    monkeypatch.setattr(auth_services, 'criar_usuario', usuario)
    monkeypatch.setattr(auth_services, 'criar_cliente', cliente)
    app = create_app()
    app.config.update(TESTING=True, SECRET_KEY='somente-testes')
    return app.test_client(), conn, usuario, cliente


@pytest.fixture
def dados():
    return {'nome': '  Ana Souza  ', 'email': ' ANA@TESTE.LOCAL ',
            'telefone': '(16) 99999-0001', 'senha': 'senha-existente'}


def test_cadastro_sem_cpf_normaliza_e_armazena_hash(cadastro, dados):
    http, conn, usuario, cliente = cadastro
    resposta = http.post('/api/v1/clientes', json=dados)
    assert resposta.status_code == 201
    assert resposta.json['cliente']['cpf'] is None
    assert usuario.call_args.kwargs['email'] == 'ana@teste.local'
    assert check_password_hash(usuario.call_args.kwargs['senha'], dados['senha'])
    assert cliente.call_args.kwargs['nome'] == 'Ana Souza'
    assert cliente.call_args.kwargs['cpf'] is None
    assert cliente.call_args.kwargs['telefone'] == dados['telefone']
    conn.commit.assert_called_once()
    conn.close.assert_called_once()


@pytest.mark.parametrize('cpf', ['invalido', '123.456.789-00', 123, None])
def test_cpf_enviado_e_ignorado(cadastro, dados, cpf):
    http, _, _, cliente = cadastro
    dados['cpf'] = cpf
    assert http.post('/api/v1/clientes', json=dados).status_code == 201
    assert cliente.call_args.kwargs['cpf'] is None


@pytest.mark.parametrize('campo,valor', [
    ('nome', ''), ('nome', 'Ana'), ('nome', 'A' * 121), ('nome', []),
    ('email', 'invalido'), ('email', 'a @teste.local'), ('email', None),
    ('telefone', '123'), ('telefone', '16999990001abc'), ('telefone', '1' * 16),
    ('telefone', None), ('telefone', []), ('senha', ''), ('senha', 123),
])
def test_cadastro_invalido_nao_grava(cadastro, dados, campo, valor):
    http, conn, usuario, cliente = cadastro
    dados[campo] = valor
    resposta = http.post('/api/v1/clientes', json=dados)
    assert resposta.status_code == 400
    assert 'erro' in resposta.json
    usuario.assert_not_called()
    cliente.assert_not_called()
    conn.commit.assert_not_called()


def test_senha_curta_mantem_regra_existente(cadastro, dados):
    # Não há mínimo de comprimento no projeto; apenas senha não vazia.
    http, _, _, _ = cadastro
    dados['senha'] = 'x'
    assert http.post('/api/v1/clientes', json=dados).status_code == 201


def test_email_duplicado_mantem_erro_padrao(cadastro, dados, monkeypatch):
    http, conn, usuario, cliente = cadastro
    monkeypatch.setattr(auth_services, 'buscar_usuario_por_email', lambda email: (1, email))
    resposta = http.post('/api/v1/clientes', json=dados)
    assert resposta.status_code == 400
    assert resposta.json == {'erro': 'Usuário já cadastrado com este e-mail.'}
    usuario.assert_not_called()
    cliente.assert_not_called()
    conn.commit.assert_not_called()


@pytest.mark.parametrize('corpo', ['null', '[]', '{'])
def test_json_invalido(cadastro, corpo):
    http, _, usuario, _ = cadastro
    resposta = http.post('/api/v1/clientes', data=corpo, content_type='application/json')
    assert resposta.status_code == 400
    usuario.assert_not_called()
