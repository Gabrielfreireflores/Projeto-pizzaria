from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from app.database import get_connection

from app.repositories.usuario_repository import (
    buscar_usuario_por_email,
    criar_usuario
)

from app.database import get_connection
from app.repositories.cliente_repository import criar_cliente


def cadastrar_usuario(email, senha, nome_perfil, descricao_perfil):
    email = email.strip().lower()

    if email == "":
        raise ValueError("O e-mail não pode ser vazio.")

    if senha == "":
        raise ValueError("A senha não pode ser vazia.")

    usuario_existente = buscar_usuario_por_email(email)

    if usuario_existente:
        raise ValueError("Usuário já cadastrado com este e-mail.")

    senha_hash = generate_password_hash(senha)

    conn = get_connection()

    try:
        usuario = criar_usuario(
            conn,
            email,
            senha_hash,
            nome_perfil,
            descricao_perfil
        )

        conn.commit()

        return usuario

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def cadastrar_cliente(email, senha, nome, cpf, telefone=None):
    email = email.strip().lower()
    nome = nome.strip()
    cpf = cpf.strip()

    if email == "" or "@" not in email:
        raise ValueError("O e-mail não pode ser vazio.")

    if senha == "":
        raise ValueError("A senha não pode ser vazia.")

    if nome == "":
        raise ValueError("O nome não pode ser vazio.")

    if cpf == "":
        raise ValueError("O CPF não pode ser vazio.")

    usuario_existente = buscar_usuario_por_email(email)

    if usuario_existente:
        raise ValueError("Usuário já cadastrado com este e-mail.")

    senha_hash = generate_password_hash(senha)

    conn = get_connection()

    try:
        usuario = criar_usuario(
            conn=conn,
            email=email,
            senha=senha_hash,
            nome_perfil="cliente",
            descricao="Usuário cliente criado pelo cadastro"
        )

        id_usuario = usuario[0]

        cliente = criar_cliente(
            conn=conn,
            id_usuario=id_usuario,
            nome=nome,
            cpf=cpf,
            telefone=telefone
        )

        conn.commit()

        return usuario, cliente

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def autenticar_usuario(email, senha):
    email = email.strip().lower()

    usuario = buscar_usuario_por_email(email)

    if usuario is None:
        raise ValueError("E-mail ou senha inválidos.")

    if not check_password_hash(usuario[3], senha):
        raise ValueError("E-mail ou senha inválidos.")

    if usuario[2] == False:
        raise ValueError("Usuário inativo.")

    return usuario