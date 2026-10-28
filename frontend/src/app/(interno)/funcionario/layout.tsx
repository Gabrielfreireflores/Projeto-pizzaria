"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { LogOut, User } from "lucide-react";
import { ProdutosProvider } from "@/hooks/use-produtos";
import { FuncionariosProvider } from "@/hooks/use-funcionarios";
import { useAuth } from "@/hooks/use-auth";
import { RequerFuncionario } from "@/components/shared/requer-funcionario";

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
  const router = useRouter();
  const { logout } = useAuth();

  async function sair() {
    await logout();
    router.replace("/login");
  }

  return (
    <RequerFuncionario><ProdutosProvider>
      <FuncionariosProvider>
        <main className="min-h-screen bg-background text-char">
          <div className="flex min-h-dvh flex-col lg:h-dvh lg:flex-row lg:overflow-hidden">

            {/* SIDEBAR */}
            <aside className="flex w-full shrink-0 flex-col border-b border-border bg-muted/40 px-4 py-4 lg:h-dvh lg:w-64 lg:border-b-0 lg:border-r lg:px-5 lg:py-6">
              <div className="border-b border-border pb-5">
                <div className="block select-none">
                  
                  {/* Logo + nome */}
                  <div className="flex items-center gap-3">
                    <img
                      src="/logo.png"
                      alt="Logo da Pizzaria do Barriga"
                      className="h-10 w-10 shrink-0 rounded-full object-cover"
                    />

                    <p className="font-display text-xl font-semibold leading-tight text-brick">
                      Pizzaria
                      <br />
                      do Barriga
                    </p>
                  </div>

                  {/* Subtítulo */}
                  <p className="mt-2 ml-[52px] text-xs text-muted-foreground">
                    Área do funcionário
                  </p>

                </div>
              </div>

              {/* Menu com scroll próprio, caso cresça */}
              <nav aria-label="Área do funcionário" className="mt-4 flex gap-1 overflow-x-auto lg:mt-5 lg:block lg:flex-1 lg:space-y-1 lg:overflow-y-auto">
                {menu.map((item) => {
                  const ativo = isAtivo(pathname, item.href);
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      className={`flex shrink-0 items-center rounded-lg px-4 py-3 text-sm font-medium transition ${
                        ativo
                          ? "bg-brick text-background shadow-sm"
                          : "text-char hover:bg-muted"
                      }`}
                    >
                      {item.label}
                    </Link>
                  );
                })}
                <button type="button" onClick={sair} className="ml-auto px-3 text-sm text-brick lg:hidden">Sair</button>
              </nav>

              {/* Rodapé: usuário + sair, estilo ERP */}
              <div className="mt-4 hidden shrink-0 border-t border-border pt-4 lg:block">
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

                  <button
                    type="button"
                    onClick={sair}
                    aria-label="Sair da conta"
                    title="Sair"
                    className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-muted-foreground transition hover:bg-muted hover:text-brick"
                  >
                    <LogOut size={16} />
                  </button>
                </div>
              </div>
            </aside>

            {/* CONTEÚDO */}
            <section className="min-w-0 flex-1 overflow-x-hidden px-4 py-6 sm:px-6 lg:min-h-0 lg:overflow-y-auto lg:px-8 xl:px-12">
              {children}
            </section>
          </div>
        </main>
      </FuncionariosProvider>
    </ProdutosProvider></RequerFuncionario>
  );
}
