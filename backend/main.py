"""Entrada WSGI reconhecida pela Vercel; importar não inicia servidor."""
from app import create_app

app = create_app()
