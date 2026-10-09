import { Size } from "./product";

export type PaymentMethod = "dinheiro" | "cartao" | "pix";

export type FulfillmentMethod = "entrega" | "retirada";

export interface CheckoutFormData {
  name: string;
  phone: string;
  address: string;
  neighborhood: string;
  paymentMethod: PaymentMethod;
  fulfillment: FulfillmentMethod;
}

export type CheckoutFormErrors = Partial<Record<keyof CheckoutFormData, string>>;

export type OrderStatus = "recebido" | "em_preparo" | "pronto" | "entregue";

export const ORDER_STATUS_LABEL: Record<OrderStatus, string> = {
  recebido: "Recebido",
  em_preparo: "Em preparo",
  pronto: "Pronto",
  entregue: "Entregue",
};

export interface OrderItem {
  menuItemId: string;
  size?: Size;
  halfMenuItemId?: string;
  note?: string;
  name: string;
  quantity: number;
  unitPrice: number;
}

export interface Order {
  number: string;
  status: OrderStatus;
  createdAt: string;
  customer: { name: string; phone: string };
  fulfillment: FulfillmentMethod;
  /** Só existe quando fulfillment é "entrega". */
  delivery?: { address: string; neighborhood: string };
  paymentMethod: PaymentMethod;
  items: OrderItem[];
  total: number;
}

/** Dados que o checkout envia; número, status e data são definidos ao criar. */
export type NewOrder = Omit<Order, "number" | "status" | "createdAt">;