from app.database import get_connection

def buscar_usuario_por_email(email: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id_usuario, email, ativo, senha FROM usuario WHERE lower(email) = %s", (email,)
            )
            resultado = cursor.fetchone()
            return resultado
    finally:
        conn.close()

def criar_usuario(email: str, senha: str, nome_perfil: str, descricao_perfil: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO usuario (email, senha, nome_perfil, descricao_perfil) VALUES (%s, %s, %s, %s) RETURNING id_usuario, email",
                (email, senha, nome_perfil, descricao_perfil)
            )
            usuario = cursor.fetchone()
            conn.commit()
            return usuario
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

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
    finally:
        conn.close()