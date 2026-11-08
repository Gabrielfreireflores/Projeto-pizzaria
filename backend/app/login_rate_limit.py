"""Limites distribuídos de login via EVAL atômico no Upstash Redis REST."""
import hashlib
import hmac
import json
import os
from urllib.parse import urlsplit

from flask import current_app
from app.provider_http import post_json_response


# Verifica todos os limites antes de consumir; incrementos e TTL são atômicos.
# A mesma hash tag mantém as chaves no mesmo slot quando há Redis Cluster.
LOGIN_SCRIPT = """
local retry = 0
local window = tonumber(ARGV[1])
for i, key in ipairs(KEYS) do
  local count = tonumber(redis.call('GET', key) or '0')
  local ttl = redis.call('TTL', key)
  if count > 0 and ttl < 0 then
    redis.call('EXPIRE', key, window)
    ttl = window
  end
  if count >= tonumber(ARGV[i + 1]) then
    retry = math.max(retry, math.max(ttl, 1))
  end
end
if retry > 0 then return {0, retry} end
for i, key in ipairs(KEYS) do
  local count = redis.call('INCR', key)
  if count == 1 then redis.call('EXPIRE', key, window) end
end
return {1, 0}
"""


def configure_login_limits(app):
    app.config.update(
        LOGIN_RATE_LIMITER=os.getenv('LOGIN_RATE_LIMITER',
                                     'upstash' if app.config['PRODUCTION'] else 'disabled'),
        UPSTASH_REDIS_REST_URL=os.getenv('UPSTASH_REDIS_REST_URL', ''),
        UPSTASH_REDIS_REST_TOKEN=os.getenv('UPSTASH_REDIS_REST_TOKEN', ''),
    )
    if app.config['LOGIN_RATE_LIMITER'] not in ('disabled', 'upstash'):
        raise RuntimeError('Limitador de login inválido.')
    for name, default, maximum in [('LOGIN_RATE_LIMIT', 10, 100),
                                    ('LOGIN_GLOBAL_LIMIT', 100, 10000),
                                    ('LOGIN_WINDOW_SECONDS', 900, 3600)]:
        try:
            value = int(os.getenv(name, str(default)))
            if not 1 <= value <= maximum:
                raise ValueError()
        except ValueError:
            raise RuntimeError('Configuração de limites de login inválida.') from None
        app.config[name] = value


def check_login_rate(email):
    config = current_app.config
    if config['LOGIN_RATE_LIMITER'] == 'disabled':
        if config['PRODUCTION']:
            raise RuntimeError('Limitador distribuído obrigatório em produção.')
        return 0
    url = config['UPSTASH_REDIS_REST_URL']
    token = config['UPSTASH_REDIS_REST_TOKEN']
    parsed = urlsplit(url)
    if (parsed.scheme != 'https' or not parsed.hostname
            or not parsed.hostname.endswith('.upstash.io') or parsed.port not in (None, 443)
            or parsed.username or parsed.password or parsed.path not in ('', '/')
            or parsed.query or parsed.fragment or not token or not config['SECRET_KEY']):
        raise RuntimeError('Limitador distribuído não configurado.')
    digest = hmac.new(config['SECRET_KEY'].encode(),
                      email.strip().lower().encode(), hashlib.sha256).hexdigest()
    command = ['EVAL', LOGIN_SCRIPT, 2, f'pizzaria:{{login}}:account:{digest}',
               'pizzaria:{login}:global', config['LOGIN_WINDOW_SECONDS'],
               config['LOGIN_RATE_LIMIT'], config['LOGIN_GLOBAL_LIMIT']]
    result = post_json_response(url.rstrip('/'), json.dumps(command).encode(), {
        'Authorization': f'Bearer {token}', 'Content-Type': 'application/json',
    }).get('result')
    if (not isinstance(result, list) or len(result) != 2
            or any(type(value) is not int for value in result)
            or result[0] not in (0, 1) or result[1] < 0
            or (result[0] == 0 and result[1] == 0)
            or (result[0] == 1 and result[1] != 0)):
        raise RuntimeError('Resposta inválida do limitador distribuído.')
    return result[1] if result[0] == 0 else 0
