# Relatório de Entrega — Sprint 3 — Pizzaria do Barriga

**Período:** a preencher pela equipe.
**Sprint Review:** a preencher pela equipe.

**Trilha:** B (Cliente real nº 1)

Equipe: Gabriel Freire Flôres (RA 2840482423010) — Marcelo Augusto Oliveira Jose (RA 2840482423043) — Christian de Lima (RA 2840482523031) — Guilherme Fabiano da Silva Gomes (RA 2840482423037)

> Registro parcial das entregas da Sprint 3, a complementar pela equipe. Situação das PRs consultada em 09/10/2026.

## 1. Planejado vs. entregue

| História (E2) | Planejada para esta sprint? | Entregue? | Observação |
|---|---|---|---|
| #4 — H04-01 Consulta de cardápio | Executada nesta sprint | Backend integrado | GET público de produtos disponíveis, agrupados por categoria, com foto, descrição e preço. PR #19 integrada. Não inclui cálculo por estoque nem integração com a tela |
| #9 Acompanhamento de pedido | Sim (Sprint 3) | Backend implementado; em revisão | Consulta restrita ao dono do pedido, com status e estimativa de entrega. PR #21 aberta na data do registro. Atualização automática na tela depende do frontend |
| #4 — Cardápio no frontend do cliente (Gabriel) | Executada nesta sprint | Entregue no frontend, com dados locais | Cardápio v2 do PDF oficial com 45 itens (31 pizzas salgadas, 5 doces, 4 bordas e 5 refrigerantes), tamanhos P e G, ingredientes e preços. 9 itens têm foto (4 pizzas e os 5 refrigerantes); as demais dependem da pizzaria. Ainda não consome o `GET /api/v1/cardapio` |
| #5 — Carrinho no frontend (Gabriel) | Evolução da história da Sprint 2 | Entregue no frontend | Tela do carrinho restaurada após regressão da PR #10, com itens por tamanho, pizza meio a meio e observação por item |
| #6 — Checkout e pedido no frontend (Gabriel) | Evolução da história da Sprint 2 | Entregue no frontend, sem backend | Checkout simplificado, Entrega (somente em Jardinópolis) ou Retirada, e pedido criado com status `recebido` gravado no navegador. Ainda não envia o pedido ao backend |
| #9 — Acompanhamento no frontend (Gabriel) | Sim (Sprint 3) | Não iniciado no frontend | Depende da revisão do endpoint (PR #21), da estimativa de entrega e do alinhamento da nomenclatura de status |
| #1 — Login com perfil no frontend (Gabriel) | História da Sprint 1 | Pendente | A interface existe; faltam validação, redirecionamento por perfil e proteção de rota. A autenticação real depende do backend |

**Artefatos de apoio entregues:**

- Migração `002_produto_cardapio.sql`, adicionando foto e descrição opcionais aos produtos.
- Testes automatizados de cardápio e acompanhamento, incluindo PostgreSQL em schemas temporários.
- Documentação dos contratos em `backend/README-cardapio.md` e `backend/README-acompanhamento-pedido.md`.
- Frontend do cliente (Gabriel Freire Flôres): dados e tipos do cardápio (`lib/data/products.ts`, `types/product.ts`), camada de pedidos (`services/orders.ts`, `types/order.ts`) e formato de pedido preparado para o backend.

## 2. Incremento funcional demonstrável

O endpoint `GET /api/v1/cardapio` consulta os produtos disponíveis e os organiza por categoria. Retorna nome, tamanho, preço, foto e descrição; categorias vazias são omitidas.

O endpoint `GET /api/v1/pedidos/{id}/acompanhamento` permite que um cliente autenticado e ativo consulte apenas seus próprios pedidos. Retorna status, estimativa de entrega e intervalo de 10 segundos para nova consulta. Pedidos entregues ou cancelados indicam encerramento do acompanhamento.

- **Link do deploy:** não registrado neste registro.
- **GIF/vídeo de demonstração:** não registrado neste registro.
- **Como reproduzir localmente:** seguir os READMEs de cada funcionalidade. Para cardápio, aplicar a migração 002 antes de consultar. Para acompanhamento, usar a sessão de um cliente e o ID de um pedido dele. A criação da tela e a alteração de status pelo funcionário não fazem parte destas entregas.

### Incremento do frontend do cliente (Gabriel Freire Flôres)

