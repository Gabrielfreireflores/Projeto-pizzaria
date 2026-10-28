"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { Navbar } from "@/components/shared/navbar";
import { useAuth, ehFuncionario } from "@/hooks/use-auth";
import { api } from "@/lib/api";

interface Item {
  produto: string;
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
  itens: Item[];
}

export default function MeusPedidosPage() {
  const { usuario, carregando, logout } = useAuth();
  const [pedidos, setPedidos] = useState<Pedido[]>([]);
  const [numero, setNumero] = useState("");
  const [erro, setErro] = useState("");
  const [loading, setLoading] = useState(true);
  const carregar = useCallback(async () => {
    try {
      setPedidos(await api<Pedido[]>("/api/v1/meus-pedidos"));
      setErro("");
    } catch (e) { setErro(e instanceof Error ? e.message : "Não foi possível consultar seus pedidos."); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => {
    if (!usuario || ehFuncionario(usuario)) return;
    carregar();
    const timer = setInterval(() => { if (!document.hidden) carregar(); }, 15000);
    return () => clearInterval(timer);
  }, [usuario, carregar]);

  const lista = pedidos.filter(p => !numero.trim() || String(p.id_pedido) === numero.replace(/\D/g, ""));
  return <main>
    <Navbar />
    <div className="mx-auto max-w-3xl px-4 py-10 sm:px-6">
      <div className="flex items-center justify-between gap-4">
        <h1 className="text-3xl font-semibold text-char">Meus pedidos</h1>
        {usuario && <button onClick={() => { logout(); setPedidos([]); }} className="text-sm text-brick underline">Sair da conta</button>}
      </div>
      {carregando ? <p role="status" className="mt-6">Verificando sua conta...</p> : !usuario ? (
        <div className="mt-6 rounded-xl border border-border p-6">
          <p>Entre para consultar os pedidos feitos com sua conta.</p>
          <p className="mt-2 text-sm text-muted-foreground">Pedidos feitos como convidado não são vinculados automaticamente a uma conta.</p>
          <div className="mt-5 flex gap-4"><Link href="/login" className="text-brick underline">Entrar</Link><Link href="/cadastro" className="text-brick underline">Criar conta</Link></div>
        </div>
      ) : ehFuncionario(usuario) ? <p className="mt-6">Use a <Link href="/funcionario" className="text-brick underline">área do funcionário</Link> para gerenciar os pedidos.</p> : (
        <>
          <p className="mt-2 text-sm text-muted-foreground">Você vê apenas os pedidos da sua conta. O status atualiza a cada 15 segundos.</p>
          <label className="mt-6 block text-sm font-semibold">Número do pedido
            <input type="search" inputMode="numeric" placeholder="Ex.: #123" value={numero} onChange={e => setNumero(e.target.value)} className="mt-2 w-full rounded-lg border border-border bg-background p-3 font-normal" />
          </label>
          {erro && <p role="alert" className="mt-4 text-brick">{erro} <button onClick={carregar} className="underline">Tentar novamente</button></p>}
          {loading ? <p role="status" className="mt-6">Carregando pedidos...</p> : !lista.length && <p className="mt-6 text-muted-foreground">Nenhum pedido encontrado nesta conta.</p>}
          <div className="mt-6 space-y-4">
            {lista.map(p => <article key={p.id_pedido} className="rounded-xl border border-border bg-background p-5">
              <div className="flex flex-wrap items-center justify-between gap-3"><h2 className="font-display text-xl font-semibold">Pedido #{p.id_pedido}</h2><span className="rounded-full bg-basil/10 px-3 py-1 text-sm font-semibold text-basil">{p.status}</span></div>
              <p className="mt-2 text-xs text-muted-foreground">{new Date(p.data_hora_pedido).toLocaleString("pt-BR")} · {p.tipo_entrega === "retirada" ? "Retirada no local" : "Entrega"}</p>
              <ul className="mt-4 space-y-2 text-sm">{p.itens.map((i, n) => <li key={n}>
                {i.quantidade}x {i.produto}
                {i.bordas?.map(b => <span key={b.produto} className="block text-muted-foreground">{b.quantidade}x {b.produto}</span>)}
                {i.observacao && <span className="block text-xs text-muted-foreground">{i.observacao}</span>}
              </li>)}</ul>
              <p className="mt-4 border-t border-border pt-3 font-semibold">Total: {Number(p.valor_total).toLocaleString("pt-BR", { style: "currency", currency: "BRL" })}</p>
            </article>)}
          </div>
        </>
      )}
    </div>
  </main>;
}
