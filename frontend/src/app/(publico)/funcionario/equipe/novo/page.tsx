"use client";

import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useFuncionarios, CargoFuncionario } from "@/hooks/use-funcionarios";

const cargos: CargoFuncionario[] = ["Cozinha", "Atendimento", "Entregador", "Gerente"];

export default function NovoFuncionarioPage() {
  const router = useRouter();
  const { adicionarFuncionario } = useFuncionarios();

  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [telefone, setTelefone] = useState("");
  const [cargo, setCargo] = useState<CargoFuncionario>(cargos[0]);
  const [senha, setSenha] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // TODO: enviar para a API (criar usuário/login do funcionário com a senha)
    adicionarFuncionario({ nome, email, telefone, cargo });

    router.push("/funcionario/equipe");
  };

  return (
    <div className="flex justify-center">
      <div className="w-full max-w-2xl">
        <header className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
          <div className="flex-1">
            <p className="text-sm font-medium text-basil">Gestão</p>
            <h1 className="mt-1 text-4xl font-semibold leading-tight text-char">
              Cadastrar funcionário
            </h1>
            <p className="mt-2 text-sm text-muted-foreground">
              Adicione um novo membro à equipe.
            </p>
          </div>

          <Link
            href="/funcionario/equipe"
            className="rounded-lg bg-brick px-4 py-2.5 text-sm font-semibold text-background transition hover:bg-brick-dark"
          >
            Voltar
          </Link>
        </header>

        <form
          onSubmit={handleSubmit}
          className="rounded-2xl border border-border bg-background p-6 shadow-sm"
        >
          <div className="grid gap-5 sm:grid-cols-2">
            <Campo label="Nome completo" htmlFor="nome" className="sm:col-span-2">
              <input
                id="nome"
                value={nome}
                onChange={(e) => setNome(e.target.value)}
                placeholder="Ex: Maria Souza"
                required
                className="w-full rounded-lg border border-border bg-muted/40 px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick"
              />
            </Campo>

            <Campo label="Cargo" htmlFor="cargo">
              <select
                id="cargo"
                value={cargo}
                onChange={(e) => setCargo(e.target.value as CargoFuncionario)}
                className="w-full rounded-lg border border-border bg-muted/40 px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick"
              >
                {cargos.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </Campo>

            <Campo label="Telefone" htmlFor="telefone">
              <input
                id="telefone"
                value={telefone}
                onChange={(e) => setTelefone(e.target.value)}
                placeholder="(16) 99999-9999"
                required
                className="w-full rounded-lg border border-border bg-muted/40 px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick"
              />
            </Campo>

            <Campo label="E-mail" htmlFor="email" className="sm:col-span-2">
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="funcionario@exemplo.com"
                required
                className="w-full rounded-lg border border-border bg-muted/40 px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick"
              />
            </Campo>

            <Campo label="Senha de acesso" htmlFor="senha" className="sm:col-span-2">
              <input
                id="senha"
                type="password"
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
                placeholder="Senha para login do funcionário"
                required
                minLength={6}
                className="w-full rounded-lg border border-border bg-muted/40 px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick"
              />
            </Campo>
          </div>

          <div className="mt-6 flex items-center justify-end gap-3 border-t border-border pt-5">
            <Link
              href="/funcionario/equipe"
              className="rounded-lg px-4 py-2.5 text-sm font-semibold text-muted-foreground transition hover:bg-muted"
            >
              Cancelar
            </Link>

            <button
              type="submit"
              className="rounded-lg bg-brick px-4 py-2.5 text-sm font-semibold text-background transition hover:bg-brick-dark"
            >
              Cadastrar funcionário
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function Campo({
  label,
  htmlFor,
  children,
  className = "",
}: {
  label: string;
  htmlFor: string;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={className}>
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