import { api } from "@/services/api";
import { MenuItem, ProductCategory, Size } from "@/types/product";

interface CardapioProduto {
  id_produto: number;
  nome: string;
  tamanho: string | null;
  preco: string; // o backend manda como texto: "49.90"
  foto: string | null;
  descricao: string | null;
}
interface CardapioCategoria {
  id_categoria: number;
  nome: string;
  produtos: CardapioProduto[];
}

const SEM_FOTO = "/produtos/sem-foto.svg";

const norm = (t: string) =>
  t.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
const slug = (t: string) => norm(t).replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");

// Nome da categoria no banco -> categoria do front.
const CATEGORIAS: Record<string, ProductCategory> = {
  pizzas: "salgada",
  "pizzas salgadas": "salgada",
  "pizzas doces": "doce",
  bordas: "borda",
  bebidas: "bebida",
};

const TAMANHOS: Record<string, Size> = {
  p: "P", pequena: "P", pequeno: "P",
  g: "G", grande: "G",
};

export async function fetchMenu(): Promise<MenuItem[]> {
  const { categorias } = (await api.cardapio()) as { categorias: CardapioCategoria[] };
  const itens = new Map<string, MenuItem>();

  for (const cat of categorias) {
    const category = CATEGORIAS[norm(cat.nome)];
    if (!category) continue; // categoria que o front ainda não conhece

    for (const p of cat.produtos) {
      const size = TAMANHOS[norm(p.tamanho ?? "")];
      const name = size ? p.nome : [p.nome, p.tamanho].filter(Boolean).join(" ");
      // Pizzas P/G viram um item só; o resto é um item por produto.
      const id = `${category}-${slug(name)}`;

      let item = itens.get(id);
      if (!item) {
        item = {
          id,
          category,
          name,
          ingredients: p.descricao ?? undefined,
          image: p.foto ?? SEM_FOTO,
          backendIds: {},
        };
        itens.set(id, item);
      }

      const preco = Number(p.preco);
      if (size) {
        item.prices = { ...item.prices, [size]: preco } as Record<Size, number>;
        item.backendIds![size] = p.id_produto;
      } else {
        item.price = preco;
        item.backendIds!.unico = p.id_produto;
      }
    }
  }

  return [...itens.values()];
}