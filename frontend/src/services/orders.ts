import { NewOrder, Order } from "@/types/order";

// Camada de acesso a pedidos. Hoje grava no localStorage; quando o backend
// estiver pronto, só o corpo destas funções muda (a assinatura continua igual).
const STORAGE_KEY = "pizzaria-orders";

function readAll(): Order[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? (JSON.parse(raw) as Order[]) : [];
  } catch {
    return [];
  }
}

function writeAll(orders: Order[]) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(orders));
  } catch {
    // armazenamento indisponível: o pedido ainda é confirmado na tela
  }
}

export async function createOrder(data: NewOrder): Promise<Order> {
  const order: Order = {
    ...data,
    number: `#${Date.now().toString().slice(-6)}`,
    status: "recebido",
    createdAt: new Date().toISOString(),
  };
  writeAll([order, ...readAll()]);
  return order;
}