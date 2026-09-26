"use client";

import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function CadastroPage() {
  const router = useRouter();

  const [nomePizzaria, setNomePizzaria] = useState("");
  const [nomeResponsavel, setNomeResponsavel] = useState("");
  const [email, setEmail] = useState("");
  const [telefone, setTelefone] = useState("");
  const [senha, setSenha] = useState("");
  const [confirmarSenha, setConfirmarSenha] = useState("");
  const [erro, setErro] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErro("");

    if (senha !== confirmarSenha) {
      setErro("As senhas não coincidem.");
      return;
    }

    if (senha.length < 6) {
      setErro("A senha precisa ter pelo menos 6 caracteres.");
      return;
    }

    // TODO: enviar para a API de cadastro
    console.log({ nomePizzaria, nomeResponsavel, email, telefone, senha });

    router.push("/login");
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-background px-4 py-12 text-char">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <Link href="/" className="inline-block">
            <p className="font-display text-2xl font-semibold text-brick">
              Pizzaria do Barriga
            </p>
          </Link>
          <p className="mt-1 text-sm text-muted-foreground">
            Crie a conta da sua pizzaria
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="rounded-2xl border border-border bg-muted/40 p-6 shadow-sm sm:p-8"
        >
          <div className="space-y-5">
            <Campo label="Nome da pizzaria" htmlFor="nomePizzaria">
              <input
                id="nomePizzaria"
                value={nomePizzaria}
                onChange={(e) => setNomePizzaria(e.target.value)}
                placeholder="Ex: Pizzaria do Barriga"
                required
                className="w-full rounded-lg border border-border bg-background px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick"
              />
            </Campo>

            <Campo label="Seu nome" htmlFor="nomeResponsavel">
              <input
                id="nomeResponsavel"
                value={nomeResponsavel}
                onChange={(e) => setNomeResponsavel(e.target.value)}
                placeholder="Nome do responsável"
                required
                className="w-full rounded-lg border border-border bg-background px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick"
              />
            </Campo>

            <Campo label="E-mail" htmlFor="email">
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="voce@exemplo.com"
                required
                className="w-full rounded-lg border border-border bg-background px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick"
              />
            </Campo>

            <Campo label="Telefone" htmlFor="telefone">
              <input
                id="telefone"
                value={telefone}
                onChange={(e) => setTelefone(e.target.value)}
                placeholder="(11) 99999-9999"
                required
                className="w-full rounded-lg border border-border bg-background px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick"
              />
            </Campo>

            <div className="grid gap-5 sm:grid-cols-2">
              <Campo label="Senha" htmlFor="senha">
                <input
                  id="senha"
                  type="password"
                  value={senha}
                  onChange={(e) => setSenha(e.target.value)}
                  placeholder="Mínimo 6 caracteres"
                  required
                  className="w-full rounded-lg border border-border bg-background px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick"
                />
              </Campo>

              <Campo label="Confirmar senha" htmlFor="confirmarSenha">
                <input
                  id="confirmarSenha"
                  type="password"
                  value={confirmarSenha}
                  onChange={(e) => setConfirmarSenha(e.target.value)}
                  placeholder="Repita a senha"
                  required
                  className="w-full rounded-lg border border-border bg-background px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick"
                />
              </Campo>
            </div>

            {erro && (
              <p className="text-sm font-medium text-brick">{erro}</p>
            )}
          </div>

          <button
            type="submit"
            className="mt-6 w-full rounded-lg bg-brick px-4 py-2.5 text-sm font-semibold text-background transition hover:bg-brick-dark"
          >
            Criar minha conta
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-muted-foreground">
          Já possui uma conta?{" "}
          <Link href="/login" className="font-medium text-brick hover:underline">
            Entrar
          </Link>
        </p>
      </div>
    </main>
  );
}

function Campo({
  label,
  htmlFor,
  children,
}: {
  label: string;
  htmlFor: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <label
        htmlFor={htmlFor}
        className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-muted-foreground"
      >
        {label}
      </label>
      {children}
    </div>
  );
}