from app.error_logging import log_internal_error

import json

import psycopg
from flask import request, jsonify, session
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

from app.services import produto_services
from app.services.permissoes import exigir_funcionario_ativo
from app.image_storage import save_product_image, get_image_storage


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
    """Valida e salva a imagem; retorna o caminho público e a referência de limpeza."""
    if arquivo and arquivo.filename:
        # Autoriza antes de gravar arquivos ou chamar qualquer serviço externo.
        exigir_funcionario_ativo(session['id_usuario'])
    return save_product_image(arquivo)


def _remover_arquivo(caminho):
    if caminho:
        try:
            get_image_storage().delete(caminho)
        except (OSError, ValueError, RuntimeError):
            log_internal_error('Não foi possível remover um arquivo de upload.')


def _id_usuario_autenticado():
    id_usuario = session.get("id_usuario")
    return type(id_usuario) is int and id_usuario > 0


def listar_produtos_controller():
    try:
        return jsonify({
            "produtos": produto_services.listar_produtos()
        }), 200
    except (psycopg.Error, RuntimeError):
        log_internal_error("Falha ao listar produtos.")
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
        log_internal_error("Falha ao cadastrar produto.")
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
        log_internal_error("Falha ao atualizar produto.")
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
        log_internal_error("Falha ao excluir produto.")
        return jsonify({
            "erro": "Não foi possível excluir o produto."
        }), 503
