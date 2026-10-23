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
            (id_cliente, id_funcionario, id_status, id_endereco,
             forma_pagamento, taxa_entrega, valor_total)
            VALUES (%s, 1, %s, %s, %s, %s, %s)
            RETURNING id_pedido, data_hora_pedido""",
            (
                pedido['id_cliente'],
                pedido['id_status'],
                pedido['id_endereco'],
                pedido['forma_pagamento'],
                pedido['taxa_entrega'],
                pedido['valor_total'],
            )
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


def listar_pedidos(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                p.id_pedido,
                p.id_cliente,
                p.id_funcionario,
                p.id_status,
                s.nome_status,
                p.id_endereco,
                p.data_hora_pedido,
                p.forma_pagamento,
                p.taxa_entrega,
                p.valor_total,
                c.nome,
                e.cep,
                e.logradouro,
                e.numero,
                e.complemento,
                e.bairro,
                e.cidade,
                e.uf
            FROM pedido p
            JOIN status s ON s.id_status = p.id_status
            JOIN cliente c ON c.id_cliente = p.id_cliente
            JOIN endereco e ON e.id_endereco = p.id_endereco
            ORDER BY p.data_hora_pedido DESC
            """
        )
        pedidos = cursor.fetchall()

        cursor.execute(
            """
            SELECT
                ip.id_pedido,
                ip.id_produto,
                pr.nome,
                ip.quantidade,
                ip.preco_unitario,
                ip.subtotal,
                ip.observacao
            FROM item_pedido ip
            JOIN produto pr ON pr.id_produto = ip.id_produto
            ORDER BY ip.id_pedido, ip.id_item_pedido
            """
        )
        itens = cursor.fetchall()

    itens_por_pedido = {}
    for item in itens:
        itens_por_pedido.setdefault(item[0], []).append({
            "id_produto": item[1],
            "produto": item[2],
            "quantidade": item[3],
            "preco_unitario": str(item[4]),
            "subtotal": str(item[5]),
            "observacao": item[6],
        })

    resultado = []
    for p in pedidos:
        resultado.append({
            "id_pedido": p[0],
            "id_cliente": p[1],
            "id_funcionario": p[2],
            "id_status": p[3],
            "status": p[4],
            "id_endereco": p[5],
            "data_hora_pedido": p[6].isoformat(),
            "forma_pagamento": p[7],
            "taxa_entrega": str(p[8]),
            "valor_total": str(p[9]),
            "cliente": p[10],
            "endereco": {
                "cep": p[11],
                "logradouro": p[12],
                "numero": p[13],
                "complemento": p[14],
                "bairro": p[15],
                "cidade": p[16],
                "uf": p[17],
            },
            "itens": itens_por_pedido.get(p[0], []),
        })

    return resultado


def atualizar_status_pedido(conn, id_pedido: int, id_status: int,
                            id_funcionario: int):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            UPDATE pedido
            SET id_status = %s, id_funcionario = %s
            WHERE id_pedido = %s
            RETURNING id_pedido
            """,
            (id_status, id_funcionario, id_pedido),
        )
        return cursor.fetchone()

def lista_status(conn):
    """Devolve [(id_status, nome_status), ...]"""
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_status, nome_status FROM status ORDER BY id_status')
        return cursor.fetchall()

def buscar_status_do_pedido(conn, id_pedido: int):
    """Devolve o id_status atual (trabando a linha) ou None se o pedido ainda não existe"""
    with conn.cursor() as cursor:
        cursor.execute(
            'SELECT id_status FROM pedido WHERE id_pedido = %s FOR UPDATE',
            (id_pedido,),
        )
        linha = cursor.fetchone()
        return linha[0] if linha else None

def trocar_status_pedido(conn, id_pedido: int, id_status: int):
    with conn.cursor() as cursor:
        cursor.execute(
            'UPDATE pedido SET id_status = %s WHERE id_pedido = %s',
            (id_status, id_pedido),
        )

# --- Mudança de status depois do aceite --------------------------------------
# status atual (sem acento, minúsculas) -> próximos status permitidos.
# O "aceitar" (Recebido -> Em preparação) continua na função aceitar_pedido.
TRANSICOES_STATUS = {
    'em preparacao': ('Saiu para entrega',),
    'saiu para entrega': ('Entregue',),
}


class TransicaoInvalida(ValueError):
    """O pedido não pode ir do status atual para o status pedido."""


def _chave_status(texto: str) -> str:
    sem_acento = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode()
    return sem_acento.strip().casefold()


def alterar_status_pedido(id_pedido: int, data: dict, id_usuario: int):
    _obter_funcionario(id_usuario)

    texto = data.get('status')
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError('Informe o novo status.')

    with transacao_pedido_repository() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT s.nome_status, p.id_funcionario
                FROM pedido p
                JOIN status s ON s.id_status = p.id_status
                WHERE p.id_pedido = %s
                FOR UPDATE OF p
                """,
                (id_pedido,),
            )
            pedido = cursor.fetchone()

        if pedido is None:
            raise LookupError('Pedido não encontrado.')

        atual, id_funcionario_pedido = pedido
        permitidos = TRANSICOES_STATUS.get(_chave_status(atual), ())
        novo_nome = next(
            (nome for nome in permitidos if _chave_status(nome) == _chave_status(texto)),
            None,
        )
        if novo_nome is None:
            raise TransicaoInvalida(
                f'Não é possível mudar o pedido de "{atual}" para "{texto.strip()}".'
            )

        status = buscar_status_repository(conn, novo_nome)
        if status is None:
            raise RuntimeError(f"Status '{novo_nome}' não cadastrado.")

        # Mantém o funcionário que já era responsável (quem aceitou o pedido).
        atualizar_status_repository(conn, id_pedido, status[0], id_funcionario_pedido)

    return {
        'id_pedido': id_pedido,
        'status': novo_nome,
        'id_funcionario': id_funcionario_pedido,
    }
