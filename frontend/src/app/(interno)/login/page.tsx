"use client";

import Image from "next/image";
import Link from "next/link";
import { useState } from "react";
import { buttonVariants } from "@/components/ui/button";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    console.log({
      email,
      senha,
    });
  }

  return (
    <main className="min-h-screen bg-background">
      <div className="grid min-h-screen lg:grid-cols-2">

        {/* LADO ESQUERDO */}
        <section className="relative hidden overflow-hidden bg-brick lg:flex">
          <div className="absolute inset-0 opacity-20">
            <Image
              src="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=1400&q=80"
              alt=""
              fill
              className="object-cover"
              priority
            />
          </div>

          <div className="absolute inset-0 bg-brick/80" />

          <div className="relative z-10 flex w-full flex-col justify-between p-12 xl:p-16">
            <div>
              <p className="text-sm font-medium tracking-wide text-crust">
                JARDINÓPOLIS-SP · FORNO A LENHA
              </p>

              <h1 className="mt-6 max-w-lg text-5xl font-semibold leading-[1.05] text-background xl:text-6xl">
                Pizza feita como em casa da Barriga.
              </h1>

              <p className="mt-6 max-w-md text-base leading-relaxed text-background/80">
                Massa fermentada por 48 horas, molho de tomate fresco e
                aquele forno a lenha que nunca esfria.
              </p>
            </div>

            <div className="flex items-center gap-3 text-sm text-background/70">
              <span className="h-px w-8 bg-crust" />
              Sua pizzaria, do seu jeito.
            </div>
          </div>
        </section>

        {/* LADO DIREITO */}
        <section className="flex min-h-screen items-center justify-center px-6 py-12 sm:px-8">
          <div className="w-full max-w-md">

            {/* Logo / marca */}
            <div className="mb-10">
              <Link
                href="/"
                className="inline-flex items-center gap-2 text-sm font-medium text-basil transition-opacity hover:opacity-70"
              >
                ← Voltar para o cardápio
              </Link>

              <div className="mt-10">
                <p className="text-sm font-medium text-basil">
                  Pizzaria do Barriga
                </p>

                <h2 className="mt-2 text-4xl font-semibold text-char">
                  Bem-vindo de volta.
                </h2>

                <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
                  Entre na sua conta para acompanhar seus pedidos e acessar
                  seu histórico.
                </p>
              </div>
            </div>

            {/* FORMULÁRIO */}
            <form onSubmit={handleSubmit} className="space-y-5">

              <div>
                <label
                  htmlFor="email"
                  className="mb-2 block text-sm font-medium text-char"
                >
                  E-mail
                </label>

                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="voce@email.com"
                  required
                  className="h-12 w-full rounded-lg border border-border bg-background px-4 text-sm text-char outline-none transition focus:border-brick focus:ring-2 focus:ring-brick/10"
                />
              </div>

              <div>
                <div className="mb-2 flex items-center justify-between">
                  <label
                    htmlFor="senha"
                    className="block text-sm font-medium text-char"
                  >
                    Senha
                  </label>

                  <Link
                    href="/recuperar-senha"
                    className="text-xs font-medium text-brick hover:underline"
                  >
                    Esqueci minha senha
                  </Link>
                </div>

                <input
                  id="senha"
                  type="password"
                  value={senha}
                  onChange={(e) => setSenha(e.target.value)}
                  placeholder="••••••••"
                  required
                  className="h-12 w-full rounded-lg border border-border bg-background px-4 text-sm text-char outline-none transition focus:border-brick focus:ring-2 focus:ring-brick/10"
                />
              </div>

              <button
                type="submit"
                className={buttonVariants({
                  size: "lg",
                  className: "w-full",
                })}
              >
                Entrar
              </button>
            </form>

            {/* CADASTRO */}
            <div className="mt-8 border-t border-border pt-6 text-center">
              <p className="text-sm text-muted-foreground">
                Ainda não possui uma conta?
              </p>

              <Link
                href="/cadastro"
                className="mt-2 inline-block text-sm font-semibold text-brick hover:underline"
              >
                Criar minha conta
              </Link>
            </div>

            {/* Rodapé */}
            <p className="mt-10 text-center text-xs text-muted-foreground">
              © {new Date().getFullYear()} Pizzaria do Barriga
            </p>
          </div>
        </section>
      </div>
    </main>
  );
}