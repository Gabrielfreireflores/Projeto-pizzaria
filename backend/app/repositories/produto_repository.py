from app.database import get_connection


def listar_produtos():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT p.id_produto, p.nome, p.tamanho, p.preco, p.disponivel, p.foto,
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
                """INSERT INTO produto (nome, tamanho, preco, id_categoria, disponivel, foto)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_produto, nome, tamanho, preco, id_categoria, disponivel, foto""",
                (produto['nome'], produto['tamanho'], produto['preco'],
                 produto['id_categoria'], produto['disponivel'], produto.get("foto"),)
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

def atualizar_produto(id_produto: int, produto: dict):
    """Atualiza o produto e substitui a receita. Devolve None se o produto não existe."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """UPDATE produto
                SET nome = %s, tamanho = %s, preco = %s, id_categoria = %s, disponivel = %s, foto = COALESCE(%s, foto)
                WHERE id_produto = %s
                RETURNING id_produto, nome, tamanho, preco, id_categoria, disponivel, foto""",
                (produto['nome'], produto['tamanho'], produto['preco'],
                 produto['id_categoria'], produto['disponivel'], produto.get("foto"), id_produto)
            )
            resultado = cursor.fetchone()
            if resultado is None:
                conn.rollback()
                return None
            cursor.execute(
                "DELETE FROM ingrediente_produto WHERE id_produto = %s", (id_produto,)
            )
            cursor.executemany(
                """INSERT INTO ingrediente_produto
                (id_produto, id_ingrediente, quantidade_necessaria)
                VALUES (%s, %s, %s)""",
                [(id_produto, item['id_ingrediente'], item['quantidade_necessaria'])
                 for item in produto['ingredientes']]
            )
            conn.commit()
            return resultado
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def excluir_produto(id_produto: int) -> bool:
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM ingrediente_produto WHERE id_produto = %s", (id_produto,)
            )
            cursor.execute("DELETE FROM produto WHERE id_produto = %s", (id_produto,))
            removido = cursor.rowcount > 0
            conn.commit()
            return removido
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
