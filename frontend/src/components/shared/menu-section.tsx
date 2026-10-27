"use client";

import { useCallback, useEffect, useState } from "react";
import { CATEGORY_LABEL } from "@/lib/data/products";
import { fetchMenu } from "@/services/menu";
import { MenuItem, ProductCategory } from "@/types/product";
import { ProductCard } from "@/components/shared/product-card";

const SECTIONS: { category: ProductCategory; id: string }[] = [
  { category: "salgada", id: "salgadas" },
  { category: "doce", id: "doces" },
  { category: "borda", id: "bordas" },
  { category: "bebida", id: "bebidas" },
];

export function MenuSection() {
  const [menu, setMenu] = useState<MenuItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setMenu(await fetchMenu());
    } catch (e) {
      setError(e instanceof Error ? e.message : "Não foi possível carregar o cardápio.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <section id="cardapio" className="scroll-mt-16 bg-background py-12 sm:py-16">
      <div className="mx-auto max-w-content px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-semibold text-char">Cardápio</h2>

        {loading && (
          <p role="status" className="mt-8 text-muted-foreground">
            Carregando cardápio...
          </p>
        )}

        {error && (
          <div role="alert" className="mt-8 rounded-lg border border-border p-6">
            <p className="text-char">{error}</p>
            <button
              type="button"
              onClick={load}
              className="mt-3 text-sm font-medium text-brick hover:underline"
            >
              Tentar novamente
            </button>
          </div>
        )}

        {!loading && !error && menu.length === 0 && (
          <p className="mt-8 text-muted-foreground">
            Nenhum item disponível no momento.
          </p>
        )}

        {menu.length > 0 && (
          <>
            <nav
              aria-label="Categorias do cardápio"
              className="sticky top-16 z-10 -mx-4 mt-4 flex gap-2 overflow-x-auto bg-background/95 px-4 py-3 backdrop-blur sm:mx-0 sm:px-0"
            >
              {SECTIONS.filter(({ category }) =>
                menu.some((item) => item.category === category)
              ).map(({ category, id }) => (
                <a
                  key={id}
                  href={`#${id}`}
                  className="shrink-0 rounded-full border border-border px-4 py-2 text-sm font-medium text-char transition-colors hover:border-brick hover:text-brick"
                >
                  {CATEGORY_LABEL[category]}
                </a>
              ))}
            </nav>

            {SECTIONS.map(({ category, id }) => {
              const items = menu.filter((item) => item.category === category);
              if (items.length === 0) return null;
              return (
                <div key={id} id={id} className="scroll-mt-32 pt-8">
                  <h3 className="text-2xl font-semibold text-char">
                    {CATEGORY_LABEL[category]}
                  </h3>
                  <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                    {items.map((item) => (
                      <ProductCard key={item.id} item={item} menu={menu} />
                    ))}
                  </div>
                </div>
              );
            })}
          </>
        )}
      </div>
    </section>
  );
}
