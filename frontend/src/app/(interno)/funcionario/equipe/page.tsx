"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Pencil, Trash2 } from "lucide-react";
import { api } from "@/services/api";
import { useAuth } from "@/hooks/use-auth";

type Membro = {
  id_funcionario: number;
  nome: string;
  cargo: string | null;
  telefone: string | null;
  email: string;
  ativo: boolean;
};

export default function EquipePage() {
  const { usuario } = useAuth();
  const [equipe, setEquipe] = useState<Membro[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);
  const [excluindoId, setExcluindoId] = useState<number | null>(null);

  useEffect(() => {
    api
      .listarEquipe()
      .then((r) => setEquipe(r.equipe ?? []))
      .catch((e) =>
        setErro(e instanceof Error ? e.message : "Não foi possível carregar a equipe."),
      )
      .finally(() => setCarregando(false));
  }, []);

  async function excluir(m: Membro) {
    const confirmou = window.confirm(
      `Excluir ${m.nome}? Essa ação não pode ser desfeita. Para apenas bloquear o acesso, use a edição e desmarque "Acesso ativo".`,
    );
    if (!confirmou) return;

    setErro(null);
    setExcluindoId(m.id_funcionario);
    try {
      await api.excluirFuncionario(m.id_funcionario);
      setEquipe((atuais) => atuais.filter((x) => x.id_funcionario !== m.id_funcionario));
    } catch (e) {
      // Ex.: já aceitou pedidos, ou é a sua própria conta: o backend explica o motivo.
      setErro(e instanceof Error ? e.message : "Não foi possível excluir o funcionário.");
    } finally {
      setExcluindoId(null);
    }
  }

  return (
    <>
      <header className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div className="flex-1">
          <p className="text-sm font-medium text-basil">Gestão</p>
          <h1 className="mt-1 text-4xl font-semibold leading-tight text-char">Equipe</h1>
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

      {erro && (
        <p role="alert" className="mb-4 text-sm text-brick">
          {erro}
        </p>
      )}

      <div className="overflow-x-auto rounded-2xl border border-border bg-background shadow-sm">
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
            {equipe.map((m) => {
              const sou = m.email === usuario?.email;
              return (
                <tr key={m.id_funcionario} className="border-b border-border last:border-0">
                  <td className="px-5 py-3 text-char">
                    <p className="font-medium">{m.nome}</p>
                    {!m.ativo && <p className="text-xs text-brick">Acesso desativado</p>}
                  </td>
                  <td className="px-5 py-3">
                    {m.cargo ? (
                      <span className="rounded-full bg-muted px-3 py-1 text-xs font-medium text-char">
                        {m.cargo}
                      </span>
                    ) : (
                      "—"
                    )}
                  </td>
                  <td className="px-5 py-3 text-char">{m.email}</td>
                  <td className="whitespace-nowrap px-5 py-3 text-char">{m.telefone ?? "—"}</td>
                  <td className="px-5 py-3">
                    <div className="flex items-center gap-3">
                      <Link
                        href={`/funcionario/equipe/${m.id_funcionario}/editar`}
                        title="Editar"
                        className="flex h-8 w-8 items-center justify-center rounded-lg text-muted-foreground transition hover:bg-muted hover:text-brick"
                      >
                        <Pencil size={16} />
                      </Link>

                      <button
                        type="button"
                        onClick={() => excluir(m)}
                        disabled={sou || excluindoId === m.id_funcionario}
                        title={sou ? "Você não pode excluir a sua própria conta" : "Excluir"}
                        className="flex h-8 w-8 items-center justify-center rounded-lg text-muted-foreground transition hover:bg-muted hover:text-brick disabled:cursor-not-allowed disabled:opacity-40"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>

        {carregando && (
          <p className="p-6 text-sm text-muted-foreground">Carregando equipe...</p>
        )}

        {!carregando && !erro && equipe.length === 0 && (
          <div className="p-12 text-center">
            <p className="font-display text-xl font-semibold text-char">
              Nenhum funcionário cadastrado
            </p>
          </div>
        )}
      </div>
    </>
  );
}