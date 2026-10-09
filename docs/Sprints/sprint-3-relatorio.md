# Relatório de Entrega — Sprint 3 — Pizzaria do Barriga

**Período:** a preencher pela equipe.
**Sprint Review:** a preencher pela equipe.

**Trilha:** B (Cliente real nº 1)

> Registro parcial das entregas da Sprint 3, a complementar pela equipe. Situação das PRs consultada em 09/10/2026.

## 1. Planejado vs. entregue

| História (E2) | Planejada para esta sprint? | Entregue? | Observação |
|---|---|---|---|
| #4 — H04-01 Consulta de cardápio | Executada nesta sprint | Backend integrado | GET público de produtos disponíveis, agrupados por categoria, com foto, descrição e preço. PR #19 integrada. Não inclui cálculo por estoque nem integração com a tela |
| #9 Acompanhamento de pedido | Sim (Sprint 3) | Backend implementado; em revisão | Consulta restrita ao dono do pedido, com status e estimativa de entrega. PR #21 aberta na data do registro. Atualização automática na tela depende do frontend |

**Artefatos de apoio entregues:**

- Migração `002_produto_cardapio.sql`, adicionando foto e descrição opcionais aos produtos.
- Testes automatizados de cardápio e acompanhamento, incluindo PostgreSQL em schemas temporários.
- Documentação dos contratos em `backend/README-cardapio.md` e `backend/README-acompanhamento-pedido.md`.

## 2. Incremento funcional demonstrável

O endpoint `GET /api/v1/cardapio` consulta os produtos disponíveis e os organiza por categoria. Retorna nome, tamanho, preço, foto e descrição; categorias vazias são omitidas.

O endpoint `GET /api/v1/pedidos/{id}/acompanhamento` permite que um cliente autenticado e ativo consulte apenas seus próprios pedidos. Retorna status, estimativa de entrega e intervalo de 10 segundos para nova consulta. Pedidos entregues ou cancelados indicam encerramento do acompanhamento.

- **Link do deploy:** não registrado neste registro.
- **GIF/vídeo de demonstração:** não registrado neste registro.
- **Como reproduzir localmente:** seguir os READMEs de cada funcionalidade. Para cardápio, aplicar a migração 002 antes de consultar. Para acompanhamento, usar a sessão de um cliente e o ID de um pedido dele. A criação da tela e a alteração de status pelo funcionário não fazem parte destas entregas.

## 3. Backlog atualizado

- H04-01: backend implementado e integrado pela [PR #19](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/19).
- História #9: backend implementado e publicado para revisão na [PR #21](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/21); integração com frontend pendente neste registro.
- Esses registros descrevem as evidências de código e PR, sem alterar automaticamente o board nem declarar concluídas todas as partes das histórias.

## 4. Evidências de teste

- Cardápio: 6 testes aprovados. Verificação conjunta com produtos e pedidos: 96 aprovados e 2 falhas preexistentes.
- Acompanhamento: 25 testes aprovados. Verificação conjunta com produtos e pedidos: 115 aprovados e as mesmas 2 falhas preexistentes.
- Execuções com Python 3.14.7 e PostgreSQL em schemas temporários. Os totais são de execuções em branches diferentes e não devem ser somados.
- Detalhes em [Evidências de teste da Sprint 3](sprint-3-evidencias-teste.md). Não houve validação ponta a ponta das telas neste registro.

## 5. Retrospectiva e contribuição individual

- [Retrospectiva da Sprint 3](sprint-3-retrospectiva.md).
- [Relatório individual de contribuição](sprint-3-contribuicao-Marcelo-Augusto-Oliveira-Jose.md).
- Commits: `d686b22` (cardápio) e `534da12` (acompanhamento).

## 6. Riscos/impedimentos para a próxima sprint

- Validar a integração das telas com os endpoints e a atualização periódica do acompanhamento.
- Alinhar o prazo estimado de entrega, inicialmente de 60 minutos, com a operação da pizzaria e confirmar o fuso dos horários gravados no banco.
- Confirmar aplicação da migração 002 no ambiente compartilhado e preenchimento de foto/descrição; registros sem esses dados retornam `null`.
- Resolver as falhas antigas de testes: rota de categorias desatualizada e divergência na atribuição de funcionário ao pedido. A suíte completa também apresentou falhas de autenticação.
- Executar novamente os testes após a integração das branches. A estimativa atual usa configuração geral; não existe previsão individual persistida por pedido.
