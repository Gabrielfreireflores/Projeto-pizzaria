from contextlib import contextmanager

from app.database import get_connection


@contextmanager
def transacao_pedido():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def buscar_status_por_nome(conn, nome: str):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_status FROM status WHERE nome_status = %s', (nome,))
        return cursor.fetchone()


def criar_pedido(conn, pedido: dict):
    with conn.cursor() as cursor:
        cursor.execute(
            """INSERT INTO pedido
            (id_cliente, id_funcionario, id_status, id_endereco, forma_pagamento,
             taxa_entrega, valor_total, nome_contato, telefone_contato)
            VALUES (%s, NULL, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_pedido, data_hora_pedido""",
            (pedido['id_cliente'], pedido['id_status'], pedido['id_endereco'],
             pedido['forma_pagamento'], pedido['taxa_entrega'], pedido['valor_total'],
             pedido['contato']['nome'], pedido['contato']['telefone'])
        )
        return cursor.fetchone()


def criar_itens_pedido(conn, id_pedido: int, itens: list):
    with conn.cursor() as cursor:
        cursor.executemany(
            """INSERT INTO item_pedido
            (id_pedido, id_produto, quantidade, preco_unitario, subtotal, observacao)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            [(id_pedido, item['id_produto'], item['quantidade'], item['preco_unitario'],
              item['subtotal'], item['observacao']) for item in itens]
        )
