"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Pencil, Trash2 } from "lucide-react";
import { api, urlFotoProduto } from "@/services/api";

type Receita = {
  id_ingrediente: number;
  nome: string;
  quantidade_necessaria: string;
  unidade_medida: string;
};

type Produto = {
  id_produto: number;
  nome: string;
  tamanho: string;
  preco: string; // o backend manda como texto: "49.90"
  disponivel: boolean;
  foto?: string | null;
  categoria: { id_categoria: number; nome: string };
  ingredientes: Receita[];
};

const moeda = (valor: string) =>
  Number(valor).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

const quantidade = (valor: string) => Number(valor).toLocaleString("pt-BR");

export default function ProdutosPage() {
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);
  const [excluindoId, setExcluindoId] = useState<number | null>(null);

  useEffect(() => {
    api
      .listarProdutos()
      .then((r) => setProdutos(r.produtos ?? []))
      .catch((e) =>
        setErro(e instanceof Error ? e.message : "Não foi possível carregar os produtos."),
      )
      .finally(() => setCarregando(false));
  }, []);

  async function excluir(p: Produto) {
    const confirmou = window.confirm(
      `Excluir "${p.nome} (${p.tamanho})"? Essa ação não pode ser desfeita.`,
    );
    if (!confirmou) return;

    setErro(null);
    setExcluindoId(p.id_produto);
    try {
      await api.excluirProduto(p.id_produto);
      setProdutos((atuais) => atuais.filter((x) => x.id_produto !== p.id_produto));
    } catch (e) {
      // Ex.: produto já usado em pedidos -> o backend explica o motivo.
      setErro(e instanceof Error ? e.message : "Não foi possível excluir o produto.");
    } finally {
      setExcluindoId(null);
    }
  }

  return (
    <>
      <header className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div className="flex-1">
          <p className="text-sm font-medium text-basil">Cardápio</p>
          <h1 className="mt-1 text-4xl font-semibold leading-tight text-char">
            Produtos
          </h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Gerencie os produtos do cardápio.
          </p>
        </div>

        <Link
          href="/funcionario/produtos/novo"
          className="rounded-lg bg-brick px-4 py-2.5 text-sm font-semibold text-background transition hover:bg-brick-dark"
        >
          + Novo produto
        </Link>
      </header>

      {erro && (
        <p role="alert" className="mb-4 text-sm text-brick">
          {erro}
        </p>
      )}

      <div className="overflow-hidden rounded-2xl border border-border bg-background shadow-sm">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="border-b border-border text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              <th className="px-5 py-3">Imagem</th>
              <th className="px-5 py-3">Produto</th>
              <th className="px-5 py-3">Preço</th>
              <th className="px-5 py-3">Categoria</th>
              <th className="px-5 py-3">Ingredientes</th>
              <th className="px-5 py-3">Ações</th>
            </tr>
          </thead>
          <tbody>
            {produtos.map((p) => (
              <tr key={p.id_produto} className="border-b border-border last:border-0">
                <td className="px-5 py-3">
                  <img
                    src={urlFotoProduto(p.foto) ?? "/produtos/sem-foto.svg"}
                    alt={p.nome}
                    className="h-10 w-14 rounded-md border border-border object-cover"
                    onError={(e) => {
                      e.currentTarget.onerror = null;
                      e.currentTarget.src = "/produtos/sem-foto.svg";
                    }}
                  />
                </td>
                <td className="px-5 py-3 text-char">
                  <p className="font-medium">{p.nome}</p>
                  <p className="text-xs text-muted-foreground">
                    {p.tamanho}
                    {!p.disponivel && " · Indisponível"}
                  </p>
                </td>
                <td className="whitespace-nowrap px-5 py-3 font-medium text-brick">
                  {moeda(p.preco)}
                </td>
                <td className="px-5 py-3 text-char">{p.categoria.nome}</td>
                <td className="px-5 py-3 text-char">
                  {p.ingredientes.length === 0
                    ? "—"
                    : p.ingredientes
                        .map(
                          (i) =>
                            `${i.nome} (${quantidade(i.quantidade_necessaria)} ${i.unidade_medida})`,
                        )
                        .join(", ")}
                </td>
                <td className="px-5 py-3">
                  <div className="flex items-center gap-3">
                    <Link
                      href={`/funcionario/produtos/${p.id_produto}/editar`}
                      title="Editar"
                      className="flex h-8 w-8 items-center justify-center rounded-lg text-muted-foreground transition hover:bg-muted hover:text-brick"
                    >
                      <Pencil size={16} />
                    </Link>

                    <button
                      type="button"
                      onClick={() => excluir(p)}
                      disabled={excluindoId === p.id_produto}
                      title="Excluir"
                      className="flex h-8 w-8 items-center justify-center rounded-lg text-muted-foreground transition hover:bg-muted hover:text-brick disabled:opacity-40"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {carregando && (
          <p className="p-6 text-sm text-muted-foreground">Carregando produtos...</p>
        )}

        {!carregando && !erro && produtos.length === 0 && (
          <div className="p-12 text-center">
            <p className="font-display text-xl font-semibold text-char">
              Nenhum produto cadastrado
            </p>
            <p className="mt-2 text-sm text-muted-foreground">
              Adicione o primeiro produto ao cardápio.
            </p>
          </div>
        )}
      </div>
    </>
  );
}