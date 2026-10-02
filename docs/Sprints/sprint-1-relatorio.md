# Relatório de Entrega — Sprint 1 e 2 — Pizzaria do Barriga

**Período:** 18/09/2026 a 02/10/2026
**Sprint Review:** 

Equipe: Gabriel Freire Flôres (RA 2840482423010) — Marcelo Augusto Oliveira Jose (RA 2840482423043) — Christian de Lima (RA 2840482523031) — Guilherme Fabiano da Silva Gomes (RA 2840482423037)
Trilha: B (Cliente real nº 1)

> **Nota sobre o prazo:** os prazos de entrega da Sprint 1 e da Sprint 2 foram unificados. Por isso, este relatório documenta as duas sprints em conjunto, mantendo a distinção clara entre o que foi planejado/entregue em cada uma.

## 1. Planejado vs. entregue

| História (E2) | Planejada para esta sprint? | Entregue? | Observação |
|---|---|---|---|
| #1 Login/autenticação | Sim (Sprint 1) | Parcial | Apenas UI (`login/page.tsx`), sem bloqueio de tentativas inválidas, sem redirecionamento por perfil, sem integração com backend. PR #8 (merge `cbda1ed`) |
| #2 Cadastro de categorias | Sim (Sprint 1) | Não | Não há tela ou lógica de administração de categorias atribuível a este integrante |
| #3 Cadastro de produtos (categoria/ingredientes) | Sim (Sprint 1) | Backend entregue; integração com interface pendente | Cadastro com validações, categoria, ingredientes, autorização e transação — Marcelo, PR #6. Produtos exibidos no Menu são dados mock (`lib/data/products.ts`), não cadastrados via interface administrativa |
| #4 Menu (exibição de produtos ao cliente) | Sim (Sprint 2) | Sim | Dados mock separados da UI. PR #7 (merge `ca5b353`) |
| #5 Carrinho de compras | Sim (Sprint 2) | Sim | Adicionar/remover produto, ajustar quantidade, subtotal/total, persistência via `localStorage`. PR #7 (merge `ca5b353`) |
| #6 Checkout | Sim (Sprint 2) | Sim | Formulário de entrega e pagamento, validação client-side, tela de confirmação "Recebido". Sem integração com backend/API. PR #7 (merge `ca5b353`) Backend de criação de pedidos entregue por Marcelo na PR #13, com validação, recálculo de valores, transação e status inicial RECEBIDO; integração com a interface ainda pendente. |
| H03-04 Consulta de produtos | Sim (Sprint 2) | Backend entregue | Categoria, ingredientes, preço e disponibilidade — Marcelo, PR #13 |
| H03-05 Contrato de Produto | Sim (Sprint 2) | Sim | Request, response, consulta e erros documentados — Marcelo, PR #14 |

**Itens entregues fora da numeração formal do Backlog (#1–#6):**
- Estrutura base do projeto frontend (Next.js, TypeScript, Tailwind) — PR #4 (commit `7fa57ec`, merge `96e4bba`).
- Home da visão do cliente (`Navbar`, `Hero`, `Sobre`, `Footer`) — PRs #4 e #8.
- Cadastro de cliente (`(publico)/cadastro/page.tsx`, UI apenas, sem backend) — PR #8 (merge `cbda1ed`).
- Vídeo no Hero (otimizado de ~21MB para ~600KB via `ffmpeg`) e imagens de produtos — PR #9 (commit `b4902bd`).
- Reconciliação da PR #10 (branch `feature/equipe-e-autenticacao`, de Christian de Lima — área de funcionário): resolução de conflitos de merge rename/delete em 13 arquivos, preservação dos hooks `use-funcionarios.tsx`/`use-produtos.tsx`, validação de build e `npm audit fix --force`. Atividade de integração, não de autoria do conteúdo da área de funcionário.

## 2. Incremento funcional demonstrável

Jornada completa do cliente navegável localmente: Home (Navbar, Hero com vídeo, Menu, Sobre, Footer) → Carrinho → Checkout → tela de confirmação de pedido ("Recebido"). Telas de Login e Cadastro de cliente acessíveis como interface, sem persistência real de dados.

O backend permite cadastrar e consultar produtos e criar pedidos no PostgreSQL pelos endpoints `POST /api/v1/produtos`, `GET /api/v1/produtos` e `POST /api/v1/pedidos`. As entregas de Marcelo seguem a organização em camadas da equipe. A persistência pela API foi testada separadamente da jornada da interface. As instruções de execução e migração estão em `backend/README-consulta-pedidos.md`, e o contrato em `docs/contratos/produto.md`.

- **Link do deploy:** 
- **GIF/vídeo de demonstração:** 
- **Como reproduzir localmente:**
  ```
  cd frontend
  npm install
  npm run dev
  ```
  Acessar `http://localhost:3000`.

## 3. Backlog atualizado

- **Mudanças de status conhecidas (com base nas evidências de código/PR, não no board):**
  - #4 Menu, #5 Carrinho, #6 Checkout: de "planejado" para "entregue" (PR #7).
  - #1 Login: de "planejado" para "entregue parcialmente" (apenas UI, PR #8).
  - #2 Cadastro de categorias: permanece conforme o registro anterior.
  - #3 Cadastro de produtos: backend entregue (PR #6), com consulta (H03-04, PR #13) e contrato (H03-05, PR #14); integração com a interface pendente.
  - #6 Checkout: criação de pedidos e status inicial RECEBIDO entregues no backend (H06-02/H06-03, PR #13); integração com a interface pendente.

## 4. Evidências de teste

No frontend, os testes realizados foram manuais, em ambiente local, com `npm run build` aprovado a cada entrega (Home, Menu, Carrinho, Checkout, Login, Cadastro, vídeo no Hero, responsividade mobile) e após o merge da PR #10 (incluindo `npm audit fix --force` seguido de novo build aprovado). Para essas entregas de frontend, não há testes automatizados, de integração ou cobertura de código registrados. No backend de produtos e pedidos, Marcelo validou 45 testes na etapa de cadastro e 92 na suíte ampliada, incluindo os anteriores e integração com PostgreSQL em schemas temporários. Esses resultados são anteriores à validação conjunta após todos os merges. Os sete exemplos JSON do contrato também tiveram a sintaxe validada; não são testes HTTP adicionais. Detalhe completo em `sprint-1-evidencias-teste.md`.

## 5. Retrospectiva e contribuição individual

- Ata de retrospectiva: `sprint-1-retrospectiva.md`
- Relatórios individuais de contribuição: `sprint-1-contribuicao-Gabriel-Freire-Flores.md`: https://github.com/Gabrielfreireflores/Projeto-pizzaria/blob/main/docs/Sprints/sprint-1-%26-2-contribuicao-Gabriel-Freire-Flores.md

- Relatório individual de Marcelo: [Sprint 1 e Sprint 2](sprint-1-&-2-contribuicao-Marcelo-Augusto-Oliveira-Jose.md).
- PRs de produtos, pedidos e contrato: [#6](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/6), [#13](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/13) e [#14](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/14).

## 6. Riscos/impedimentos para a próxima sprint

- Recomenda-se sincronizar branches de longa duração com a `main` com mais frequência, para evitar o acúmulo de conflitos como os ocorridos na reconciliação da PR #10.
- [INFORMAÇÃO NECESSÁRIA] quanto a outros riscos formalmente levantados pela equipe para a próxima sprint.
- Validar a integração de login/sessão e frontend com produtos e pedidos, aplicar a migração no banco compartilhado e executar a suíte na versão Python prevista após os merges. A disponibilidade retornada pela consulta não implementa cálculo por estoque.
