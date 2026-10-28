"use client";

import { createContext, useContext, useState, ReactNode } from "react";

const MenuSearchContext = createContext<{ query: string; setQuery: (value: string) => void } | null>(null);

export function MenuSearchProvider({ children }: { children: ReactNode }) {
  const [query, setQuery] = useState("");
  return <MenuSearchContext.Provider value={{ query, setQuery }}>{children}</MenuSearchContext.Provider>;
}

export function useMenuSearch() {
  const value = useContext(MenuSearchContext);
  if (!value) throw new Error("Busca do cardápio indisponível.");
  return value;
}
