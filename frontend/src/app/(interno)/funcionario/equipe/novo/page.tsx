"use client";

import { useRouter } from "next/navigation";
import { api } from "@/services/api";
import { EquipeForm } from "@/components/shared/equipe-form";

export default function NovoFuncionarioPage() {
  const router = useRouter();

  return (
    <EquipeForm
      modo="novo"
      titulo="Cadastrar funcionário"
      descricao="Adicione um novo membro à equipe."
      onSubmit={async (d) => {
        await api.criarFuncionario({
          nome: d.nome,
          cpf: d.cpf,
          cargo: d.cargo,
          telefone: d.telefone,
          email: d.email,
          senha: d.senha,
        });
        router.push("/funcionario/equipe");
      }}
    />
  );
}