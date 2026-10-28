from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import psycopg

from app.database import get_connection

from app.repositories.usuario_repository import (
    buscar_usuario_por_email,
    criar_usuario
)

from app.database import get_connection
from app.repositories.cliente_repository import criar_cliente
from app.schemas.cliente_schema import validar_cadastro_cliente


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


def cadastrar_cliente(email, senha, nome, telefone=None):
    dados = validar_cadastro_cliente(email, senha, nome, telefone)
    email, senha, nome, telefone = (dados[c] for c in ('email', 'senha', 'nome', 'telefone'))

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
            cpf=None,
            telefone=telefone
        )

        conn.commit()

        return usuario, cliente

    except psycopg.errors.UniqueViolation:
        conn.rollback()
        raise ValueError('Usuário já cadastrado com este e-mail.') from None
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

    if usuario[2] is False:
        raise ValueError("Usuário inativo.")
    
    

    return usuario