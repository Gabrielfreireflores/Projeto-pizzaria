"use client";

import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { Navbar } from "@/components/shared/navbar";
import { useAuth, ehCliente } from "@/hooks/use-auth";
import { api } from "@/lib/api";

interface Item {
  nome: string;
  tamanho: string;
  quantidade: number;
  observacao: string | null;
  bordas: { produto: string; quantidade: number }[];
}
interface Pedido {
  id_pedido: number;
  status: string;
  valor_total: string;
  data_hora_pedido: string;
  tipo_entrega: string;
  forma_pagamento: string;
  taxa_entrega: string;
  endereco: { logradouro: string; numero: string; bairro: string; cidade: string; uf: string; complemento: string | null } | null;
  itens: Item[];
}

export default function MeusPedidosPage() {
  const { usuario, carregando } = useAuth();
  const router = useRouter();
  const [pedidos, setPedidos] = useState<Pedido[]>([]);
  const [numero, setNumero] = useState("");
  const [erro, setErro] = useState("");
  const [loading, setLoading] = useState(true);
  const carregar = useCallback(async () => {
    setLoading(true);
    try {
      setPedidos(await api<Pedido[]>("/api/v1/meus-pedidos"));
      setErro("");
    } catch (e) { setErro(e instanceof Error ? e.message : "Não foi possível consultar seus pedidos."); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => {
    if (carregando) return;
    if (!ehCliente(usuario)) { router.replace("/login?next=/meus-pedidos"); return; }
    carregar();
  }, [usuario, carregando, carregar, router]);

  if (carregando || !ehCliente(usuario)) return <main><Navbar /><p role="status" className="p-8">Verificando sua conta...</p></main>;

  const lista = pedidos.filter(p => !numero.trim() || String(p.id_pedido) === numero.replace(/\D/g, ""));
  return <main>
    <Navbar />
    <div className="mx-auto max-w-3xl px-4 py-10 sm:px-6">
      <div className="flex items-center justify-between gap-4">
        <h1 className="text-3xl font-semibold text-char">Meus pedidos</h1>
        <button onClick={carregar} disabled={loading} className="rounded-lg border border-border px-4 py-2 text-sm text-brick disabled:opacity-50">Atualizar</button>
      </div>
      <p className="mt-2 text-sm text-muted-foreground">Você vê apenas os pedidos da sua conta. Use Atualizar para consultar o status.</p>
          <label className="mt-6 block text-sm font-semibold">Número do pedido
            <input type="search" inputMode="numeric" placeholder="Ex.: #123" value={numero} onChange={e => setNumero(e.target.value)} className="mt-2 w-full rounded-lg border border-border bg-background p-3 font-normal" />
          </label>
          {erro && <p role="alert" className="mt-4 text-brick">{erro} <button onClick={carregar} className="underline">Tentar novamente</button></p>}
          {loading ? <p role="status" className="mt-6">Carregando pedidos...</p> : !erro && !lista.length && <p className="mt-6 text-muted-foreground">{numero ? "Nenhum pedido encontrado." : "Você ainda não fez pedidos"}</p>}
          <div className="mt-6 space-y-4">
            {lista.map(p => <article key={p.id_pedido} className="rounded-xl border border-border bg-background p-5">
              <div className="flex flex-wrap items-center justify-between gap-3"><h2 className="font-display text-xl font-semibold">Pedido #{p.id_pedido}</h2><span className={`rounded-full px-3 py-1 text-sm font-semibold ${p.status === "Recebido" ? "bg-brick/10 text-brick" : p.status === "Em preparação" ? "bg-crust/20 text-char" : p.status === "Saiu para entrega" ? "bg-basil/10 text-basil" : "bg-muted text-muted-foreground"}`}>{p.status}</span></div>
              <p className="mt-2 text-xs text-muted-foreground">{new Date(p.data_hora_pedido).toLocaleString("pt-BR")} · {p.tipo_entrega === "retirada" ? "Retirada no local" : "Entrega"}</p>
              <ul className="mt-4 space-y-2 text-sm">{p.itens.map((i, n) => <li key={n}>
                {i.quantidade}x {i.nome} · {i.tamanho}
                {i.bordas?.map(b => <span key={b.produto} className="block text-muted-foreground">{b.quantidade}x {b.produto}</span>)}
                {i.observacao && <span className="block text-xs text-muted-foreground">{i.observacao}</span>}
              </li>)}</ul>
              {p.endereco && <p className="mt-4 text-sm">{p.endereco.logradouro}, {p.endereco.numero}{p.endereco.complemento ? ` · ${p.endereco.complemento}` : ""} · {p.endereco.bairro} · {p.endereco.cidade}/{p.endereco.uf}</p>}
              <p className="mt-2 text-sm">Pagamento: {p.forma_pagamento}</p>
              <p className="mt-1 text-xs text-muted-foreground">Taxa de entrega: {Number(p.taxa_entrega).toLocaleString("pt-BR", { style: "currency", currency: "BRL" })}</p>
              <p className="mt-4 border-t border-border pt-3 font-semibold">Total: {Number(p.valor_total).toLocaleString("pt-BR", { style: "currency", currency: "BRL" })}</p>
            </article>)}
          </div>
    </div>
  </main>;
}
