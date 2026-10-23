from app.database import get_connection


def listar_equipe():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT f.id_funcionario, f.nome, f.cpf, f.cargo, f.telefone, u.email, u.ativo
                FROM funcionario f
                JOIN usuario u ON u.id_usuario = f.id_usuario
                ORDER BY f.nome"""
            )
            return cursor.fetchall()
    finally:
        conn.close()


def buscar_id_usuario(id_funcionario: int):
    """Devolve o id_usuario do funcionário, ou None se ele não existe."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id_usuario FROM funcionario WHERE id_funcionario = %s",
                (id_funcionario,),
            )
            linha = cursor.fetchone()
            return linha[0] if linha else None
    finally:
        conn.close()


def criar_membro(dados: dict, senha_hash: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """INSERT INTO usuario (email, senha, nome_perfil, descricao)
                VALUES (%s, %s, 'funcionario', 'Funcionário cadastrado pela equipe')
                RETURNING id_usuario, email, ativo""",
                (dados['email'], senha_hash),
            )
            usuario = cursor.fetchone()
            # AJUSTE: se a tabela funcionario tiver outras colunas obrigatórias, inclua aqui.
            cursor.execute(
                """INSERT INTO funcionario (id_usuario, nome, cpf, cargo, telefone)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_funcionario""",
                (usuario[0], dados['nome'], dados['cpf'], dados['cargo'], dados['telefone']),
            )
            id_funcionario = cursor.fetchone()[0]
            conn.commit()
            return (id_funcionario, dados['nome'], dados['cpf'], dados['cargo'],
                    dados['telefone'], usuario[1], usuario[2])
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def atualizar_membro(id_funcionario: int, dados: dict, senha_hash=None):
    """Devolve a linha atualizada, ou None se o funcionário não existe."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """UPDATE funcionario SET nome = %s, cpf = %s, cargo = %s, telefone = %s
                WHERE id_funcionario = %s
                RETURNING id_usuario""",
                (dados['nome'], dados['cpf'], dados['cargo'], dados['telefone'], id_funcionario),
            )
            linha = cursor.fetchone()
            if linha is None:
                conn.rollback()
                return None
            if senha_hash:
                cursor.execute(
                    "UPDATE usuario SET email = %s, ativo = %s, senha = %s WHERE id_usuario = %s",
                    (dados['email'], dados['ativo'], senha_hash, linha[0]),
                )
            else:
                cursor.execute(
                    "UPDATE usuario SET email = %s, ativo = %s WHERE id_usuario = %s",
                    (dados['email'], dados['ativo'], linha[0]),
                )
            conn.commit()
            return (id_funcionario, dados['nome'], dados['cpf'], dados['cargo'],
                    dados['telefone'], dados['email'], dados['ativo'])
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def excluir_membro(id_funcionario: int) -> bool:
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM funcionario WHERE id_funcionario = %s RETURNING id_usuario",
                (id_funcionario,),
            )
            linha = cursor.fetchone()
            if linha is None:
                conn.rollback()
                return False
            cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (linha[0],))
            conn.commit()
            return True
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()