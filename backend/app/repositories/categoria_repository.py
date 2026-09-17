from app.database import get_connection

def criar_categoria(nome: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO categoria (nome) VALUES (%s) RETURNING id_categoria, nome", (nome,)
            )
            categoria = cursor.fetchone()
            conn.commit()
            return categoria
    finally:
        conn.close()

def buscar_categoria_por_id(id_categoria: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT nome FROM categoria WHERE id_categoria = %s", (id_categoria,)
            )
            resultado = cursor.fetchone()
            return resultado
    finally:
        conn.close()

def buscar_categoria_por_nome(nome: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id_categoria, nome FROM categoria WHERE lower(nome) = %s", (nome,)
            )
            resultado = cursor.fetchone()
            return resultado
    finally:
        conn.close()

def remover_categoria(nome: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM categoria WHERE nome = %s", (nome,)
            )
            conn.commit()
            return 1
    finally:
        conn.close()

def listar_categorias():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT id_categoria, nome FROM categoria"
            )
            resultado = cursor.fetchall()
            return resultado
    finally:
        conn.close()