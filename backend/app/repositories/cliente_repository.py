def buscar_cliente_por_usuario(conn, id_usuario: int):
    with conn.cursor() as cursor:
        cursor.execute(
            """SELECT c.id_cliente, u.ativo, u.nome_perfil
            FROM cliente c JOIN usuario u ON u.id_usuario = c.id_usuario
            WHERE u.id_usuario = %s FOR SHARE OF c, u""", (id_usuario,)
        )
        return cursor.fetchone()
