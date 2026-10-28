
import json
import os
import uuid

import psycopg
from flask import request, jsonify, session, current_app
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

from app.services import produto_services


EXTENSOES_PERMITIDAS = {".jpg", ".jpeg", ".png", ".webp"}
MIMETYPES_PERMITIDOS = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


def _ler_dados_produto():
    """Lê JSON ou os campos de um formulário multipart."""
    if request.mimetype == "multipart/form-data":
        data = request.form.to_dict()

        try:
            data["id_categoria"] = int(data.get("id_categoria", ""))
        except (TypeError, ValueError):
            raise ValueError("Categoria inválida.") from None

        disponivel = data.get("disponivel", "true").strip().lower()
        if disponivel not in ("true", "false"):
            raise ValueError("Disponibilidade inválida.")

        data["disponivel"] = disponivel == "true"

        try:
            data["ingredientes"] = json.loads(
                data.get("ingredientes", "[]")
            )
        except (json.JSONDecodeError, TypeError):
            raise ValueError("A lista de ingredientes é inválida.") from None

        return data, request.files.get("foto")

    try:
        data = request.get_json()
    except (BadRequest, UnsupportedMediaType):
        raise ValueError("Envie um objeto JSON válido.") from None

    if not isinstance(data, dict):
        raise ValueError("Envie um objeto JSON.")

    return data, None


def _salvar_foto(arquivo):
    """Valida e salva a imagem; retorna o caminho público e o caminho físico."""
    if not arquivo or not arquivo.filename:
        return None, None

    nome_original = arquivo.filename
    extensao = os.path.splitext(nome_original)[1].lower()

    if extensao not in EXTENSOES_PERMITIDAS:
        raise ValueError("Formato inválido. Use JPG, PNG ou WebP.")

    if arquivo.mimetype not in MIMETYPES_PERMITIDOS:
        raise ValueError("O arquivo enviado não é uma imagem permitida.")

    pasta = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(pasta, exist_ok=True)

    nome_arquivo = f"{uuid.uuid4().hex}{extensao}"
    caminho_fisico = os.path.join(pasta, nome_arquivo)

    # Lê no máximo 5 MB + 1 byte para verificar o tamanho real do arquivo.
    conteudo = arquivo.stream.read(5 * 1024 * 1024 + 1)

    if len(conteudo) > 5 * 1024 * 1024:
        raise ValueError("A foto deve ter no máximo 5 MB.")

    if not conteudo:
        raise ValueError("A imagem enviada está vazia.")

    with open(caminho_fisico, "wb") as destino:
        destino.write(conteudo)

    caminho_publico = (
        f'{current_app.config["UPLOAD_URL"]}/{nome_arquivo}'
    )

    return caminho_publico, caminho_fisico


def _remover_arquivo(caminho):
    if caminho and os.path.isfile(caminho):
        try:
            os.remove(caminho)
        except OSError:
            current_app.logger.exception(
                "Não foi possível remover um arquivo de upload."
            )


def _id_usuario_autenticado():
    id_usuario = session.get("id_usuario")
    return type(id_usuario) is int and id_usuario > 0


def listar_produtos_controller():
    try:
        return jsonify({
            "produtos": produto_services.listar_produtos()
        }), 200
    except (psycopg.Error, RuntimeError):
        current_app.logger.exception("Falha ao listar produtos.")
        return jsonify({
            "erro": "Não foi possível listar os produtos."
        }), 503


def criar_produto_controller():
    if not _id_usuario_autenticado():
        return jsonify({"erro": "Autenticação necessária."}), 401

    caminho_fisico = None
    sucesso = False

    try:
        data, arquivo = _ler_dados_produto()

        caminho_publico, caminho_fisico = _salvar_foto(arquivo)
        if caminho_publico:
            data["foto"] = caminho_publico

        produto = produto_services.criar_produto(
            data,
            session["id_usuario"],
        )

        sucesso = True
        return jsonify(produto), 201

    except produto_services.ProdutoDuplicado as e:
        return jsonify({"erro": str(e)}), 409
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403
    except (psycopg.Error, RuntimeError):
        current_app.logger.exception("Falha ao cadastrar produto.")
        return jsonify({
            "erro": "Não foi possível cadastrar o produto."
        }), 503
    finally:
        if not sucesso:
            _remover_arquivo(caminho_fisico)


def atualizar_produto_controller(id_produto):
    if not _id_usuario_autenticado():
        return jsonify({"erro": "Autenticação necessária."}), 401

    caminho_fisico = None
    sucesso = False

    try:
        data, arquivo = _ler_dados_produto()

        caminho_publico, caminho_fisico = _salvar_foto(arquivo)
        if caminho_publico:
            data["foto"] = caminho_publico

        produto = produto_services.atualizar_produto(
            id_produto,
            data,
            session["id_usuario"],
        )

        sucesso = True
        return jsonify(produto), 200

    except produto_services.ProdutoDuplicado as e:
        return jsonify({"erro": str(e)}), 409
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403
    except produto_services.ProdutoNaoEncontrado as e:
        return jsonify({"erro": str(e)}), 404
    except (psycopg.Error, RuntimeError):
        current_app.logger.exception("Falha ao atualizar produto.")
        return jsonify({
            "erro": "Não foi possível atualizar o produto."
        }), 503
    finally:
        if not sucesso:
            _remover_arquivo(caminho_fisico)


def excluir_produto_controller(id_produto):
    if not _id_usuario_autenticado():
        return jsonify({"erro": "Autenticação necessária."}), 401

    try:
        produto_services.excluir_produto(
            id_produto,
            session["id_usuario"],
        )
        return "", 204
    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403
    except produto_services.ProdutoNaoEncontrado as e:
        return jsonify({"erro": str(e)}), 404
    except produto_services.ProdutoEmUso as e:
        return jsonify({"erro": str(e)}), 409
    except (psycopg.Error, RuntimeError):
        current_app.logger.exception("Falha ao excluir produto.")
        return jsonify({
            "erro": "Não foi possível excluir o produto."
        }), 503
