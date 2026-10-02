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
| #2 Cadastro de categorias | Sim (Sprint 1) | Sim | Há tela ou lógica de administração de categorias atribuível a este integrante |
| #3 Cadastro de produtos (categoria/ingredientes) | Sim (Sprint 1) | Não | Produtos exibidos no Menu são dados mock (`lib/data/products.ts`), não cadastrados via interface administrativa |
| #4 Menu (exibição de produtos ao cliente) | Sim (Sprint 2) | Sim | Dados mock separados da UI. PR #7 (merge `ca5b353`) |
| #5 Carrinho de compras | Sim (Sprint 2) | Sim | Adicionar/remover produto, ajustar quantidade, subtotal/total, persistência via `localStorage`. PR #7 (merge `ca5b353`) |
| #6 Checkout | Sim (Sprint 2) | Sim | Formulário de entrega e pagamento, validação client-side, tela de confirmação "Recebido". Sem integração com backend/API. PR #7 (merge `ca5b353`) |

**Itens entregues fora da numeração formal do Backlog (#1–#6):**
- Estrutura base do projeto frontend (Next.js, TypeScript, Tailwind) — PR #4 (commit `7fa57ec`, merge `96e4bba`).
- Home da visão do cliente (`Navbar`, `Hero`, `Sobre`, `Footer`) — PRs #4 e #8.
- Cadastro de cliente (`(publico)/cadastro/page.tsx`, UI apenas, sem backend) — PR #8 (merge `cbda1ed`).
- Vídeo no Hero (otimizado de ~21MB para ~600KB via `ffmpeg`) e imagens de produtos — PR #9 (commit `b4902bd`).
- Reconciliação da PR #10 (branch `feature/equipe-e-autenticacao`, de Christian de Lima — área de funcionário): resolução de conflitos de merge rename/delete em 13 arquivos, preservação dos hooks `use-funcionarios.tsx`/`use-produtos.tsx`, validação de build e `npm audit fix --force`. Atividade de integração, não de autoria do conteúdo da área de funcionário.

## 2. Incremento funcional demonstrável

Jornada completa do cliente navegável localmente: Home (Navbar, Hero com vídeo, Menu, Sobre, Footer) → Carrinho → Checkout → tela de confirmação de pedido ("Recebido"). Telas de Login e Cadastro de cliente acessíveis como interface, sem persistência real de dados.

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
  - #2 Cadastro de categorias, #3 Cadastro de produtos: permanecem pendentes.

## 4. Evidências de teste

Testes realizados foram manuais, em ambiente local, com `npm run build` aprovado a cada entrega (Home, Menu, Carrinho, Checkout, Login, Cadastro, vídeo no Hero, responsividade mobile) e após o merge da PR #10 (incluindo `npm audit fix --force` seguido de novo build aprovado). Não há testes automatizados, de integração ou cobertura de código registrados. Detalhe completo em `sprint-1-evidencias-teste.md`.

## 5. Retrospectiva e contribuição individual

- Ata de retrospectiva: `sprint-1-retrospectiva.md`
- Relatórios individuais de contribuição: `sprint-1-contribuicao-Gabriel-Freire-Flores.md`: https://github.com/Gabrielfreireflores/Projeto-pizzaria/blob/main/docs/Sprints/sprint-1-%26-2-contribuicao-Gabriel-Freire-Flores.md

## 6. Riscos/impedimentos para a próxima sprint

- Recomenda-se sincronizar branches de longa duração com a `main` com mais frequência, para evitar o acúmulo de conflitos como os ocorridos na reconciliação da PR #10.
- [INFORMAÇÃO NECESSÁRIA] quanto a outros riscos formalmente levantados pela equipe para a próxima sprint.
