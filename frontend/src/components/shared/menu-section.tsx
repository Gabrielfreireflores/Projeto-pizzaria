import { products } from "@/lib/data/products";
import { ProductCard } from "@/components/shared/product-card";

export function MenuSection() {
  const pizzas = products.filter((p) => p.category === "pizza");
  const bebidas = products.filter((p) => p.category === "bebida");

  return (
    <>
      <section id="cardapio" className="bg-background py-16 sm:py-20">
        <div className="mx-auto max-w-content px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-semibold text-char">
            Pizzas mais pedidas
          </h2>
          <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {pizzas.map((pizza) => (
              <ProductCard key={pizza.id} product={pizza} />
            ))}
          </div>
        </div>
      </section>

      <section id="bebidas" className="bg-muted py-16 sm:py-20">
        <div className="mx-auto max-w-content px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-semibold text-char">Bebidas</h2>
          <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {bebidas.map((bebida) => (
              <ProductCard key={bebida.id} product={bebida} />
            ))}
          </div>
        </div>
      </section>
    </>
  );
}