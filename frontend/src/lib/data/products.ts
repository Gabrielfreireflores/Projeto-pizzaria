import { Product } from "@/types/product";

export const products: Product[] = [
  {
    id: "pizza-margherita",
    category: "pizza",
    name: "Margherita",
    description: "Molho de tomate fresco, mussarela, manjericão e azeite.",
    price: 42.9,
    image:
      "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=600&q=80",
  },
  {
    id: "pizza-calabresa",
    category: "pizza",
    name: "Calabresa",
    description: "Calabresa fatiada, cebola roxa e azeitonas pretas.",
    price: 44.9,
    image:
      "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=600&q=80",
  },
  {
    id: "pizza-quatro-queijos",
    category: "pizza",
    name: "Quatro Queijos",
    description: "Mussarela, provolone, parmesão e gorgonzola.",
    price: 49.9,
    image:
      "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600&q=80",
  },
  {
    id: "pizza-frango-catupiry",
    category: "pizza",
    name: "Frango com Catupiry",
    description: "Frango desfiado temperado e catupiry cremoso.",
    price: 46.9,
    image:
      "https://images.unsplash.com/photo-1601924582970-9238bcb495d9?w=600&q=80",
  },
  {
    id: "bebida-coca-lata",
    category: "bebida",
    name: "Coca-Cola Lata",
    description: "350ml, bem gelada.",
    price: 6.5,
    image:
      "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=600&q=80",
  },
  {
    id: "bebida-guarana-lata",
    category: "bebida",
    name: "Guaraná Antarctica Lata",
    description: "350ml, bem gelada.",
    price: 6.5,
    image:
      "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=600&q=80",
  },
  {
    id: "bebida-suco-laranja",
    category: "bebida",
    name: "Suco de Laranja Natural",
    description: "500ml, feito na hora.",
    price: 9.9,
    image:
      "https://images.unsplash.com/photo-1613478223719-2ab802602423?w=600&q=80",
  },
];