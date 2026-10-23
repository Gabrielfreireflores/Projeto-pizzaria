"use client";

import { ReactNode, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth, ehFuncionario } from "@/hooks/use-auth";

export function RequerFuncionario({ children }: { children: ReactNode }) {
  const { usuario, carregando } = useAuth();
  const router = useRouter();
  const autorizado = ehFuncionario(usuario);

  useEffect(() => {
    if (!carregando && !autorizado) router.replace("/login");
  }, [carregando, autorizado, router]);

  if (carregando || !autorizado) return null;
  return <>{children}</>;
}