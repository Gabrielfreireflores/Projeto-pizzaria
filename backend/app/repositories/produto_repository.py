from app.database import get_connection


def criar_produto(produto: dict):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """INSERT INTO produto (nome, tamanho, preco, id_categoria, disponivel)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_produto, nome, tamanho, preco, id_categoria, disponivel""",
                (produto['nome'], produto['tamanho'], produto['preco'],
                 produto['id_categoria'], produto['disponivel'])
            )
            resultado = cursor.fetchone()
            cursor.executemany(
                """INSERT INTO ingrediente_produto
                (id_produto, id_ingrediente, quantidade_necessaria)
                VALUES (%s, %s, %s)""",
                [(resultado[0], item['id_ingrediente'], item['quantidade_necessaria'])
                 for item in produto['ingredientes']]
            )
            # Produto e receita são persistidos juntos.
            conn.commit()
            return resultado
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
