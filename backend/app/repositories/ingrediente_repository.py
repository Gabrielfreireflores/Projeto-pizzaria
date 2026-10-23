from app.database import get_connection


def listar_ingredientes():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT id_ingrediente, nome, quantidade_estoque, unidade_medida
                FROM ingrediente
                ORDER BY nome"""
            )
            return cursor.fetchall()
    finally:
        conn.close()