Fluxo demonstrável no navegador, sem backend: cardápio v2 em categorias, com seletor de tamanho P/G, pizza meio a meio e observação por item; sacola com quantidades e total; checkout com opção de Entrega (somente em Jardinópolis) ou Retirada; criação do pedido com status `recebido` e confirmação em tela.

- **Branch:** `feat/cardapio-v2-pedido` (commits `d962689` e `f9e9faa`).
- **Como reproduzir localmente:** na pasta `frontend/`, executar `npm ci` e `npm run dev`; abrir `http://localhost:3000`, adicionar pizzas ao pedido (tamanho, meio a meio, observação), abrir a sacola e finalizar o pedido. O pedido fica registrado no navegador (chave `pizzaria-orders` do localStorage).
- **Link do deploy / vídeo de demonstração:** não registrados.

## 3. Backlog atualizado

- H04-01: backend implementado e integrado pela [PR #19](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/19).
- História #9: backend implementado e publicado para revisão na [PR #21](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/21); integração com frontend pendente neste registro.
- Esses registros descrevem as evidências de código e PR, sem alterar automaticamente o board nem declarar concluídas todas as partes das histórias.
- Frontend (Gabriel): cardápio v2, carrinho com meio a meio e observação, checkout com Entrega/Retirada e criação do pedido implementados na branch `feat/cardapio-v2-pedido`; consumo de `GET /api/v1/cardapio` e envio do pedido ao backend pendentes.
- Frontend (Gabriel): login com perfil (#1) e acompanhamento do pedido (#9) pendentes no frontend.

## 4. Evidências de teste

- Cardápio: 6 testes aprovados. Verificação conjunta com produtos e pedidos: 96 aprovados e 2 falhas preexistentes.
- Acompanhamento: 25 testes aprovados. Verificação conjunta com produtos e pedidos: 115 aprovados e as mesmas 2 falhas preexistentes.
- Execuções com Python 3.14.7 e PostgreSQL em schemas temporários. Os totais são de execuções em branches diferentes e não devem ser somados.
- Detalhes em [Evidências de teste da Sprint 3](sprint-3-evidencias-teste.md). Não houve validação ponta a ponta das telas neste registro.
- Frontend (Gabriel): `npm run build` aprovado (Next.js 16.3.4 e React 19) e fluxo completo testado manualmente; pedido conferido no localStorage do navegador. Não há testes automatizados no frontend. Detalhes na página de evidências.

## 5. Retrospectiva e contribuição individual

- [Retrospectiva da Sprint 3](sprint-3-retrospectiva.md).
- [Relatório individual de contribuição](sprint-3-contribuicao-Marcelo-Augusto-Oliveira-Jose.md).
- Commits: `d686b22` (cardápio) e `534da12` (acompanhamento).
- [Relatório individual — Gabriel Freire Flôres](sprint-3-contribuicao-Gabriel-Freire-Flores.md).
- Commits do frontend: `d962689` (cardápio v2, meio a meio, observação, checkout, retirada e pedido) e `f9e9faa` (atualização de dependências).

## 6. Riscos/impedimentos para a próxima sprint

- Validar a integração das telas com os endpoints e a atualização periódica do acompanhamento.
- Alinhar o prazo estimado de entrega, inicialmente de 60 minutos, com a operação da pizzaria e confirmar o fuso dos horários gravados no banco.
- Confirmar aplicação da migração 002 no ambiente compartilhado e preenchimento de foto/descrição; registros sem esses dados retornam `null`.
- Resolver as falhas antigas de testes: rota de categorias desatualizada e divergência na atribuição de funcionário ao pedido. A suíte completa também apresentou falhas de autenticação.
- Executar novamente os testes após a integração das branches. A estimativa atual usa configuração geral; não existe previsão individual persistida por pedido.
- Frontend (Gabriel): somente 9 dos 45 itens do cardápio têm foto; as demais dependem da pizzaria.
- Frontend (Gabriel): alinhar a nomenclatura de status do pedido entre frontend (`recebido`, `em_preparo`, `pronto`, `entregue`), backend ("Recebido", "Em preparação") e área do funcionário ("Em produção", "Pronto", "Entregue").
- Frontend (Gabriel): verificar se o contrato de criação de pedido do backend comporta meio a meio, observação e retirada, e mapear os tamanhos P e G do cardápio do backend.
