import Link from "next/link";
import { Navbar } from "@/components/shared/navbar";
import { Input } from "@/components/ui/input";
import { buttonVariants } from "@/components/ui/button";

export default function LoginPage() {
  return (
    <main>
      <Navbar />
      <div className="mx-auto flex max-w-content justify-center px-4 py-16 sm:px-6 lg:px-8">
        <div className="w-full max-w-sm">
          <h1 className="text-2xl font-semibold text-char">Entrar</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Acesse sua conta para acompanhar seus pedidos.
          </p>

          <form className="mt-8 space-y-4">
            <div>
              <label htmlFor="email" className="mb-1 block text-sm font-medium text-char">
                E-mail
              </label>
              <Input id="email" type="email" placeholder="voce@email.com" required />
            </div>

            <div>
              <label htmlFor="password" className="mb-1 block text-sm font-medium text-char">
                Senha
              </label>
              <Input id="password" type="password" placeholder="••••••••" required />
            </div>

            <button
              type="submit"
              className={`${buttonVariants({ size: "lg" })} w-full`}
            >
              Entrar
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