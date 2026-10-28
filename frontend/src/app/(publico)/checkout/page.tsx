"use client";

import Link from "next/link";
import { useState, type FormEvent } from "react";
import { useCart } from "@/hooks/use-cart";
import { useAuth, ehFuncionario } from "@/hooks/use-auth";
import { Navbar } from "@/components/shared/navbar";
import { CheckoutFormData, CheckoutFormErrors, Order, PaymentMethod } from "@/types/order";
import { createOrder } from "@/services/orders";

const money = (v: number) => v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
const INITIAL_FORM: CheckoutFormData = { name: "", phone: "", address: "", neighborhood: "", paymentMethod: "pix", fulfillment: "entrega" };
const PAYMENTS: { value: PaymentMethod; label: string }[] = [
  { value: "dinheiro", label: "Dinheiro" }, { value: "pix", label: "Pix" }, { value: "cartao", label: "Cartão" },
];
const inputClass = "mt-2 w-full rounded-lg border border-border bg-background p-3 text-sm font-normal outline-none focus:border-brick";

function validate(form: CheckoutFormData): CheckoutFormErrors {
  const errors: CheckoutFormErrors = {};
  if (form.name.trim().split(/\s+/).length < 2 || form.name.trim().length > 120) errors.name = "Informe nome e sobrenome (até 120 caracteres).";
  if (!/^[+()\d .-]+$/.test(form.phone.trim()) || !/^\d{10,15}$/.test(form.phone.replace(/\D/g, "")) || form.phone.length > 20) errors.phone = "Informe um telefone válido com DDD.";
  if (form.fulfillment === "entrega") {
    if (form.address.trim().length < 5 || form.address.length > 160) errors.address = "Informe rua e número (até 160 caracteres).";
    if (!form.neighborhood.trim() || form.neighborhood.length > 100) errors.neighborhood = "Informe o bairro (até 100 caracteres).";
  }
  return errors;
}

