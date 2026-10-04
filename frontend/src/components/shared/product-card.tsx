"use client";

import Image from "next/image";
import { useState } from "react";
import { MenuItem, Size } from "@/types/product";
import { SIZE_LABEL, menu, precoMeioAMeio } from "@/lib/data/products";
import { useCart } from "@/hooks/use-cart";

const currencyFormatter = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

const SIZES: Size[] = ["P", "G"];

function hash(text: string) {
  let h = 0;
  for (const char of text) h = (h * 31 + char.charCodeAt(0)) >>> 0;
  return h.toString(36);
}

function chipClass(active: boolean) {
  return `rounded-full border px-3 py-1 text-xs font-medium transition-colors ${
    active
      ? "border-brick bg-brick/10 text-brick"
      : "border-border text-char hover:border-brick/50"
  }`;
}

export function ProductCard({ item }: { item: MenuItem }) {
  const { addItem } = useCart();
  const [size, setSize] = useState<Size>("G");
  const [added, setAdded] = useState(false);
  const [halfMode, setHalfMode] = useState(false);
  const [halfId, setHalfId] = useState("");
  const [showNote, setShowNote] = useState(false);
  const [note, setNote] = useState("");

  const prices = item.prices;
  const isPizza = item.category === "salgada" || item.category === "doce";
  const half = halfMode ? menu.find((m) => m.id === halfId) : undefined;
  const waitingHalf = halfMode && !half;

  const priceFor = (s: Size) =>
    prices ? (half ? precoMeioAMeio(item, half, s) : prices[s]) : (item.price ?? 0);
  const price = prices ? priceFor(size) : (item.price ?? 0);

  function handleAdd() {
    if (waitingHalf) return;
    const cleanNote = note.trim();
    const label =
      item.category === "borda"
        ? `Borda ${item.name}`
        : half
          ? `Meio a meio: ${item.name} / ${half.name}`
          : item.name;

    const idParts = [half ? `${item.id}+${half.id}` : item.id];
    if (prices) idParts.push(size);
    if (cleanNote) idParts.push(`obs${hash(cleanNote.toLowerCase())}`);

    addItem({
      id: idParts.join("-"),
      category: item.category,
      name: prices ? `${label} (${SIZE_LABEL[size]})` : label,
      description: half
        ? `½ ${item.name}: ${item.ingredients}; ½ ${half.name}: ${half.ingredients}`
        : (item.ingredients ?? ""),
      price,
      image: item.image,
      menuItemId: item.id,
      size: prices ? size : undefined,
      halfMenuItemId: half?.id,
      note: cleanNote || undefined,
    });

    setAdded(true);
    setTimeout(() => setAdded(false), 1500);
    setNote("");
    setShowNote(false);
    setHalfMode(false);
    setHalfId("");
  }

  return (
    <div className="flex flex-col overflow-hidden rounded-lg border border-border bg-background shadow-sm">
      <div className="relative h-40 w-full sm:h-44">
        <Image
          src={item.image}
          alt={item.name}
          fill
          sizes="(min-width: 1280px) 25vw, (min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw"
          className="object-cover"
        />
      </div>

      <div className="flex flex-1 flex-col p-4">
        <h3 className="text-lg font-semibold text-char">{item.name}</h3>
        {item.ingredients && (
          <p className="mt-1 text-sm leading-relaxed text-muted-foreground first-letter:uppercase">
            {item.ingredients}
          </p>
        )}

        <div className="mt-auto pt-4">
          {prices && (
            <div
              role="radiogroup"
              aria-label={`Tamanho de ${item.name}`}
              className="grid grid-cols-2 gap-2"
            >
              {SIZES.map((option) => {
                const selected = size === option;
                return (
                  <button
                    key={option}
                    type="button"
                    role="radio"
                    aria-checked={selected}
                    onClick={() => setSize(option)}
                    className={`rounded-sm border px-3 py-2 text-left transition-colors ${
                      selected
                        ? "border-brick bg-brick/10 text-brick"
                        : "border-border text-char hover:border-brick/50"
                    }`}
                  >
                    <span className="block text-xs">
                      {option} · {SIZE_LABEL[option]}
                    </span>
                    <span className="block text-sm font-semibold">
                      {currencyFormatter.format(priceFor(option))}
                    </span>
                  </button>
                );
              })}
            </div>
          )}

          {isPizza && (
            <div className="mt-3 space-y-2">
              <div className="flex flex-wrap gap-2">
                <button
                  type="button"
                  aria-pressed={halfMode}
                  onClick={() => {
                    setHalfMode((value) => !value);
                    setHalfId("");
                  }}
                  className={chipClass(halfMode)}
                >
                  Meio a meio
                </button>
                <button
                  type="button"
                  aria-pressed={showNote}
                  onClick={() => setShowNote((value) => !value)}
                  className={chipClass(showNote || note.trim() !== "")}
                >
                  Observação
                </button>
              </div>

              {halfMode && (
                <>
                  <select
                    value={halfId}
                    onChange={(e) => setHalfId(e.target.value)}
                    aria-label="Segundo sabor"
                    className="w-full rounded-sm border border-border bg-background px-3 py-2 text-sm text-char outline-none focus:border-brick"
                  >
                    <option value="">Escolha o segundo sabor</option>
                    {menu
                      .filter((m) => m.category === item.category && m.id !== item.id)
                      .map((m) => (
                        <option key={m.id} value={m.id}>
                          {m.name}
                        </option>
                      ))}
                  </select>
                  {half && (
                    <p className="text-xs text-muted-foreground first-letter:uppercase">
                      {half.name}: {half.ingredients}
                    </p>
                  )}
                </>
              )}

              {showNote && (
                <input
                  value={note}
                  maxLength={80}
                  onChange={(e) => setNote(e.target.value)}
                  placeholder="Ex.: sem cebola, sem azeitona"
                  aria-label="Observação do item"
                  className="w-full rounded-sm border border-border px-3 py-2 text-sm outline-none focus:border-brick"
                />
              )}
            </div>
          )}

          <button
            type="button"
            onClick={handleAdd}
            disabled={waitingHalf}
            className={`${prices ? "mt-3" : ""} w-full rounded-sm bg-brick px-4 py-3 text-sm font-medium text-background transition-colors hover:bg-brick-dark disabled:cursor-not-allowed disabled:opacity-50`}
          >
            {added
              ? "Adicionado!"
              : waitingHalf
                ? "Escolha o segundo sabor"
                : `Adicionar · ${currencyFormatter.format(price)}`}
          </button>
        </div>
      </div>
    </div>
  );
}