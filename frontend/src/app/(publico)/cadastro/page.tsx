import Link from "next/link";
import { Navbar } from "@/components/shared/navbar";
import { Input } from "@/components/ui/input";
import { buttonVariants } from "@/components/ui/button";

export default function CadastroPage() {
  return (
    <main>
      <Navbar />
      <div className="mx-auto flex max-w-content justify-center px-4 py-16 sm:px-6 lg:px-8">
        <div className="w-full max-w-sm">
          <h1 className="text-2xl font-semibold text-char">Criar conta</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Cadastre-se para acompanhar seus pedidos na Pizzaria do Barriga.
          </p>

          <form className="mt-8 space-y-4">
            <div>
              <label htmlFor="name" className="mb-1 block text-sm font-medium text-char">
                Nome
              </label>
              <Input id="name" type="text" placeholder="Seu nome completo" required />
            </div>

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

            <div>
              <label
                htmlFor="confirmPassword"
                className="mb-1 block text-sm font-medium text-char"
              >
                Confirmar senha
              </label>
              <Input id="confirmPassword" type="password" placeholder="••••••••" required />
            </div>

            <button
              type="submit"
              className={`${buttonVariants({ size: "lg" })} w-full`}
            >
              Cadastrar
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-muted-foreground">
            Já tem conta?{" "}
            <Link href="/login" className="font-medium text-brick hover:underline">
              Entrar
            </Link>
          </p>
        </div>
      </div>
    </main>
  );
}