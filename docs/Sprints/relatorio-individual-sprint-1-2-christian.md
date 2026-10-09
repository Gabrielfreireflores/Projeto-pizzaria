# Relatório Individual de Contribuição — Sprint 1 & 2 — Christian de Lima (RA 2840482523031)

**Papel nesta sprint:** Frontend

## 1. O que fiz

| Item | PR/commit | Status |
| --- | --- | --- |
| Layout compartilhado da área do funcionário (sidebar, navegação, item ativo) | `feat: cadastro, login, área do funcionário e gestão de equipe/produtos` | Concluído |
| Hook `use-produtos.tsx` (contexto de produtos e categorias) | `feat: cadastro, login, área do funcionário e gestão de equipe/produtos` | Concluído |
| Hook `use-funcionarios.tsx` (contexto de equipe) | `feat: cadastro, login, área do funcionário e gestão de equipe/produtos` | Concluído |
| Página de Pedidos (`/funcionario`) com atualização de status | `feat: cadastro, login, área do funcionário e gestão de equipe/produtos` | Concluído |
| Listagem, cadastro e edição de Produtos (`/funcionario/produtos`) | `feat: cadastro, login, área do funcionário e gestão de equipe/produtos` | Concluído |
| Listagem, cadastro e edição de Equipe (`/funcionario/equipe`) | `feat: cadastro, login, área do funcionário e gestão de equipe/produtos` | Concluído |
| Página de Cadastro da pizzaria (`/cadastro`) | `feat: cadastro, login, área do funcionário e gestão de equipe/produtos` | Concluído |
| Página de Login (`/login`) | `feat: cadastro, login, área do funcionário e gestão de equipe/produtos` | Em andamento |
| Abertura do PR da branch `feature/equipe-e-autenticacao` para a `main` | [PR nº a preencher] | A fazer |

## 2. Rituais que participei

- [x]  Weeklies
- [x]  Sprint Review
- [x]  Retrospectiva

## 3. Dificuldades e o que aprendi

- Estrutura de layout: nas primeiras versões, duplicava a sidebar e o container flex dentro de cada `page.tsx`, o que quebrava o posicionamento do conteúdo. Aprendi a manter toda a estrutura compartilhada (`<main>`, `<aside>`, `<section>`) apenas no `layout.tsx`, deixando cada página responsável somente pelo seu conteúdo específico.
- Context API: enfrentei o erro useProdutos precisa estar dentro de useProvider por esquecer de envolver o layout com o Provider correspondente. Aprendi que é importânte posicionar o Provider no nível mais alto da árvore de componentes que precisa acessar aquele estado.
- Imports relativos: tive dificuldade em contar corretamente os `../` em rotas aninhadas (ex: `[id]/editar`). Passei a usar o alias `@/` configurado no `tsconfig.json` para evitar esse tipo de erro.
- Controle de versão: por engano, enviei um commit diretamente à branch `main`, fora do fluxo de Pull Request adotado pelo time. Aprendi a reverter esse commit com segurança usando `git revert` (que preserva o histórico, em vez de reescrevê-lo) e a reenviar o conteúdo por meio de uma branch dedicada, respeitando o processo de revisão combinado com a equipe.
