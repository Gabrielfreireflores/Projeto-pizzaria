// import Link from "next/link";
// import { Navbar } from "@/components/shared/navbar";
// import { Input } from "@/components/ui/input";
// import { buttonVariants } from "@/components/ui/button";

// export default function LoginPage() {
//   return (
//     <main>
//       <Navbar />
//       <div className="mx-auto flex max-w-content justify-center px-4 py-16 sm:px-6 lg:px-8">
//         <div className="w-full max-w-sm">
//           <h1 className="text-2xl font-semibold text-char">Entrar</h1>
//           <p className="mt-1 text-sm text-muted-foreground">
//             Acesse sua conta para acompanhar seus pedidos.
//           </p>

//           <form className="mt-8 space-y-4">
//             <div>
//               <label htmlFor="email" className="mb-1 block text-sm font-medium text-char">
//                 E-mail
//               </label>
//               <Input id="email" type="email" placeholder="voce@email.com" required />
//             </div>

//             <div>
//               <label htmlFor="password" className="mb-1 block text-sm font-medium text-char">
//                 Senha
//               </label>
//               <Input id="password" type="password" placeholder="••••••••" required />
//             </div>

//             <button
//               type="submit"
//               className={`${buttonVariants({ size: "lg" })} w-full`}
//             >
//               Entrar
//             </button>
//           </form>

//           <p className="mt-6 text-center text-sm text-muted-foreground">
//             Não tem conta?{" "}
//             <Link href="/cadastro" className="font-medium text-brick hover:underline">
//               Cadastre-se
//             </Link>
//           </p>
//         </div>
//       </div>
//     </main>
//   );
// }

"use client";

import { FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Navbar } from "@/components/shared/navbar";
import { Input } from "@/components/ui/input";
import { buttonVariants } from "@/components/ui/button";
import { useAuth, ehFuncionario } from "@/hooks/use-auth";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    if (new URLSearchParams(window.location.search).has("expirada"))
      setErro("Sua sessão expirou. Entre novamente para finalizar o pedido. A sacola foi preservada.");
  }, []);

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setErro(null);
    setEnviando(true);
    try {
      const usuario = await login(email, senha);
      const next = new URLSearchParams(window.location.search).get("next");
      const destino = next?.startsWith("/") && !next.startsWith("//") && !next.includes("\\") ? next : "/";
      router.push(ehFuncionario(usuario) ? "/funcionario" : destino);
    } catch (err) {
      setErro(err instanceof Error ? err.message : "Não foi possível entrar.");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <main>
      <Navbar />
      <div className="mx-auto flex max-w-content justify-center px-4 py-16 sm:px-6 lg:px-8">
        <div className="w-full max-w-sm">
          <h1 className="text-2xl font-semibold text-char">Entrar</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Acesse sua conta para acompanhar seus pedidos.
          </p>

          <form onSubmit={handleSubmit} className="mt-8 space-y-4">
            <div>
              <label htmlFor="email" className="mb-1 block text-sm font-medium text-char">
                E-mail
              </label>
              <Input
                id="email"
                type="email"
                placeholder="voce@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div>
              <label htmlFor="password" className="mb-1 block text-sm font-medium text-char">
                Senha
              </label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
                required
              />
            </div>

            {erro && (
              <p role="alert" className="text-sm text-brick">
                {erro}
              </p>
            )}

            <button
              type="submit"
              disabled={enviando}
              className={`${buttonVariants({ size: "lg" })} w-full`}
            >
              {enviando ? "Entrando..." : "Entrar"}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-muted-foreground">
            Não tem conta?{" "}
            <Link href="/cadastro" className="font-medium text-brick hover:underline">
              Cadastre-se
            </Link>
          </p>
        </div>
      </div>
    </main>
  );
}
