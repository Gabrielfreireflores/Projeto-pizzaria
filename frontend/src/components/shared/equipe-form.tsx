// "use client";

// import Link from "next/link";
// import { FormEvent, useState } from "react";

// export type DadosForm = {
//   nome: string;
//   cpf: string;
//   cargo: string;
//   telefone: string;
//   email: string;
//   senha: string;
//   ativo: boolean;
// };

// type Props = {
//   modo: "novo" | "editar";
//   titulo: string;
//   descricao: string;
//   inicial?: Partial<DadosForm>;
//   onSubmit: (dados: DadosForm) => Promise<void>;
// };

// function formatarCPF(valor: string) {
//   const numeros = valor.replace(/\D/g, "").slice(0, 11);

//   return numeros
//     .replace(/(\d{3})(\d)/, "$1.$2")
//     .replace(/(\d{3})(\d)/, "$1.$2")
//     .replace(/(\d{3})(\d{1,2})$/, "$1-$2");
// }

// const inputCls =
//   "w-full rounded-lg border border-border bg-muted/40 px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick";

// // Sugestões de cargo (o campo aceita qualquer texto). Edite à vontade.
// const CARGOS = ["Cozinha", "Atendimento", "Entrega", "Gerência"];

// export function EquipeForm({ modo, titulo, descricao, inicial, onSubmit }: Props) {
//   const [nome, setNome] = useState(inicial?.nome ?? "");
//   const [cargo, setCargo] = useState(inicial?.cargo ?? "");
//   const [telefone, setTelefone] = useState(inicial?.telefone ?? "");
//   const [email, setEmail] = useState(inicial?.email ?? "");
//   const [senha, setSenha] = useState("");
//   const [ativo, setAtivo] = useState(inicial?.ativo ?? true);
//   const [cpf, setCpf] = useState(inicial?.cpf ?? "");

//   const [erro, setErro] = useState<string | null>(null);
//   const [enviando, setEnviando] = useState(false);

//   async function handleSubmit(e: FormEvent<HTMLFormElement>) {
//     e.preventDefault();
//     setErro(null);

//     const exigeSenha = modo === "novo" || senha.length > 0;
//     if (exigeSenha && senha.length < 8) {
//       setErro("A senha deve ter pelo menos 8 caracteres.");
//       return;
//     }

//     setEnviando(true);
//     try {
//       await onSubmit({
//         nome: nome.trim(),
//         cargo: cargo.trim(),
//         telefone: telefone.trim(),
//         email: email.trim(),
//         senha,
//         ativo,
//       });
//     } catch (err) {
//       setErro(err instanceof Error ? err.message : "Não foi possível salvar.");
//     } finally {
//       setEnviando(false);
//     }
//   }

//   return (
//     <div className="flex justify-center">
//       <div className="w-full max-w-2xl">
//         <header className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
//           <div className="flex-1">
//             <p className="text-sm font-medium text-basil">Gestão</p>
//             <h1 className="mt-1 text-4xl font-semibold leading-tight text-char">{titulo}</h1>
//             <p className="mt-2 text-sm text-muted-foreground">{descricao}</p>
//           </div>

//           <Link
//             href="/funcionario/equipe"
//             className="rounded-lg bg-brick px-4 py-2.5 text-sm font-semibold text-background transition hover:bg-brick-dark"
//           >
//             Voltar
//           </Link>
//         </header>

//         <form
//           onSubmit={handleSubmit}
//           className="rounded-2xl border border-border bg-background p-6 shadow-sm"
//         >
//           <div className="grid gap-5 sm:grid-cols-2">
//             <Campo label="Nome completo" htmlFor="nome" className="sm:col-span-2">
//               <input
//                 id="nome"
//                 value={nome}
//                 onChange={(e) => setNome(e.target.value)}
//                 placeholder="Ex: Maria Souza"
//                 required
//                 className={inputCls}
//               />
//             </Campo>

//             <Campo label="Cargo" htmlFor="cargo">
//               <input
//                 id="cargo"
//                 list="cargos"
//                 value={cargo}
//                 onChange={(e) => setCargo(e.target.value)}
//                 placeholder="Ex: Cozinha"
//                 required
//                 className={inputCls}
//               />
//               <datalist id="cargos">
//                 {CARGOS.map((c) => (
//                   <option key={c} value={c} />
//                 ))}
//               </datalist>
//             </Campo>

//             <Campo label="Telefone" htmlFor="telefone">
//               <input
//                 id="telefone"
//                 value={telefone}
//                 onChange={(e) => setTelefone(e.target.value)}
//                 inputMode="tel"
//                 placeholder="(16) 99999-9999"
//                 className={inputCls}
//               />
//             </Campo>

