import pytest
from unittest.mock import patch, Mock
from app.services.auth_services import cadastrar_usuario, autenticar_usuario

# ==============================================================================
# SEÇÃO 1: TESTES DA FUNÇÃO `cadastrar_usuario`
# ==============================================================================

def test_cadastrar_usuario_sucesso():
    conn = Mock()

    with patch(
        'app.services.auth_services.get_connection',
        return_value=conn
    ):
        with patch(
            'app.services.auth_services.buscar_usuario_por_email',
            return_value=None
        ):
            with patch(
                'app.services.auth_services.criar_usuario',
                return_value=(1, "admin@pizzaria.com")
            ) as mock_criar:
                with patch(
                    'app.services.auth_services.generate_password_hash',
                    return_value="hash_fake_123"
                ):
                    resultado = cadastrar_usuario(
                        "  ADMIN@pizzaria.com  ",
                        "senha123",
                        "Gerente",
                        "Acesso total"
                    )

    assert resultado == (1, "admin@pizzaria.com")
    mock_criar.assert_called_once_with(
        conn,
        "admin@pizzaria.com",
        "hash_fake_123",
        "Gerente",
        "Acesso total"
    )
    conn.commit.assert_called_once()
    conn.close.assert_called_once()


def test_autenticar_usuario_inativo_deve_falhar():
    usuario_inativo_fake = (
        2,
        "demitido@pizzaria.com",
        False,
        "hash_qualquer",
    )

    with patch(
        "app.services.auth_services.buscar_usuario_por_email",
        return_value=usuario_inativo_fake,
    ), patch(
        "app.services.auth_services.check_password_hash",
        return_value=True,
    ):
        with pytest.raises(
            ValueError,
            match=r"Usuário inativo\.",
        ):
            autenticar_usuario(
                "demitido@pizzaria.com",
                "senha123",
            )

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


def test_autenticar_usuario_senha_incorreta_deve_falhar():
    """Valida a negação de login se a senha informada não corresponder ao hash."""
    usuario_db_fake = (1, "admin@pizzaria.com", True, "hash_senha_correta")
    
    with patch('app.services.auth_services.buscar_usuario_por_email', return_value=usuario_db_fake):
        # Simula que o 'check_password_hash' retornou False (senha incorreta)
        with patch('app.services.auth_services.check_password_hash', return_value=False):
            
            with pytest.raises(ValueError, match="E-mail ou senha inválidos."):
                autenticar_usuario("admin@pizzaria.com", "senha_errada")