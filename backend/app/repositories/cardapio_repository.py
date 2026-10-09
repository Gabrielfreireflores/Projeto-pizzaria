from app.database import get_connection


def listar_cardapio():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT c.id_categoria, c.nome, p.id_produto, p.nome,
                          p.tamanho, p.preco, p.foto, p.descricao
                FROM produto p
                JOIN categoria c ON c.id_categoria = p.id_categoria
                WHERE p.disponivel = TRUE
                ORDER BY c.nome, c.id_categoria, p.nome, p.id_produto"""
            )
            return cursor.fetchall()
    finally:
        conn.close()
