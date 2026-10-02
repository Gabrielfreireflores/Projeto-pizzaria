export type ProductCategory = "pizza" | "bebida";

export interface Product {
  id: string;
  category: ProductCategory;
  name: string;
  description: string;
  price: number;
  image: string;
}