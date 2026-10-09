import os
import uuid
import pytest

from app import create_app
from app.database import get_connection


@pytest.fixture
def app():
    """
    Cria uma aplicação Flask específica para os testes.
    """
    os.environ.setdefault(
        "DATABASE_URL",
        os.getenv("DATABASE_URL")
    )

    app = create_app()

    app.config.update(
        TESTING=True,
        SECRET_KEY="chave-secreta-testes",
        TAXA_ENTREGA="5.00",
    )

    yield app


@pytest.fixture
def client(app):
    """
    Cliente HTTP do Flask.
    """
    return app.test_client()


@pytest.fixture
def dados_cliente():
    """
    Gera dados únicos para evitar conflito de e-mail/CPF.
    """
    identificador = uuid.uuid4().hex[:8]

    return {
        "email": f"teste_{identificador}@email.com",
        "senha": "Senha@123",
        "nome": "Cliente Teste",
        "cpf": f"123.{identificador[:3]}.{identificador[3:6]}-00",
        "telefone": "16999999999",
    }


def buscar_usuario_por_email(email):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_usuario, email, ativo, nome_perfil
                FROM usuario
                WHERE lower(email) = lower(%s)
                """,
                (email,),
            )

            return cursor.fetchone()

    finally:
        conn.close()


def buscar_cliente_por_usuario(id_usuario):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_cliente, id_usuario, nome, cpf, telefone
                FROM cliente
                WHERE id_usuario = %s
                """,
                (id_usuario,),
            )

            return cursor.fetchone()

    finally:
        conn.close()


def buscar_pedido(id_pedido):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id_pedido,
                    id_cliente,
                    id_funcionario,
                    id_status,
                    id_endereco,
                    forma_pagamento,
                    taxa_entrega,
                    valor_total
                FROM pedido
                WHERE id_pedido = %s
                """,
                (id_pedido,),
            )

            return cursor.fetchone()

    finally:
        conn.close()


def buscar_itens_pedido(id_pedido):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id_pedido,
                    id_produto,
                    quantidade,
                    preco_unitario,
                    subtotal,
                    observacao
                FROM item_pedido
                WHERE id_pedido = %s
                ORDER BY id_produto
                """,
                (id_pedido,),
            )

            return cursor.fetchall()

    finally:
        conn.close()


def buscar_produto():
    """
    Busca um produto existente e disponível para usar no teste.
    """
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_produto, preco
                FROM produto
                WHERE disponivel = TRUE
                ORDER BY id_produto
                LIMIT 1
                """
            )

            return cursor.fetchone()

    finally:
        conn.close()


def buscar_status_recebido():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_status
                FROM status
                WHERE lower(nome_status) = lower(%s)
                """,
                ("recebido",),
            )

            resultado = cursor.fetchone()

            return resultado[0] if resultado else None

    finally:
        conn.close()


# ============================================================
# CADASTRO
# ============================================================


def test_cadastro_cliente_cria_usuario_e_cliente(
    client,
    dados_cliente,
):
    resposta = client.post(
        "/api/v1/clientes",
        json=dados_cliente,
    )

    assert resposta.status_code == 201

    usuario = buscar_usuario_por_email(
        dados_cliente["email"]
    )

    assert usuario is not None

    id_usuario = usuario[0]

    assert usuario[1] == dados_cliente["email"]
    assert usuario[2] is True

    cliente = buscar_cliente_por_usuario(id_usuario)

    assert cliente is not None

    assert cliente[1] == id_usuario
    assert cliente[2] == dados_cliente["nome"]
    assert cliente[3] == dados_cliente["cpf"]
    assert cliente[4] == dados_cliente["telefone"]


# ============================================================
# LOGIN
# ============================================================


