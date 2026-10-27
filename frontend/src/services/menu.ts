import { api } from "@/lib/api";
import { FOTOS, SEM_FOTO, slug } from "@/lib/data/products";
import { MenuItem, ProductCategory, Size } from "@/types/product";

interface ApiProduto {
  id_produto: number;
  nome: string;
  tamanho: string;
  preco: string;
  foto: string | null;
  descricao: string | null;
}

interface ApiCategoria {
  id_categoria: number;
  nome: string;
  produtos: ApiProduto[];
}

const norm = (text: string) => text.trim().toLowerCase();

// Categorias do backend -> categorias do frontend. Outras categorias são ignoradas.
const CATEGORY_BY_NAME: Record<string, ProductCategory> = {
  "pizzas salgadas": "salgada",
  "pizzas doces": "doce",
  bordas: "borda",
  bebidas: "bebida",
};

// No backend cada tamanho é um produto; "Único" (ou qualquer outro) = preço único.
const SIZE_BY_LABEL: Record<string, Size> = { pequena: "P", grande: "G" };

// Só aceita foto do backend se o Next puder exibi-la (arquivo local ou Unsplash).
const fotoValida = (foto: string | null) =>
  foto && (foto.startsWith("/") || foto.startsWith("https://images.unsplash.com/"))
    ? foto
    : undefined;

/** Lê o cardápio do backend e agrupa os produtos (um por tamanho) em itens com P/G. */
export async function fetchMenu(): Promise<MenuItem[]> {
  const { categorias } = await api<{ categorias: ApiCategoria[] }>("/api/v1/cardapio");

  const items = new Map<string, MenuItem & { order: number }>();

  for (const categoria of categorias) {
    const category = CATEGORY_BY_NAME[norm(categoria.nome)];
    if (!category) continue;

    for (const produto of categoria.produtos) {
      // Bordas são cadastradas como "Borda Catupiry" para não colidir com a pizza.
      const name = category === "borda" ? produto.nome.replace(/^borda\s+/i, "") : produto.nome;
      const id = `${category}-${slug(name)}`;
      const price = Number(produto.preco);
      const size = SIZE_BY_LABEL[norm(produto.tamanho)];

      let item = items.get(id);
      if (!item) {
        item = {
          id,
          category,
          name,
          image: FOTOS[id] ?? fotoValida(produto.foto) ?? SEM_FOTO,
          order: produto.id_produto,
        };
        items.set(id, item);
      }
      item.order = Math.min(item.order, produto.id_produto);
      item.ingredients ??= produto.descricao ?? undefined;

      if (size) {
        item.prices = { ...item.prices, [size]: price } as Record<Size, number>;
        item.productIds = { ...item.productIds, [size]: produto.id_produto };
      } else {
        item.price = price;
        item.productId = produto.id_produto;
      }
    }
  }

  return [...items.values()]
    .filter((item) => !item.prices || (item.prices.P && item.prices.G)) // precisa dos dois tamanhos
    .sort((a, b) => a.order - b.order)
    .map(({ order: _order, ...item }) => item);
}
