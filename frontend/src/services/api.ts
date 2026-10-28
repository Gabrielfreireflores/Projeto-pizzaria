// // frontend/src/services/api.ts
// export class ApiError extends Error {
//   status: number;
//   data: any;
//   constructor(status: number, message: string, data: any = null) {
//     super(message);
//     this.status = status;
//     this.data = data;
//   }
// }

// const API_URL = process.env.NEXT_PUBLIC_API_URL ?? ''; // vazio = usa o proxy

// export async function apiFetch<T = any>(
//   endpoint: string, options: RequestInit = {}): Promise<T> {
//   const { headers, ...rest } = options;
//   const res = await fetch(`${API_URL}${endpoint}`, {
//     credentials: 'include',
//     ...rest,
//     headers: {
//       ...(rest.body ? { 'Content-Type': 'application/json' } : {}),
//       ...headers,
//     },
//   });

//   const isJson = (res.headers.get('content-type') ?? '').includes('application/json');
//   const data = isJson ? await res.json() : null;

//   if (!res.ok) {
//     throw new ApiError(res.status, data?.erro ?? data?.mensagem ?? `Erro HTTP ${res.status}`, data);
//   }
//   return data as T;
// }

// export type NovoProduto = {
//   nome: string;
//   tamanho: string;
//   preco: number | string;
//   id_categoria: number;
//   disponivel: boolean;
//   ingredientes: { id_ingrediente: number; quantidade_necessaria: number | string }[];
// };

// export type NovoFuncionario = {
//   nome: string;
//   cpf: string;
//   cargo: string;
//   telefone: string;
//   email: string;
//   senha: string;
// };

// export type EdicaoFuncionario = {
//   nome: string;
//   cpf: string;
//   cargo: string;
//   telefone: string;
//   email: string;
//   ativo: boolean;
//   senha?: string; // só é enviada quando se quer trocar a senha
// };

// export const api = {
//   login: (email: string, senha: string) =>
//     apiFetch('/api/v1/login', { method: 'POST', body: JSON.stringify({ email, senha }) }),
//   usuarioAtual: () => apiFetch('/api/v1/me'),
//   logout: () => apiFetch('/api/v1/logout', { method: 'POST' }),
//   cardapio: () => apiFetch('/api/v1/cardapio'),
//   cadastrarCliente: (dados: {
//     nome: string;
//     cpf: string;
//     telefone: string;
//     email: string;
//     senha: string;
//   }) =>
//     apiFetch('/api/v1/clientes', { method: 'POST', body: JSON.stringify(dados) }),

//   // Funcionário
//   listarProdutos: () => apiFetch('/api/v1/produtos'),
//   criarProduto: (dados: NovoProduto) =>
//     apiFetch('/api/v1/produtos', { method: 'POST', body: JSON.stringify(dados) }),
//   atualizarProduto: (id: number, dados: NovoProduto) =>
//     apiFetch(`/api/v1/produtos/${id}`, { method: 'PUT', body: JSON.stringify(dados) }),
//   excluirProduto: (id: number) =>
//     apiFetch(`/api/v1/produtos/${id}`, { method: 'DELETE' }),
//   listarCategorias: () => apiFetch('/api/categorias'),
//   criarCategoria: (nome: string) =>
//     apiFetch('/api/categorias', { method: 'POST', body: JSON.stringify({ nome }) }),
//   listarIngredientes: () => apiFetch('/api/v1/ingredientes'),
//   criarIngrediente: (dados: {
//     nome: string;
//     unidade_medida: string;
//     quantidade_estoque: number | string;
//   }) => apiFetch('/api/v1/ingredientes', { method: 'POST', body: JSON.stringify(dados) }),

//   // Equipe
//   listarEquipe: () => apiFetch('/api/v1/funcionarios'),
//   criarFuncionario: (dados: NovoFuncionario) =>
//     apiFetch('/api/v1/funcionarios', { method: 'POST', body: JSON.stringify(dados) }),
//   atualizarFuncionario: (id: number, dados: EdicaoFuncionario) =>
//     apiFetch(`/api/v1/funcionarios/${id}`, { method: 'PUT', body: JSON.stringify(dados) }),
//   excluirFuncionario: (id: number) =>
//     apiFetch(`/api/v1/funcionarios/${id}`, { method: 'DELETE' }),

//   //Pedidos (funcionário)
//   listarPedidos: () => apiFetch('/api/v1/pedidos'),
//   aceitarPedido: (id: number) =>
//     apiFetch(`/api/v1/pedidos/${id}/aceitar`, { method: 'POST' }),
//   alterarStatusPedido: (id: number, status: string) =>
//     apiFetch(`/api/v1/pedidos/${id}/status`, {
//       method: 'PUT',
//       body: JSON.stringify({ status }),
//     }),
// };


export class ApiError extends Error {
  status: number;
  data: any;