def test_login_cria_sessao(
    client,
    dados_cliente,
):
    cadastro = client.post(
        "/api/v1/clientes",
        json=dados_cliente,
    )

    assert cadastro.status_code == 201

    resposta = client.post(
        "/api/v1/login",
        json={
            "email": dados_cliente["email"],
            "senha": dados_cliente["senha"],
        },
    )

    assert resposta.status_code == 200

    dados = resposta.get_json()

    assert dados["mensagem"] == "Login realizado com sucesso."
    assert dados["usuario"]["email"] == dados_cliente["email"]

    with client.session_transaction() as sess:
        assert "id_usuario" in sess
        assert isinstance(sess["id_usuario"], int)
        assert sess["id_usuario"] > 0


def test_login_senha_incorreta(
    client,
    dados_cliente,
):
    cadastro = client.post(
        "/api/v1/clientes",
        json=dados_cliente,
    )

    assert cadastro.status_code == 201

    resposta = client.post(
        "/api/v1/login",
        json={
            "email": dados_cliente["email"],
            "senha": "senha-obviamente-incorreta",
        },
    )

    assert resposta.status_code == 401


# ============================================================
# /ME
# ============================================================


def test_me_retorna_usuario_autenticado(
    client,
    dados_cliente,
):
    cadastro = client.post(
        "/api/v1/clientes",
        json=dados_cliente,
    )

    assert cadastro.status_code == 201

    login = client.post(
        "/api/v1/login",
        json={
            "email": dados_cliente["email"],
            "senha": dados_cliente["senha"],
        },
    )

    assert login.status_code == 200

    resposta = client.get("/api/v1/me")

    assert resposta.status_code == 200

    dados = resposta.get_json()

    assert dados["usuario"]["email"] == dados_cliente["email"]


def test_me_sem_autenticacao(
    client,
):
    resposta = client.get("/api/v1/me")

    assert resposta.status_code == 401


# ============================================================
# LOGOUT
# ============================================================


def test_logout_remove_sessao(
    client,
    dados_cliente,
):
    cadastro = client.post(
        "/api/v1/clientes",
        json=dados_cliente,
    )

    assert cadastro.status_code == 201

    login = client.post(
        "/api/v1/login",
        json={
            "email": dados_cliente["email"],
            "senha": dados_cliente["senha"],
        },
    )

    assert login.status_code == 200

    with client.session_transaction() as sess:
        assert "id_usuario" in sess

    logout = client.post("/api/v1/logout")

    assert logout.status_code == 200

    with client.session_transaction() as sess:
        assert "id_usuario" not in sess

    me = client.get("/api/v1/me")

    assert me.status_code == 401


# ============================================================
# PEDIDO
# ============================================================


