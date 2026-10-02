import { buttonVariants } from "@/components/ui/button";

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-background">
      <div className="mx-auto grid max-w-content items-center gap-12 px-4 py-16 sm:px-6 md:grid-cols-2 md:py-24 lg:px-8">
        <div className="max-w-md">
          <p className="text-sm font-medium text-basil">
            Jardinópolis-SP 
          </p>
          <h1 className="mt-4 text-4xl font-semibold leading-[1.1] text-char sm:text-5xl">
            Sabores que reúnem família, amigos e criam bons momentos.
          </h1>
          <p className="mt-5 text-base leading-relaxed text-muted-foreground">
            Massa fermentada, molho de tomate fresco e um forno
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
            <video
              src="/calabresavideo-otimizado2.mp4"
              autoPlay
              muted
              loop
              playsInline
              className="h-full w-full object-cover"
            />
          </div>
          <span className="absolute -bottom-2 right-4 rounded-full bg-brick px-4 py-2 text-sm font-medium text-background shadow-lg sm:right-8">
            Pronta em ~40 min
          </span>
        </div>
      </div>
    </section>
  );
}