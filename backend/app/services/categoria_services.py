from app.repositories.categoria_repository import buscar_categoria_por_id as buscar_categoria_por_id_repository
from app.repositories.categoria_repository import remover_categoria as remover_categoria_repository
from app.repositories.categoria_repository import criar_categoria as criar_categoria_repository
from app.repositories.categoria_repository import buscar_categoria_por_nome as buscar_categoria_por_nome_repository
from app.repositories.categoria_repository import buscar_categoria_por_nome as buscar_categoria_por_nome_repository
from app.repositories.categoria_repository import listar_categorias as listar_categorias_repository

def buscar_categoria_por_id(id_categoria: int):
    resultado = buscar_categoria_por_id_repository(id_categoria)
    if resultado is None:
        raise ValueError(f"Categoria {id_categoria} não encontrada.")
    return resultado

def criar_categoria(nome: str):
    nome = nome.strip().lower()
    if nome == "":
        raise ValueError("O nome da categoria não pode ser vazio.")

    if buscar_categoria_por_nome_repository(nome) is not None:
        raise ValueError(f"Categoria '{nome}' já existe.")  
    
    return criar_categoria_repository(nome)

def remover_categoria(nome: str): ## INTEGRAR VALIDACAO COM PRODUTOS -> SE HOUVER PRODUTOS ASSOCIADOS A UMA CATEGORIA, A CATEGORIA NAO DEVE SER EXCLUIDA
    nome = nome.strip().lower()
    if buscar_categoria_por_nome_repository(nome) is None:
        raise ValueError(f"Categoria '{nome}' não está cadastrada, portanto não pode ser removida")
    if nome == "":
        raise ValueError("O nome da categoria a ser removida não pode ser vazio")

    return remover_categoria_repository(nome)

def listar_categorias():
    if listar_categorias_repository is None:
        return "Sem categorias cadastradas"
    return listar_categorias_repository()