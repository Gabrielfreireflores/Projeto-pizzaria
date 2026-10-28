"use client";

import Image from "next/image";
import { useEffect, useRef, useState } from "react";
import { X, Minus, Plus } from "lucide-react";
import { MenuItem, Size } from "@/types/product";
import { SIZE_LABEL, precoMeioAMeio } from "@/lib/data/products";
import { useCart } from "@/hooks/use-cart";

const money = (value: number) => value.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

interface ProductCardProps {
  item: MenuItem;
  menu: MenuItem[];
  expanded: boolean;
  onToggle: () => void;
}

export function ProductCard({ item, menu, expanded, onToggle }: ProductCardProps) {
  const { addItem } = useCart();
  const dialog = useRef<HTMLDialogElement>(null);
  const [size, setSize] = useState<Size>("G");
  const [halfId, setHalfId] = useState("");
  const [borderId, setBorderId] = useState("");
  const [note, setNote] = useState("");
  const [quantity, setQuantity] = useState(1);
  const isPizza = item.category === "salgada" || item.category === "doce";
  const half = menu.find(m => m.id === halfId && (m.category === "salgada" || m.category === "doce"));
  const border = menu.find(m => m.id === borderId);
  const pizzaPrice = item.prices
    ? half ? precoMeioAMeio(item, half, size) : item.prices[size]
    : item.price ?? 0;
  const borderPrice = border?.prices?.[size] ?? 0;
  const price = pizzaPrice + borderPrice;
  const startingAt = item.prices ? Math.min(item.prices.P, item.prices.G) : item.price ?? 0;

  useEffect(() => {
    if (!expanded) return;
    const node = dialog.current;
    const overflow = document.body.style.overflow;
    node?.showModal();
    document.body.style.overflow = "hidden";
    return () => {
      node?.close();
      document.body.style.overflow = overflow;
    };
  }, [expanded]);

  function handleAdd() {
    const billed = half && item.prices && (half.prices?.[size] ?? 0) > item.prices[size] ? half : item;
    const productId = item.prices ? billed.productIds?.[size] : item.productId;
    if (!productId || (border && !border.productIds?.[size])) return;
    const cleanNote = note.trim();
    const label = half ? `Meio a meio: ${item.name} / ${half.name}` : item.name;
    const orderNote = [half ? label : "", cleanNote].filter(Boolean).join(" - ") || undefined;
    const id = [item.id, size, halfId, borderId, cleanNote].join(":");
    addItem({
      id, category: item.category,
      name: item.prices ? `${label} (${SIZE_LABEL[size]})` : label,
      description: item.ingredients ?? "", price, image: item.image,
      menuItemId: item.id, size: item.prices ? size : undefined,
      productId, halfMenuItemId: half?.id, note: cleanNote || undefined, orderNote,
      border: border ? { productId: border.productIds![size]!, name: border.name, price: borderPrice } : undefined,
    }, quantity);
    onToggle();
  }

  return (
    <>
      <button type="button" onClick={onToggle} aria-haspopup="dialog" aria-expanded={expanded}
        className="group flex h-[330px] w-full flex-col overflow-hidden rounded-xl border border-border bg-background text-left shadow-sm transition hover:border-brick/50 hover:shadow-md focus-visible:outline focus-visible:outline-2 focus-visible:outline-brick sm:h-[350px]">
        <span className="relative block h-40 w-full shrink-0 sm:h-44">
          <Image src={item.image} alt={item.name} fill sizes="(min-width: 1280px) 25vw, (min-width: 640px) 50vw, 100vw" className="object-cover transition-transform group-hover:scale-105" />
        </span>
        <span className="flex min-h-0 flex-1 flex-col p-4">
          <span className="line-clamp-1 text-lg font-semibold text-char">{item.name}</span>
          <span className="mt-1 line-clamp-2 min-h-10 text-sm leading-5 text-muted-foreground first-letter:uppercase">{item.ingredients || "Confira as opções deste produto."}</span>
          <span className="mt-auto flex items-center justify-between gap-2 pt-3 text-sm font-semibold text-char">
            <span>{item.prices ? "A partir de " : ""}{money(startingAt)}</span>
            <Plus className="h-5 w-5 text-brick" aria-hidden="true" />
          </span>
        </span>
      </button>

      {expanded && (
        <dialog ref={dialog} aria-labelledby={`titulo-${item.id}`} onCancel={e => { e.preventDefault(); onToggle(); }}
          onClick={e => { if (e.target === e.currentTarget) onToggle(); }}
          className="m-auto max-h-[calc(100dvh-1rem)] w-[calc(100%-1rem)] max-w-4xl overflow-hidden rounded-2xl bg-background p-0 text-char shadow-2xl backdrop:bg-char/60 sm:max-h-[85dvh]">
          <div className="flex max-h-[calc(100dvh-1rem)] flex-col sm:max-h-[85dvh] sm:flex-row">
            <div className="relative hidden w-[43%] shrink-0 bg-muted sm:block">
              <Image src={item.image} alt={item.name} fill sizes="420px" className="object-cover" />
            </div>
            <div className="flex min-h-0 min-w-0 flex-1 flex-col">
              <header className="flex shrink-0 items-center justify-between gap-3 border-b border-border px-5 py-4">
                <h2 id={`titulo-${item.id}`} className="text-lg font-semibold">Monte seu pedido</h2>
                <button type="button" onClick={onToggle} aria-label="Fechar detalhes do produto" className="rounded-full bg-muted p-2 hover:bg-border"><X size={20} /></button>
              </header>
              <div className="min-h-0 space-y-5 overflow-y-auto p-5">
                <div className="relative h-40 overflow-hidden rounded-lg sm:hidden"><Image src={item.image} alt="" fill sizes="(max-width: 639px) 100vw, 1px" className="object-cover" /></div>
                <div>
                  <h3 className="font-display text-2xl font-semibold">{item.name}</h3>
                  <p className="mt-2 text-sm text-muted-foreground first-letter:uppercase">{item.ingredients}</p>
                </div>
                {item.prices && (
                  <fieldset>
                    <legend className="mb-2 font-semibold">Tamanho</legend>
                    <div className="grid grid-cols-2 gap-2">
                      {(["P", "G"] as Size[]).map(option => (
                        <label key={option} className={`cursor-pointer rounded-lg border p-3 text-sm ${size === option ? "border-brick bg-brick/10" : "border-border"}`}>
                          <input type="radio" name={`tamanho-${item.id}`} value={option} checked={size === option} onChange={() => setSize(option)} className="mr-2 accent-brick" />
                          {SIZE_LABEL[option]}<span className="mt-1 block font-semibold">{money(item.prices![option])}</span>
                        </label>
                      ))}
                    </div>
                  </fieldset>
                )}
                {isPizza && (
                  <>
                    <label className="block text-sm font-semibold">Segundo sabor (opcional)
                      <select value={halfId} onChange={e => setHalfId(e.target.value)} className="mt-2 w-full rounded-lg border border-border bg-background p-3 font-normal">
                        <option value="">Um sabor: {item.name}</option>
                        {(["salgada", "doce"] as const).map(category => (
                          <optgroup key={category} label={category === "salgada" ? "Pizzas salgadas" : "Pizzas doces"}>
                            {menu.filter(m => m.category === category && m.id !== item.id).map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
                          </optgroup>
                        ))}
                      </select>
                      <span className="mt-1 block text-xs font-normal text-muted-foreground">Combine sabores doces e salgados. Vale o preço do sabor de maior valor.</span>
                    </label>
                    <label className="block text-sm font-semibold">Borda (opcional)
                      <select value={borderId} onChange={e => setBorderId(e.target.value)} className="mt-2 w-full rounded-lg border border-border bg-background p-3 font-normal">
                        <option value="">Sem borda recheada</option>
                        {menu.filter(m => m.category === "borda" && m.productIds?.[size]).map(m => <option key={m.id} value={m.id}>{m.name} · + {money(m.prices?.[size] ?? 0)}</option>)}
                      </select>
                      <span className="mt-1 block text-xs font-normal text-muted-foreground">O tamanho da borda acompanha o da pizza.</span>
                    </label>
                  </>
                )}
                <label className="block text-sm font-semibold">Observação
                  <textarea value={note} maxLength={80} onChange={e => setNote(e.target.value)} placeholder="Ex.: sem cebola" rows={2} className="mt-2 w-full resize-none rounded-lg border border-border bg-background p-3 font-normal" />
                </label>
              </div>
              <footer className="flex shrink-0 items-center gap-3 border-t border-border bg-background p-4">
                <div className="flex items-center gap-2 rounded-lg bg-muted p-2">
                  <button type="button" aria-label="Diminuir quantidade" disabled={quantity <= 1} onClick={() => setQuantity(q => q - 1)} className="p-1 disabled:opacity-30"><Minus size={18} /></button>
                  <span className="min-w-5 text-center text-sm">{quantity}</span>
                  <button type="button" aria-label="Aumentar quantidade" disabled={quantity >= 99} onClick={() => setQuantity(q => q + 1)} className="p-1 disabled:opacity-30"><Plus size={18} /></button>
                </div>
                <button type="button" onClick={handleAdd} className="flex min-w-0 flex-1 flex-wrap items-center justify-between gap-1 rounded-lg bg-brick px-4 py-3 text-sm font-semibold text-background hover:bg-brick-dark">
                  <span>Adicionar</span><span>{money(price * quantity)}</span>
                </button>
              </footer>
            </div>
          </div>
        </dialog>
      )}
    </>
  );
}
