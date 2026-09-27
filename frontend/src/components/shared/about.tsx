import Image from "next/image";

export function About() {
  return (
    <section id="sobre" className="bg-background py-16 sm:py-20">
      <div className="mx-auto grid max-w-content items-center gap-10 px-4 sm:px-6 md:grid-cols-2 lg:px-8">
        <div className="relative aspect-[4/3] w-full overflow-hidden rounded-lg">
          <Image
            src="https://images.unsplash.com/photo-1590947132387-155cc02f3212?w=800&q=80"
            alt="Forno a lenha da Pizzaria do Barriga"
            fill
            sizes="(min-width: 768px) 40vw, 100vw"
            className="object-cover"
          />
        </div>

        <div>
          <p className="text-sm font-medium text-basil">Sobre nós</p>
          <h2 className="mt-2 text-3xl font-semibold text-char">
            Tradição de família em cada fatia
          </h2>
          <p className="mt-4 leading-relaxed text-muted-foreground">
            A Pizzaria do Barriga nasceu em Jardinópolis-SP com uma receita
            simples: massa de longa fermentação, ingredientes selecionados e
            um forno a lenha que nunca esfria. Hoje seguimos servindo a
            vizinhança com o mesmo carinho do primeiro dia.
          </p>
          <p className="mt-4 text-sm text-muted-foreground">
            📍 Jardinópolis-SP
          </p>
        </div>
      </div>
    </section>
  );
}