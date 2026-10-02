"use client";

import Link from "next/link";
import { useState } from "react";

type PedidoStatus = "Em produção" | "Pronto" | "Entregue";

interface Pedido {
  id: number;
  cliente: string;
  itens: string[];
  total: string;
  status: PedidoStatus;
}

const pedidosIniciais: Pedido[] = [
  {
    id: 1,
    cliente: "André",
    itens: ["1x Pizza Margherita", "1x Coca-Cola 350 mL"],
    total: "R$ 42,00",
    status: "Em produção",
  },
  {
    id: 2,
    cliente: "Mariana",
    itens: ["1x Pizza Calabresa", "1x Pizza Quatro Queijos"],
    total: "R$ 78,00",
    status: "Em produção",
  },
  {
    id: 3,
    cliente: "Carlos",
    itens: ["1x Pizza Portuguesa", "1x Guaraná 1 L"],
    total: "R$ 55,00",
    status: "Pronto",
  },
];

export default function FuncionarioPage() {
  const [pedidos, setPedidos] = useState(pedidosIniciais);

  function alterarStatus(id: number) {
    setPedidos((pedidosAtuais) =>
      pedidosAtuais.map((pedido) => {
        if (pedido.id !== id) return pedido;

        const proximoStatus: Record<PedidoStatus, PedidoStatus> = {
          "Em produção": "Pronto",
          Pronto: "Entregue",
          Entregue: "Entregue",
        };

        return {
          ...pedido,
          status: proximoStatus[pedido.status],
        };
      }),
    );
  }

  return (
    <main className="min-h-screen bg-background text-char">
      <div className="flex min-h-screen">

        {/* CONTEÚDO */}
        <section className="flex-1 px-6 py-8 sm:px-8 lg:px-12">

          {/* Cabeçalho */}
          <header className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
            <div>
              <p className="text-sm font-medium text-basil">
                Cozinha
              </p>

              <h1 className="mt-1 text-4xl font-semibold leading-tight text-char">
                Pedidos em produção
              </h1>

              <p className="mt-2 text-sm text-muted-foreground">
                Gerencie os pedidos recebidos pela pizzaria.
              </p>
            </div>

            <div className="rounded-full bg-basil/10 px-4 py-2 text-sm font-medium text-basil">
              {pedidos.filter((pedido) => pedido.status === "Em produção").length}{" "}
              pedidos em produção
            </div>
          </header>

          {/* PEDIDOS */}
          <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">

            {pedidos.map((pedido) => (
              <article
                key={pedido.id}
                className="rounded-2xl border border-border bg-background p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
              >

                {/* Cabeçalho do pedido */}
                <div className="flex items-start justify-between gap-4">

                  <div>
                    <p className="font-display text-xl font-semibold text-char">
                      Pedido #{String(pedido.id).padStart(3, "0")}
                    </p>

                    <p className="mt-1 text-sm text-muted-foreground">
                      Cliente:{" "}
                      <span className="font-medium text-char">
                        {pedido.cliente}
                      </span>
                    </p>
                  </div>

                  <Status status={pedido.status} />

                </div>

                {/* Itens */}
                <div className="mt-5">
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                    Itens
                  </p>

                  <div className="space-y-1">
                    {pedido.itens.map((item) => (
                      <p
                        key={item}
                        className="text-sm text-char"
                      >
                        {item}
                      </p>
                    ))}
                  </div>
                </div>

                {/* Total */}
                <div className="mt-5 flex items-center justify-between border-t border-border pt-4">

                  <span className="text-sm font-medium text-muted-foreground">
                    Total
                  </span>

                  <span className="font-display text-xl font-semibold text-brick">
                    {pedido.total}
                  </span>

                </div>

                {/* Botão */}
                {pedido.status !== "Entregue" && (
                  <button
                    onClick={() => alterarStatus(pedido.id)}
                    className="mt-4 w-full rounded-lg bg-brick px-4 py-2.5 text-sm font-semibold text-background transition hover:bg-brick-dark"
                  >
                    {pedido.status === "Em produção"
                      ? "Marcar como pronto"
                      : "Marcar como entregue"}
                  </button>
                )}

              </article>
            ))}

          </div>

          {/* Estado vazio */}
          {pedidos.length === 0 && (
            <div className="rounded-2xl border border-dashed border-border p-12 text-center">
              <p className="font-display text-xl font-semibold text-char">
                Nenhum pedido no momento
              </p>

              <p className="mt-2 text-sm text-muted-foreground">
                Quando um cliente realizar um pedido, ele aparecerá aqui.
              </p>
            </div>
          )}

        </section>
      </div>
    </main>
  );
}

function Status({ status }: { status: PedidoStatus }) {
  const estilos: Record<PedidoStatus, string> = {
    "Em produção": "bg-crust/20 text-char",
    Pronto: "bg-basil/10 text-basil",
    Entregue: "bg-muted text-muted-foreground",
  };


  return (
    <span
      className={`whitespace-nowrap rounded-full px-3 py-1 text-xs font-semibold ${estilos[status]}`}
    >
      {status}
    </span>
  );
}