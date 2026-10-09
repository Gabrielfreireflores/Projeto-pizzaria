from app.database import get_connection
from app.exceptions.custom_exceptions import ChaveUnicaVioladaError, ErroBancoDadosError, SintaxeSQLError
from contextlib import contextmanager

def buscar_usuario_por_email(email: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id_usuario, email, ativo, senha FROM usuario WHERE lower(email) = %s", (email,)
            )
            resultado = cursor.fetchone()
            return resultado

    except psycopg.errors.SyntaxError as e:
        raise SintaxeSQLError("Erro de sintaxe SQL.") from e

    except psycopg.DatabaseError as e:
        raise ErroBancoDadosError("Erro interno ao acessar o banco de dados.") from e

    finally:
        conn.close()

def criar_usuario(conn, email: str, senha: str, nome_perfil: str, descricao: str):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO usuario
                (email, senha, nome_perfil, descricao)
            VALUES
                (%s, %s, %s, %s)
            RETURNING id_usuario, email
            """,
            (email, senha, nome_perfil, descricao)
        )

        return cursor.fetchone()

def buscar_usuario_por_id(id_usuario: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT id_usuario, email, ativo, nome_perfil, descricao
                FROM usuario
                WHERE id_usuario = %s""", (id_usuario,)
            )
            resultado = cursor.fetchone()
            return resultado
    except psycopg.DatabaseError as e:
        raise ErroBancoDadosError("Erro interno ao acessar o banco de dados.") from e
    finally:
        conn.close()


@contextmanager
def transacao_auth():
    conn = get_connection()

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()