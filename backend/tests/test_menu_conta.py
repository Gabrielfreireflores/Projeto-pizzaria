import pytest

from app import create_app
from app.controllers import auth_controller


@pytest.mark.parametrize('perfil,nome,telefone,cargo', [
    ('cliente', 'Ana Souza', '16999999999', None),
    ('funcionario', 'Bruno Lima', None, 'Atendente'),
])
def test_me_devolve_dados_da_conta_sem_campos_sensiveis(monkeypatch, perfil, nome, telefone, cargo):
    app = create_app()
    app.config.update(TESTING=True, SECRET_KEY='teste-menu-conta')
    monkeypatch.setattr(auth_controller, 'buscar_usuario_por_id', lambda _: (
        123, 'conta@teste.local', True, perfil, 'Descricao interna', nome, telefone, cargo,
    ))
    client = app.test_client()
    with client.session_transaction() as sess:
        sess['id_usuario'] = 123
    resposta = client.get('/api/v1/me')
    assert resposta.status_code == 200
    assert resposta.json['usuario'] == {
        'id': 123, 'email': 'conta@teste.local', 'ativo': True, 'perfil': perfil,
        'nome': nome, 'telefone': telefone, 'cargo': cargo,
    }
    assert not {'cpf', 'senha', 'hash', 'descricao'} & resposta.json['usuario'].keys()
