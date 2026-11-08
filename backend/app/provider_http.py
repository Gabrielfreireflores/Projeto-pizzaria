"""HTTP de provedores: TLS padrão, timeout, resposta limitada e sem redirects."""
import json
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def post_json_response(url, body, headers, timeout=5):
    request = Request(url, data=body, method='POST', headers=headers)
    try:
        with build_opener(NoRedirect()).open(request, timeout=timeout) as response:
            content = response.read(65537)
            if response.status != 200 or len(content) > 65536:
                raise ValueError('Resposta inválida.')
            result = json.loads(content)
            if not isinstance(result, dict):
                raise ValueError('Resposta inválida.')
            return result
    except HTTPError as error:
        error.close()
        raise RuntimeError('Serviço externo indisponível.') from None
    except (URLError, OSError, ValueError):
        # Nunca propaga corpo, URL com tokens ou cabeçalhos do provedor.
        raise RuntimeError('Serviço externo indisponível.') from None
