"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useCallback, useEffect, useRef, useState } from "react";
import { User } from "lucide-react";
import { ehCliente, ehFuncionario, useAuth } from "@/hooks/use-auth";

export function AccountMenu() {
  const { usuario, carregando, logout } = useAuth();
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [saindo, setSaindo] = useState(false);
  const [menuWidth, setMenuWidth] = useState(288);
  const [erro, setErro] = useState("");
  const container = useRef<HTMLDivElement>(null);
  const trigger = useRef<HTMLButtonElement>(null);
  const menu = useRef<HTMLDivElement>(null);
  const focusOnOpen = useRef(false);
  const closeTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const ajustarLargura = useCallback(() => {
    const right = trigger.current?.getBoundingClientRect().right ?? window.innerWidth - 16;
    setMenuWidth(Math.min(288, window.innerWidth - 32, right - 16));
  }, []);

  useEffect(() => { setOpen(false); }, [pathname]);
  useEffect(() => () => { if (closeTimer.current) clearTimeout(closeTimer.current); }, []);

  useEffect(() => {
    if (!open) return;
    if (focusOnOpen.current) menu.current?.querySelector<HTMLElement>('[role="menuitem"]')?.focus();
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
    window.addEventListener("resize", ajustarLargura);
    return () => {
      document.removeEventListener("pointerdown", outside);
      document.removeEventListener("keydown", escape);
      window.removeEventListener("hashchange", close);
      window.removeEventListener("resize", ajustarLargura);
    };
  }, [open, ajustarLargura]);

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

  const iconClass = "flex h-9 w-9 shrink-0 sm:h-10 sm:w-10 items-center justify-center rounded-sm text-char/80 transition-colors hover:bg-char/5 hover:text-brick";
  if (carregando) return <span aria-label="Verificando conta" className={iconClass}><User className="h-5 w-5" aria-hidden="true" /></span>;
  const nome = usuario?.nome?.trim() || usuario?.email.split("@")[0] || "";
  const partes = nome.split(/\s+/);
  const iniciais = ((partes[0]?.[0] ?? "") + (partes.length > 1 ? partes[partes.length - 1][0] : "")).toLocaleUpperCase("pt-BR");
  const funcionario = ehFuncionario(usuario);

  return <div ref={container} className="relative" onPointerEnter={event => {
    if (closeTimer.current) clearTimeout(closeTimer.current);
    if (event.pointerType === "mouse") {
      ajustarLargura();
      focusOnOpen.current = false;
      setOpen(true);
    }
  }} onPointerLeave={event => {
    if (event.pointerType === "mouse") closeTimer.current = setTimeout(() => {
      if (!container.current?.contains(document.activeElement)) setOpen(false);
    }, 200);
  }} onBlur={event => {
    if (!event.currentTarget.contains(event.relatedTarget as Node | null)) setOpen(false);
  }}>
    <button ref={trigger} type="button" aria-haspopup="menu" aria-expanded={open} aria-controls="menu-conta" aria-label="Abrir menu da conta" onClick={() => {
      ajustarLargura();
      focusOnOpen.current = true;
      setOpen(true);
      menu.current?.querySelector<HTMLElement>('[role="menuitem"]')?.focus();
    }} className="flex h-9 items-center sm:h-10 rounded-sm text-char/80 hover:bg-char/5 hover:text-brick">
      <User className="mx-2 h-5 w-5 shrink-0 sm:mx-2.5" aria-hidden="true" />
      <span className={usuario ? "max-w-[3ch] truncate pr-1 text-sm sm:max-w-[10ch] sm:pr-2" : "pr-1 text-xs text-brick sm:pr-2 sm:text-sm"}>{usuario ? partes[0] : "Entrar"}</span>
    </button>
    {open && <div ref={menu} id="menu-conta" style={{ width: menuWidth }} role="menu" aria-label="Menu da conta" className="absolute right-0 top-full z-50 mt-2 w-72 max-w-[calc(100vw-2rem)] rounded-lg border border-border bg-background shadow-lg">
      {usuario && <><div role="presentation" className="flex gap-3 p-4">
        <span aria-hidden="true" className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-brick/10 font-semibold text-brick">{iniciais}</span>
        <div className="min-w-0 flex-1">
          <p className="break-words text-sm font-semibold text-char">{nome}</p>
          <p title={usuario.email} className="mt-1 truncate text-xs text-muted-foreground">{usuario.email}</p>
          {usuario.telefone && <p className="mt-1 text-xs text-muted-foreground">{usuario.telefone}</p>}
          <span className="mt-2 inline-block rounded-full bg-brick/10 px-2 py-1 text-xs text-brick">{funcionario ? "Funcionário" : "Cliente"}{funcionario && usuario.cargo ? ` · ${usuario.cargo}` : ""}</span>
        </div>
      </div>
      <div role="separator" className="border-t border-border" /></>}
      <div role="presentation" className="space-y-1 p-2">
        {!usuario && <>
          <Link role="menuitem" href="/login" onClick={() => setOpen(false)} className="block rounded-md px-3 py-2 text-sm text-char hover:bg-char/5">Entrar</Link>
          <Link role="menuitem" href="/cadastro" onClick={() => setOpen(false)} className="block rounded-md px-3 py-2 text-sm text-char hover:bg-char/5">Cadastrar</Link>
        </>}
        {ehCliente(usuario) && <Link role="menuitem" href="/meus-pedidos" onClick={() => setOpen(false)} className="block rounded-md px-3 py-2 text-sm text-char hover:bg-char/5">Meus pedidos</Link>}
        {funcionario && <Link role="menuitem" href="/funcionario" onClick={() => setOpen(false)} className="block rounded-md bg-brick px-3 py-2 text-sm font-semibold text-background hover:bg-brick-dark">Acessar painel interno</Link>}
        {usuario && <button role="menuitem" type="button" disabled={saindo} onClick={sair} className="block w-full rounded-md px-3 py-2 text-left text-sm text-brick hover:bg-brick/10 disabled:opacity-50">{saindo ? "Saindo..." : "Sair"}</button>}
        {erro && <p role="alert" className="px-3 py-2 text-xs text-brick">{erro}</p>}
      </div>
    </div>}
  </div>;
}
