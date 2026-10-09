export type ProductCategory = "salgada" | "doce" | "borda" | "bebida";

export type Size = "P" | "G";

/** Item do cardápio: um sabor com os dois tamanhos. */
export interface MenuItem {
  id: string;
  category: ProductCategory;
  name: string;
  ingredients?: string;
  prices?: Record<Size, number>; // itens com tamanho P/G
  price?: number; // itens de preço único (bebidas)
  image: string;
}

/** Linha do carrinho: um item do cardápio já com o tamanho escolhido. */
export interface Product {
  id: string;
  category: ProductCategory;
  name: string;
  description: string;
  price: number;
  image: string;
  /** Item de origem no cardápio e tamanho escolhido (usados no pedido). */
  menuItemId?: string;
  size?: Size;
  /** Segundo sabor, quando a pizza é meio a meio. */
  halfMenuItemId?: string;
  /** Observação do cliente (ex.: retirar ingredientes). */
  note?: string;
}