//             <Campo label="E-mail" htmlFor="email" className="sm:col-span-2">
//               <input
//                 id="email"
//                 type="email"
//                 value={email}
//                 onChange={(e) => setEmail(e.target.value)}
//                 placeholder="funcionario@exemplo.com"
//                 required
//                 className={inputCls}
//               />
//             </Campo>

//             <Campo
//               label={modo === "novo" ? "Senha de acesso" : "Nova senha (opcional)"}
//               htmlFor="senha"
//               className="sm:col-span-2"
//             >
//               <input
//                 id="senha"
//                 type="password"
//                 autoComplete="new-password"
//                 value={senha}
//                 onChange={(e) => setSenha(e.target.value)}
//                 placeholder={
//                   modo === "novo"
//                     ? "Mínimo de 8 caracteres"
//                     : "Deixe em branco para manter a senha atual"
//                 }
//                 required={modo === "novo"}
//                 className={inputCls}
//               />
//             </Campo>

//             {modo === "editar" && (
//               <label className="flex items-center gap-2 text-sm text-char sm:col-span-2">
//                 <input
//                   type="checkbox"
//                   checked={ativo}
//                   onChange={(e) => setAtivo(e.target.checked)}
//                 />
//                 Acesso ativo (desmarque para impedir o login sem apagar o histórico)
//               </label>
//             )}
//           </div>

//           {erro && (
//             <p role="alert" className="mt-5 text-sm text-brick">
//               {erro}
//             </p>
//           )}

//           <div className="mt-6 flex items-center justify-end gap-3 border-t border-border pt-5">
//             <Link
//               href="/funcionario/equipe"
//               className="rounded-lg px-4 py-2.5 text-sm font-semibold text-muted-foreground transition hover:bg-muted"
//             >
//               Cancelar
//             </Link>

//             <button
//               type="submit"
//               disabled={enviando}
//               className="rounded-lg bg-brick px-4 py-2.5 text-sm font-semibold text-background transition hover:bg-brick-dark disabled:opacity-60"
//             >
//               {enviando
//                 ? "Salvando..."
//                 : modo === "novo"
//                   ? "Cadastrar funcionário"
//                   : "Salvar alterações"}
//             </button>
//           </div>
//         </form>
//       </div>
//     </div>
//   );
// }

// function Campo({
//   label,
//   htmlFor,
//   children,
//   className = "",
// }: {
//   label: string;
//   htmlFor: string;
//   children: React.ReactNode;
//   className?: string;
// }) {
//   return (
//     <div className={className}>
//       <label
//         htmlFor={htmlFor}
//         className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-muted-foreground"
//       >
//         {label}
//       </label>
//       {children}
//     </div>
//   );
// }


"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";

export type DadosForm = {
  nome: string;
  cpf: string;
  cargo: string;
  telefone: string;
  email: string;
  senha: string;
  ativo: boolean;
};

type Props = {
  modo: "novo" | "editar";
  titulo: string;
  descricao: string;
  inicial?: Partial<DadosForm>;
  onSubmit: (dados: DadosForm) => Promise<void>;
};

const inputCls =
  "w-full rounded-lg border border-border bg-muted/40 px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick";

// Sugestões de cargo.
const CARGOS = ["Cozinha", "Atendimento", "Entrega", "Gerência"];

// Aplica a máscara 000.000.000-00.
function formatarCPF(valor: string) {
  const numeros = valor.replace(/\D/g, "").slice(0, 11);

  return numeros
    .replace(/(\d{3})(\d)/, "$1.$2")
    .replace(/(\d{3})(\d)/, "$1.$2")
    .replace(/(\d{3})(\d{1,2})$/, "$1-$2");
}

