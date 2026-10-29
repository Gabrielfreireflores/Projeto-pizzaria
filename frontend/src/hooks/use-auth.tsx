"use client";

import { createContext, useCallback, useContext, useEffect, useState, ReactNode } from "react";
import { api } from "@/services/api";

export type Usuario = { id: number; email: string; ativo: boolean; perfil: string; nome?: string; telefone?: string };

const semAcento = (t: string) =>
  t.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();

export function ehFuncionario(usuario: Usuario | null) {
  return !!usuario && semAcento(usuario.perfil) === "funcionario";
}

export function ehCliente(usuario: Usuario | null) {
  return !!usuario && usuario.ativo && semAcento(usuario.perfil) === "cliente";
}

type AuthState = {
  usuario: Usuario | null;
  carregando: boolean;
  login: (email: string, senha: string) => Promise<Usuario>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [carregando, setCarregando] = useState(true);

  // Ao abrir o app, pergunta ao backend se já existe sessão.
  useEffect(() => {
    api.usuarioAtual()
      .then((r) => setUsuario(r.usuario))
      .catch(() => setUsuario(null)) // 401 aqui só quer dizer "sem sessão"
      .finally(() => setCarregando(false));
  }, []);

  const login = useCallback(async (email: string, senha: string) => {
    await api.login(email, senha);
    const r = await api.usuarioAtual();
    setUsuario(r.usuario);
    return r.usuario as Usuario;
  }, []);

  const logout = useCallback(async () => {
    await api.logout();
    setUsuario(null);
  }, []);

  return (
    <AuthContext.Provider value={{ usuario, carregando, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth precisa estar dentro de um AuthProvider");
  return ctx;
}