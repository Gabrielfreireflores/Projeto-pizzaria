"use client";

import Link from "next/link";
import { useState } from "react";
import { Menu, X, ShoppingBag, User, Search, ClipboardList } from "lucide-react";
import { useCart } from "@/hooks/use-cart";
import { useMenuSearch } from "@/hooks/use-menu-search";
import { useAuth, ehFuncionario } from "@/hooks/use-auth";
import { useRouter } from "next/navigation";

const NAV_LINKS = [
  { href: "/#cardapio", label: "Cardápio" },
  { href: "/#bebidas", label: "Bebidas" },
  { href: "/#sobre", label: "Sobre" },
  { href: "/#contato", label: "Contato" },
];

export function Navbar() {
  const [open, setOpen] = useState(false);
  const { itemCount } = useCart();
  const { query, setQuery } = useMenuSearch();
  const { usuario } = useAuth();
  const router = useRouter();

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-background/95 backdrop-blur">
      <div className="mx-auto flex max-w-content flex-wrap items-center justify-between gap-x-3 gap-y-2 px-4 py-3 sm:px-6 lg:px-8">
        <Link href="/" className="flex items-center gap-2" onClick={() => setOpen(false)}>
          <img
            src="/logo.png"
            alt="Logo da Pizzaria do Barriga"
            className="h-9 w-9 rounded-full object-cover"
          />
          <span className="font-display text-lg font-semibold leading-none text-char">
            Pizzaria
            <br />
            do Barriga
          </span>
        </Link>

        <nav className="hidden items-center gap-5 xl:flex">
          {NAV_LINKS.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="text-sm font-medium text-char/80 transition-colors hover:text-brick"
            >
              {link.label}
            </a>
          ))}
        </nav>

        <form role="search" onSubmit={e => { e.preventDefault(); router.push('/#cardapio'); }} className="order-last flex w-full items-center gap-2 rounded-lg border border-border bg-background px-3 sm:order-none sm:ml-auto sm:w-64">
          <Search size={17} className="shrink-0 text-muted-foreground" aria-hidden="true" />
          <input type="search" aria-label="Busque por um produto" placeholder="Busque por um produto" value={query} onChange={e => setQuery(e.target.value)} className="min-w-0 flex-1 bg-transparent py-2 text-sm outline-none" />
          <button type="submit" className="sr-only">Buscar</button>
        </form>

        <div className="flex items-center gap-1">
          <Link
            href={usuario ? ehFuncionario(usuario) ? "/funcionario" : "/meus-pedidos" : "/login"}
            aria-label="Entrar na minha conta"
            className="flex h-10 w-10 items-center justify-center rounded-sm text-char/80 transition-colors hover:bg-char/5 hover:text-brick"
          >
            <User className="h-5 w-5" />
          </Link>
          <Link href="/meus-pedidos" aria-label="Meus pedidos" title="Meus pedidos" className="flex h-10 w-10 items-center justify-center rounded-sm text-char/80 hover:bg-char/5"><ClipboardList className="h-5 w-5" /></Link>
          <Link
            href="/carrinho"
            aria-label="Ver sacola"
            className="relative flex h-10 w-10 items-center justify-center rounded-sm text-char/80 transition-colors hover:bg-char/5 hover:text-brick"
          >
            <ShoppingBag className="h-5 w-5" />
            {itemCount > 0 && (
              <span className="absolute -right-0.5 -top-0.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-brick px-1 text-[10px] font-semibold leading-none text-background">
                {itemCount}
              </span>
            )}
          </Link>
          <button
            type="button"
            aria-label={open ? "Fechar menu" : "Abrir menu"}
            aria-expanded={open}
            onClick={() => setOpen((v) => !v)}
            className="ml-1 flex h-10 w-10 items-center justify-center rounded-sm text-char/80 hover:bg-char/5 md:hidden"
          >
            {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {open && (
        <nav className="border-t border-border bg-background md:hidden">
          <div className="mx-auto flex max-w-content flex-col px-4 py-2 sm:px-6">
            {NAV_LINKS.map((link) => (
              <a
                key={link.href}
                href={link.href}
                onClick={() => setOpen(false)}
                className="border-b border-border/60 py-3 text-sm font-medium text-char/80 last:border-none hover:text-brick"
              >
                {link.label}
              </a>
            ))}
          </div>
        </nav>
      )}
    </header>
  );
}
