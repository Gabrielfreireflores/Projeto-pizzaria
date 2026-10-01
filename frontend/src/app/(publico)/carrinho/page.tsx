"use client";

import { useMemo, useState, type FormEvent } from "react";
import { useCart } from "@/hooks/use-cart";
import { Navbar } from "@/components/shared/navbar";
import { CheckoutFormData, CheckoutFormErrors, PaymentMethod } from "@/types/order";

const currencyFormatter = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

const INITIAL_FORM: CheckoutFormData = {
  name: "",
  phone: "",
  cep: "",
  address: "",
  number: "",
  complement: "",
  neighborhood: "",
  city: "",
  state: "",
  paymentMethod: "pix",
};

const PAYMENT_OPTIONS: { value: PaymentMethod; label: string }[] = [
  { value: "pix", label: "Pix" },
  { value: "cartao", label: "Cartão (crédito/débito na entrega)" },
  { value: "dinheiro", label: "Dinheiro" },
];

function validate(form: CheckoutFormData): CheckoutFormErrors {
  const errors: CheckoutFormErrors = {};

  if (form.name.trim().length < 3) {
    errors.name = "Informe seu nome completo.";
  }
  if (form.phone.replace(/\D/g, "").length < 10) {
    errors.phone = "Informe um telefone válido com DDD.";
  }
  if (form.cep.replace(/\D/g, "").length !== 8) {
    errors.cep = "CEP deve ter 8 dígitos.";
  }
  if (!form.address.trim()) {
    errors.address = "Informe o endereço.";
  }
  if (!form.number.trim()) {
    errors.number = "Informe o número.";
  }
  if (!form.neighborhood.trim()) {
    errors.neighborhood = "Informe o bairro.";
  }
  if (!form.city.trim()) {
    errors.city = "Informe a cidade.";
  }
  if (form.state.trim().length !== 2) {
    errors.state = "Use a sigla do estado (ex: SP).";
  }

  return errors;
}

interface OrderSnapshot {
  orderNumber: string;
  form: CheckoutFormData;
  items: { name: string; quantity: number; price: number }[];
  total: number;
}

