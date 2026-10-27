"use client";

import { useCallback, useEffect, useState } from "react";
import { api } from "@/services/api";

type Pedido = {
  id: number;
  cliente: string;
  itens: string[];
  total: number;
  status: string; // texto como veio do backend
  criadoEm: string | null;
};

type Etapa = {
  rotulo: string;
  estilo: string;
  acao?: { texto: string; executar: (id: number) => Promise<unknown> };
};

const semAcento = (t: string) =>
  t.normalize("NFD").replace(/[\u0300-\u036f]/g, "").trim().toLowerCase();

// Etapas do fluxo. A chave é o status sem acento e em minúsculas.
const ETAPAS: Record<string, Etapa> = {
  recebido: {
    rotulo: "Recebido",
    estilo: "bg-brick/10 text-brick",
    acao: { texto: "Aceitar pedido", executar: (id) => api.aceitarPedido(id) },
  },
  "em preparacao": {
    rotulo: "Em preparação",
    estilo: "bg-crust/20 text-char",
    acao: {
      texto: "Enviar para entrega",
      executar: (id) => api.alterarStatusPedido(id, "Saiu para entrega"),
    },
  },
  "saiu para entrega": {
    rotulo: "Saiu para entrega",
    estilo: "bg-basil/10 text-basil",
    acao: {
      texto: "Marcar como entregue",
      executar: (id) => api.alterarStatusPedido(id, "Entregue"),
    },
  },
  entregue: {
    rotulo: "Entregue",
    estilo: "bg-muted text-muted-foreground",
  },
  cancelado: {
    rotulo: "Cancelado",
    estilo: "bg-muted text-muted-foreground",
  },
};

const moeda = (valor: number) =>
  valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

const hora = (iso: string | null) => {
  if (!iso) return "";
  const d = new Date(iso);
  return isNaN(d.getTime())
    ? ""
    : d.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
};

// ---- Tradução do que a API devolve para o que a tela usa ----
// Se os cards aparecerem com "—" ou "Produto #?", compare o JSON de
// http://localhost:3000/api/v1/pedidos (logado) com estas duas funções.
function textoItem(i: any): string {
  const produto = typeof i.produto === "string" ? i.produto : i.produto?.nome;
  const nome = i.nome ?? produto ?? i.nome_produto ?? `Produto #${i.id_produto ?? "?"}`;
  const obs = i.observacao;
  return `${i.quantidade ?? 1}x ${nome}${obs ? ` — ${obs}` : ""}`;
}

function paraPedido(r: any): Pedido {
  const brutos: any[] = r.itens ?? r.items ?? [];
  return {
    id: Number(r.id_pedido ?? r.id),
    cliente: String(r.contato?.nome ?? r.cliente?.nome ?? r.cliente ?? r.nome_cliente ?? "—"),
    status: String(r.status?.nome ?? r.status ?? r.nome_status ?? ""),
    total: Number(r.valor_total ?? r.total ?? 0),
    criadoEm: r.data_hora_pedido ?? null,
    itens: brutos.map(textoItem),
  };
}

