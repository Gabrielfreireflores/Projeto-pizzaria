import pytest
from unittest.mock import patch
from app.services.auth_services import cadastrar_usuario, autenticar_usuario

# ==============================================================================
# SEÇÃO 1: TESTES DA FUNÇÃO `cadastrar_usuario`
# ==============================================================================

def test_cadastrar_usuario_sucesso():
    """Valida o cadastro quando todos os dados são válidos."""
    # MOCK 1: Simula que o e-mail NÃO existe no banco de dados
    with patch('app.services.auth_services.buscar_usuario_por_email', return_value=None):
        # MOCK 2: Simula o salvamento no banco e a geração de hash da senha
        with patch('app.services.auth_services.criar_usuario', return_value=(1, "admin@pizzaria.com")) as mock_criar:
            with patch('app.services.auth_services.generate_password_hash', return_value="hash_fake_123"):
                
                # Executa a função do serviço
                resultado = cadastrar_usuario("  ADMIN@pizzaria.com  ", "senha123", "Gerente", "Acesso total")
                
                # ASSERT 1: Verifica o retorno da função
                assert resultado == (1, "admin@pizzaria.com")
                
                # ASSERT 2: Garante que o e-mail foi tratado (lower e strip) e a senha virou hash
                mock_criar.assert_called_once_with("admin@pizzaria.com", "hash_fake_123", "Gerente", "Acesso total")


def test_cadastrar_usuario_email_vazio_deve_falhar():
    """Valida se o e-mail vazio ou com apenas espaços lança ValueError."""
    with pytest.raises(ValueError, match="O e-mail não pode ser vazio."):
        cadastrar_usuario("   ", "senha123", "Gerente", "Acesso total")


def test_cadastrar_usuario_senha_vazia_deve_falhar():
    """Valida se a senha vazia lança ValueError."""
    with pytest.raises(ValueError, match="A senha não pode ser vazia."):
        cadastrar_usuario("usuario@pizzaria.com", "", "Gerente", "Acesso total")


def test_cadastrar_usuario_duplicado_deve_falhar():
    """Valida o bloqueio quando o e-mail já existe no banco de dados."""
    usuario_existente_fake = (1, "admin@pizzaria.com", True, "hash123")
    
    # Simula que o banco ENCONTROU o usuário
    with patch('app.services.auth_services.buscar_usuario_por_email', return_value=usuario_existente_fake):
        with pytest.raises(ValueError, match="Usuário já cadastrado com este e-mail."):
            cadastrar_usuario("admin@pizzaria.com", "senha123", "Gerente", "Acesso total")


# ==============================================================================
# SEÇÃO 2: TESTES DA FUNÇÃO `autenticar_usuario`
# ==============================================================================

def test_autenticar_usuario_sucesso():
    """Valida o login quando o e-mail e senha estão corretos e o usuário está ativo."""
    # Estrutura do usuário retornado pelo banco: (id, email, ativo, senha_hash)
    usuario_db_fake = (1, "admin@pizzaria.com", True, "hash_senha_correta")
    
    with patch('app.services.auth_services.buscar_usuario_por_email', return_value=usuario_db_fake):
        # Simula que o 'check_password_hash' validou a senha com sucesso (True)
        with patch('app.services.auth_services.check_password_hash', return_value=True):
            
            resultado = autenticar_usuario("  ADMIN@PIZZARIA.COM ", "senha123")
            
            assert resultado == usuario_db_fake


def test_autenticar_usuario_nao_encontrado_deve_falhar():
    """Valida a falha de autenticação quando o e-mail não existe no banco."""
    with patch('app.services.auth_services.buscar_usuario_por_email', return_value=None):
        with pytest.raises(ValueError, match="E-mail ou senha inválidos."):
            autenticar_usuario("naoexistente@pizzaria.com", "senha123")


def test_autenticar_usuario_inativo_deve_falhar():
    """Valida a negação de login se a conta do usuário estiver inativa (usuario[2] == False)."""
    # Indice 2 = False (Usuário Inativo)
    usuario_inativo_fake = (2, "demitido@pizzaria.com", False, "hash_qualquer")
    
    with patch('app.services.auth_services.buscar_usuario_por_email', return_value=usuario_inativo_fake):
        with pytest.raises(ValueError, match="Usuário inativo."):
            autenticar_usuario("demitido@pizzaria.com", "senha123")


def test_autenticar_usuario_senha_incorreta_deve_falhar():
    """Valida a negação de login se a senha informada não corresponder ao hash."""
    usuario_db_fake = (1, "admin@pizzaria.com", True, "hash_senha_correta")
    
    with patch('app.services.auth_services.buscar_usuario_por_email', return_value=usuario_db_fake):
        # Simula que o 'check_password_hash' retornou False (senha incorreta)
        with patch('app.services.auth_services.check_password_hash', return_value=False):
            
            with pytest.raises(ValueError, match="E-mail ou senha inválidos."):
                autenticar_usuario("admin@pizzaria.com", "senha_errada")