  constructor(status: number, message: string, data: any = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

const API_URL = "";

export function urlFotoProduto(foto?: string | null): string | null {
  if (!foto) return null;

  if (/^https?:\/\//i.test(foto)) {
    return foto;
  }

  return foto.startsWith("/") ? foto : `/${foto}`;
}

export async function apiFetch<T = any>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const { headers, ...rest } = options;

  const isFormData =
    typeof FormData !== "undefined" && rest.body instanceof FormData;

  const res = await fetch(`${API_URL}${endpoint}`, {
    credentials: "include",
    ...rest,
    headers: {
      // O navegador define automaticamente o Content-Type e o boundary
      // quando o corpo é FormData.
      ...(rest.body && !isFormData
        ? { "Content-Type": "application/json" }
        : {}),
      ...headers,
    },
  });

  const contentType = res.headers.get("content-type") ?? "";
  const isJson = contentType.includes("application/json");

  const data = isJson ? await res.json() : null;

  if (!res.ok) {
    throw new ApiError(
      res.status,
      data?.erro ??
        data?.mensagem ??
        `Erro HTTP ${res.status}`,
      data
    );
  }

  return data as T;
}

// ============================================================
// TIPOS
// ============================================================

export type IngredienteProduto = {
  id_ingrediente: number;
  quantidade_necessaria: number | string;
};

export type NovoProduto = {
  nome: string;
  descricao?: string;
  tamanho: string;
  preco: number | string;
  id_categoria: number;
  disponivel: boolean;
  ingredientes: IngredienteProduto[];
};

export type ProdutoComFoto = NovoProduto & {
  // File é preenchido pelo input de seleção de imagem.
  // null ou undefined significa que nenhuma foto nova foi selecionada.
  foto?: File | null;
};

export type NovoFuncionario = {
  nome: string;
  cpf: string;
  cargo: string;
  telefone: string;
  email: string;
  senha: string;
};

export type EdicaoFuncionario = {
  nome: string;
  cpf: string;
  cargo: string;
  telefone: string;
  email: string;
  ativo: boolean;
  senha?: string;
};

// ============================================================
// PRODUTOS
// ============================================================

/**
 * Converte os dados do produto para FormData quando há uma foto.
 * Sem foto, mantém o envio JSON utilizado anteriormente.
 */
function prepararDadosProduto(dados: ProdutoComFoto): BodyInit {
  if (dados.foto) {
    const formData = new FormData();

    formData.append("nome", dados.nome);
    if (dados.descricao !== undefined) formData.append("descricao", dados.descricao);
    formData.append("tamanho", dados.tamanho);
    formData.append("preco", String(dados.preco));
    formData.append("id_categoria", String(dados.id_categoria));
    formData.append("disponivel", String(dados.disponivel));
    formData.append("ingredientes", JSON.stringify(dados.ingredientes));
    formData.append("foto", dados.foto);

    return formData;
  }

  const { foto: _foto, ...produto } = dados;
  return JSON.stringify(produto);
}

export const api = {
  // ----------------------------------------------------------
  // AUTENTICAÇÃO
  // ----------------------------------------------------------

  login: (email: string, senha: string) =>
    apiFetch("/api/v1/login", {
      method: "POST",
      body: JSON.stringify({ email, senha }),
    }),

  usuarioAtual: () => apiFetch("/api/v1/me"),

  logout: () =>
    apiFetch("/api/v1/logout", {
      method: "POST",
    }),

  // ----------------------------------------------------------
  // CARDÁPIO
  // ----------------------------------------------------------

  cardapio: () => apiFetch("/api/v1/cardapio"),

  // ----------------------------------------------------------
  // CLIENTES
  // ----------------------------------------------------------

  cadastrarCliente: (dados: {
    nome: string;
    telefone: string;
    email: string;
    senha: string;
  }) =>
    apiFetch("/api/v1/clientes", {
      method: "POST",
      body: JSON.stringify(dados),
    }),

  // ----------------------------------------------------------
  // PRODUTOS
  // ----------------------------------------------------------

  listarProdutos: () => apiFetch("/api/v1/produtos"),

  criarProduto: (dados: ProdutoComFoto) =>
    apiFetch("/api/v1/produtos", {
      method: "POST",
      body: prepararDadosProduto(dados),
    }),

  atualizarProduto: (id: number, dados: ProdutoComFoto) =>
    apiFetch(`/api/v1/produtos/${id}`, {
      method: "PUT",
      body: prepararDadosProduto(dados),
    }),

  excluirProduto: (id: number) =>
    apiFetch(`/api/v1/produtos/${id}`, {
      method: "DELETE",
    }),

  // ----------------------------------------------------------
  // CATEGORIAS
  // ----------------------------------------------------------

  listarCategorias: () => apiFetch("/api/categorias"),

  criarCategoria: (nome: string) =>
    apiFetch("/api/categorias", {
      method: "POST",
      body: JSON.stringify({ nome }),
    }),

  // ----------------------------------------------------------
  // INGREDIENTES
  // ----------------------------------------------------------

  listarIngredientes: () => apiFetch("/api/v1/ingredientes"),

  criarIngrediente: (dados: {
    nome: string;
    unidade_medida: string;
    quantidade_estoque: number | string;
  }) =>
    apiFetch("/api/v1/ingredientes", {
      method: "POST",
      body: JSON.stringify(dados),
    }),

  // ----------------------------------------------------------
  // FUNCIONÁRIOS
  // ----------------------------------------------------------

  listarEquipe: () => apiFetch("/api/v1/funcionarios"),

  criarFuncionario: (dados: NovoFuncionario) =>
    apiFetch("/api/v1/funcionarios", {
      method: "POST",
      body: JSON.stringify(dados),
    }),

  atualizarFuncionario: (id: number, dados: EdicaoFuncionario) =>
    apiFetch(`/api/v1/funcionarios/${id}`, {
      method: "PUT",
      body: JSON.stringify(dados),
    }),

  excluirFuncionario: (id: number) =>
    apiFetch(`/api/v1/funcionarios/${id}`, {
      method: "DELETE",
    }),

  // ----------------------------------------------------------
  // PEDIDOS
  // ----------------------------------------------------------

  listarPedidos: () => apiFetch("/api/v1/pedidos"),

  aceitarPedido: (id: number) =>
    apiFetch(`/api/v1/pedidos/${id}/aceitar`, {
      method: "POST",
    }),

  alterarStatusPedido: (id: number, status: string) =>
    apiFetch(`/api/v1/pedidos/${id}/status`, {
      method: "PUT",
      body: JSON.stringify({ status }),
    }),
};
