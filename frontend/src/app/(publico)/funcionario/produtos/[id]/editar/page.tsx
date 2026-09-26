"use client";

import Link from "next/link";
import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useProdutos } from "../../../../../../hooks/use-produtos";

const NOVA_CATEGORIA = "__nova__";

export default function EditarProdutoPage() {
  const router = useRouter();
  const { id } = useParams<{ id: string }>();
  const { produtos, categorias, atualizarProduto, adicionarCategoria } =
    useProdutos();

  const produto = produtos.find((p) => p.id === Number(id));

  const [nome, setNome] = useState(produto?.nome ?? "");
  const [descricao, setDescricao] = useState(produto?.descricao ?? "");
  const [categoria, setCategoria] = useState(produto?.categoria ?? categorias[0] ?? "");
  const [preco, setPreco] = useState(produto?.preco ?? "");
  const [imagemUrl, setImagemUrl] = useState(produto?.imagemUrl ?? "");

  const [mostrarNovaCategoria, setMostrarNovaCategoria] = useState(false);
  const [nomeNovaCategoria, setNomeNovaCategoria] = useState("");

  if (!produto) {
    return (
      <div className="rounded-2xl border border-dashed border-border p-12 text-center">
        <p className="font-display text-xl font-semibold text-char">
          Produto não encontrado
        </p>
        <Link
          href="/funcionario/produtos"
          className="mt-4 inline-block text-sm font-medium text-brick hover:underline"
        >
          Voltar para produtos
        </Link>
      </div>
    );
  }

    const handleSelectCategoria = (valor: string) => {
    if (valor === NOVA_CATEGORIA) {
        setMostrarNovaCategoria(true);
        return;
    }
    setCategoria(valor);
    };

    const handleAdicionarCategoria = () => {
    const nomeFormatado = nomeNovaCategoria.trim();
    if (!nomeFormatado) return;

    adicionarCategoria(nomeFormatado);
    setCategoria(nomeFormatado);
    setNomeNovaCategoria("");
    setMostrarNovaCategoria(false);
    };

    const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    atualizarProduto(produto.id, { nome, descricao, categoria, preco, imagemUrl });

    router.push("/funcionario/produtos");
    };

  return (
    <div className="flex justify-center">
      <div className="w-full max-w-2xl">
        <header className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
          <div className="flex-1">
            <p className="text-sm font-medium text-basil">Cardápio</p>
            <h1 className="mt-1 text-4xl font-semibold leading-tight text-char">
              Editar produto
            </h1>
            <p className="mt-2 text-sm text-muted-foreground">
              Atualize as informações deste item do cardápio.
            </p>
          </div>

          <Link
            href="/funcionario/produtos"
            className="text-sm font-medium text-muted-foreground transition hover:text-brick"
          >
            Voltar
          </Link>
        </header>

        <form
          onSubmit={handleSubmit}
          className="rounded-2xl border border-border bg-background p-6 shadow-sm"
        >
          <div className="grid gap-5 sm:grid-cols-2">
            <Campo label="Nome do produto" htmlFor="nome" className="sm:col-span-2">
              <input
                id="nome"
                value={nome}
                onChange={(e) => setNome(e.target.value)}
                required
                className="w-full rounded-lg border border-border bg-muted/40 px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick"
              />
            </Campo>

            <Campo label="Categoria" htmlFor="categoria">
              <select
                id="categoria"
                value={categoria}
                onChange={(e) => handleSelectCategoria(e.target.value)}
                className="w-full rounded-lg border border-border bg-muted/40 px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick"
              >
                {categorias.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
                <option value={NOVA_CATEGORIA}>+ Nova categoria</option>
              </select>

              {mostrarNovaCategoria && (
                <div className="mt-2 flex gap-2">
                  <input
                    autoFocus
                    value={nomeNovaCategoria}
                    onChange={(e) => setNomeNovaCategoria(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") {
                        e.preventDefault();
                        handleAdicionarCategoria();
                      }
                    }}
                    placeholder="Nome da categoria"
                    className="w-full rounded-lg border border-border bg-muted/40 px-3 py-2 text-sm text-char outline-none transition focus:border-brick"
                  />
                  <button
                    type="button"
                    onClick={handleAdicionarCategoria}
                    className="whitespace-nowrap rounded-lg bg-brick px-3 py-2 text-sm font-semibold text-background transition hover:bg-brick-dark"
                  >
                    Adicionar
                  </button>
                </div>
              )}
            </Campo>

            <Campo label="Preço" htmlFor="preco">
              <input
                id="preco"
                value={preco}
                onChange={(e) => setPreco(e.target.value)}
                required
                className="w-full rounded-lg border border-border bg-muted/40 px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick"
              />
            </Campo>

            <Campo label="Descrição" htmlFor="descricao" className="sm:col-span-2">
              <textarea
                id="descricao"
                value={descricao}
                onChange={(e) => setDescricao(e.target.value)}
                rows={3}
                className="w-full resize-none rounded-lg border border-border bg-muted/40 px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick"
              />
            </Campo>

            <Campo label="URL da imagem" htmlFor="imagem" className="sm:col-span-2">
              <input
                id="imagem"
                value={imagemUrl}
                onChange={(e) => setImagemUrl(e.target.value)}
                className="w-full rounded-lg border border-border bg-muted/40 px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick"
              />
            </Campo>
          </div>

          <div className="mt-6 flex items-center justify-end gap-3 border-t border-border pt-5">
            <Link
              href="/funcionario/produtos"
              className="rounded-lg px-4 py-2.5 text-sm font-semibold text-muted-foreground transition hover:bg-muted"
            >
              Cancelar
            </Link>

            <button
              type="submit"
              className="rounded-lg bg-brick px-4 py-2.5 text-sm font-semibold text-background transition hover:bg-brick-dark"
            >
              Salvar alterações
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function Campo({
  label,
  htmlFor,
  children,
  className = "",
}: {
  label: string;
  htmlFor: string;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={className}>
      <label
        htmlFor={htmlFor}
        className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-muted-foreground"
      >
        {label}
      </label>
      {children}
    </div>
  );
}