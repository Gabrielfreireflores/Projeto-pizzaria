from app.database import get_connection

def buscar_cliente_por_usuario(conn, id_usuario: int):
    with conn.cursor() as cursor:
        cursor.execute(
            """SELECT c.id_cliente, u.ativo, u.nome_perfil
            FROM cliente c JOIN usuario u ON u.id_usuario = c.id_usuario
            WHERE u.id_usuario = %s FOR SHARE OF c, u""", (id_usuario,)
        )
        return cursor.fetchone()

def criar_cliente(conn, id_usuario: int, nome: str, cpf: str, telefone=None):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO cliente
                (id_usuario, nome, cpf, telefone)
            VALUES
                (%s, %s, %s, %s)
            RETURNING id_cliente, id_usuario, nome, cpf, telefone
            """,
            (id_usuario, nome, cpf, telefone)
        )

        return cursor.fetchone()
