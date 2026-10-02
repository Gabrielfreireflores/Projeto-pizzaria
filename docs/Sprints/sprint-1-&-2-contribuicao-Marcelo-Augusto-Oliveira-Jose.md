# Relatório Individual de Contribuição — Sprint 1 e Sprint 2

> Documentado em conjunto devido à unificação dos prazos de entrega das duas Sprints.

## Identificação do integrante

* **Nome:** Marcelo Augusto Oliveira Jose
* **RA:** 2840482423043
* **Usuário GitHub:** `marcelo0liveira`
* **Papel na Sprint 1:** Dados
* **Atuação na Sprint 2:** Desenvolvimento Backend — produtos, pedidos, testes e documentação.

## Atividades realizadas

### Sprint 1

* Implementação do cadastro de produtos com categoria e ingredientes.
* Validação dos campos obrigatórios, preço, ingredientes e quantidades.
* Verificação de permissão de funcionário ativo para cadastrar produtos.
* Tratamento de produtos duplicados e de referências inválidas no banco.
* Organização do código em routes, services, repositories e schemas.
* Ajustes conforme a revisão do colega, incluindo repository de funcionário e aliases.
* Execução de testes automatizados e manuais do cadastro.

### Sprint 2

* Implementação da consulta de produtos com categoria, ingredientes, preço e disponibilidade.
* Implementação da criação de pedidos com validação de contato, endereço e itens.
* Cálculo dos valores do pedido no backend a partir dos preços do banco.
* Gravação de endereço, pedido e itens em uma transação, com rollback em caso de falha.
* Definição do status inicial do pedido como RECEBIDO.
* Criação da migração de banco para os dados de contato e pedido sem funcionário atribuído inicialmente.
* Adequação aos controllers utilizados no backend e ampliação dos testes automatizados.
* Documentação do contrato da API de produtos e das contribuições nas sprints.

## Funcionalidades/artefatos produzidos

* Cadastro e consulta de produtos: routes, controller, service, repository e schema de produto.
* Repository de funcionário para consulta de permissão.
* Criação de pedidos: routes, controller, service, repository e schema de pedido.
* Repositories auxiliares de cliente e endereço.
* Enum de status em `backend/app/models/status_pedido.py`.
* Migração em `db/migrations/001_pedido_contato.sql`.
* Testes em `backend/tests/test_produtos.py` e `backend/tests/test_consulta_pedidos.py`.
* Contrato em `docs/contratos/produto.md` e instruções em `backend/README-consulta-pedidos.md`.

## Entregas realizadas

* **Sprint 1:** domínio e cadastro de produtos, com validações, autorização e persistência no PostgreSQL.
* **Sprint 2:** consulta de produtos, criação de pedidos e status inicial RECEBIDO.
* **Sprint 2:** testes automatizados, contrato da API de produtos e documentação das contribuições.

## Participação na Sprint

Atuação no desenvolvimento do backend, nos testes e na documentação. Alinhamento do código ao padrão utilizado pelo colega, atendimento aos comentários de revisão e envio das entregas para validação por PR.

## Commits relacionados

### Sprint 1

* `b7fb4f5` — implementação do cadastro de produtos.
* `cad3ce7` — separação do repository de funcionário e ajuste do alias do schema.

### Sprint 2

* `96d1490` — consulta de produtos e criação de pedidos com status Recebido.
* `bbc87e1` — documentação do contrato da API de produtos.

## Pull Requests relacionadas

* [PR #6 — Cadastro de produtos](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/6).
* [PR #13 — Consulta de produtos e criação de pedidos](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/13).
* [PR #14 — Contrato da API de produtos](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/14).

## Evidências das atividades

* Histórico de commits e PRs com as implementações e revisões.
* Cadastro de produtos validado com 45 testes aprovados.
* Suíte ampliada para 92 testes aprovados, incluindo os anteriores e testes de integração com PostgreSQL.
* Validação manual de cadastro, duplicidade e permissões.
* Contrato documentado com exemplos de requisição, resposta e erros.

## Observações

As contribuições concentraram-se no backend de produtos e pedidos, seguindo a organização em camadas utilizada pela equipe.

Os resultados dos testes correspondem às versões verificadas durante o desenvolvimento. A integração completa com o frontend e a validação conjunta após os merges permanecem como próximos passos.
