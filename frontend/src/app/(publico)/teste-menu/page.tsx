"use client";

import { useEffect, useState } from "react";
import { fetchMenu } from "@/services/menu";
import { MenuItem } from "@/types/product";

export default function TesteMenu() {
  const [itens, setItens] = useState<MenuItem[] | string>("carregando...");

  useEffect(() => {
    fetchMenu().then(setItens).catch((e) => setItens(`erro: ${e.message}`));
  }, []);

  return <pre className="p-6 text-sm">{JSON.stringify(itens, null, 2)}</pre>;
}