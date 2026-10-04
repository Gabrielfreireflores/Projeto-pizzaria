import { MenuItem, ProductCategory, Size } from "@/types/product";

export const SIZE_LABEL: Record<Size, string> = { P: "Pequena", G: "Grande" };

export const CATEGORY_LABEL: Record<ProductCategory, string> = {
  salgada: "Pizzas Salgadas",
  doce: "Pizzas Doces",
  borda: "Bordas",
  bebida: "Bebidas",
};

const SEM_FOTO = "/produtos/sem-foto.svg";
const unsplash = (photo: string) =>
  `https://images.unsplash.com/photo-${photo}?w=600&q=80`;

// Fotos por id. Item que não estiver aqui usa SEM_FOTO.
// Para trocar/adicionar uma foto, basta editar esta tabela.
const FOTOS: Record<string, string> = {
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

const slug = (text: string) =>
  text
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");

// Mesma ordem do PDF: preço G, depois preço P.
const preco = (G: number, P: number): Record<Size, number> => ({ G, P });

function criar(
  category: ProductCategory,
  name: string,
  extra: Partial<Pick<MenuItem, "ingredients" | "prices" | "price">>
): MenuItem {
  const id = `${category}-${slug(name)}`;
  return { id, category, name, image: FOTOS[id] ?? SEM_FOTO, ...extra };
}

const salgada = (name: string, ingredients: string, prices: Record<Size, number>) =>
  criar("salgada", name, { ingredients, prices });
const doce = (name: string, ingredients: string, prices: Record<Size, number>) =>
  criar("doce", name, { ingredients, prices });
const borda = (name: string, prices: Record<Size, number>) =>
  criar("borda", name, { prices });
const bebida = (name: string, price: number) => criar("bebida", name, { price });

export const menu: MenuItem[] = [
  // Pizzas Salgadas
  salgada("Mussarela", "mussarela, tomate", preco(45, 30)),
  salgada("Calabresa", "cebola, calabresa, mussarela, tomate", preco(45, 30)),
  salgada("Bauru", "presunto, mussarela, tomate", preco(45, 30)),
  salgada("Marguerita", "mussarela, parmesão, manjericão, tomate", preco(45, 30)),
  salgada("Milho", "mussarela, milho, tomate", preco(45, 30)),
  salgada("Milho c/ Catupiry", "mussarela, milho, catupiry", preco(50, 35)),
  salgada("Frango c/ Catupiry", "frango, mussarela, catupiry", preco(50, 35)),
  salgada("Caipira", "mussarela, frango, milho, catupiry", preco(50, 35)),
  salgada("Americana", "frango, bacon, mussarela, cheddar", preco(50, 35)),
  salgada("Calabresa c/ Catupiry", "calabresa, mussarela, catupiry", preco(50, 35)),
  salgada("Quatro Queijos", "mussarela, catupiry, parmesão, provolone", preco(50, 35)),
  salgada("Portuguesa", "presunto, palmito, ervilha, ovo, tomate, cebola, mussarela", preco(50, 35)),
  salgada("Paulista", "presunto, palmito, ervilha, mussarela, cebola, tomate, bacon", preco(50, 35)),
  salgada("Chefinho", "calabresa, frango, milho, mussarela, catupiry", preco(50, 35)),
  salgada("Palmito", "palmito, mussarela, tomate", preco(50, 35)),
  salgada("Bacon", "bacon, mussarela, tomate", preco(50, 35)),
  salgada("Brócolis", "brócolis, mussarela, cebola, tomate, alho frito", preco(48, 30)),
  salgada("Brócolis c/ Catupiry", "mussarela, brócolis, catupiry, bacon", preco(50, 35)),
  salgada("Lombo", "mussarela, lombo, catupiry", preco(50, 35)),
  salgada("Atum", "mussarela, atum, cebola", preco(48, 30)),
  salgada("Mineira", "presunto, mussarela, milho, catupiry", preco(50, 35)),
  salgada("Baiana", "calabresa, ovo, cebola, pimenta, mussarela", preco(48, 30)),
  salgada("Mexicana", "mussarela, cebola, bacon, alho frito, tomate, parmesão", preco(50, 35)),
  salgada("Pizzaiolo", "mussarela, presunto, catupiry, tomate, palmito", preco(50, 35)),
  salgada("Frango & Cheddar", "mussarela, frango, cheddar", preco(50, 35)),
  salgada("À Moda da Casa", "calabresa, ovo, milho, tomate, mussarela", preco(48, 30)),
  salgada("Brócolis & Bacon", "brócolis, mussarela, bacon", preco(48, 30)),
  salgada("Toscana c/ Catupiry", "calabresa moída, catupiry, cebola, mussarela", preco(50, 35)),
  salgada("Toscana c/ Cheddar", "calabresa moída, mussarela, cheddar", preco(50, 35)),
  salgada("Dois queijos", "mussarela, catupiry", preco(48, 30)),
  salgada("Calabresa Paulistana", "calabresa, cebola", preco(45, 30)),

  // Pizzas Doces
  doce("Chocolate", "chocolate, granulado", preco(50, 30)),
  doce("Chocolate c/ Morango", "chocolate, morango, leite condensado", preco(50, 30)),
  doce("Prestígio", "chocolate, coco ralado, leite condensado", preco(50, 30)),
  doce("Banana", "banana, canela e leite condensado", preco(45, 30)),
  doce("Banana Chok", "banana e chocolate", preco(50, 30)),

  // Bordas
  borda("Catupiry", preco(15, 8)),
  borda("Cheddar", preco(15, 8)),
  borda("Mussarela", preco(15, 8)),
  borda("Chocolate", preco(15, 8)),

  // Refrigerantes (preço único)
  bebida("Coca-Cola 2L", 15),
  bebida("Fanta Laranja 2L", 13),
  bebida("Sprite Limão 2L", 13),
  bebida("Jaboti 2L", 8),
  bebida("Coca-Cola Lata 350ml", 6),
];

/** Meio a meio: vale o preço da metade mais cara (regra a confirmar com a pizzaria). */
export function precoMeioAMeio(a: MenuItem, b: MenuItem, size: Size): number {
  return Math.max(a.prices?.[size] ?? 0, b.prices?.[size] ?? 0);
}