"use client";

import { createContext, useContext, useState, ReactNode } from "react";

export type CargoFuncionario = "Cozinha" | "Atendimento" | "Entregador" | "Gerente";

export interface Funcionario {
  id: number;
  nome: string;
  email: string;
  telefone: string;
  cargo: CargoFuncionario;
}

interface FuncionariosContextType {
  funcionarios: Funcionario[];
  adicionarFuncionario: (funcionario: Omit<Funcionario, "id">) => void;
  atualizarFuncionario: (id: number, dados: Omit<Funcionario, "id">) => void;
  removerFuncionario: (id: number) => void;
}

const FuncionariosContext = createContext<FuncionariosContextType | undefined>(
  undefined,
);

const funcionariosIniciais: Funcionario[] = [
  {
    id: 1,
    nome: "André Silva",
    email: "andre@pizzariadobarriga.com",
    telefone: "(16) 99999-0001",
    cargo: "Cozinha",
  },
];

export function FuncionariosProvider({ children }: { children: ReactNode }) {
  const [funcionarios, setFuncionarios] = useState<Funcionario[]>(
    funcionariosIniciais,
  );

  function adicionarFuncionario(funcionario: Omit<Funcionario, "id">) {
    setFuncionarios((atuais) => [
      ...atuais,
      {
        ...funcionario,
        id: atuais.length ? Math.max(...atuais.map((f) => f.id)) + 1 : 1,
      },
    ]);
  }

  function atualizarFuncionario(id: number, dados: Omit<Funcionario, "id">) {
    setFuncionarios((atuais) =>
      atuais.map((f) => (f.id === id ? { ...dados, id } : f)),
    );
  }

  function removerFuncionario(id: number) {
    setFuncionarios((atuais) => atuais.filter((f) => f.id !== id));
  }

  return (
    <FuncionariosContext.Provider
      value={{
        funcionarios,
        adicionarFuncionario,
        atualizarFuncionario,
        removerFuncionario,
      }}
    >
      {children}
    </FuncionariosContext.Provider>
  );
}

export function useFuncionarios() {
  const context = useContext(FuncionariosContext);
  if (!context) {
    throw new Error(
      "useFuncionarios precisa estar dentro de um FuncionariosProvider",
    );
  }
  return context;
}