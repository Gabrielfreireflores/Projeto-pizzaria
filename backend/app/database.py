##  código de conexão ao banco de dados 
## outro componentes podem chamar a funcao para se conectar ao banco de dados

import os

import psycopg
from psycopg.conninfo import conninfo_to_dict
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL não foi definida.")

    try:
        params = conninfo_to_dict(database_url)
        timeout = int(os.getenv('DB_CONNECT_TIMEOUT', '10'))
        if not 1 <= timeout <= 30:
            raise ValueError()
    except (psycopg.Error, ValueError):
        raise RuntimeError('Configuração de conexão PostgreSQL inválida.') from None
    production = os.getenv('APP_ENV') == 'production' or os.getenv('VERCEL') == '1'
    if production:
        mode = params.get('sslmode', 'require')
        if mode not in ('require', 'verify-ca', 'verify-full'):
            raise RuntimeError('A conexão PostgreSQL exige TLS em produção.')
        params['sslmode'] = mode
        if params.get('host', '').endswith('.neon.tech'):
            params.setdefault('channel_binding', 'require')
    # O pool é do provedor (URL -pooler), não um pool persistente no processo.
    # Sem prepared statements automáticos, funciona também com transaction pooling.
    params['connect_timeout'] = timeout
    return psycopg.connect(**params, prepare_threshold=None)
