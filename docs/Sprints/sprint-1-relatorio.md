# Relatório de Entrega — Sprint 1 e Sprint 2

Equipe: Gabriel Freire Flôres (RA 2840482423010) — Marcelo Augusto Oliveira Jose (RA 2840482423043) — Christian de Lima (RA 2840482523031) — Guilherme Fabiano da Silva Gomes (RA 2840482423037) Trilha: B (Cliente real nº 1)

> **Nota sobre o prazo:** os prazos de entrega da Sprint 1 e da Sprint 2 foram unificados. Por isso, este relatório documenta as duas sprints em conjunto, mantendo a distinção clara entre o que foi planejado/entregue em cada uma.

## Objetivo da Sprint

**Sprint 1:** segundo o Backlog Priorizado, a Sprint 1 tinha como alvo as histórias #1 (Login/autenticação), #2 (Cadastro de categorias) e #3 (Cadastro de produtos vinculados a categoria/ingredientes).

**Sprint 2:** conforme formalizado pela equipe, a Sprint 2 teve como alvo as histórias #4 (Menu — exibição de produtos ao cliente), #5 (Carrinho de compras) e #6 (Checkout — finalização de pedido).

## Planejamento da Sprint

- Histórias planejadas na Sprint 1 (Backlog): #1 Login, #2 Cadastro de categorias, #3 Cadastro de produtos.
- Histórias planejadas na Sprint 2 (Backlog): #4 Menu, #5 Carrinho, #6 Checkout.
- Papéis definidos no Termo de Aceite para a Sprint 1: Gabriel Freire Flôres (Product Owner), Marcelo Augusto Oliveira Jose (Dados), Christian de Lima (Desenvolvedor Frontend), Guilherme Fabiano da Silva Gomes (Dados).

## Itens efetivamente realizados