export default function CheckoutPage() {
  const { items, subtotal, clearCart } = useCart();
  const [form, setForm] = useState<CheckoutFormData>(INITIAL_FORM);
  const [errors, setErrors] = useState<CheckoutFormErrors>({});
  const [order, setOrder] = useState<OrderSnapshot | null>(null);

  const isCartEmpty = items.length === 0;

  const total = useMemo(() => subtotal, [subtotal]);

  function updateField<K extends keyof CheckoutFormData>(
    field: K,
    value: CheckoutFormData[K]
  ) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const validationErrors = validate(form);
    setErrors(validationErrors);
    if (Object.keys(validationErrors).length > 0) return;

    const orderNumber = `#${Date.now().toString().slice(-6)}`;
    setOrder({
      orderNumber,
      form,
      items: items.map(({ product, quantity }) => ({
        name: product.name,
        quantity,
        price: product.price,
      })),
      total,
    });
    clearCart();
  }

  if (order) {
    return (
      <main>
        <Navbar />
        <div className="mx-auto max-w-content px-4 py-16 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-lg rounded-lg border border-border p-8 text-center">
            <span className="inline-block rounded-full bg-basil/10 px-4 py-1 text-sm font-medium text-basil">
              Recebido
            </span>
            <h1 className="mt-4 text-2xl font-semibold text-char">
              Pedido {order.orderNumber} confirmado!
            </h1>
            <p className="mt-2 text-sm text-muted-foreground">
              Obrigado, {order.form.name.split(" ")[0]}. Seu pedido foi
              recebido e já vamos preparar.
            </p>

            <div className="mt-6 space-y-2 rounded-md bg-muted p-4 text-left text-sm">
              {order.items.map((item) => (
                <div key={item.name} className="flex justify-between">
                  <span>
                    {item.quantity}x {item.name}
                  </span>
                  <span>{currencyFormatter.format(item.price * item.quantity)}</span>
                </div>
              ))}
              <div className="mt-2 flex justify-between border-t border-border pt-2 font-semibold text-char">
                <span>Total</span>
                <span>{currencyFormatter.format(order.total)}</span>
              </div>
            </div>

            <div className="mt-6 text-left text-sm text-muted-foreground">
              <p>
                Entrega: {order.form.address}, {order.form.number}
                {order.form.complement && ` - ${order.form.complement}`}
                <br />
                {order.form.neighborhood} · {order.form.city}/{order.form.state}
              </p>
              <p className="mt-1">
                Pagamento:{" "}
                {PAYMENT_OPTIONS.find((p) => p.value === order.form.paymentMethod)?.label}
              </p>
            </div>

            <a
              href="/#cardapio"
              className="mt-8 inline-block text-sm font-medium text-brick hover:underline"
            >
              Voltar ao cardápio
            </a>
          </div>
        </div>
      </main>
    );
  }

  if (isCartEmpty) {
    return (
      <main>
        <Navbar />
        <div className="mx-auto max-w-content px-4 py-16 sm:px-6 lg:px-8">
          <p className="text-muted-foreground">
            Sua sacola está vazia.{" "}
            <a href="/#cardapio" className="text-brick hover:underline">
              Ver cardápio
            </a>
          </p>
        </div>
      </main>
    );
  }

  return (
    <main>
      <Navbar />
      <div className="mx-auto max-w-content px-4 py-12 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-semibold text-char">Finalizar pedido</h1>

        <div className="mt-8 grid gap-10 lg:grid-cols-3">
          <form onSubmit={handleSubmit} className="space-y-5 lg:col-span-2" noValidate>
            <Field label="Nome completo" error={errors.name}>
              <input
                value={form.name}
                onChange={(e) => updateField("name", e.target.value)}
                className={inputClass(!!errors.name)}
              />
            </Field>

            <Field label="Telefone" error={errors.phone}>
              <input
                value={form.phone}
                onChange={(e) => updateField("phone", e.target.value)}
                placeholder="(16) 99999-9999"
                className={inputClass(!!errors.phone)}
              />
            </Field>

            <div className="grid grid-cols-2 gap-4">
              <Field label="CEP" error={errors.cep}>
                <input
                  value={form.cep}
                  onChange={(e) => updateField("cep", e.target.value)}
                  placeholder="14680-000"
                  className={inputClass(!!errors.cep)}
                />
              </Field>
              <Field label="Número" error={errors.number}>
                <input
                  value={form.number}
                  onChange={(e) => updateField("number", e.target.value)}
                  className={inputClass(!!errors.number)}
                />
              </Field>
            </div>

            <Field label="Endereço" error={errors.address}>
              <input
                value={form.address}
                onChange={(e) => updateField("address", e.target.value)}
                className={inputClass(!!errors.address)}
              />
            </Field>

            <Field label="Complemento (opcional)">
              <input
                value={form.complement}
                onChange={(e) => updateField("complement", e.target.value)}
                className={inputClass(false)}
              />
            </Field>

            <div className="grid grid-cols-3 gap-4">
              <Field label="Bairro" error={errors.neighborhood} className="col-span-2">
                <input
                  value={form.neighborhood}
                  onChange={(e) => updateField("neighborhood", e.target.value)}
                  className={inputClass(!!errors.neighborhood)}
                />
              </Field>
              <Field label="UF" error={errors.state}>
                <input
                  value={form.state}
                  maxLength={2}
                  onChange={(e) => updateField("state", e.target.value.toUpperCase())}
                  className={inputClass(!!errors.state)}
                />
              </Field>
            </div>

            <Field label="Cidade" error={errors.city}>
              <input
                value={form.city}
                onChange={(e) => updateField("city", e.target.value)}
                className={inputClass(!!errors.city)}
              />
            </Field>

            <fieldset>
              <legend className="text-sm font-medium text-char">Forma de pagamento</legend>
              <div className="mt-2 space-y-2">
                {PAYMENT_OPTIONS.map((option) => (
                  <label
                    key={option.value}
                    className="flex items-center gap-2 text-sm text-char/80"
                  >
                    <input
                      type="radio"
                      name="paymentMethod"
                      checked={form.paymentMethod === option.value}
                      onChange={() => updateField("paymentMethod", option.value)}
                    />
                    {option.label}
                  </label>
                ))}
              </div>
            </fieldset>

            <button
              type="submit"
              className="w-full rounded-sm bg-brick px-6 py-3 text-sm font-medium text-background transition-colors hover:bg-brick-dark"
            >
              Confirmar pedido
            </button>
          </form>

          <div className="h-fit rounded-lg border border-border p-6">
            <h2 className="font-semibold text-char">Resumo do pedido</h2>
            <ul className="mt-4 space-y-2 text-sm">
              {items.map(({ product, quantity }) => (
                <li key={product.id} className="flex justify-between">
                  <span>
                    {quantity}x {product.name}
                  </span>
                  <span>{currencyFormatter.format(product.price * quantity)}</span>
                </li>
              ))}
            </ul>
            <div className="mt-4 flex justify-between border-t border-border pt-4 text-lg font-semibold text-char">
              <span>Total</span>
              <span>{currencyFormatter.format(total)}</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

function inputClass(hasError: boolean) {
  return `w-full rounded-sm border px-3 py-2 text-sm outline-none focus:border-brick ${
    hasError ? "border-brick" : "border-border"
  }`;
}

function Field({
  label,
  error,
  className,
  children,
}: {
  label: string;
  error?: string;
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <div className={className}>
      <label className="mb-1 block text-sm font-medium text-char">{label}</label>
      {children}
      {error && <p className="mt-1 text-xs text-brick">{error}</p>}
    </div>
  );
}