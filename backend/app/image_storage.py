"""Contrato mínimo de armazenamento local e Blob opcional, sem migração de imagens."""
from io import BytesIO
from pathlib import Path
from uuid import uuid4
import warnings

from flask import current_app
from PIL import Image, UnidentifiedImageError
from app.error_logging import log_internal_error
from app.blob_storage import BlobImageStorage

MAX_BYTES = 3 * 1024 * 1024
MAX_PIXELS = 20_000_000
FORMATS = {
    '.jpg': ('JPEG', 'image/jpeg'), '.jpeg': ('JPEG', 'image/jpeg'),
    '.png': ('PNG', 'image/png'), '.webp': ('WEBP', 'image/webp'),
}


class LocalImageStorage:
    def save(self, content, extension):
        folder = Path(current_app.config['UPLOAD_FOLDER']).resolve()
        try:
            folder.mkdir(parents=True, exist_ok=True)
        except OSError:
            raise RuntimeError('Não foi possível preparar o armazenamento de imagens.') from None
        # Nunca usamos o nome fornecido pelo cliente na construção do caminho.
        name = f'{uuid4().hex}{extension}'
        target = folder / name
        created = False
        try:
            with target.open('xb') as output:
                created = True
                output.write(content)
        except OSError:
            if created:
                try:
                    target.unlink(missing_ok=True)
                except OSError:
                    log_internal_error('Falha ao limpar upload incompleto.')
            raise RuntimeError('Não foi possível armazenar a imagem.') from None
        return f"{current_app.config['UPLOAD_URL']}/{name}", str(target)

    def delete(self, key):
        folder = Path(current_app.config['UPLOAD_FOLDER']).resolve()
        candidate = Path(key)
        target = candidate.resolve()
        if target.parent != folder or candidate.is_symlink():
            raise ValueError('Referência de upload inválida.')
        target.unlink(missing_ok=True)


class DisabledImageStorage:
    def save(self, content, extension):
        raise RuntimeError('Armazenamento persistente de imagens não configurado.')

    def delete(self, key):
        raise RuntimeError('Armazenamento persistente de imagens não configurado.')


def get_image_storage():
    # Contrato preservado para estender com outros adaptadores persistentes se necessário.
    if current_app.config['IMAGE_STORAGE'] == 'blob':
        return BlobImageStorage()
    return (LocalImageStorage() if current_app.config['IMAGE_STORAGE'] == 'local'
            else DisabledImageStorage())


def save_product_image(file):
    if not file or not file.filename:
        return None, None
    extension = Path(file.filename).suffix.lower()
    expected = FORMATS.get(extension)
    if expected is None or file.mimetype != expected[1]:
        raise ValueError('Formato inválido. Use JPG, PNG ou WebP.')
    # Lê no máximo o limite + 1 byte para verificar o tamanho real do arquivo.
    content = file.stream.read(MAX_BYTES + 1)
    if len(content) > MAX_BYTES:
        raise ValueError('A foto deve ter no máximo 3 MiB.')
    if not content:
        raise ValueError('A imagem enviada está vazia.')
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(BytesIO(content)) as image:
                if (image.format != expected[0] or image.width * image.height > MAX_PIXELS
                        or getattr(image, 'n_frames', 1) != 1):
                    raise ValueError('Formato ou dimensões de imagem inválidos.')
                image.verify()
            with Image.open(BytesIO(content)) as image:
                image.load()  # Também rejeita imagens truncadas que só possuem cabeçalho válido.
    except (UnidentifiedImageError, OSError, SyntaxError, Image.DecompressionBombError,
            Image.DecompressionBombWarning):
        raise ValueError('O conteúdo do arquivo não é uma imagem válida.') from None
    return get_image_storage().save(content, extension)
