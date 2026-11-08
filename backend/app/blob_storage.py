"""Fotos públicas do cardápio no SDK Python oficial do Vercel Blob."""
from contextlib import contextmanager
import os
import re
from urllib.parse import urlsplit
from uuid import uuid4

import httpx2
from vercel.api import session
from vercel.blob import sync as blob


class BlobImageStorage:
    @contextmanager
    def _session(self):
        token = os.getenv('BLOB_READ_WRITE_TOKEN', '')
        store = os.getenv('BLOB_STORE_ID', '').removeprefix('store_')
        if not token or not re.fullmatch(r'[a-zA-Z0-9_-]+', store):
            raise RuntimeError('Armazenamento Blob não configurado.')
        # Configuração explícita evita credenciais automáticas de CLI/OIDC ou URLs alternativas.
        options = blob.SyncBlobServiceOptions(
            base_url='https://vercel.com/api/blob',
            credentials_factory=lambda: blob.BlobCredentials(token=token, store_id=store),
        )
        try:
            with session(service_options=[options], httpx_client_factory=lambda:
                         httpx2.Client(timeout=10, follow_redirects=False)):
                yield store.lower()
        except (blob.BlobError, httpx2.HTTPError, ValueError):
            raise RuntimeError('Serviço de imagens indisponível.') from None

    def save(self, content, extension):
        key = f'pizzaria/produtos/{uuid4().hex}{extension}'
        mime = 'image/jpeg' if extension in ('.jpg', '.jpeg') else f'image/{extension[1:]}'
        with self._session() as store:
            uploaded = blob.put_blob(key, content, access='public', content_type=mime,
                                     add_random_suffix=False, allow_overwrite=False)
            parsed = urlsplit(uploaded.url)
            if (uploaded.pathname != key or parsed.scheme != 'https'
                    or parsed.netloc != f'{store}.public.blob.vercel-storage.com'
                    or parsed.path != f'/{key}' or parsed.query or parsed.fragment):
                raise RuntimeError('Resposta inválida do armazenamento de imagens.')
        return uploaded.url, key

    def delete(self, key):
        if not isinstance(key, str) or not re.fullmatch(
                r'pizzaria/produtos/[0-9a-f]{32}\.(?:jpg|jpeg|png|webp)', key):
            raise ValueError('Referência de upload inválida.')
        with self._session():
            blob.delete_blob(key)
