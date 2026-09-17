"use client";

import Link from "next/link";
import { useState } from "react";
import { Menu, X, ShoppingBag, User } from "lucide-react";

const NAV_LINKS = [
  { href: "#cardapio", label: "Cardápio" },
  { href: "#bebidas", label: "Bebidas" },
  { href: "#sobre", label: "Sobre" },
  { href: "#contato", label: "Contato" },
];

export function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-background/95 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-content items-center justify-between px-4 sm:px-6 lg:px-8">
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

        <nav className="hidden items-center gap-8 md:flex">
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

        <div className="flex items-center gap-1">
          <Link
            href="/login"
            aria-label="Entrar na minha conta"
            className="flex h-10 w-10 items-center justify-center rounded-sm text-char/80 transition-colors hover:bg-char/5 hover:text-brick"
          >
            <User className="h-5 w-5" />
          </Link>
          <button
            type="button"
            aria-label="Ver sacola"
            className="flex h-10 w-10 items-center justify-center rounded-sm text-char/80 transition-colors hover:bg-char/5 hover:text-brick"
          >
            <ShoppingBag className="h-5 w-5" />
          </button>
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
