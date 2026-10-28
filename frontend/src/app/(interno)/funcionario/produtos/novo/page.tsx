"use client";

import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { X } from "lucide-react";
import { api } from "@/services/api";

const NOVA_CATEGORIA = "__nova__";

type Categoria = { id: number; nome: string };
type Ingrediente = { id_ingrediente: number; nome: string; unidade_medida: string };
type LinhaIngrediente = { id: string; quantidade: string };

// Estilo base dos campos. "inputCls" ocupa a largura toda; os campos da
// linha de ingrediente usam "campoBase" para controlar a largura à mão.
const campoBase =
  "rounded-lg border border-border bg-muted/40 px-4 py-2.5 text-sm text-char outline-none transition focus:border-brick";
const inputCls = `w-full ${campoBase}`;

// A API de categorias devolve pares [id, nome]; aceita objetos também.
function paraCategoria(c: any): Categoria {
  return Array.isArray(c)
    ? { id: Number(c[0]), nome: String(c[1]) }
    : { id: Number(c.id_categoria ?? c.id), nome: String(c.nome) };
}

// "R$ 52,90" -> "52.90"
const limpar = (v: string) => v.trim().replace(/^R\$\s*/i, "").replace(",", ".");

// Categorias com "bebida" no nome não têm receita: só tamanho e preço.
const semAcento = (t: string) =>
  t.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
const ehBebida = (nome: string) => semAcento(nome).includes("bebida");

