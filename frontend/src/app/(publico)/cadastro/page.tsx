"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useRef, useState } from "react";
import { Navbar } from "@/components/shared/navbar";
import { Input } from "@/components/ui/input";
import { api } from "@/services/api";
import { useAuth } from "@/hooks/use-auth";

type Campo = "nome" | "email" | "telefone" | "senha";
type Erros = Partial<Record<Campo, string>>;

function mascaraCelular(value: string) {
  const digits = value.replace(/\D/g, "").slice(0, 15);
  if (digits.length > 11) return `+${digits}`;
  if (!digits) return "";
  if (digits.length <= 2) return `(${digits}`;
  const local = digits.slice(2);
  const split = digits.length > 10 ? 5 : 4;
  return `(${digits.slice(0, 2)}) ${local.slice(0, split)}${local.length > split ? `-${local.slice(split)}` : ""}`;
}

export default function CadastroPage() {
  const router = useRouter();
  const { login } = useAuth();
  const formRef = useRef<HTMLFormElement>(null);
  const [telefone, setTelefone] = useState("");
  const [erros, setErros] = useState<Erros>({});
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  function exibirErros(found: Erros) {
    setErros(found);
    const first = Object.keys(found)[0];
    if (first) {
      requestAnimationFrame(() => {
        formRef.current?.querySelector<HTMLInputElement>(`[name="${first}"]`)?.focus();
      });
    }
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const nome = String(form.get("nome") ?? "").trim();
    const email = String(form.get("email") ?? "").trim().toLowerCase();
    const senha = String(form.get("senha") ?? "");
    const found: Erros = {};
    if (nome.split(/\s+/).length < 2 || nome.length > 120) found.nome = "Informe nome e sobrenome com até 120 caracteres.";
    if (email.length > 160 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) found.email = "Informe um e-mail válido com até 160 caracteres.";
    if (!/^[+()\d .-]+$/.test(telefone) || !/^\d{10,15}$/.test(telefone.replace(/\D/g, "")) || telefone.length > 20) found.telefone = "Informe um celular válido com DDD, de 10 a 15 dígitos.";
    if (!senha) found.senha = "A senha não pode ser vazia.";
    setError("");
    exibirErros(found);
    if (Object.keys(found).length) return;
    setSubmitting(true);
    try {
      await api.cadastrarCliente({ nome, telefone, email, senha });
      setSuccess(true);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Não foi possível criar sua conta.";
      if (/cadastrado.*e-mail/i.test(message)) exibirErros({ email: message });
      else setError(message);
      setSubmitting(false);
      return;
    }
    try {
      await login(email, senha);
      router.push("/meus-pedidos");
    } catch {
      setError("Sua conta foi criada. Acesse Entrar para fazer login.");
    } finally {
      setSubmitting(false);
    }
  }

  function erro(campo: Campo) {
    return erros[campo] ? <span id={`erro-${campo}`} className="mt-1 block text-xs font-normal text-brick" aria-live="polite">{erros[campo]}</span> : null;
  }

  return (
    <main>
      <Navbar />
      <div className="mx-auto max-w-md px-4 py-12 sm:px-6">
        <h1 className="text-3xl font-semibold text-char">Criar conta</h1>
        <p className="mt-2 text-sm text-muted-foreground">
          Com sua conta, acompanhe os pedidos feitos enquanto estiver conectado.
        </p>
        <form ref={formRef} onSubmit={submit} noValidate className="mt-7 space-y-4">
          <label htmlFor="cadastro-nome" className="block text-sm font-medium">
            Nome completo
            <Input id="cadastro-nome" name="nome" autoComplete="name" maxLength={120} required disabled={submitting || success} aria-invalid={!!erros.nome} aria-describedby={erros.nome ? "erro-nome" : undefined} className="mt-1" />
            {erro("nome")}
          </label>
          <label htmlFor="cadastro-email" className="block text-sm font-medium">
            E-mail
            <Input id="cadastro-email" name="email" type="email" autoComplete="email" maxLength={160} required disabled={submitting || success} aria-invalid={!!erros.email} aria-describedby={erros.email ? "erro-email" : undefined} className="mt-1" />
            {erro("email")}
          </label>
          <label htmlFor="cadastro-telefone" className="block text-sm font-medium">
            Celular
            <Input id="cadastro-telefone" name="telefone" type="tel" inputMode="tel" autoComplete="tel" value={telefone} onChange={event => setTelefone(mascaraCelular(event.target.value))} placeholder="(16) 99999-9999" maxLength={20} required disabled={submitting || success} aria-invalid={!!erros.telefone} aria-describedby={erros.telefone ? "erro-telefone" : undefined} className="mt-1" />
            {erro("telefone")}
          </label>
          <label htmlFor="cadastro-senha" className="block text-sm font-medium">
            Senha
            <Input id="cadastro-senha" name="senha" type="password" autoComplete="new-password" required disabled={submitting || success} aria-invalid={!!erros.senha} aria-describedby={erros.senha ? "erro-senha" : undefined} className="mt-1" />
            {erro("senha")}
          </label>
          {error && <p role="alert" aria-live="assertive" className="text-sm text-brick">{error}</p>}
          {success && <p role="status" aria-live="polite" className="text-sm text-basil">Conta criada com sucesso.</p>}
          <button disabled={submitting || success} className="w-full rounded-lg bg-brick px-4 py-3 font-semibold text-background disabled:opacity-50">
            {submitting ? "Criando conta..." : success ? "Conta criada" : "Criar conta"}
          </button>
        </form>
        <p className="mt-5 text-sm text-muted-foreground">
          Já tem conta? <Link href="/login" className="text-brick underline">Entrar</Link>
        </p>
      </div>
    </main>
  );
}
