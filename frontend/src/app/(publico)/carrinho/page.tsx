"use client";

import Image from "next/image";
import Link from "next/link";
import { Minus, Plus, Trash2 } from "lucide-react";
import { useCart } from "@/hooks/use-cart";
import { buttonVariants } from "@/components/ui/button";
import { Navbar } from "@/components/shared/navbar";

const currencyFormatter = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

export default function CartPage() {
  const { items, increment, decrement, removeItem, clearCart, subtotal } =
    useCart();

  return (
    <main>
      <Navbar />
      <div className="mx-auto max-w-content px-4 py-12 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-semibold text-char">Sua sacola</h1>

        {items.length === 0 ? (
          <div className="mt-10 flex flex-col items-start gap-4">
            <p className="text-muted-foreground">Sua sacola está vazia.</p>
            <a href="/#cardapio" className={buttonVariants()}>
              Ver cardápio
            </a>
          </div>
        ) : (
          <div className="mt-8 grid gap-10 lg:grid-cols-3">
            <ul className="space-y-4 lg:col-span-2">
              {items.map(({ product, quantity }) => (
                <li
                  key={product.id}
                  className="flex items-center gap-4 rounded-lg border border-border p-4"
                >
                  <div className="relative h-20 w-20 shrink-0 overflow-hidden rounded-sm">
                    <Image
                      src={product.image}
                      alt={product.name}
                      fill
                      sizes="80px"
                      className="object-cover"
                    />
                  </div>

                  <div className="flex-1">
                    <p className="font-medium text-char">{product.name}</p>
                    <p className="text-sm text-muted-foreground">
                      {currencyFormatter.format(product.price)} un.
                    </p>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      aria-label="Diminuir quantidade"
                      onClick={() => decrement(product.id)}
                      className="flex h-8 w-8 items-center justify-center rounded-sm border border-border text-char hover:bg-char/5"
                    >
                      <Minus className="h-4 w-4" />
                    </button>
                    <span className="w-6 text-center text-sm font-medium">
                      {quantity}
                    </span>
                    <button
                      type="button"
                      aria-label="Aumentar quantidade"
                      onClick={() => increment(product.id)}
                      className="flex h-8 w-8 items-center justify-center rounded-sm border border-border text-char hover:bg-char/5"
                    >
                      <Plus className="h-4 w-4" />
                    </button>
                  </div>

                  <p className="w-20 text-right font-medium text-char">
                    {currencyFormatter.format(product.price * quantity)}
                  </p>

                  <button
                    type="button"
                    aria-label="Remover item"
                    onClick={() => removeItem(product.id)}
                    className="flex h-8 w-8 items-center justify-center rounded-sm text-muted-foreground hover:bg-char/5 hover:text-brick"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </li>
              ))}
            </ul>

            <div className="h-fit rounded-lg border border-border p-6">
              <div className="flex items-center justify-between text-sm text-muted-foreground">
                <span>Subtotal</span>
                <span>{currencyFormatter.format(subtotal)}</span>
              </div>
              <div className="mt-2 flex items-center justify-between text-lg font-semibold text-char">
                <span>Total</span>
                <span>{currencyFormatter.format(subtotal)}</span>
              </div>

              <a
                href="/checkout"
                className="mt-6 block rounded-sm bg-brick px-6 py-3 text-center text-sm font-medium text-background transition-colors hover:bg-brick-dark"
              >
                Finalizar pedido
              </a>
              <a href="/#cardapio" className="mt-3 block text-center text-sm font-medium text-brick hover:underline">
                Continuar comprando
              </a>
              <button
                type="button"
                onClick={clearCart}
                className="mt-3 w-full text-center text-sm text-muted-foreground hover:text-brick"
              >
                Esvaziar sacola
              </button>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}