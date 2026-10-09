"use client";

import Image from "next/image";
import Link from "next/link";
import { Minus, Plus, Trash2 } from "lucide-react";
import { useCart } from "@/hooks/use-cart";
import { Navbar } from "@/components/shared/navbar";

const currencyFormatter = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

export default function CarrinhoPage() {
  const { items, increment, decrement, removeItem, clearCart, itemCount, subtotal } =
    useCart();

  if (items.length === 0) {
    return (
      <main>
        <Navbar />
        <div className="mx-auto max-w-content px-4 py-16 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-semibold text-char">Sua sacola</h1>
          <p className="mt-4 text-muted-foreground">
            Sua sacola está vazia.{" "}
            <Link href="/#cardapio" className="text-brick hover:underline">
              Ver cardápio
            </Link>
          </p>
        </div>
      </main>
    );
  }

  return (
    <main>
      <Navbar />
      <div className="mx-auto max-w-content px-4 py-12 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between gap-4">
          <h1 className="text-3xl font-semibold text-char">Sua sacola</h1>
          <button
            type="button"
            onClick={clearCart}
            className="text-sm text-muted-foreground transition-colors hover:text-brick"
          >
            Esvaziar sacola
          </button>
        </div>

        <div className="mt-8 grid gap-10 lg:grid-cols-3">
          <ul className="space-y-4 lg:col-span-2">
            {items.map(({ product, quantity }) => (
              <li
                key={product.id}
                className="flex gap-4 rounded-lg border border-border bg-background p-4"
              >
                <div className="relative h-20 w-20 shrink-0 overflow-hidden rounded-md">
                  <Image
                    src={product.image}
                    alt={product.name}
                    fill
                    sizes="80px"
                    className="object-cover"
                  />
                </div>

                <div className="flex min-w-0 flex-1 flex-col justify-between">
                  <div className="flex items-start justify-between gap-2">
                    <div className="min-w-0">
                      <h2 className="font-semibold text-char">
                        {product.name}
                      </h2>
                      <p className="text-sm text-muted-foreground">
                        {currencyFormatter.format(product.price)} cada
                      </p>
                      {product.note && (
                        <p className="mt-0.5 text-xs text-muted-foreground">
                          Obs.: {product.note}
                        </p>
                      )}
                    </div>
                    <button
                      type="button"
                      onClick={() => removeItem(product.id)}
                      aria-label={`Remover ${product.name}`}
                      className="shrink-0 text-muted-foreground transition-colors hover:text-brick"
                    >
                      <Trash2 size={18} />
                    </button>
                  </div>

                  <div className="mt-3 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <button
                        type="button"
                        onClick={() => decrement(product.id)}
                        aria-label={`Diminuir quantidade de ${product.name}`}
                        className="flex h-8 w-8 items-center justify-center rounded-sm border border-border text-char transition-colors hover:bg-muted"
                      >
                        <Minus size={14} />
                      </button>
                      <span className="w-6 text-center text-sm font-medium text-char">
                        {quantity}
                      </span>
                      <button
                        type="button"
                        onClick={() => increment(product.id)}
                        aria-label={`Aumentar quantidade de ${product.name}`}
                        className="flex h-8 w-8 items-center justify-center rounded-sm border border-border text-char transition-colors hover:bg-muted"
                      >
                        <Plus size={14} />
                      </button>
                    </div>
                    <span className="font-display text-lg font-semibold text-brick">
                      {currencyFormatter.format(product.price * quantity)}
                    </span>
                  </div>
                </div>
              </li>
            ))}
          </ul>

          <div className="h-fit rounded-lg border border-border p-6">
            <h2 className="font-semibold text-char">Resumo</h2>
            <div className="mt-4 flex justify-between text-sm text-muted-foreground">
              <span>
                {itemCount} {itemCount === 1 ? "item" : "itens"}
              </span>
              <span>{currencyFormatter.format(subtotal)}</span>
            </div>
            <div className="mt-4 flex justify-between border-t border-border pt-4 text-lg font-semibold text-char">
              <span>Total</span>
              <span>{currencyFormatter.format(subtotal)}</span>
            </div>

            <Link
              href="/checkout"
              className="mt-6 block w-full rounded-sm bg-brick px-6 py-3 text-center text-sm font-medium text-background transition-colors hover:bg-brick-dark"
            >
              Finalizar pedido
            </Link>
            <Link
              href="/#cardapio"
              className="mt-3 block text-center text-sm text-muted-foreground hover:text-brick"
            >
              Continuar comprando
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}