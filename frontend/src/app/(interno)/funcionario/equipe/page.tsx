"use client";

import Link from "next/link";
import { Pencil, Trash2 } from "lucide-react";
import { useFuncionarios } from "@/hooks/use-funcionarios";

export default function EquipePage() {
  const { funcionarios, removerFuncionario } = useFuncionarios();

  return (
    <>
      <header className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div className="flex-1">
          <p className="text-sm font-medium text-basil">Gestão</p>
          <h1 className="mt-1 text-4xl font-semibold leading-tight text-char">
            Equipe
          </h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Gerencie os funcionários da pizzaria.
          </p>
        </div>

        <Link
          href="/funcionario/equipe/novo"
          className="rounded-lg bg-brick px-4 py-2.5 text-sm font-semibold text-background transition hover:bg-brick-dark"
        >
          + Novo funcionário
        </Link>
      </header>

      <div className="overflow-hidden rounded-2xl border border-border bg-background shadow-sm">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="border-b border-border text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              <th className="px-5 py-3">Nome</th>
              <th className="px-5 py-3">Cargo</th>
              <th className="px-5 py-3">E-mail</th>
              <th className="px-5 py-3">Telefone</th>
              <th className="px-5 py-3">Ações</th>
            </tr>
          </thead>
          <tbody>
            {funcionarios.map((funcionario) => (
              <tr key={funcionario.id} className="border-b border-border last:border-0">
                <td className="px-5 py-3 font-medium text-char">
                  {funcionario.nome}
                </td>
                <td className="px-5 py-3">
                  <span className="rounded-full bg-basil/10 px-3 py-1 text-xs font-semibold text-basil">
                    {funcionario.cargo}
                  </span>
                </td>
                <td className="px-5 py-3 text-char">{funcionario.email}</td>
                <td className="px-5 py-3 text-char">{funcionario.telefone}</td>
                <td className="px-5 py-3">
                  <div className="flex items-center gap-3">
                    <Link
                      href={`/funcionario/equipe/${funcionario.id}/editar`}
                      title="Editar"
                      className="flex h-8 w-8 items-center justify-center rounded-lg text-muted-foreground transition hover:bg-muted hover:text-brick"
                    >
                      <Pencil size={16} />
                    </Link>

                    <button
                      onClick={() => removerFuncionario(funcionario.id)}
                      title="Excluir"
                      className="flex h-8 w-8 items-center justify-center rounded-lg text-muted-foreground transition hover:bg-muted hover:text-brick"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {funcionarios.length === 0 && (
          <div className="p-12 text-center">
            <p className="font-display text-xl font-semibold text-char">
              Nenhum funcionário cadastrado
            </p>
            <p className="mt-2 text-sm text-muted-foreground">
              Adicione o primeiro funcionário da equipe.
            </p>
          </div>
        )}
      </div>
    </>
  );
}