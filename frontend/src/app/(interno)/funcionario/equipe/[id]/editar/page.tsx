"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { api } from "@/services/api";
import { EquipeForm } from "@/components/shared/equipe-form";

type Membro = {
  id_funcionario: number;
  nome: string;
  cpf: string;
  cargo: string | null;
  telefone: string | null;
  email: string;
  ativo: boolean;
};

export default function EditarFuncionarioPage() {
  const router = useRouter();
  const { id } = useParams<{ id: string }>();

  const [membro, setMembro] = useState<Membro | null>(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    api
      .listarEquipe()
      .then((r) =>
        setMembro(
          (r.equipe ?? []).find((m: Membro) => m.id_funcionario === Number(id)) ?? null,
        ),
      )
      .catch((e) =>
        setErro(e instanceof Error ? e.message : "Não foi possível carregar o funcionário."),
      )
      .finally(() => setCarregando(false));
  }, [id]);

  if (carregando) {
    return <p className="text-sm text-muted-foreground">Carregando funcionário...</p>;
  }

  if (erro || !membro) {
    return (
      <div className="rounded-2xl border border-dashed border-border p-12 text-center">
        <p className="font-display text-xl font-semibold text-char">
          {erro ?? "Funcionário não encontrado"}
        </p>
        <Link
          href="/funcionario/equipe"
          className="mt-4 inline-block text-sm font-medium text-brick hover:underline"
        >
          Voltar para a equipe
        </Link>
      </div>
    );
  }

  return (
    <EquipeForm
      modo="editar"
      titulo="Editar funcionário"
      descricao="Atualize os dados deste membro da equipe."
      inicial={{
        nome: membro.nome,
        cpf: membro.cpf ?? "",
        cargo: membro.cargo ?? "",
        telefone: membro.telefone ?? "",
        email: membro.email,
        ativo: membro.ativo,
      }}
      onSubmit={async (d) => {
        await api.atualizarFuncionario(membro.id_funcionario, {
          nome: d.nome,
          cpf: d.cpf,
          cargo: d.cargo,
          telefone: d.telefone,
          email: d.email,
          ativo: d.ativo,
          ...(d.senha ? { senha: d.senha } : {}),
        });
        router.push("/funcionario/equipe");
      }}
    />
  );
}