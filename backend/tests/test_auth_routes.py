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
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ==============================================================================
# TESTES DA ROTA DE FUNCIONÁRIO (/auth/cadastro/funcionario)
# ==============================================================================

def test_rota_cadastrar_funcionario_sucesso(client):
    """Valida o cadastro com sucesso via POST enviando um JSON válido."""
    
    # 1. MOCK DO SERVICE: Simula o retorno de sucesso do cadastrar_usuario
    usuario_fake = (1, "funcionario@pizzaria.com")
    with patch('app.services.auth_services.cadastrar_usuario', return_value=usuario_fake) as mock_service:
        
        # 2. Executa a requisição POST simulada com JSON no corpo
        payload = {
            "email": "funcionario@pizzaria.com",
            "senha": "senhaSegura123"
        }
        resposta = client.post('/auth/cadastro/funcionario', json=payload)
        
        # 3. VERIFICAÇÕES (ASSERTIONS)
        # 3.1. Código HTTP deve ser 201 (Created)
        assert resposta.status_code == 201
        
        # 3.2. Estrutura e conteúdo da resposta JSON
        dados_resposta = resposta.get_json()
        assert dados_resposta["mensagem"] == "Usuário do perfil 'Funcionário' cadastrado com sucesso."
        assert dados_resposta["usuario"]["id"] == 1
        assert dados_resposta["usuario"]["email"] == "funcionario@pizzaria.com"
        
        # 3.3. Garante que o Controller injetou o perfil "Funcionário" no Service
        mock_service.assert_called_once_with(
            email="funcionario@pizzaria.com",
            senha="senhaSegura123",
            nome_perfil="Funcionário",
            descricao_perfil="Cadastro do perfil Funcionário"
        )


def test_rota_cadastrar_funcionario_sem_email_deve_falhar(client):
    """Valida a falha HTTP 400 quando o campo obrigatório 'email' não é enviado."""
    payload = {
        "senha": "senhaSegura123"
        # Sem campo e-mail
    }
    
    resposta = client.post('/auth/cadastro/funcionario', json=payload)
    
    assert resposta.status_code == 400
    dados = resposta.get_json()
    assert dados["erro"] == "E-mail e senha são campos obrigatórios."


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
        resposta = client.post('/auth/cadastro/cliente', json=payload)
        
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
        resposta = client.post('/auth/cadastro/cliente', json=payload)
        
        # O Controller deve capturar o ValueError e responder status HTTP 400
        assert resposta.status_code == 400
        assert resposta.get_json()["erro"] == "Usuário já cadastrado com este e-mail."