export default function CheckoutPage() {
  const { items, subtotal, clearCart } = useCart();
  const { usuario } = useAuth();
  const [form, setForm] = useState<CheckoutFormData>(INITIAL_FORM);
  const [errors, setErrors] = useState<CheckoutFormErrors>({});
  const [step, setStep] = useState(1);
  const [order, setOrder] = useState<Order | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const update = <K extends keyof CheckoutFormData>(key: K, value: CheckoutFormData[K]) => setForm(prev => ({ ...prev, [key]: value }));

  async function submit(event: FormEvent) {
    event.preventDefault();
    const found = validate(form);
    setErrors(found);
    if (Object.keys(found).length) { setStep(1); return; }
    if (step < 3) { setStep(s => s + 1); return; }
    setSubmitting(true);
    setError("");
    try {
      const created = await createOrder({
        customer: { name: form.name.trim(), phone: form.phone.trim() },
        fulfillment: form.fulfillment,
        delivery: form.fulfillment === "entrega" ? { address: form.address.trim(), neighborhood: form.neighborhood.trim() } : undefined,
        paymentMethod: form.paymentMethod,
        items: items.map(({ product, quantity }) => ({
          menuItemId: product.menuItemId ?? product.id, productId: product.productId,
          orderNote: product.orderNote, size: product.size, halfMenuItemId: product.halfMenuItemId,
          note: product.note, border: product.border, name: product.name, quantity, unitPrice: product.price,
        })),
        total: subtotal,
      });
      setOrder(created);
      clearCart();
    } catch (e) { setError(e instanceof Error ? e.message : "Não foi possível enviar o pedido."); }
    finally { setSubmitting(false); }
  }

  if (order) return <main><Navbar /><div className="mx-auto max-w-lg px-4 py-12">
    <div className="rounded-xl border border-border p-6 text-center">
      <span className="rounded-full bg-basil/10 px-4 py-1 text-sm text-basil">Recebido</span>
      <h1 className="mt-5 text-2xl font-semibold">Pedido {order.number} confirmado!</h1>
      <p className="mt-2 text-sm text-muted-foreground">Obrigado, {order.customer.name}. Seu pedido foi recebido pela pizzaria.</p>
      <ul className="mt-6 space-y-3 rounded-lg bg-muted p-4 text-left text-sm">{order.items.map((i, n) => <li key={n}>
        <div className="flex justify-between gap-3"><span>{i.quantity}x {i.name}</span><span className="shrink-0">{money(i.unitPrice * i.quantity)}</span></div>
        {i.border && <p className="text-xs text-muted-foreground">Borda: {i.border.name} (incluída)</p>}
        {i.note && <p className="text-xs text-muted-foreground">Obs.: {i.note}</p>}
      </li>)}</ul>
      <p className="mt-4 text-lg font-semibold">Total confirmado: {money(order.total)}</p>
      <p className="mt-3 text-sm text-muted-foreground">{order.delivery ? `${order.delivery.address} · ${order.delivery.neighborhood}` : "Retirada no local"}</p>
      <p className="mt-1 text-sm text-muted-foreground">Pagamento: {PAYMENTS.find(p => p.value === order.paymentMethod)?.label}</p>
      {usuario && !ehFuncionario(usuario) ? <Link href="/meus-pedidos" className="mt-6 block rounded-lg bg-brick p-3 text-background">Acompanhar meu pedido</Link> : <p className="mt-6 text-sm text-muted-foreground">Guarde o número do seu pedido. Para acompanhar próximos pedidos pela conta, <Link href="/cadastro" className="text-brick underline">cadastre-se</Link> e entre antes de pedir.</p>}
      <Link href="/#cardapio" className="mt-5 inline-block text-brick underline">Voltar ao cardápio</Link>
    </div>
  </div></main>;

  if (!items.length) return <main><Navbar /><div className="mx-auto max-w-content px-4 py-12"><h1 className="text-3xl font-semibold">Finalizar pedido</h1><p className="mt-5">Sua sacola está vazia. <Link href="/#cardapio" className="text-brick underline">Ver cardápio</Link></p></div></main>;

  return <main><Navbar /><div className="mx-auto max-w-content px-4 py-10 sm:px-6">
    <h1 className="text-3xl font-semibold text-char">Finalizar pedido</h1>
    <ol aria-label="Etapas do pedido" className="mt-6 grid grid-cols-3 gap-2 text-center text-xs sm:text-sm">
      {["Seus dados", "Pagamento", "Confirmação"].map((label, i) => <li key={label} aria-current={step === i + 1 ? "step" : undefined} className={`rounded-lg border px-2 py-3 ${step === i + 1 ? "border-brick bg-brick/10 font-semibold text-brick" : "border-border text-muted-foreground"}`}>{i + 1}. {label}</li>)}
    </ol>
    <div className="mt-7 grid items-start gap-7 lg:grid-cols-3">
      <form onSubmit={submit} noValidate className="space-y-5 rounded-xl border border-border p-5 lg:col-span-2 sm:p-6">
        {step === 1 && <>
          <h2 className="text-xl font-semibold">Contato e entrega</h2>
          {!usuario && <p className="text-sm text-muted-foreground">Você pode pedir sem conta. Para acompanhar pela área de pedidos, <Link href="/login" className="text-brick underline">entre</Link> ou <Link href="/cadastro" className="text-brick underline">crie sua conta</Link> antes de confirmar.</p>}
          {ehFuncionario(usuario) && <p role="alert" className="text-sm text-brick">Há uma sessão de funcionário neste navegador. Saia da conta ou use uma janela anônima para pedir como cliente.</p>}
          <label className="block text-sm font-semibold">Nome e sobrenome<input name="nome" autoComplete="name" value={form.name} maxLength={120} onChange={e => update("name", e.target.value)} className={inputClass} aria-invalid={!!errors.name} />{errors.name && <span role="alert" className="mt-1 block text-xs text-brick">{errors.name}</span>}</label>
          <label className="block text-sm font-semibold">Telefone com DDD<input name="telefone" type="tel" autoComplete="tel" value={form.phone} maxLength={20} onChange={e => update("phone", e.target.value)} placeholder="(16) 99999-9999" className={inputClass} aria-invalid={!!errors.phone} />{errors.phone && <span role="alert" className="mt-1 block text-xs text-brick">{errors.phone}</span>}</label>
          <fieldset><legend className="text-sm font-semibold">Como você quer receber?</legend><div className="mt-2 grid grid-cols-2 gap-2">{(["entrega", "retirada"] as const).map(value => <button key={value} type="button" aria-pressed={form.fulfillment === value} onClick={() => update("fulfillment", value)} className={`rounded-lg border p-3 text-sm ${form.fulfillment === value ? "border-brick bg-brick/10" : "border-border"}`}>{value === "entrega" ? "Entrega" : "Retirada"}</button>)}</div></fieldset>
          {form.fulfillment === "entrega" && <>
            <label className="block text-sm font-semibold">Rua e número<input name="endereco" autoComplete="street-address" value={form.address} onChange={e => update("address", e.target.value)} placeholder="Rua das Flores, 123" maxLength={160} className={inputClass} aria-invalid={!!errors.address} />{errors.address && <span role="alert" className="mt-1 block text-xs text-brick">{errors.address}</span>}</label>
            <label className="block text-sm font-semibold">Bairro<input name="bairro" value={form.neighborhood} maxLength={100} onChange={e => update("neighborhood", e.target.value)} className={inputClass} aria-invalid={!!errors.neighborhood} />{errors.neighborhood && <span role="alert" className="mt-1 block text-xs text-brick">{errors.neighborhood}</span>}</label>
          </>}
        </>}
        {step === 2 && <>
          <h2 className="text-xl font-semibold">Forma de pagamento</h2>
          <p className="text-sm text-muted-foreground">Informe como pretende pagar na entrega ou retirada. Não há cobrança online.</p>
          <fieldset className="space-y-3"><legend className="sr-only">Escolha uma forma de pagamento</legend>{PAYMENTS.map(p => <label key={p.value} className={`flex cursor-pointer items-center gap-3 rounded-lg border p-4 ${form.paymentMethod === p.value ? "border-brick bg-brick/10" : "border-border"}`}><input type="radio" name="paymentMethod" checked={form.paymentMethod === p.value} onChange={() => update("paymentMethod", p.value)} className="accent-brick" />{p.label}</label>)}</fieldset>
        </>}
        {step === 3 && <>
          <h2 className="text-xl font-semibold">Confira antes de confirmar</h2>
          <div className="space-y-2 rounded-lg bg-muted p-4 text-sm"><p className="font-semibold">{form.name}</p><p>{form.phone}</p><p>{form.fulfillment === "entrega" ? `${form.address} · ${form.neighborhood}` : "Retirada no local"}</p><p>Pagamento: {PAYMENTS.find(p => p.value === form.paymentMethod)?.label}</p></div>
          <p className="text-sm text-muted-foreground">Confira os itens e as bordas no resumo. O total final é calculado pela pizzaria ao receber o pedido.</p>
        </>}
        {error && <p role="alert" className="text-sm text-brick">{error}</p>}
        <div className="flex gap-3 border-t border-border pt-5">
          {step > 1 && <button type="button" disabled={submitting} onClick={() => setStep(s => s - 1)} className="rounded-lg border border-border px-5 py-3 text-sm">Voltar</button>}
          <button type="submit" disabled={submitting || ehFuncionario(usuario)} className="flex-1 rounded-lg bg-brick px-4 py-3 text-sm font-semibold text-background disabled:opacity-50">{submitting ? "Enviando..." : step < 3 ? "Continuar" : "Confirmar pedido"}</button>
        </div>
      </form>
      <aside className="rounded-xl border border-border p-5">
        <h2 className="text-lg font-semibold">Resumo do pedido</h2>
        <ul className="mt-4 space-y-4 text-sm">{items.map(({ product: p, quantity }) => <li key={p.id}><div className="flex justify-between gap-3"><span>{quantity}x {p.name}</span><span className="shrink-0">{money(p.price * quantity)}</span></div>{p.border && <p className="mt-1 text-xs text-brick">Borda: {p.border.name} (incluída)</p>}{p.note && <p className="mt-1 text-xs text-muted-foreground">Obs.: {p.note}</p>}</li>)}</ul>
        <p className="mt-5 flex justify-between border-t border-border pt-4 font-semibold"><span>Subtotal</span><span>{money(subtotal)}</span></p>
        <p className="mt-2 text-xs text-muted-foreground">{form.fulfillment === "retirada" ? "Retirada: sem taxa." : "Taxa de entrega: a consultar. O total confirmado considera a taxa configurada pela pizzaria."}</p>
        <Link href="/carrinho" className="mt-5 inline-block text-sm text-brick underline">Editar sacola</Link>
      </aside>
    </div>
  </div></main>;
}
