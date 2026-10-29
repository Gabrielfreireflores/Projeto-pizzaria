import { api, ApiError } from "@/lib/api";
import { NewOrder, Order, OrderItem, OrderStatus, PaymentMethod } from "@/types/order";

const PAYMENT_LABEL: Record<PaymentMethod, string> = {
  pix: "Pix",
  cartao: "Cartão",
  dinheiro: "Dinheiro",
};

const STATUS_BY_NAME: Record<string, OrderStatus> = {
  recebido: "recebido",
  "em preparação": "em_preparo",
  "saiu para entrega": "pronto",
  entregue: "entregue",
};

interface ApiPedido {
  id_pedido: number;
  status: string;
  data_hora_pedido: string;
  valor_total: string | number;
}

/** "Rua das Flores, 123" -> rua + número. Sem número no fim, vai tudo como rua. */
function splitAddress(address: string) {
  const text = address.trim();
  const match = text.match(/^(.*?)[,\s]+(\d+[\w/-]*)$/);
  if (match && match[1].trim().length >= 2) {
    return { logradouro: match[1].trim(), numero: match[2] };
  }
  return { logradouro: text };
}

/**
 * O backend não aceita o mesmo produto duas vezes no pedido. Linhas do carrinho
 * que cobram o mesmo produto (ex.: com observações diferentes) viram um item só.
 */
function toApiItems(items: OrderItem[]) {
  const grouped = new Map<number, { quantidade: number; partes: { quantidade: number; obs: string }[]; bordas: Map<number, number> }>();

  for (const item of items) {
    if (!item.productId) {
      throw new Error(
        `"${item.name}" está desatualizado. Remova da sacola e adicione de novo.`
      );
    }
    const entry = grouped.get(item.productId) ?? { quantidade: 0, partes: [], bordas: new Map<number, number>() };
    entry.quantidade += item.quantity;
    entry.partes.push({ quantidade: item.quantity, obs: [item.orderNote, item.border ? `Borda: ${item.border.name}` : ""].filter(Boolean).join(" - ") });
    if (item.border) entry.bordas.set(item.border.productId, (entry.bordas.get(item.border.productId) ?? 0) + item.quantity);
    grouped.set(item.productId, entry);
  }

  return [...grouped].map(([id_produto, { quantidade, partes, bordas }]) => {
    const observacao =
      partes.length === 1
        ? partes[0].obs
        : partes.map((p) => `${p.quantidade}x ${p.obs || "sem observação"}`).join(" | ");
    if (observacao.length > 500) {
      throw new Error('As observações deste produto ultrapassam 500 caracteres. Reduza as observações na sacola.');
    }
    return {
      id_produto,
      quantidade,
      observacao: observacao || null,
      bordas: [...bordas].map(([id_produto, quantidade]) => ({ id_produto, quantidade })),
    };
  });
}

/** Cria o pedido para o cliente autenticado; uma sessão expirada preserva a sacola. */
export async function createOrder(data: NewOrder): Promise<Order> {
  const body = {
    contato: { nome: data.customer.name, telefone: data.customer.phone },
    tipo_entrega: data.fulfillment,
    ...(data.delivery && {
      endereco: {
        ...splitAddress(data.delivery.address),
        bairro: data.delivery.neighborhood,
      },
    }),
    forma_pagamento: PAYMENT_LABEL[data.paymentMethod],
    itens: toApiItems(data.items),
  };

  let pedido: ApiPedido;
  try {
    pedido = await api<ApiPedido>("/api/v1/pedidos", {
      method: "POST",
      body: JSON.stringify(body),
    });
  } catch (e) {
    if (e instanceof ApiError && e.status === 401 && typeof window !== "undefined") {
      window.location.assign("/login?next=/checkout&expirada=1");
    }
    throw e;
  }

  return {
    ...data,
    number: `#${pedido.id_pedido}`,
    status: STATUS_BY_NAME[pedido.status.trim().toLowerCase()] ?? "recebido",
    createdAt: pedido.data_hora_pedido,
    total: Number(pedido.valor_total), // valor confirmado pelo backend (inclui taxa)
  };
}
