# Documentação Final — Projeto-pizzaria

- **Sistema:** Pizzaria do Barriga — aplicação web para pedidos e gestão da pizzaria (Trilha B, cliente real nº 1)
- **Equipe:** Gabriel Freire Flôres, Marcelo Augusto Oliveira Jose, Christian de Lima, Guilherme Fabiano da Silva Gomes
- **Disciplina e semestre:** Laboratório de Engenharia de Software - 5º Semestre
- **Repositório:** https://github.com/Gabrielfreireflores/Projeto-pizzaria
- **Deploy definitivo:** frontend em https://projeto-pizzaria-frontend-seven.vercel.app (Vercel); backend (Vercel); banco de dados (Neon)
- **Versão entregue:** https://github.com/Gabrielfreireflores/Projeto-pizzaria

## Resumo

Aplicação web para a Pizzaria do Barriga (Jardinópolis-SP), que antes recebia pedidos por WhatsApp e anotava tudo em papel. O cliente consulta o cardápio, monta o carrinho e finaliza o pedido pelo site; a equipe acompanha e atualiza o status dos pedidos em uma área interna, onde também gerencia produtos com ingredientes e os membros da equipe.

## 1. Índice de artefatos do semestre

| Entrega | Documento | Arquivo |
|---|---|---|
| E1 | Documento de Visão (21/08/2026) | `docs/documento-de-visao.md` |
| E2 | Backlog + Termo de Aceite do Projeto (28/08/2026) | `docs/BackLog.md`, `docs/TermoAceite.md` |
| E3 | UML + DER + DDL | `docs/uml/Uml.md`, `docs/uml/Uml-v2.md`, `docs/der/der.md`, `db/schema.sql`, `db/migrations/` |
| E4 | README + Protótipo + Plano de Testes | `README.md`, `docs/Roteiro do Protótipo Navegável — Pizzaria do Barriga.md` (protótipo no [Figma](https://www.figma.com/design/hd8egMUs65MPhKonVAZqMm/Pizzaria-do-Barriga)), `docs/plano_de_teste.md` |
| E5–E8 | Relatórios de sprint | Sprint 1: `docs/Sprints/sprint-1-relatorio.md`, `sprint-1-retrospectiva.md`, `sprint-1-evidencias-teste.md`; Sprint 2: [pendente]; Sprint 3: `docs/Sprints/sprint-3-relatorio.md`, `sprint-3-retrospectiva.md`, `sprint-3-evidencias-teste.md`; Sprint 4: [pendente] |
| E9 | Relatório de testes + Termo de Aceite do Cliente | [pendente: relatório final de testes], [pendente: termo de aceite do cliente] |

**Contribuições individuais** (em `docs/Sprints/`):

- `Sprint1_2_GuilhermeGomes.md`
- `relatorio-individual-sprint-1-2-christian.md`
- `relatorio-individual-sprint-3-4-Christian.md`
- `sprint-1-&-2-contribuicao-Gabriel-Freire-Flores.md`
- `sprint-1-&-2-contribuicao-Marcelo-Augusto-Oliveira-Jose.md`
- `sprint-3-contribuicao-Gabriel-Freire-Flores.md`
- `sprint-3-contribuicao-Marcelo-Augusto-Oliveira-Jose.md`

**Documentação técnica complementar:** `backend/DOCS_API.md`, `backend/README-cardapio.md`, `backend/README-consulta-pedidos.md`, `docs/contratos/produto.md`.

## 2. Desvios do escopo original (vs. E2)

Os itens abaixo comparam o que foi planejado no Documento de Visão, no Backlog e no Termo de Aceite com o que foi entregue.

| Item | Planejado (E1/E2) | Entregue | Justificativa |
|---|---|---|---|
| Produtos sem ingredientes (história #3) | Todo produto exige ao menos um ingrediente (relacionamento N:N) | Bebidas são cadastradas só com tamanho e preço; pizzas e sobremesas mantêm os ingredientes | Bebidas não têm receita |
| Disponibilidade por estoque de ingredientes (história #4 e regra de negócio do Documento de Visão) | Cardápio lista apenas produtos com estoque de ingredientes suficiente | [confirmar: a disponibilidade parece controlada por ativação/desativação do produto, sem controle de estoque] | Foi criada uma categoria para bebidas e não ajustamos o cadastro para fazer um controle exato de estoque |
| Dashboard de vendas e exportação em CSV (história #10, Could, Sprint 4) | Dashboard com pedidos, faturamento e produtos mais vendidos, e exportação em CSV | Não entregue | A equipe não sentiu a necessidade de realizar essa análise. Observação: a história #10 depende de um dashboard que não tem história própria no Backlog |
| Funcionalidades adicionais | Não previstas no Backlog | Adicionado: bordas por item (005), CPF opcional no cadastro do cliente (005), cadastro simplificado e menu da conta do cliente | Avaliamos que essas funcionalidades iriam agregar mais valor ao negócio |

## 3. Arquitetura final (resumo)

O frontend em Next.js (App Router, TypeScript e Tailwind CSS) consome uma API REST em Flask, com PostgreSQL como banco único, conforme a stack definida no Termo de Aceite.

- **Backend (`backend/app/`):** organizado em camadas — `routes`, `controllers`, `services`, `repositories`, `models`, `schemas`, `exceptions` e `utils` —, com acesso ao banco em `database.py` e ponto de entrada em `run.py`. A API está documentada em `backend/DOCS_API.md`.
- **Banco (`db/`):** esquema em `schema.sql`, evoluído por migrations: contato do pedido (001), cardápio de produtos (002), checkout de convidado e retirada (003), carga do cardápio v2 (004), bordas por item (005), CPF opcional no cliente (005), desativação do refrigerante legado (006), correção do status de preparação (007) e remoção de produtos legados (008). O modelo UML foi revisado na v2 (`docs/uml/Uml-v2.md`).
- **Frontend (`frontend/src/`):** `app` (rotas), `components`, `hooks`, `services` (chamadas à API), `lib`, `styles` e `types`. A área interna do funcionário reúne pedidos, produtos e equipe.
- **Módulos funcionais:** autenticação (cliente e funcionário), cardápio e produtos (com ingredientes), pedidos (checkout, consulta e atualização de status), conta do cliente e equipe.

## 4. Como contribuir e rodar

O passo a passo completo está no `README.md` da raiz. Resumo:

1. **Banco:** criar um banco PostgreSQL local, aplicar `db/schema.sql` e as migrations de `db/migrations/` em ordem numérica.
2. **Backend:** em `backend/`, criar e ativar um ambiente virtual, instalar `requirements.txt` (e `requirements-dev.txt` para os testes), copiar `.env.example` para `.env`, definir `DATABASE_URL` e iniciar com `python run.py`.
3. **Frontend:** em `frontend/`, executar `npm install` e `npm run dev`.
4. **Testes do backend:** [comando, ex.: pytest em `backend/`].


## 5. Limitações conhecidas e trabalho futuro

**Funcionalidades não entregues ou adiadas**

- Dashboard de vendas e exportação em CSV (história #10).
- Controle de disponibilidade por estoque de ingredientes.

**Dívidas técnicas conhecidas**

- Duas migrations com o mesmo número (`005_bordas_por_item.sql` e `005_cliente_cpf_opcional.sql`): a ordem de aplicação fica ambígua. A correção é renumerar uma delas.
- Os testes automatizados cobrem apenas o backend (`backend/tests/`); o frontend foi verificado manualmente.
- O cardápio é carregado pelo navegador a partir da API (a página inicial mostra “Carregando cardápio...” até a resposta), então a vitrine depende da disponibilidade do backend.

**Trabalho futuro**

- Testes automatizados do frontend (fluxo de pedido e área do funcionário).
- Renumerar as migrations e registrar a ordem de aplicação no `README.md`.
- Adicionar dashboard de faturamento vs custo
- Adicionar dashboard com os + produtos +pedidos e clientes que mais pedem
- Avaliar realização de promoções.

## 6. Resultado dos testes

O Plano de Testes (`docs/plano_de_teste.md`) prevê testes unitários e de integração com PyTest e pytest-flask, mais testes manuais ao fim de cada sprint, e define os casos CT01 a CT06 (login, categorias, produtos, carrinho e finalização do pedido). O backend tem testes automatizados em `backend/tests/`, cobrindo autenticação (rotas e serviços), cadastro simplificado, cardápio, produtos, bordas por cliente, consulta e status de pedidos, menu da conta e a integração entre autenticação e pedidos.

As evidências por sprint estão em `docs/Sprints/sprint-1-evidencias-teste.md` e `docs/Sprints/sprint-3-evidencias-teste.md`.
