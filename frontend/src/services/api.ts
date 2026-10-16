// frontend/src/services/api.ts
export class ApiError extends Error {
  status: number;
  data: any;
  constructor(status: number, message: string, data: any = null) {
    super(message);
    this.status = status;
    this.data = data;
  }
}

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? ''; // vazio = usa o proxy

export async function apiFetch<T = any>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const { headers, ...rest } = options;
  const res = await fetch(`${API_URL}${endpoint}`, {
    credentials: 'include',
    ...rest,
    headers: {
      ...(rest.body ? { 'Content-Type': 'application/json' } : {}),
      ...headers,
    },
  });

  const isJson = (res.headers.get('content-type') ?? '').includes('application/json');
  const data = isJson ? await res.json() : null;

  if (!res.ok) {
    throw new ApiError(res.status, data?.erro ?? data?.mensagem ?? `Erro HTTP ${res.status}`, data);
  }
  return data as T;
}

export const api = {
  login: (email: string, senha: string) =>
    apiFetch('/api/v1/login', { method: 'POST', body: JSON.stringify({ email, senha }) }),
  usuarioAtual: () => apiFetch('/api/v1/me'),
  logout: () => apiFetch('/api/v1/logout', { method: 'POST' }),
  cardapio: () => apiFetch('/api/v1/cardapio'),
  // o resto (clientes, produtos, pedidos) você adiciona no mesmo padrão, conforme integrar
};