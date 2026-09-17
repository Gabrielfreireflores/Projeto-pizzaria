import Image from "next/image";
import { buttonVariants } from "@/components/ui/button";

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-background">
      <div className="mx-auto grid max-w-content items-center gap-12 px-4 py-16 sm:px-6 md:grid-cols-2 md:py-24 lg:px-8">
        <div className="max-w-md">
          <p className="text-sm font-medium text-basil">
            Jardinópolis-SP · forno a lenha
          </p>
          <h1 className="mt-4 text-4xl font-semibold leading-[1.1] text-char sm:text-5xl">
            Pizza feita como em casa da Barriga.
          </h1>
          <p className="mt-5 text-base leading-relaxed text-muted-foreground">
            Massa fermentada por 48 horas, molho de tomate fresco e um forno
            que não esfria. Escolha sua pizza e receba quentinha, do jeito que
            a família gosta.
          </p>
          <div className="mt-8 flex items-center gap-4">
            <a href="#cardapio" className={buttonVariants({ size: "lg" })}>
              Ver cardápio
            </a>
          </div>
        </div>

        <div className="relative mx-auto aspect-square w-full max-w-sm md:max-w-md">
          <div className="absolute inset-0 rounded-full border-2 border-dashed border-crust/60" />
          <div className="absolute inset-4 overflow-hidden rounded-full shadow-xl">
            <Image
              src="https://images.unsplash.com/photo-1548365328-9f547fb0953b?w=800&q=80"
              alt="Pizza de mussarela recém-saída do forno a lenha"
              fill
              sizes="(min-width: 768px) 28rem, 20rem"
              className="object-cover"
              priority
            />
          </div>
          <span className="absolute -bottom-2 right-4 rounded-full bg-brick px-4 py-2 text-sm font-medium text-background shadow-lg sm:right-8">
            Pronta em ~30 min
          </span>
        </div>
      </div>
    </section>
  );
}
