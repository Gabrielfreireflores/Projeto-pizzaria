from app.database import get_connection


def buscar_funcionario_por_usuario(id_usuario: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT u.ativo, u.nome_perfil, f.id_funcionario
                FROM usuario u
                LEFT JOIN funcionario f ON f.id_usuario = u.id_usuario
                WHERE u.id_usuario = %s""", (id_usuario,)
            )
            return cursor.fetchone()
    finally:
        conn.close()
