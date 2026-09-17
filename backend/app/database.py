##  código de conexão ao banco de dados 
## outro componentes podem chamar a funcao para se conectar ao banco de dados

import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL não foi definida.")

    return psycopg.connect(database_url)