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
  "salgada-bauru": "/produtos/salgada-bauru.webp",
  "salgada-portuguesa": "/produtos/salgada-portuguesa.webp",
  "salgada-milho": "/produtos/salgada-milho.webp",
  "salgada-paulista": "/produtos/salgada-paulista.webp",
  "salgada-palmito": "/produtos/salgada-palmito.webp",
  "salgada-milho-c-catupiry": "/produtos/salgada-milho-c-catupiry.webp",
  "salgada-bacon": "/produtos/salgada-bacon.webp",
  "salgada-caipira": "/produtos/salgada-caipira.webp",
  "salgada-brocolis": "/produtos/salgada-brocolis.webp",
  "salgada-americana": "/produtos/salgada-americana.webp",
  "salgada-brocolis-c-catupiry": "/produtos/salgada-brocolis-c-catupiry.webp",
  "salgada-calabresa-c-catupiry": "/produtos/salgada-calabresa-c-catupiry.webp",
  "salgada-baiana": "/produtos/salgada-baiana.webp",
  "salgada-lombo": "/produtos/salgada-lombo.webp",
  "salgada-mexicana": "/produtos/salgada-mexicana.webp",
  "salgada-a-moda-da-casa": "/produtos/salgada-a-moda-da-casa.webp",
  "salgada-atum": "/produtos/salgada-atum.webp",
  "salgada-pizzaiolo": "/produtos/salgada-pizzaiolo.webp",
  "salgada-toscana-c-catupiry": "/produtos/salgada-toscana-c-catupiry.webp",
  "salgada-mineira": "/produtos/salgada-mineira.webp",
  "salgada-brocolis-bacon": "/produtos/salgada-brocolis-bacon.webp",
  "salgada-frango-cheddar": "/produtos/salgada-frango-cheddar.webp",
  "salgada-toscana-c-cheddar": "/produtos/salgada-toscana-c-cheddar.webp",
  "salgada-dois-queijos": "/produtos/salgada-dois-queijos.webp",
  "salgada-calabresa-paulistana": "/produtos/salgada-calabresa-paulistana.webp",
  "doce-chocolate": "/produtos/doce-chocolate.webp",
  "doce-prestigio": "/produtos/doce-prestigio.webp",
  "doce-banana": "/produtos/doce-banana.webp",
  "doce-banana-chok": "/produtos/doce-banana-chok.webp",
  "salgada-mussarela": "/produtos/salgada-mussarela.webp",
  "salgada-chefinho": "/produtos/salgada-chefinho.webp",
  "doce-chocolate-c-morango": "/produtos/doce-chocolate-c-morango.webp",
  "salgada-marguerita": "/produtos/salgada-marguerita.webp",
  "salgada-calabresa": "/produtos/salgada-calabresa.webp",
  "salgada-quatro-queijos": "/produtos/salgada-quatro-queijos.webp",
  "salgada-frango-c-catupiry": "/produtos/salgada-frango-c-catupiry.webp",
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
