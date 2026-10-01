"use client";

import { createContext, useContext, useState, ReactNode } from "react";

export interface Produto {
  id: number;
  nome: string;
  descricao: string;
  categoria: string;
  preco: string;
  imagemUrl: string;
}

interface ProdutosContextType {
  produtos: Produto[];
  categorias: string[];
  adicionarProduto: (produto: Omit<Produto, "id">) => void;
  atualizarProduto: (id: number, dados: Omit<Produto, "id">) => void;
  adicionarCategoria: (nome: string) => void;
  removerProduto: (id: number) => void;
}

const ProdutosContext = createContext<ProdutosContextType | undefined>(
  undefined,
);

const produtosIniciais: Produto[] = [
  {
    id: 1,
    nome: "Coca Cola Lata",
    descricao: "Lata 350 mL, gelada",
    categoria: "Bebida",
    preco: "R$ 10,00",
    imagemUrl: "/produtos/coca-lata.jpg",
  },
];

const categoriasIniciais = ["Pizza", "Bebida", "Sobremesa"];

export function ProdutosProvider({ children }: { children: ReactNode }) {
  const [produtos, setProdutos] = useState<Produto[]>(produtosIniciais);
  const [categorias, setCategorias] = useState<string[]>(categoriasIniciais);

  function adicionarProduto(produto: Omit<Produto, "id">) {
    setProdutos((atuais) => [
      ...atuais,
      { ...produto, id: atuais.length ? Math.max(...atuais.map((p) => p.id)) + 1 : 1 },
    ]);
  }

  function atualizarProduto(id: number, dados: Omit<Produto, "id">) {
    setProdutos((atuais) =>
      atuais.map((p) => (p.id === id ? { ...dados, id } : p)),
    );
  }

  function adicionarCategoria(nome: string) {
    setCategorias((atuais) =>
      atuais.includes(nome) ? atuais : [...atuais, nome],
    );
  }

  function removerProduto(id: number) {
    setProdutos((atuais) => atuais.filter((p) => p.id !== id));
  }

  return (
    <ProdutosContext.Provider
      value={{
        produtos,
        categorias,
        adicionarProduto,
        atualizarProduto,
        adicionarCategoria,
        removerProduto,
      }}
    >
      {children}
    </ProdutosContext.Provider>
  );
}

export function useProdutos() {
  const context = useContext(ProdutosContext);
  if (!context) {
    throw new Error("useProdutos precisa estar dentro de um ProdutosProvider");
  }
  return context;
}