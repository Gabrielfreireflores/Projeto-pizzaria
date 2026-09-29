from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from app.repositories.usuario_repository import (
    buscar_usuario_por_email,
    criar_usuario
)

def cadastrar_usuario(email, senha, nome_perfil, descricao_perfil):
    email = email.strip().lower()
    if email == "":
        raise ValueError("O e-mail não pode ser vazio.")
    if senha == "":
        raise ValueError("A senha não pode ser vazia.")
    usuario_existente = buscar_usuario_por_email(email)
    if usuario_existente:
        raise ValueError("Usuário já cadastrado com este e-mail.")
    senha_hash = generate_password_hash(senha)
    return criar_usuario(email, senha_hash, nome_perfil, descricao_perfil)

def autenticar_usuario(email, senha):
    email = email.strip().lower()
    usuario = buscar_usuario_por_email(email)
    if usuario is None:
        raise ValueError("E-mail ou senha inválidos.")
    if not check_password_hash(usuario[3], senha):
        raise ValueError("E-mail ou senha inválidos.")
    if usuario[2] == False:
        raise ValueError("Usuário inativo.")
    return usuario
    
    
 