def test_cliente_autenticado_cria_pedido(
    client,
    dados_cliente,
):
    # 1. Cadastro
    cadastro = client.post(
        "/api/v1/clientes",
        json=dados_cliente,
    )

    assert cadastro.status_code == 201

    # 2. Login
    login = client.post(
        "/api/v1/login",
        json={
            "email": dados_cliente["email"],
            "senha": dados_cliente["senha"],
        },
    )

    assert login.status_code == 200

    # 3. Descobre o usuário criado
    usuario = buscar_usuario_por_email(
        dados_cliente["email"]
    )

    assert usuario is not None

    id_usuario = usuario[0]

    # 4. Descobre o cliente relacionado
    cliente_db = buscar_cliente_por_usuario(id_usuario)

    assert cliente_db is not None

    id_cliente = cliente_db[0]

    # 5. Produto real existente
    produto = buscar_produto()

    assert produto is not None

    id_produto = produto[0]
    preco = produto[1]

    # 6. Cria pedido
    payload = {
        "itens": [
            {
                "id_produto": id_produto,
                "quantidade": 2,
                "observacao": "Teste automatizado",
            }
        ],
        "forma_pagamento": "PIX",
        "contato": {
            "nome": dados_cliente["nome"],
            "telefone": dados_cliente["telefone"],
        },
        "endereco": {
            "cep": "14000000",
            "logradouro": "Rua de Teste",
            "numero": "123",
            "complemento": "",
            "bairro": "Centro",
            "cidade": "Ribeirão Preto",
            "uf": "SP",
        },
    }

    resposta = client.post(
        "/api/v1/pedidos",
        json=payload,
    )

    print("\nSTATUS:", resposta.status_code)
    print("RESPOSTA:", resposta.get_json())

    assert resposta.status_code == 201

    dados = resposta.get_json()

    assert "id_pedido" in dados

    id_pedido = dados["id_pedido"]

    # 7. Verifica o pedido no banco
    pedido_db = buscar_pedido(id_pedido)

    assert pedido_db is not None

    assert pedido_db[0] == id_pedido

    # O ID do cliente deve vir da sessão,
    # e não do JSON enviado pelo cliente.
    assert pedido_db[1] == id_cliente

    assert pedido_db[2] == 1

    status_recebido = buscar_status_recebido()

    assert status_recebido is not None
    assert pedido_db[3] == status_recebido

    # 8. Verifica os itens
    itens_db = buscar_itens_pedido(id_pedido)

    assert len(itens_db) == 1

    item = itens_db[0]

    assert item[0] == id_pedido
    assert item[1] == id_produto
    assert item[2] == 2

    # O preço deve vir do banco.
    assert item[3] == preco

    assert item[4] == preco * 2


def test_pedido_sem_login(
    client,
):
    payload = {
        "itens": [],
        "forma_pagamento": "PIX",
        "contato": {
            "nome": "Teste",
            "telefone": "16999999999",
        },
        "endereco": {
            "cep": "14000000",
            "logradouro": "Rua de Teste",
            "numero": "123",
            "bairro": "Centro",
            "cidade": "Ribeirão Preto",
            "uf": "SP",
        },
    }

    resposta = client.post(
        "/api/v1/pedidos",
        json=payload,
    )

    assert resposta.status_code == 401


# ============================================================
# SEGURANÇA DO id_cliente
# ============================================================


def test_pedido_nao_deve_aceitar_id_cliente_do_payload(
    client,
    dados_cliente,
):
    cadastro = client.post(
        "/api/v1/clientes",
        json=dados_cliente,
    )

    assert cadastro.status_code == 201

    login = client.post(
        "/api/v1/login",
        json={
            "email": dados_cliente["email"],
            "senha": dados_cliente["senha"],
        },
    )

    assert login.status_code == 200

    usuario = buscar_usuario_por_email(
        dados_cliente["email"]
    )

    assert usuario is not None

    id_usuario = usuario[0]

    cliente_db = buscar_cliente_por_usuario(id_usuario)

    assert cliente_db is not None

    id_cliente_real = cliente_db[0]

    produto = buscar_produto()

    assert produto is not None

    id_produto = produto[0]

    payload = {
        # Este valor deve ser ignorado pelo backend.
        "id_cliente": 999999,

        "itens": [
            {
                "id_produto": id_produto,
                "quantidade": 1,
                "observacao": "Teste de segurança",
            }
        ],
        "forma_pagamento": "PIX",
        "contato": {
            "nome": dados_cliente["nome"],
            "telefone": dados_cliente["telefone"],
        },
        "endereco": {
            "cep": "14000000",
            "logradouro": "Rua de Teste",
            "numero": "123",
            "bairro": "Centro",
            "cidade": "Ribeirão Preto",
            "uf": "SP",
        },
    }

    resposta = client.post(
        "/api/v1/pedidos",
        json=payload,
    )

    assert resposta.status_code == 201

    dados = resposta.get_json()

    pedido_db = buscar_pedido(
        dados["id_pedido"]
    )

    assert pedido_db is not None

    # Deve utilizar o cliente da sessão.
    assert pedido_db[1] == id_cliente_real

    # Jamais o 999999 enviado pelo cliente.
    assert pedido_db[1] != 999999