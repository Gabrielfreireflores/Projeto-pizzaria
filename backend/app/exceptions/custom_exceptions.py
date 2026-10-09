class AppBaseException(Exception):
    """Exceção base para todas as exceções da aplicação."""
    def __init__(self, message="Ocorreu um erro no sistema.", status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


# --- EXCEÇÕES DE NEGÓCIO ---

class RegraDeNegocioError(AppBaseException):
    """Para validações e regras de negócio violadas (ex: e-mail duplicado, saldo insuficiente)."""
    def __init__(self, message="Regra de negócio violada."):
        super().__init__(message, status_code=400)

class NaoEncontradoError(AppBaseException):
    """Para registros não encontrados no banco (ex: usuário não existe)."""
    def __init__(self, message="Recurso não encontrado."):
        super().__init__(message, status_code=404)

class NaoAutorizadoError(AppBaseException):
    """Para falha de login ou token inválido."""
    def __init__(self, message="Credenciais inválidas ou token expirado."):
        super().__init__(message, status_code=401)

class AcessoProibidoError(AppBaseException):
    """Para usuário sem permissão suficiente."""
    def __init__(self, message="Acesso negado a este recurso."):
        super().__init__(message, status_code=403)


# --- EXCEÇÕES DE INFRAESTRUTURA ---

class ErroBancoDadosError(AppBaseException):
    """Para falhas técnicas de conexão ou erro interno no banco."""
    def __init__(self, message="Erro interno ao acessar o banco de dados."):
        super().__init__(message, status_code=500)

class SintaxeSQLError(AppBaseException):
    """Para erros de sintaxe SQL."""
    def __init__(self, message="Erro de sintaxe SQL."):
        super().__init__(message, status_code=500)

class ChaveUnicaVioladaError(AppBaseException):
    """Para violação de chave única (ex: e-mail duplicado)."""
    def __init__(self, message="Violação de chave única no banco de dados."):
        super().__init__(message, status_code=400)

# --- EXCEÇÕES DE ENTRADA DE DADOS ---

class RequisicaoInvalidaError(AppBaseException):
    """Para requisições inválidas (ex: JSON malformado, campos obrigatórios ausentes)."""
    def __init__(self, message="Requisição inválida."):
        super().__init__(message, status_code=400)