export function EquipeForm({
  modo,
  titulo,
  descricao,
  inicial,
  onSubmit,
}: Props) {
  const [nome, setNome] = useState(inicial?.nome ?? "");
  const [cpf, setCpf] = useState(
    formatarCPF(inicial?.cpf ?? "")
  );
  const [cargo, setCargo] = useState(inicial?.cargo ?? "");
  const [telefone, setTelefone] = useState(inicial?.telefone ?? "");
  const [email, setEmail] = useState(inicial?.email ?? "");
  const [senha, setSenha] = useState("");
  const [ativo, setAtivo] = useState(inicial?.ativo ?? true);

  const [erro, setErro] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setErro(null);

    const cpfNumeros = cpf.replace(/\D/g, "");

    if (modo === "novo" && cpfNumeros.length !== 11) {
      setErro("Informe um CPF com 11 dígitos.");
      return;
    }

    const exigeSenha = modo === "novo" || senha.length > 0;

    if (exigeSenha && senha.length < 8) {
      setErro("A senha deve ter pelo menos 8 caracteres.");
      return;
    }

    setEnviando(true);

    try {
      await onSubmit({
        nome: nome.trim(),
        cpf: cpf.trim(),
        cargo: cargo.trim(),
        telefone: telefone.trim(),
        email: email.trim(),
        senha,
        ativo,
      });
    } catch (err) {
      setErro(
        err instanceof Error
          ? err.message
          : "Não foi possível salvar."
      );
    } finally {
      setEnviando(false);
    }
  }

  return (
    <div className="flex justify-center">
      <div className="w-full max-w-2xl">
        <header className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
          <div className="flex-1">
            <p className="text-sm font-medium text-basil">
              Gestão
            </p>

            <h1 className="mt-1 text-4xl font-semibold leading-tight text-char">
              {titulo}
            </h1>

            <p className="mt-2 text-sm text-muted-foreground">
              {descricao}
            </p>
          </div>

          <Link
            href="/funcionario/equipe"
            className="rounded-lg bg-brick px-4 py-2.5 text-sm font-semibold text-background transition hover:bg-brick-dark"
          >
            Voltar
          </Link>
        </header>

        <form
          onSubmit={handleSubmit}
          className="rounded-2xl border border-border bg-background p-6 shadow-sm"
        >
          <div className="grid gap-5 sm:grid-cols-2">
            <Campo
              label="Nome completo"
              htmlFor="nome"
              className="sm:col-span-2"
            >
              <input
                id="nome"
                value={nome}
                onChange={(e) => setNome(e.target.value)}
                placeholder="Ex: Maria Souza"
                required
                maxLength={120}
                className={inputCls}
              />
            </Campo>

            <Campo label="CPF" htmlFor="cpf">
              <input
                id="cpf"
                type="text"
                value={cpf}
                onChange={(e) => setCpf(formatarCPF(e.target.value))}
                inputMode="numeric"
                autoComplete="off"
                placeholder="000.000.000-00"
                maxLength={14}
                required={modo === "novo"}
                className={inputCls}
              />
            </Campo>

            <Campo label="Cargo" htmlFor="cargo">
              <input
                id="cargo"
                list="cargos"
                value={cargo}
                onChange={(e) => setCargo(e.target.value)}
                placeholder="Ex: Cozinha"
                required
                maxLength={80}
                className={inputCls}
              />

              <datalist id="cargos">
                {CARGOS.map((c) => (
                  <option key={c} value={c} />
                ))}
              </datalist>
            </Campo>

            <Campo label="Telefone" htmlFor="telefone">
              <input
                id="telefone"
                value={telefone}
                onChange={(e) => setTelefone(e.target.value)}
                inputMode="tel"
                placeholder="(16) 99999-9999"
                maxLength={20}
                className={inputCls}
              />
            </Campo>

            <Campo
              label="E-mail"
              htmlFor="email"
              className="sm:col-span-2"
            >
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="funcionario@exemplo.com"
                required
                maxLength={160}
                className={inputCls}
              />
            </Campo>

            <Campo
              label={
                modo === "novo"
                  ? "Senha de acesso"
                  : "Nova senha (opcional)"
              }
              htmlFor="senha"
              className="sm:col-span-2"
            >
              <input
                id="senha"
                type="password"
                autoComplete="new-password"
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
                placeholder={
                  modo === "novo"
                    ? "Mínimo de 8 caracteres"
                    : "Deixe em branco para manter a senha atual"
                }
                required={modo === "novo"}
                minLength={modo === "novo" ? 8 : undefined}
                maxLength={128}
                className={inputCls}
              />
            </Campo>

            {modo === "editar" && (
              <label className="flex items-center gap-2 text-sm text-char sm:col-span-2">
                <input
                  type="checkbox"
                  checked={ativo}
                  onChange={(e) => setAtivo(e.target.checked)}
                />
                Acesso ativo (desmarque para impedir o login sem apagar o histórico)
              </label>
            )}
          </div>

          {erro && (
            <p role="alert" className="mt-5 text-sm text-brick">
              {erro}
            </p>
          )}

          <div className="mt-6 flex items-center justify-end gap-3 border-t border-border pt-5">
            <Link
              href="/funcionario/equipe"
              className="rounded-lg px-4 py-2.5 text-sm font-semibold text-muted-foreground transition hover:bg-muted"
            >
              Cancelar
            </Link>

            <button
              type="submit"
              disabled={enviando}
              className="rounded-lg bg-brick px-4 py-2.5 text-sm font-semibold text-background transition hover:bg-brick-dark disabled:opacity-60"
            >
              {enviando
                ? "Salvando..."
                : modo === "novo"
                  ? "Cadastrar funcionário"
                  : "Salvar alterações"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function Campo({
  label,
  htmlFor,
  children,
  className = "",
}: {
  label: string;
  htmlFor: string;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={className}>
      <label
        htmlFor={htmlFor}
        className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-muted-foreground"
      >
        {label}
      </label>

      {children}
    </div>
  );
}
