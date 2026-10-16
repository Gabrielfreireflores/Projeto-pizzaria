# Relatório Individual de Contribuição — Sprint 3

## Identificação do integrante

* **Nome:** Marcelo Augusto Oliveira Jose
* **RA:** 2840482423043
* **Usuário GitHub:** `marcelo0liveira`
* **Atuação na Sprint 3:** Desenvolvimento Backend — cardápio, acompanhamento de pedidos, testes e documentação.

## Atividades realizadas

* Implementação da consulta pública de cardápio, retornando somente produtos disponíveis.
* Organização dos produtos por categoria, com nome, tamanho, preço, foto e descrição.
* Criação de migração para adicionar os campos opcionais de foto e descrição aos produtos, preservando os registros existentes.
* Registro do blueprint de cardápio na aplicação Flask.
* Implementação da consulta de acompanhamento do pedido pelo cliente.
* Validação da sessão e do perfil de cliente ativo, permitindo acesso apenas aos próprios pedidos.
* Retorno do status atual e de estimativa de entrega configurável, com prazo padrão de 60 minutos após a criação.
* Indicação de atraso quando a previsão é ultrapassada, sem alterar automaticamente o status do pedido.
* Definição do contrato de atualização periódica para o frontend, com intervalo de 10 segundos e encerramento após entrega ou cancelamento.
* Tratamento de erros e uso de respostas sem cache no acompanhamento.
* Organização das funcionalidades em routes, controllers, services e repositories, seguindo o padrão da equipe.
* Criação e execução de testes automatizados, incluindo integração com PostgreSQL em schemas temporários.
* Identificação de falhas preexistentes nos testes de categorias, pedidos e autenticação.
* Documentação dos endpoints, das regras e das instruções de migração e integração.
* Publicação das implementações em branches e PRs para revisão.

## Funcionalidades/artefatos produzidos

* Consulta de cardápio: `backend/app/routes/cardapio_routes.py`, `backend/app/controllers/cardapio_controller.py`, `backend/app/services/cardapio_services.py` e `backend/app/repositories/cardapio_repository.py`.
* Registro do cardápio em `backend/app/__init__.py`.
* Migração em `db/migrations/002_produto_cardapio.sql`.
* Acompanhamento de pedidos: `backend/app/controllers/acompanhamento_controller.py`, `backend/app/services/acompanhamento_services.py` e `backend/app/repositories/acompanhamento_repository.py`.
* Inclusão da rota de acompanhamento em `backend/app/routes/pedido_routes.py`.
* Testes em `backend/tests/test_cardapio.py` e `backend/tests/test_acompanhamento.py`.
* Documentação em `backend/README-cardapio.md` e `backend/README-acompanhamento-pedido.md`.

## Entregas realizadas

* **H04-01 — Consulta de cardápio:** endpoint `GET /api/v1/cardapio`, com filtro de disponibilidade e agrupamento por categoria.
* **História 9 — Acompanhamento de pedido:** endpoint `GET /api/v1/pedidos/{id}/acompanhamento`, com autorização, status e estimativa de entrega.
* **Testes e documentação:** validação das funcionalidades e contratos para integração com o frontend.

## Participação na Sprint

Atuação na implementação do backend, na persistência e consulta de dados, nos testes e na documentação. Manutenção do padrão em camadas utilizado pela equipe e preparação das entregas para revisão, preservando as funcionalidades dos demais integrantes.

## Commits relacionados

* [`d686b22`](https://github.com/Gabrielfreireflores/Projeto-pizzaria/commit/d686b221924159f2af49d27e3c71073bd26bc6da) — consulta de cardápio por categoria com produtos disponíveis.
* [`534da12`](https://github.com/Gabrielfreireflores/Projeto-pizzaria/commit/534da12d842162c16dc886a497fb6bbecd0b7262) — acompanhamento de pedido com status e estimativa de entrega.

## Pull Requests relacionadas

* [PR #19 — Consulta de cardápio por categoria](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/19): integrada à `main` em 09/10/2026.
* [PR #21 — Acompanhamento de pedido com status e estimativa de entrega](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/21): aberta para revisão na consulta realizada em 09/10/2026.

## Evidências das atividades

* Histórico de commits e PRs com as implementações publicadas.
* Consulta de cardápio validada com 6 testes aprovados, incluindo filtro de disponibilidade, agrupamento, campos opcionais e reaplicação da migração.
* Acompanhamento validado com 25 testes aprovados, incluindo sessão, permissão, proteção de pedidos de outros clientes, estimativa e leitura de mudança de status no banco.
* Verificação conjunta do cardápio com produtos e pedidos: 96 testes aprovados e 2 falhas preexistentes.
* Verificação conjunta do acompanhamento com produtos e pedidos: 115 testes aprovados e as mesmas 2 falhas preexistentes. As execuções ocorreram em branches diferentes e seus totais não devem ser somados.
* Testes executados com Python 3.14.7 e PostgreSQL em schemas temporários, sem aplicar as migrações às tabelas compartilhadas durante os testes.
* Documentação com exemplos de resposta, erros, configuração e orientações para o frontend.

## Observações

As contribuições desta sprint concentraram-se no backend. A atualização automática na tela depende da implementação das consultas periódicas pelo frontend; a alteração de status pelo funcionário pertence à história 8.

A disponibilidade do cardápio usa o campo do cadastro, sem cálculo por estoque. Foto e descrição retornam `null` até serem preenchidas. Upload e edição desses campos pela API não fazem parte desta entrega.

O prazo padrão de entrega precisa ser alinhado com a pizzaria. A consulta interpreta os horários existentes no banco no fuso `America/Sao_Paulo`; essa configuração deve ser confirmada no ambiente de uso. O acompanhamento não exige nova migração.

Permanecem pendentes a integração com as telas e a correção das falhas antigas: rota de categorias desatualizada nos testes, divergência sobre a atribuição de funcionário no pedido e falhas de autenticação observadas na suíte completa. Os resultados registrados correspondem às versões testadas durante o desenvolvimento, não a uma validação final de todos os merges.
