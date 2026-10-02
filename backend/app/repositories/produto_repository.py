from app.database import get_connection


def listar_produtos():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT p.id_produto, p.nome, p.tamanho, p.preco, p.disponivel,
                          c.id_categoria, c.nome, i.id_ingrediente, i.nome,
                          ip.quantidade_necessaria, i.unidade_medida
                FROM produto p JOIN categoria c ON c.id_categoria = p.id_categoria
                LEFT JOIN ingrediente_produto ip ON ip.id_produto = p.id_produto
                LEFT JOIN ingrediente i ON i.id_ingrediente = ip.id_ingrediente
                ORDER BY p.id_produto, i.id_ingrediente"""
            )
            return cursor.fetchall()
    finally:
        conn.close()


def buscar_produtos_para_pedido(conn, ids: list):
    with conn.cursor() as cursor:
        # Mantém preço e disponibilidade estáveis até o fim da transação.
        cursor.execute(
            """SELECT id_produto, preco, disponivel FROM produto
            WHERE id_produto = ANY(%s) ORDER BY id_produto FOR SHARE""", (ids,)
        )
        return cursor.fetchall()


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