export default function FuncionarioPage() {
  const [pedidos, setPedidos] = useState<Pedido[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);
  const [erroAcao, setErroAcao] = useState<string | null>(null);
  const [agindoId, setAgindoId] = useState<number | null>(null);
  const [mostrarEntregues, setMostrarEntregues] = useState(false);

  const carregar = useCallback(async () => {
    try {
      const r = await api.listarPedidos();
      const lista: any[] = Array.isArray(r) ? r : (r.pedidos ?? []);
      setPedidos(lista.map(paraPedido));
      setErro(null);
    } catch (e) {
      setErro(e instanceof Error ? e.message : "Não foi possível carregar os pedidos.");
    } finally {
      setCarregando(false);
    }
  }, []);

  // Carrega ao abrir e atualiza sozinho a cada 15 segundos (novos pedidos aparecem).
  useEffect(() => {
    carregar();
    const timer = setInterval(carregar, 15000);
    return () => clearInterval(timer);
  }, [carregar]);

  async function avancar(p: Pedido, etapa: Etapa) {
    if (!etapa.acao) return;
    setErroAcao(null);
    setAgindoId(p.id);
    try {
      await etapa.acao.executar(p.id);
    } catch (e) {
      setErroAcao(e instanceof Error ? e.message : "Não foi possível atualizar o pedido.");
    } finally {
      await carregar();
      setAgindoId(null);
    }
  }

  const chave = (p: Pedido) => semAcento(p.status);
  const visiveis = pedidos
    .filter((p) => mostrarEntregues || !["entregue", "cancelado"].includes(chave(p)))
    .sort((a, b) => a.id - b.id);
  const novos = pedidos.filter((p) => chave(p) === "recebido").length;
  const emPreparo = pedidos.filter((p) => chave(p) === "em preparacao").length;

  return (
    <>
      <header className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <p className="text-sm font-medium text-basil">Cozinha</p>
          <h1 className="mt-1 text-4xl font-semibold leading-tight text-char">Pedidos</h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Gerencie os pedidos recebidos pela pizzaria. A lista atualiza sozinha.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <span className="rounded-full bg-brick/10 px-4 py-2 text-sm font-medium text-brick">
            {novos} {novos === 1 ? "novo" : "novos"}
          </span>
          <span className="rounded-full bg-basil/10 px-4 py-2 text-sm font-medium text-basil">
            {emPreparo} em preparação
          </span>
        </div>
      </header>

      <label className="mb-5 flex items-center gap-2 text-sm text-char">
        <input
          type="checkbox"
          checked={mostrarEntregues}
          onChange={(e) => setMostrarEntregues(e.target.checked)}
        />
        Mostrar entregues e cancelados
      </label>

      {erro && (
        <p role="alert" className="mb-4 text-sm text-brick">
          {erro}
        </p>
      )}
      {erroAcao && (
        <p role="alert" className="mb-4 text-sm text-brick">
          {erroAcao}
        </p>
      )}

      <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
        {visiveis.map((pedido) => {
          const etapa = ETAPAS[chave(pedido)];
          return (
            <article
              key={pedido.id}
              className="rounded-2xl border border-border bg-background p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="font-display text-xl font-semibold text-char">
                    Pedido #{String(pedido.id).padStart(3, "0")}
                  </p>
                  <p className="mt-1 text-sm text-muted-foreground">
                    Cliente: <span className="font-medium text-char">{pedido.cliente}</span>
                  </p>
                  {hora(pedido.criadoEm) && (
                    <p className="text-xs text-muted-foreground">
                      Recebido às {hora(pedido.criadoEm)}
                    </p>
                  )}
                </div>

                <span
                  className={`whitespace-nowrap rounded-full px-3 py-1 text-xs font-semibold ${
                    etapa?.estilo ?? "bg-muted text-muted-foreground"
                  }`}
                >
                  {etapa?.rotulo ?? pedido.status}
                </span>
              </div>

              <div className="mt-5">
                <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                  Itens
                </p>
                <div className="space-y-1">
                  {pedido.itens.length === 0 ? (
                    <p className="text-sm text-muted-foreground">—</p>
                  ) : (
                    pedido.itens.map((item, i) => (
                      <p key={i} className="text-sm text-char">
                        {item}
                      </p>
                    ))
                  )}
                </div>
              </div>

              <div className="mt-5 flex items-center justify-between border-t border-border pt-4">
                <span className="text-sm font-medium text-muted-foreground">Total</span>
                <span className="font-display text-xl font-semibold text-brick">
                  {moeda(pedido.total)}
                </span>
              </div>

              {etapa?.acao && (
                <button
                  type="button"
                  onClick={() => avancar(pedido, etapa)}
                  disabled={agindoId === pedido.id}
                  className="mt-4 w-full rounded-lg bg-brick px-4 py-2.5 text-sm font-semibold text-background transition hover:bg-brick-dark disabled:opacity-60"
                >
                  {agindoId === pedido.id ? "Atualizando..." : etapa.acao.texto}
                </button>
              )}
            </article>
          );
        })}
      </div>

      {carregando && <p className="text-sm text-muted-foreground">Carregando pedidos...</p>}

      {!carregando && !erro && visiveis.length === 0 && (
        <div className="rounded-2xl border border-dashed border-border p-12 text-center">
          <p className="font-display text-xl font-semibold text-char">
            Nenhum pedido no momento
          </p>
          <p className="mt-2 text-sm text-muted-foreground">
            Quando um cliente realizar um pedido, ele aparecerá aqui.
          </p>
        </div>
      )}
    </>
  );
}