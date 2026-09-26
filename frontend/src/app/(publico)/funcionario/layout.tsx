"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LogOut, User } from "lucide-react";
import { ProdutosProvider } from "@/hooks/use-produtos";
import { FuncionariosProvider } from "@/hooks/use-funcionarios";

const menu = [
  { href: "/funcionario", label: "Pedidos" },
  { href: "/funcionario/produtos", label: "Produtos" },
  { href: "/funcionario/equipe", label: "Equipe" },
];

function isAtivo(pathname: string, href: string) {
  if (href === "/funcionario") {
    return pathname === "/funcionario";
  }
  return pathname === href || pathname.startsWith(href + "/");
}

export default function FuncionarioLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  return (
    <ProdutosProvider>
      <FuncionariosProvider>
        <main className="min-h-screen bg-background text-char">
          <div className="flex min-h-screen">

            {/* SIDEBAR */}
            <aside className="flex h-screen w-64 flex-col border-r border-border bg-muted/40 px-5 py-6">
              <div className="border-b border-border pb-5">
                <Link href="/" className="block">
                  <p className="font-display text-xl font-semibold text-brick">
                    Pizzaria do Barriga
                  </p>
                  <p className="mt-1 text-xs text-muted-foreground">
                    Área do funcionário
                  </p>
                </Link>
              </div>

              {/* Menu com scroll próprio, caso cresça */}
              <nav className="mt-5 flex-1 space-y-1 overflow-y-auto">
                {menu.map((item) => {
                  const ativo = isAtivo(pathname, item.href);
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      className={`flex items-center rounded-lg px-4 py-3 text-sm font-medium transition ${
                        ativo
                          ? "bg-brick text-background shadow-sm"
                          : "text-char hover:bg-muted"
                      }`}
                    >
                      {item.label}
                    </Link>
                  );
                })}
              </nav>

              {/* Rodapé: usuário + sair, estilo ERP */}
              <div className="mt-4 shrink-0 border-t border-border pt-4">
                <div className="flex items-center gap-3 rounded-xl bg-background p-3 shadow-sm">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-brick/10 text-brick">
                    <User size={18} />
                  </div>

                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-semibold text-char">
                      Funcionário
                    </p>
                    <p className="truncate text-xs text-muted-foreground">
                      Cozinha
                    </p>
                  </div>

                  <Link
                    href="/login"
                    title="Sair"
                    className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-muted-foreground transition hover:bg-muted hover:text-brick"
                  >
                    <LogOut size={16} />
                  </Link>
                </div>
              </div>
            </aside>

            {/* CONTEÚDO */}
            <section className="flex-1 overflow-y-auto px-6 py-8 sm:px-8 lg:px-12">
              {children}
            </section>
          </div>
        </main>
      </FuncionariosProvider>
    </ProdutosProvider>
  );
}