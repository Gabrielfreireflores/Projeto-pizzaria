# Relatório Individual de Contribuição — Sprint 1 e Sprint 2

> Documentado em conjunto devido à unificação dos prazos de entrega das duas Sprints.

## Identificação do integrante

- **Nome:** Gabriel Freire Flôres
- **RA:** 2840482423010
- **Papel na Sprint 1 (conforme Termo de Aceite):** Product Owner
- **Papel na Sprint 2: Criação do design, marca e Front do cliente.

## Atividades realizadas

### Sprint 1
- Criação da estrutura base do frontend do projeto (Next.js, TypeScript, Tailwind).
- Criação da página inicial/home da visão do cliente.
- Criação dos estilos iniciais do frontend (paleta de cores, tipografia).
- Implementação da interface de Login (front-end apenas).
- Implementação da interface de Cadastro de cliente (front-end apenas).
- Implementação da seção Sobre e do Footer.
- Ajuste de responsividade mobile na tela de carrinho.
- Execução local do frontend e validação de renderização a cada entrega.

### Sprint 2
- Implementação do Menu de produtos (pizzas e bebidas), com dados separados da UI.
- Implementação do Carrinho de compras (adicionar, remover, ajustar quantidade, subtotal/total, persistência local).
- Implementação do Checkout (formulário de entrega, forma de pagamento, validação, resumo do pedido, tela de confirmação).
- Inclusão e otimização de vídeo no Hero da home (compressão de ~21MB para ~600KB via `ffmpeg`).
- Inclusão de imagens de produtos (bebidas).
- Diagnóstico e resolução de erro de build (arquivo `carrinho/page.tsx` salvo vazio).
- Diagnóstico e resolução de conflito de referência Git (`cannot lock ref`) e reconciliação entre a branch `feature/frontend` e a `main`, incluindo identificação de que o histórico da `main` continha um commit de outro integrante (`0fd8a98`) posteriormente revertido (`ccbbdfc`).
- Reconciliação da PR #10 (branch `feature/equipe-e-autenticacao`, de Christian de Lima): resolução de 13 conflitos de merge do tipo rename/delete na pasta `funcionario/`, identificação e correção de risco de perda acidental dos hooks `use-funcionarios.tsx` e `use-produtos.tsx` durante o merge, validação de build (`npm run build`) e aplicação de `npm audit fix --force` para correção de vulnerabilidades de dependências, seguida de nova validação de build. Mesclagem final da PR #10 à `main`. Esta atividade é de integração/reconciliação de código de outro integrante, não de autoria do conteúdo da área de funcionário em si.
- Execução local do frontend (`npm run build`) e validação de renderização a cada entrega.

## Funcionalidades/artefatos produzidos

- Página inicial pública (`frontend/src/app/(publico)/page.tsx`), com `Navbar`, `Hero` (com vídeo), `MenuSection`, `About` e `Footer`.
- Interface de Login (`login/page.tsx`) e Cadastro (`frontend/src/app/(publico)/cadastro/page.tsx`).
- Carrinho de compras (`frontend/src/app/(publico)/carrinho/page.tsx`) e hook de estado (`frontend/src/hooks/use-cart.tsx`).
- Checkout (`frontend/src/app/(publico)/checkout/page.tsx`).
- Componentes de UI reutilizáveis (`components/ui/button.tsx`, `components/ui/input.tsx`) e componentes compartilhados (`components/shared/`).
- Dados mock de produtos separados da UI (`lib/data/products.ts`).
- Estilos globais e paleta de cores (`frontend/src/app/globals.css`).
- Configuração base do projeto Next.js/TypeScript/Tailwind (`package.json`, `tailwind.config.ts`, `tsconfig.json`, `postcss.config.mjs`, `next.config.mjs`).

## Entregas realizadas

- Sprint 1: estrutura base do frontend, home, interfaces de Login/Cadastro/Sobre/Footer — sem integração com backend ou banco de dados.
- Sprint 2: jornada completa de compra do cliente no frontend (Menu → Carrinho → Checkout → Confirmação) — sem integração com backend ou banco de dados; checkout é demonstração de front-end, sem persistência real do pedido. Adicionalmente, reconciliação da PR #10 (integração de código de outro integrante à `main`).

## Participação na Sprint

Participação comprovada na implementação técnica do frontend em ambas as Sprints, incluindo atividade de integração/reconciliação de código de outro integrante (PR #10), conforme evidências abaixo. <img width="946" height="1020" alt="Captura de tela 2026-09-27 162322" src="https://github.com/user-attachments/assets/abf3c714-7219-4b9d-afd4-4627928fdab3" /> 
 quanto à participação em reuniões, decisões de planejamento ou outras atividades não técnicas.

## Commits relacionados

- "feat: implementação do front inicial" (`7fa57ec`) — Sprint 1 (base do frontend).
- "feat: login, cadastro, sobre, footer e ajuste mobile do carrinho" (`2dc2ae7`) — Sprint 1 (itens finais).
- Commits referentes a Menu, Carrinho e Checkout na branch `feature/frontend` — Sprint 2. [INFORMAÇÃO NECESSÁRIA] quanto aos hashes individuais desses commits (não fornecidos).
- Commit referente à inclusão do vídeo no Hero (`b4902bd`) — Sprint 2.
- Commit de merge de reconciliação da `main` na branch `feature/equipe-e-autenticacao` (PR #10) — [INFORMAÇÃO NECESSÁRIA] quanto ao hash exato desse commit de merge.

## Pull Requests relacionadas

- PR #4 — merge `96e4bba` — estrutura base e home (Sprint 1).
- PR #7 — merge `ca5b353` — Menu, Carrinho e Checkout (Sprint 2).
- PR #8 — merge `cbda1ed` — Login, Cadastro, Sobre, Footer, ajuste mobile do carrinho (Sprint 1).
- PR #9 referente ao vídeo no Hero — commit `b4902bd` Alterações na página do cliente, inclusão de vídeo, alteração de textos padrões e mais informações da pizzaria, com redirecionamento para instagram, contatos, ainda falta adicionar imagens das pizzas e completar o cardápio.
- PR #10 — branch `feature/equipe-e-autenticacao` (conteúdo de autoria de Christian de Lima), reconciliada com a `main` e mesclada por este integrante, com resolução de conflitos e validação de build.

## Evidências das atividades

- Histórico de atividade do repositório mostrando os commits e merges listados acima.
- Execução local do frontend (`npm run build`) e validação visual da renderização de cada entrega — evidência baseada em relato próprio;<img width="1617" height="951" alt="image" src="https://github.com/user-attachments/assets/f8c9e9d7-3680-4dde-82c4-89c03886f177" />
 para print/log adicional.
- Build aprovado após a mesclagem da PR #10, incluindo execução de `npm audit fix --force` — evidência baseada em relato próprio.
- Arquivo `frontend.zip` fornecido, contendo o estado final do código-fonte do frontend correspondente às entregas descritas.

## Observações

Não estão sendo atribuídas a este integrante atividades de backend, banco de dados, UML/DER, plano de testes ou testes automatizados, por não haver comprovação de autoria dessas partes nestas Sprints. O conteúdo funcional da área de funcionário (páginas, hooks `use-funcionarios.tsx` e `use-produtos.tsx`) desenvolvido por Christian de Lima (commit `0fd8a98`, revertido em `ccbbdfc`, reintroduzido via PR #10) não é atribuído a este integrante como autoria — a atividade deste integrante nesse episódio se limitou à reconciliação de merge e validação de build.
