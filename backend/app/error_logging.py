"""Logs técnicos sem reproduzir SQL, parâmetros, senhas ou texto de exceções."""
import sys
from flask import current_app


def log_internal_error(message):
    error = sys.exception()
    current_app.logger.error('%s (%s)', message, type(error).__name__)
