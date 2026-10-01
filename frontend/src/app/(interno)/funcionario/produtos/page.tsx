"use client";

import Link from "next/link";
import { Pencil, Trash2 } from "lucide-react";
import { useProdutos } from "../../../../hooks/use-produtos";

export default function ProdutosPage() {
  const { produtos, removerProduto } = useProdutos();

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

      <div className="overflow-hidden rounded-2xl border border-border bg-background shadow-sm">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="border-b border-border text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              <th className="px-5 py-3">Imagem</th>
              <th className="px-5 py-3">Preço</th>
              <th className="px-5 py-3">Categoria</th>
              <th className="px-5 py-3">Descrição</th>
              <th className="px-5 py-3">Ações</th>
            </tr>
          </thead>
          <tbody>
            {produtos.map((produto) => (
              <tr key={produto.id} className="border-b border-border last:border-0">
                <td className="px-5 py-3">
                  <img
                    src="/produtos/image.png"
                    alt={produto.nome}
                    className="h-10 w-14 rounded-md object-cover"
                  />
                </td>
                <td className="px-5 py-3 font-medium text-brick">{produto.preco}</td>
                <td className="px-5 py-3 text-char">{produto.categoria}</td>
                <td className="px-5 py-3 text-char">{produto.nome}</td>
                <td className="px-5 py-3">
                  <div className="flex items-center gap-3">
                    <Link
                      href={`/funcionario/produtos/${produto.id}/editar`}
                      title="Editar"
                      className="flex h-8 w-8 items-center justify-center rounded-lg text-muted-foreground transition hover:bg-muted hover:text-brick"
                    >
                      <Pencil size={16} />
                    </Link>

                    <button
                      onClick={() => removerProduto(produto.id)}
                      title="Excluir"
                      className="flex h-8 w-8 items-center justify-center rounded-lg text-muted-foreground transition hover:bg-muted hover:text-brick"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {produtos.length === 0 && (
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