def buscar_acompanhamento(conn, id_pedido: int, id_cliente: int):
    with conn.cursor() as cursor:
        cursor.execute(
            """SELECT p.id_pedido, s.nome_status,
                      p.data_hora_pedido AT TIME ZONE 'America/Sao_Paulo'
            FROM pedido p
            JOIN status s ON s.id_status = p.id_status
            WHERE p.id_pedido = %s AND p.id_cliente = %s""",
            (id_pedido, id_cliente),
        )
        return cursor.fetchone()
