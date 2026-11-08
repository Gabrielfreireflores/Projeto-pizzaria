from . import api_client
import pytest
from unittest.mock import patch
from app import create_app

@pytest.fixture
def client():
    """
    FIXTURE DO PYTEST:
    Cria uma instância da aplicação Flask configurada para modo de teste
    e disponibiliza um cliente HTTP em memória (test_client).
    """
    app = create_app()
    app.config.update(TESTING=True, SECRET_KEY='somente-testes')
    with api_client(app) as client:
        yield client


# ==============================================================================
# TESTES DA ROTA DE FUNCIONÁRIO (/auth/cadastro/funcionario)
# ==============================================================================

def test_rota_cadastrar_funcionario_publico_bloqueado(client):
    """O endpoint legado nunca cria usuários; o cadastro legítimo usa a equipe."""
    with patch('app.services.auth_services.cadastrar_usuario') as service:
        response = client.post('/auth/api/cadastro/funcionario', json={
            'email': 'funcionario@pizzaria.com', 'senha': 'senhaSegura123',
        })
        assert response.status_code == 403
        service.assert_not_called()


def test_rota_cadastrar_funcionario_bloqueada_mesmo_com_sessao(client):
    with client.session_transaction() as sess:
        sess['id_usuario'] = 1
    assert client.post('/auth/api/cadastro/funcionario', json={}).status_code == 403


# ==============================================================================
# TESTES DA ROTA DE CLIENTE (/auth/cadastro/cliente)
# ==============================================================================

def test_rota_cadastrar_cliente_sucesso(client):
    """Valida o auto-cadastro público de cliente e a injeção do perfil 'Cliente'."""
    usuario_fake = (2, "cliente@email.com")
    with patch('app.services.auth_services.cadastrar_usuario', return_value=usuario_fake) as mock_service:
        
        payload = {
            "email": "cliente@email.com",
            "senha": "123"
        }
        resposta = client.post('/auth/api/cadastro/cliente', json=payload)
        
        assert resposta.status_code == 201
        
        # Verifica se o perfil injetado foi "Cliente"
        mock_service.assert_called_once_with(
            email="cliente@email.com",
            senha="123",
            nome_perfil="Cliente",
            descricao_perfil="Cadastro do perfil Cliente"
        )


def test_rota_cadastrar_cliente_email_duplicado_deve_falhar(client):
    """Valida a conversão do ValueError da camada de Service em resposta HTTP 400."""
    # Simula que o AuthService lançou um ValueError por e-mail duplicado
    with patch('app.services.auth_services.cadastrar_usuario', side_effect=ValueError("Usuário já cadastrado com este e-mail.")):
        
        payload = {
            "email": "duplicado@email.com",
            "senha": "123"
        }
        resposta = client.post('/auth/api/cadastro/cliente', json=payload)
        
        # O Controller deve capturar o ValueError e responder status HTTP 400
        assert resposta.status_code == 400
        assert resposta.get_json()["erro"] == "Usuário já cadastrado com este e-mail."