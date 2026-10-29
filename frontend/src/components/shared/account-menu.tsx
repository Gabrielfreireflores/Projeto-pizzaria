"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { User } from "lucide-react";
import { ehCliente, ehFuncionario, useAuth } from "@/hooks/use-auth";

export function AccountMenu() {
  const { usuario, carregando, logout } = useAuth();
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [saindo, setSaindo] = useState(false);
  const [erro, setErro] = useState("");
  const container = useRef<HTMLDivElement>(null);
  const trigger = useRef<HTMLButtonElement>(null);
  const menu = useRef<HTMLDivElement>(null);

  useEffect(() => { setOpen(false); }, [pathname]);

  useEffect(() => {
    if (!open) return;
    menu.current?.querySelector<HTMLElement>('[role="menuitem"]')?.focus();
    const outside = (event: PointerEvent) => {
      if (!container.current?.contains(event.target as Node)) setOpen(false);
    };
    const escape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        event.preventDefault();
        setOpen(false);
        trigger.current?.focus();
      }
    };
    const close = () => setOpen(false);
    document.addEventListener("pointerdown", outside);
    document.addEventListener("keydown", escape);
    window.addEventListener("hashchange", close);
    return () => {
      document.removeEventListener("pointerdown", outside);
      document.removeEventListener("keydown", escape);
      window.removeEventListener("hashchange", close);
    };
  }, [open]);

  async function sair() {
    setSaindo(true);
    setErro("");
    try {
      await logout();
      setOpen(false);
      if (pathname === "/meus-pedidos" || pathname === "/funcionario" || pathname.startsWith("/funcionario/")) window.location.replace("/");
    } catch (e) {
      setErro(e instanceof Error ? e.message : "Não foi possível sair. Tente novamente.");
    } finally { setSaindo(false); }
  }

  const iconClass = "flex h-10 w-10 shrink-0 items-center justify-center rounded-sm text-char/80 transition-colors hover:bg-char/5 hover:text-brick";
  if (carregando) return <span aria-label="Verificando conta" className={iconClass}><User className="h-5 w-5" aria-hidden="true" /></span>;
  if (!usuario) return <div className="flex items-center">
    <Link href="/login" aria-label="Entrar na minha conta" className={iconClass}><User className="h-5 w-5" /></Link>
    <Link href="/login" className="px-2 text-sm text-brick">Entrar</Link>
  </div>;

  const nome = usuario.nome?.trim() || usuario.email.split("@")[0];
  const partes = nome.split(/\s+/);
  const iniciais = (partes[0][0] + (partes.length > 1 ? partes[partes.length - 1][0] : "")).toLocaleUpperCase("pt-BR");
  const funcionario = ehFuncionario(usuario);

  return <div ref={container} className="relative" onBlur={event => {
    if (!event.currentTarget.contains(event.relatedTarget as Node | null)) setOpen(false);
  }}>
    <button ref={trigger} type="button" aria-haspopup="menu" aria-expanded={open} aria-controls="menu-conta" aria-label="Abrir menu da conta" onClick={() => setOpen(prev => !prev)} className="flex h-10 items-center rounded-sm text-char/80 hover:bg-char/5 hover:text-brick">
      <User className="mx-2.5 h-5 w-5 shrink-0" aria-hidden="true" />
      <span className="max-w-[10ch] truncate pr-2 text-sm">{partes[0]}</span>
    </button>
    {open && <div ref={menu} id="menu-conta" role="menu" aria-label="Menu da conta" className="absolute right-0 top-full z-50 mt-2 w-72 max-w-[calc(100vw-2rem)] rounded-lg border border-border bg-background shadow-lg">
      <div role="presentation" className="flex gap-3 p-4">
        <span aria-hidden="true" className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-brick/10 font-semibold text-brick">{iniciais}</span>
        <div className="min-w-0 flex-1">
          <p className="break-words text-sm font-semibold text-char">{nome}</p>
          <p title={usuario.email} className="mt-1 truncate text-xs text-muted-foreground">{usuario.email}</p>
          {usuario.telefone && <p className="mt-1 text-xs text-muted-foreground">{usuario.telefone}</p>}
          <span className="mt-2 inline-block rounded-full bg-brick/10 px-2 py-1 text-xs text-brick">{funcionario ? "Funcionário" : "Cliente"}{funcionario && usuario.cargo ? ` · ${usuario.cargo}` : ""}</span>
        </div>
      </div>
      <div role="separator" className="border-t border-border" />
      <div role="presentation" className="space-y-1 p-2">
        {ehCliente(usuario) && <Link role="menuitem" href="/meus-pedidos" onClick={() => setOpen(false)} className="block rounded-md px-3 py-2 text-sm text-char hover:bg-char/5">Meus pedidos</Link>}
        {funcionario && <Link role="menuitem" href="/funcionario" onClick={() => setOpen(false)} className="block rounded-md bg-brick px-3 py-2 text-sm font-semibold text-background hover:bg-brick-dark">Acessar painel interno</Link>}
        <button role="menuitem" type="button" disabled={saindo} onClick={sair} className="block w-full rounded-md px-3 py-2 text-left text-sm text-brick hover:bg-brick/10 disabled:opacity-50">{saindo ? "Saindo..." : "Sair"}</button>
        {erro && <p role="alert" className="px-3 py-2 text-xs text-brick">{erro}</p>}
      </div>
    </div>}
  </div>;
}