### Sprint 1
- Criação da estrutura base do projeto frontend (Next.js, TypeScript, Tailwind, configuração inicial) — PR #4 (commit `7fa57ec`, merge `96e4bba`).
- Criação da página inicial/home da visão do cliente (`(publico)/page.tsx`), com componentes `Navbar` e `Hero`.
- Criação dos estilos iniciais (`globals.css`, paleta de cores, tipografia).
- Implementação da interface de **Login** (`login/page.tsx`) — apenas front-end, sem integração com backend/autenticação real.
- Implementação da interface de **Cadastro de cliente** (`(publico)/cadastro/page.tsx`) — apenas front-end, sem integração com backend.
- Implementação da seção **Sobre** (`components/shared/about.tsx`) e do **Footer** (`components/shared/footer.tsx`).
- Ajuste de responsividade mobile na tela de carrinho.
- Entregas acima referentes ao commit "feat: login, cadastro, sobre, footer e ajuste mobile do carrinho", mesclado via PR #8 (merge `cbda1ed`).
- **Não realizado:** Cadastro de categorias (História #2) e Cadastro de produtos vinculados a categoria/ingredientes (História #3), conforme planejado no Backlog original da Sprint 1. Não há, no repositório, tela ou lógica de administração de categorias/produtos atribuível a este integrante.
- **Desvio importante:** a interface de Login entregue é de front-end apenas (sem bloqueio de tentativas inválidas, sem redirecionamento por perfil, sem integração com backend), o que difere do escopo descrito para a História #1 no Backlog.

### Sprint 2
- Implementação do **Menu** de produtos ao cliente (`components/shared/menu-section.tsx`, `components/shared/product-card.tsx`), com dados mock (`lib/data/products.ts`), separando dados da UI.
- Implementação do **Carrinho de compras** (`(publico)/carrinho/page.tsx`, `hooks/use-cart.tsx`), com adicionar/remover produto, aumentar/diminuir quantidade, subtotal/total, esvaziar carrinho e persistência via `localStorage`.
- Implementação do **Checkout** (`(publico)/checkout/page.tsx`), com formulário de entrega (nome, telefone, CEP, endereço, número, complemento, bairro, cidade, UF), forma de pagamento, validação client-side, resumo do pedido e tela de confirmação com status "Recebido". Sem integração com backend/API — apenas demonstração de front-end.
- Entregas acima mescladas via PR #7 (merge `ca5b353`).
- Inclusão de imagens de produtos (bebidas) e vídeo no Hero da página inicial (`public/calabresavideo-otimizado2.mp4`), com otimização de peso do arquivo de vídeo (de ~21MB para ~600KB, via compressão com `ffmpeg`) visando leveza de carregamento.
- Ajustes de navegabilidade entre Menu → Carrinho → Checkout → Confirmação.
- Entregas de vídeo/imagens mescladas via PR referente ao commit `b4902bd` (PR #9).
- Reconciliação da PR #10 (branch `feature/equipe-e-autenticacao`, de Christian de Lima — reintrodução da área de funcionário): resolução de conflitos de merge do tipo rename/delete em 13 arquivos da pasta `funcionario/`, com preservação integral do conteúdo da branch de Christian (incluindo os hooks `use-funcionarios.tsx` e `use-produtos.tsx`, que estavam em risco de ser apagados no merge). PR #10 mesclada com sucesso à `main` após validação de build. Esta atividade é de reconciliação/integração, não de autoria do conteúdo da área de funcionário.

## Incremento/entrega demonstrável

- Site público navegável de ponta a ponta na jornada do cliente: Home (Navbar, Hero com vídeo, Menu, Sobre, Footer) → Carrinho → Checkout → tela de confirmação de pedido.
- Telas de Login e Cadastro de cliente acessíveis, com formulários funcionais em termos de interface (sem persistência real de dados).

## Situação do produto ao final das Sprints 1 e 2

- Frontend: rota pública (`(publico)/`) com Home, Cadastro, Carrinho e Checkout implementados;
- Backend: [INFORMAÇÃO NECESSÁRIA] 
- Banco de dados: [INFORMAÇÃO NECESSÁRIA] 
- Não existe, ao final destas duas Sprints, integração funcional entre frontend, backend e banco de dados.

## Validações e testes realizados

- Execução local do frontend (`npm run build` / `npm run dev`) e validação visual de cada entrega (Home, Menu, Carrinho, Checkout, Login, Cadastro, vídeo no Hero, responsividade mobile), com build TypeScript/Next.js aprovado a cada etapa.
- Execução de `npm run build` após o merge da PR #10, com resultado aprovado. O `npm` apontou vulnerabilidades de dependências, corrigidas com `npm audit fix --force`, seguido de nova validação de build aprovada.

## Pendências

- Implementação de backend real para Login, Cadastro e Checkout (atualmente apenas UI).
- Integração frontend/backend/banco de dados.

## Diferenças entre o planejado e o realizado

- Divergência de versões de stack, conforme já registrado no relatório anterior: README/Termo de Aceite citam Next.js 16.3.4, React 19.3.0, TypeScript 7.0.2 e Tailwind 4.3.3; o `package.json` do frontend usa Next 14.2.5, React 18.3.1, TypeScript ^5.5.4 e Tailwind ^3.4.9.

## Riscos ou impedimentos

- Conflito de trabalho paralelo com outro integrante da equipe.

## Referências/evidências das entregas

- PR #4 — branch `feature/frontend`, commit "feat: implementação do front inicial" (`7fa57ec`), merge `96e4bba` — estrutura base e home.
- PR #7 — merge `ca5b353` — Menu, Carrinho, Checkout (Sprint 2).
- PR #8 — merge `cbda1ed` — commit "feat: login, cadastro, sobre, footer e ajuste mobile do carrinho" (`2dc2ae7`) (Sprint 1, itens finais).
- PR #9 do vídeo no Hero — commit `b4902bd`.
- PR #10 — branch `feature/equipe-e-autenticacao`, reconciliada e mesclada à `main` com participação deste integrante na resolução de conflitos.
- Estrutura de arquivos do frontend no repositório: `frontend/src/app/(publico)/page.tsx`, `frontend/src/app/(interno)/login/page.tsx`, `frontend/src/app/(publico)/cadastro/page.tsx`, `frontend/src/app/(publico)/carrinho/page.tsx`, `frontend/src/app/(publico)/checkout/page.tsx`, `frontend/src/components/shared/`, `frontend/src/hooks/use-cart.tsx`.

## Relação com os demais entregáveis da Sprint

Este relatório está diretamente relacionado à Ata de Retrospectiva (`sprint-1-retrospectiva.md`), ao Relatório Individual de Contribuição de: (`sprint-1-contribuicao-Gabriel-Freire-Flores.md`) e às Evidências de Teste (`sprint-1-evidencias-teste.md`), que detalham, respectivamente, a avaliação do processo, a contribuição individual comprovada e as validações realizadas nestas etapas.
