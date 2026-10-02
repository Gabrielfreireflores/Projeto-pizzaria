export type PaymentMethod = "dinheiro" | "cartao" | "pix";

export interface CheckoutFormData {
  name: string;
  phone: string;
  cep: string;
  address: string;
  number: string;
  complement: string;
  neighborhood: string;
  city: string;
  state: string;
  paymentMethod: PaymentMethod;
}

export type CheckoutFormErrors = Partial<Record<keyof CheckoutFormData, string>>;