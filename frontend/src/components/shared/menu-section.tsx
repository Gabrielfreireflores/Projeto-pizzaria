import { menu, CATEGORY_LABEL } from "@/lib/data/products";
import { ProductCategory } from "@/types/product";
import { ProductCard } from "@/components/shared/product-card";

const SECTIONS: { category: ProductCategory; id: string }[] = [
  { category: "salgada", id: "salgadas" },
  { category: "doce", id: "doces" },
  { category: "borda", id: "bordas" },
  { category: "bebida", id: "bebidas" },
];

export function MenuSection() {
  return (
    <section id="cardapio" className="scroll-mt-16 bg-background py-12 sm:py-16">
      <div className="mx-auto max-w-content px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-semibold text-char">Cardápio</h2>

        <nav
          aria-label="Categorias do cardápio"
          className="sticky top-16 z-10 -mx-4 mt-4 flex gap-2 overflow-x-auto bg-background/95 px-4 py-3 backdrop-blur sm:mx-0 sm:px-0"
        >
          {SECTIONS.map(({ category, id }) => (
            <a
              key={id}
              href={`#${id}`}
              className="shrink-0 rounded-full border border-border px-4 py-2 text-sm font-medium text-char transition-colors hover:border-brick hover:text-brick"
            >
              {CATEGORY_LABEL[category]}
            </a>
          ))}
        </nav>

        {SECTIONS.map(({ category, id }) => (
          <div key={id} id={id} className="scroll-mt-32 pt-8">
            <h3 className="text-2xl font-semibold text-char">
              {CATEGORY_LABEL[category]}
            </h3>
            <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {menu
                .filter((item) => item.category === category)
                .map((item) => (
                  <ProductCard key={item.id} item={item} />
                ))}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}