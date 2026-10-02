def criar_endereco(conn, id_cliente: int, endereco: dict):
    with conn.cursor() as cursor:
        cursor.execute(
            """INSERT INTO endereco
            (id_cliente, cep, logradouro, numero, complemento, bairro, cidade, uf)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_endereco""",
            (id_cliente, endereco['cep'], endereco['logradouro'], endereco['numero'],
             endereco['complemento'], endereco['bairro'], endereco['cidade'], endereco['uf'])
        )
        return cursor.fetchone()[0]
