def api_client(app):
    """Cliente da API com proteção CSRF; testes de rejeição usam test_client diretamente."""
    client = app.test_client()
    client.environ_base['HTTP_X_CSRF_PROTECTION'] = '1'
    return client
