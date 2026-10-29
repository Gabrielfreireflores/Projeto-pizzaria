"use client";

import Link from "next/link";
import Image from "next/image";
import { useEffect, useRef, useState } from "react";
import { Menu, X, ShoppingBag, Search } from "lucide-react";
import { useCart } from "@/hooks/use-cart";
import { useMenuSearch } from "@/hooks/use-menu-search";
import { AccountMenu } from "@/components/shared/account-menu";
import { useRouter } from "next/navigation";

const NAV_LINKS = [
  { href: "/#cardapio", label: "Cardápio" },
  { href: "/#bebidas", label: "Bebidas" },
  { href: "/#sobre", label: "Sobre" },
  { href: "/#contato", label: "Contato" },
];

export function Navbar() {
  const [open, setOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const searchInput = useRef<HTMLInputElement>(null);
  const { itemCount } = useCart();
  const { query, setQuery } = useMenuSearch();
  const router = useRouter();

  useEffect(() => { if (searchOpen) searchInput.current?.focus(); }, [searchOpen]);

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-background/95 backdrop-blur">
      <div className="mx-auto flex max-w-content h-[calc(var(--header-h)-1px)] items-center justify-between gap-2 px-4 sm:px-6 lg:px-8">
        <Link href="/" className="flex shrink-0 items-center gap-1.5 sm:gap-3" onClick={() => setOpen(false)}>
          <Image
            src="/logo.png"
            alt="Logo da Pizzaria do Barriga"
            width={72}
            height={72}
            priority
            sizes="(min-width: 640px) 72px, 48px"
            className="h-12 w-12 shrink-0 object-contain sm:h-[72px] sm:w-[72px]"
          />
          <span className="font-display text-sm font-semibold leading-tight sm:text-xl text-char">
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

        <form role="search" onSubmit={e => { e.preventDefault(); setSearchOpen(false); router.push('/#cardapio'); }} className={`${searchOpen ? 'flex' : 'hidden'} absolute inset-x-4 top-full mt-2 items-center gap-2 rounded-lg border border-border bg-background px-3 shadow-sm sm:static sm:ml-auto sm:mt-0 sm:flex sm:w-64 sm:shadow-none`}>
          <Search size={17} className="shrink-0 text-muted-foreground" aria-hidden="true" />
          <input ref={searchInput} type="search" aria-label="Busque por um produto" placeholder="Busque por um produto" value={query} onChange={e => setQuery(e.target.value)} className="min-w-0 flex-1 bg-transparent py-2 text-sm outline-none" />
          <button type="submit" className="sr-only">Buscar</button>
          <button type="button" onClick={() => setSearchOpen(false)} aria-label="Fechar busca" className="flex h-9 w-9 shrink-0 items-center justify-center text-char sm:hidden"><X size={18} /></button>
        </form>

        <div className="flex shrink-0 items-center gap-1">
          <button type="button" onClick={() => setSearchOpen(value => !value)} aria-label="Abrir busca" aria-expanded={searchOpen} className="flex h-9 w-9 items-center justify-center rounded-sm text-char/80 hover:bg-char/5 sm:hidden"><Search className="h-5 w-5" /></button>
          <AccountMenu />
          <Link
            href="/carrinho"
            aria-label="Ver sacola"
            className="relative flex h-9 w-9 sm:h-10 sm:w-10 items-center justify-center rounded-sm text-char/80 transition-colors hover:bg-char/5 hover:text-brick"
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
            className="flex h-9 w-9 sm:h-10 sm:w-10 items-center justify-center rounded-sm text-char/80 hover:bg-char/5 md:hidden"
          >
            {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {open && (
        <nav className="absolute inset-x-0 top-full border-t border-border bg-background shadow-sm md:hidden">
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
