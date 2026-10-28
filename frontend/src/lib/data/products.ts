import { MenuItem, ProductCategory, Size } from "@/types/product";

export const SIZE_LABEL: Record<Size, string> = { P: "Pequena", G: "Grande" };

export const CATEGORY_LABEL: Record<ProductCategory, string> = {
  salgada: "Pizzas Salgadas",
  doce: "Pizzas Doces",
  borda: "Bordas",
  bebida: "Bebidas",
};

export const SEM_FOTO = "/produtos/sem-foto.svg";
const unsplash = (photo: string) =>
  `https://images.unsplash.com/photo-${photo}?w=600&q=80`;

// O cardápio (sabores, tamanhos e preços) agora vem do backend
// (db/migrations/004_seed_cardapio_v2.sql). Aqui ficam só as fotos por id.
// Item que não estiver aqui usa a foto do backend (se houver) ou SEM_FOTO.
export const FOTOS: Record<string, string> = {
  "salgada-mussarela": "/produtos/salgada-mussarela.webp",
  "salgada-chefinho": "/produtos/salgada-chefinho.webp",
  "doce-chocolate-c-morango": "/produtos/doce-chocolate-c-morango.webp",
  "salgada-marguerita": unsplash("1574071318508-1cdbab80d002"),
  "salgada-calabresa": unsplash("1628840042765-356cda07504e"),
  "salgada-quatro-queijos": unsplash("1513104890138-7c749659a591"),
  "salgada-frango-c-catupiry": unsplash("1601924582970-9238bcb495d9"),
  "bebida-coca-cola-2l": "/coca2l.png",
  "bebida-fanta-laranja-2l": "/fanta2l.png",
  "bebida-sprite-limao-2l": "/sprite2l.png",
  "bebida-jaboti-2l": "/jaboti2l.png",
  "bebida-coca-cola-lata-350ml": unsplash("1554866585-cd94860890b7"),
};

export const slug = (text: string) =>
  text
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");

/** Meio a meio: vale o preço da metade mais cara (regra a confirmar com a pizzaria). */
export function precoMeioAMeio(a: MenuItem, b: MenuItem, size: Size): number {
  return Math.max(a.prices?.[size] ?? 0, b.prices?.[size] ?? 0);
}
