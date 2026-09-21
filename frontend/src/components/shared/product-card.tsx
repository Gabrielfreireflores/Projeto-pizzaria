"use client";

import Image from "next/image";
import { Product } from "@/types/product";
import { useCart } from "@/hooks/use-cart";

const currencyFormatter = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

export function ProductCard({ product }: { product: Product }) {
  const { addItem } = useCart();

  return (
    <div className="flex flex-col overflow-hidden rounded-lg border border-border bg-background shadow-sm">
      <div className="relative h-44 w-full">
        <Image
          src={product.image}
          alt={product.name}
          fill
          sizes="(min-width: 1024px) 25vw, (min-width: 640px) 50vw, 100vw"
          className="object-cover"
        />
      </div>
      <div className="flex flex-1 flex-col p-4">
        <h3 className="text-lg font-semibold text-char">{product.name}</h3>
        <p className="mt-1 flex-1 text-sm leading-relaxed text-muted-foreground">
          {product.description}
        </p>
        <div className="mt-4 flex items-center justify-between">
          <span className="font-display text-lg font-semibold text-brick">
            {currencyFormatter.format(product.price)}
          </span>
          <button
            type="button"
            onClick={() => addItem(product)}
            className="rounded-sm bg-brick px-4 py-2 text-sm font-medium text-background transition-colors hover:bg-brick-dark"
          >
            Adicionar
          </button>
        </div>
      </div>
    </div>
  );
}