"use client";

import Link from "next/link";
import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useFuncionarios, CargoFuncionario } from "@/hooks/use-funcionarios";

const cargos: CargoFuncionario[] = ["Cozinha", "Atendimento", "Entregador", "Gerente"];

export default function EditarFuncionarioPage() {
  const router = useRouter();
  const { id } = useParams<{ id: string }>();
  const { funcionarios, atualizarFuncionario } = useFuncionarios();

  const funcionario = funcionarios.find((f) => f.id === Number(id));

  const [nome, setNome] = useState(funcionario?.nome ?? "");
  const [email, setEmail] = useState(funcionario?.email ?? "");
  const [telefone, setTelefone] = useState(funcionario?.telefone ?? "");
  const [cargo, setCargo] = useState<CargoFuncionario>(
    funcionario?.cargo ?? cargos[0],
  );

  if (!funcionario) {
    return (
      <div className="rounded-2xl border border-dashed border-border p-12 text-center">
        <p className="font-display text-xl font-semibold text-char">
          Funcionário não encontrado
        </p>
        <Link
          href="/funcionario/equipe"
          className="mt-4 inline-block text-sm font-medium text-brick hover:underline"
        >
          Voltar para equipe
        </Link>
      </div>
    );
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    atualizarFuncionario(funcionario.id, { nome, email, telefone, cargo });

    router.push("/funcionario/equipe");
  };

  return (
    <div className="flex justify-center">
      <div className="w-full max-w-2xl">
        <header className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
          <div className="flex-1">
            <p className="text-sm font-medium text-basil">Gestão</p>
            <h1 className="mt-1 text-4xl font-semibold leading-tight text-char">
              Editar funcionário
            </h1>
            <p className="mt-2 text-sm text-muted-foreground">
              Atualize os dados deste membro da equipe.
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
                required
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
              Salvar alterações
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