export default function NovoProdutoPage() {
  const router = useRouter();

  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [ingredientes, setIngredientes] = useState<Ingrediente[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [erroCarga, setErroCarga] = useState<string | null>(null);

  const [nome, setNome] = useState("");
  const [descricao, setDescricao] = useState("");
  const [tamanho, setTamanho] = useState("");
  const [preco, setPreco] = useState("");
  const [idCategoria, setIdCategoria] = useState("");
  const [disponivel, setDisponivel] = useState(true);
  const [linhas, setLinhas] = useState<LinhaIngrediente[]>([{ id: "", quantidade: "" }]);

  const [mostrarNovaCategoria, setMostrarNovaCategoria] = useState(false);
  const [nomeNovaCategoria, setNomeNovaCategoria] = useState("");

  const [erro, setErro] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  const categoriaAtual = categorias.find((c) => String(c.id) === idCategoria);
  const semIngredientes = !!categoriaAtual && ehBebida(categoriaAtual.nome);

  const [foto, setFoto] = useState<File | null>(null);
  const [previsualizacao, setPrevisualizacao] = useState<string | null>(null);

  async function carregarCategorias() {
    const r = await api.listarCategorias();
    const lista: Categoria[] = (r.categorias ?? []).map(paraCategoria);
    setCategorias(lista);
    return lista;
  }

  useEffect(() => {
    if (!foto) {
      setPrevisualizacao(null);
      return;
    }

    const url = URL.createObjectURL(foto);
    setPrevisualizacao(url);

    return () => URL.revokeObjectURL(url);
  }, [foto]);

  useEffect(() => {
    Promise.all([carregarCategorias(), api.listarIngredientes()])
      .then(([cats, ing]) => {
        setIdCategoria((atual) => atual || String(cats.find(c => c.nome === "Pizzas Salgadas")?.id ?? cats[0]?.id ?? ""));
        setIngredientes(ing.ingredientes ?? []);
      })
      .catch((e) =>
        setErroCarga(e instanceof Error ? e.message : "Não foi possível carregar os dados."),
      )
      .finally(() => setCarregando(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function handleSelectCategoria(valor: string) {
    if (valor === NOVA_CATEGORIA) {
      setMostrarNovaCategoria(true);
      return;
    }
    setIdCategoria(valor);
  }

  async function handleAdicionarCategoria() {
    const nomeFormatado = nomeNovaCategoria.trim();
    if (!nomeFormatado) return;
    setErro(null);
    try {
      await api.criarCategoria(nomeFormatado);
      const lista = await carregarCategorias();
      const criada = lista.find((c) => c.nome.toLowerCase() === nomeFormatado.toLowerCase());
      if (criada) setIdCategoria(String(criada.id));
      setNomeNovaCategoria("");
      setMostrarNovaCategoria(false);
    } catch (e) {
      setErro(e instanceof Error ? e.message : "Não foi possível criar a categoria.");
    }
  }

  function atualizarLinha(indice: number, campos: Partial<LinhaIngrediente>) {
    setLinhas((atuais) => atuais.map((l, i) => (i === indice ? { ...l, ...campos } : l)));
  }

  function adicionarLinha() {
    setLinhas((atuais) => [...atuais, { id: "", quantidade: "" }]);
  }

  function removerLinha(indice: number) {
    setLinhas((atuais) =>
      atuais.length === 1 ? [{ id: "", quantidade: "" }] : atuais.filter((_, i) => i !== indice),
    );
  }

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setErro(null);

    const precoLimpo = limpar(preco);
    if (!/^\d+(\.\d{1,2})?$/.test(precoLimpo)) {
      setErro("Informe o preço com até 2 casas decimais. Ex.: 52,90");
      return;
    }
    if (!idCategoria) {
      setErro("Escolha uma categoria.");
      return;
    }

    // Bebida não envia ingredientes.
    const itens: { id_ingrediente: number; quantidade_necessaria: string }[] = [];
    if (!semIngredientes) {
      for (const l of linhas) {
        if (!l.id && !l.quantidade.trim()) continue; // linha vazia
        const qtd = limpar(l.quantidade);
        if (!l.id || !/^\d+(\.\d{1,3})?$/.test(qtd) || Number(qtd) <= 0) {
          setErro(
            "Em cada ingrediente, escolha o item e informe uma quantidade maior que zero (até 3 casas decimais).",
          );
          return;
        }
        itens.push({ id_ingrediente: Number(l.id), quantidade_necessaria: qtd });
      }
    }

    setEnviando(true);
    try {
      await api.criarProduto({
        nome: nome.trim(),
        descricao: descricao.trim(),
        tamanho: tamanho.trim(),
        preco: precoLimpo,
        id_categoria: Number(idCategoria),
        disponivel,
        ingredientes: itens,
        foto,
      });
      router.push("/funcionario/produtos");
    } catch (err) {
      setErro(err instanceof Error ? err.message : "Não foi possível salvar o produto.");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <div className="flex min-w-0 justify-center">
      <div className="w-full max-w-2xl">
        <header className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
          <div className="flex-1">
            <p className="text-sm font-medium text-basil">Cardápio</p>
            <h1 className="mt-1 text-4xl font-semibold leading-tight text-char">
              Cadastrar produto
            </h1>
            <p className="mt-2 text-sm text-muted-foreground">
              Adicione um novo item ao cardápio.
            </p>
          </div>

          <Link
            href="/funcionario/produtos"
            className="rounded-lg bg-brick px-4 py-2.5 text-sm font-semibold text-background transition hover:bg-brick-dark"
          >
            Voltar
          </Link>
        </header>

        {erroCarga && (
          <p role="alert" className="mb-4 text-sm text-brick">
            {erroCarga}
          </p>
        )}

        <form
          onSubmit={handleSubmit}
          className="rounded-2xl border border-border bg-background p-6 shadow-sm"
        >
          <div className="grid gap-5 sm:grid-cols-2">
            <Campo label="Nome do produto" htmlFor="nome" className="sm:col-span-2">
              <input
                id="nome"
                maxLength={120}
                value={nome}
                onChange={(e) => setNome(e.target.value)}
                placeholder="Ex: Pizza de Calabresa"
                required
                className={inputCls}
              />
            </Campo>

            <Campo label="Descrição (opcional)" htmlFor="descricao" className="sm:col-span-2">
              <textarea id="descricao" value={descricao} onChange={e => setDescricao(e.target.value)} rows={3} className={inputCls} placeholder="Descreva os ingredientes e o produto para o cardápio." />
            </Campo>

            <div className="sm:col-span-2">
              <label
                htmlFor="foto"
                className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-muted-foreground"
              >
                Foto do produto
              </label>

              <input
                id="foto"
                type="file"
                accept="image/jpeg,image/png,image/webp"
                onChange={(e) => {
                  const arquivo = e.target.files?.[0] ?? null;

                  if (arquivo && arquivo.size > 5 * 1024 * 1024) {
                    setErro("A imagem deve ter no máximo 5 MB.");
                    e.target.value = "";
                    setFoto(null);
                    return;
                  }

                  setErro(null);
                  setFoto(arquivo);
                }}
                className={inputCls}
              />

              <p className="mt-1 text-xs text-muted-foreground">
                JPG, PNG ou WebP. Tamanho máximo: 5 MB.
              </p>

              {previsualizacao && (
                <div className="mt-3">
                  <img
                    src={previsualizacao}
                    alt="Prévia da foto do produto"
                    className="h-48 w-48 rounded-xl border border-border object-cover"
                  />
                </div>
              )}
            </div>

            <Campo label="Tamanho" htmlFor="tamanho">
              <input
                id="tamanho"
                maxLength={30}
                list="tamanhos"
                value={tamanho}
                onChange={(e) => setTamanho(e.target.value)}
                placeholder="Ex: Grande, 2 litros"
                required
                className={inputCls}
              />
              <datalist id="tamanhos">
                <option value="Pequena" />
                <option value="Grande" />
                <option value="Único" />
              </datalist>
              {categoriaAtual && ["Pizzas Salgadas", "Pizzas Doces", "Bordas"].includes(categoriaAtual.nome) && <p className="mt-1 text-xs text-muted-foreground">Para aparecer agrupado no cardápio, cadastre Pequena e Grande com o mesmo nome.</p>}
            </Campo>

            <Campo label="Preço" htmlFor="preco">
              <input
                id="preco"
                value={preco}
                onChange={(e) => setPreco(e.target.value)}
                inputMode="decimal"
                placeholder="0,00"
                required
                className={inputCls}
              />
            </Campo>

            <Campo label="Categoria" htmlFor="categoria" className="sm:col-span-2">
              <select
                id="categoria"
                value={idCategoria}
                onChange={(e) => handleSelectCategoria(e.target.value)}
                disabled={carregando}
                className={inputCls}
              >
                {categorias.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.nome}
                  </option>
                ))}
                <option value={NOVA_CATEGORIA}>+ Nova categoria</option>
              </select>

              {mostrarNovaCategoria && (
                <div className="mt-2 flex gap-2">
                  <input
                    autoFocus
                    value={nomeNovaCategoria}
                    onChange={(e) => setNomeNovaCategoria(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") {
                        e.preventDefault();
                        handleAdicionarCategoria();
                      }
                    }}
                    placeholder="Nome da categoria"
                    className="min-w-0 flex-1 rounded-lg border border-border bg-muted/40 px-3 py-2 text-sm text-char outline-none transition focus:border-brick"
                  />
                  <button
                    type="button"
                    onClick={handleAdicionarCategoria}
                    className="shrink-0 whitespace-nowrap rounded-lg bg-brick px-3 py-2 text-sm font-semibold text-background transition hover:bg-brick-dark"
                  >
                    Adicionar
                  </button>
                </div>
              )}
            </Campo>

            {semIngredientes ? (
              <p className="text-xs text-muted-foreground sm:col-span-2">
                Bebidas são cadastradas só com tamanho e preço, sem ingredientes.
              </p>
            ) : (
              <div className="sm:col-span-2">
                <p className="mb-1.5 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                  Ingredientes (opcionais)
                </p>

                <div className="space-y-2">
                  {linhas.map((linha, i) => {
                    const unidade = ingredientes.find(
                      (ing) => String(ing.id_ingrediente) === linha.id,
                    )?.unidade_medida;

                    return (
                      <div key={i} className="grid grid-cols-[minmax(0,1fr)_4rem_2.25rem] items-center gap-2 sm:flex">
                        <select
                          value={linha.id}
                          onChange={(e) => atualizarLinha(i, { id: e.target.value })}
                          aria-label="Ingrediente"
                          className={`${campoBase} col-span-3 min-w-0 w-full sm:w-auto sm:flex-1`}
                        >
                          <option value="">Selecione...</option>
                          {ingredientes.map((ing) => (
                            <option
                              key={ing.id_ingrediente}
                              value={ing.id_ingrediente}
                              disabled={linhas.some(
                                (outra, j) => j !== i && outra.id === String(ing.id_ingrediente),
                              )}
                            >
                              {ing.nome}
                            </option>
                          ))}
                        </select>

                        <input
                          value={linha.quantidade}
                          onChange={(e) => atualizarLinha(i, { quantidade: e.target.value })}
                          inputMode="decimal"
                          placeholder="Qtd."
                          aria-label="Quantidade"
                          className={`${campoBase} w-full min-w-0 sm:w-28 sm:shrink-0`}
                        />

                        <span className="w-16 shrink-0 truncate text-sm text-muted-foreground">
                          {unidade ?? ""}
                        </span>

                        <button
                          type="button"
                          onClick={() => removerLinha(i)}
                          aria-label="Remover ingrediente"
                          className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg text-muted-foreground transition hover:bg-muted hover:text-brick"
                        >
                          <X size={16} />
                        </button>
                      </div>
                    );
                  })}
                </div>

                <button
                  type="button"
                  onClick={adicionarLinha}
                  className="mt-3 text-sm font-semibold text-brick hover:underline"
                >
                  + Adicionar ingrediente
                </button>

                <p className="mt-2 text-xs text-muted-foreground">
                  A receita é opcional. Quando informada, use a unidade do ingrediente. Ex.: 150 g de um ingrediente em
                  kg é 0,150.
                </p>
              </div>
            )}

            <label className="flex items-center gap-2 text-sm text-char sm:col-span-2">
              <input
                type="checkbox"
                checked={disponivel}
                onChange={(e) => setDisponivel(e.target.checked)}
              />
              Disponível no cardápio
            </label>
          </div>

          {erro && (
            <p role="alert" className="mt-5 text-sm text-brick">
              {erro}
            </p>
          )}

          <div className="mt-6 flex items-center justify-end gap-3 border-t border-border pt-5">
            <Link
              href="/funcionario/produtos"
              className="rounded-lg px-4 py-2.5 text-sm font-semibold text-muted-foreground transition hover:bg-muted"
            >
              Cancelar
            </Link>

            <button
              type="submit"
              disabled={enviando || carregando}
              className="rounded-lg bg-brick px-4 py-2.5 text-sm font-semibold text-background transition hover:bg-brick-dark disabled:opacity-60"
            >
              {enviando ? "Salvando..." : "Salvar produto"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function Campo({
  label,
  htmlFor,
  children,
  className = "",
}: {
  label: string;
  htmlFor: string;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={className}>
      <label
        htmlFor={htmlFor}
        className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-muted-foreground"
      >
        {label}
      </label>
      {children}
    </div>
  );
}
