# Relatório Individual de Contribuição — Sprint 1 e Sprint 2

> Documentado em conjunto devido à unificação dos prazos de entrega das duas Sprints.

## Identificação do integrante

* **Nome:** Guilherme Fabiano da Silva Gomes
* **RA:** 2840482423010
* **Usuário GitHub:** `valkyrjiano`
* **Papel na Sprint 1:** Product Owner
* **Papel na Sprint 2:** Desenvolvimento Backend/Scrum Master - Desenvolvimento do Projeto e Organização do Board.

## Atividades realizadas

### Sprint 1

* Participação na definição e organização inicial das funcionalidades do projeto.
* Implementação do backend da funcionalidade de cadastro e gerenciamento de categorias.
* Criação da estrutura inicial da aplicação Flask.
* Implementação da conexão do backend com o PostgreSQL utilizando `psycopg` e `DATABASE_URL`.
* Implementação do repository de categorias, responsável pelas operações de persistência no banco.
* Implementação do service de categorias, concentrando regras de negócio e validações.
* Implementação das rotas HTTP de categorias.
* Organização inicial do backend utilizando separação entre `routes`, `services`, `repositories` e aplicação principal.
* Implementação das operações relacionadas a categorias, incluindo criação, consulta/listagem e remoção.
* Participação na organização da documentação inicial do projeto.
* Execução local do backend e validação das funcionalidades implementadas.

### Sprint 2

* Implementação da estrutura de autenticação de usuários.
* Implementação do repository responsável pelas operações de usuários.
* Implementação do service de autenticação, incluindo normalização de e-mail, validação de dados e regras de cadastro.
* Implementação de armazenamento seguro das senhas utilizando hash.
* Implementação da validação de usuário ativo durante a autenticação.
* Implementação do controller de autenticação para tratamento das requisições HTTP.
* Implementação das rotas de cadastro de clientes e funcionários.
* Registro do Blueprint de autenticação na aplicação Flask.
* Refatoração das rotas de categorias para adequação à arquitetura em camadas utilizada na autenticação.
* Inclusão de tratamento de rollback nas operações de banco de dados de categorias em caso de falha.
* Criação de testes automatizados para as rotas e serviços de autenticação.
* Implementação de testes para cadastro de funcionário, cadastro de cliente, validação de campos obrigatórios, e-mail duplicado e regras da camada de serviço.
* Diagnóstico e resolução de conflitos de integração entre branches durante a evolução do projeto.
* Participação na organização da documentação das Sprints 1 e 2.

## Funcionalidades/artefatos produzidos

* Backend de categorias:

  * `backend/app/database.py`
  * `backend/app/repositories/categoria_repository.py`
  * `backend/app/services/categoria_services.py`
  * `backend/app/routes/categoria_routes.py`
  * `backend/app/__init__.py`
  * `backend/run.py`

* Backend de autenticação:

  * `backend/app/controllers/auth_controller.py`
  * `backend/app/repositories/usuario_repository.py`
  * `backend/app/services/auth_services.py`
  * `backend/app/routes/auth_routes.py`

* Testes automatizados:

  * `backend/tests/test_auth_routes.py`
  * `backend/tests/test_auth_services.py`

* Estrutura de autenticação para cadastro de:

  * clientes;
  * funcionários;
  * usuários ativos;
  * usuários com senha armazenada por hash.

* Estrutura de backend organizada em camadas:

  * `routes`;
  * `controllers`;
  * `services`;
  * `repositories`.

* Documentação das Sprints 1 e 2:

  * Relatório das Sprints;
  * Contribuição Individual;
  * Evidências de Teste;
  * Retrospectiva.

## Entregas realizadas

* **Sprint 1:** implementação do backend de categorias, incluindo conexão com PostgreSQL, repository, service, rotas e estrutura inicial da aplicação Flask.

* **Sprint 2:** implementação da autenticação de usuários, incluindo cadastro de clientes e funcionários, regras de validação, hash de senha, controllers, services, repository, rotas e testes automatizados.

* **Sprint 2:** refatoração da estrutura de categorias para adequação à arquitetura em camadas utilizada no backend.

* **Sprint 2:** documentação consolidada das Sprints 1 e 2.

## Participação na Sprint

Participação comprovada na implementação técnica do backend em ambas as Sprints, incluindo o desenvolvimento da funcionalidade de categorias na Sprint 1, desenvolvimento da autenticação e respectivos testes na Sprint 2, além de atividades de integração e reconciliação de código de outros integrantes.

## Commits relacionados

### Sprint 1

* `a078cff` — `feature adicionar categoria v1` — implementação da funcionalidade de categorias.
* `c2c51ce` — atualização/reconciliação da branch de categorias com a `main`.
* `83735c0` — merge da implementação de categorias à `main`.

### Sprint 2

* `ec57127` — `feat(auth): implementa rotas, controllers e testes de autenticação` — implementação da autenticação, controllers, repository, services, rotas e testes.
* `f401feaa` — atualização/reconciliação da branch de autenticação com a `main`.
* `5f05dc2` — merge da implementação de autenticação à `main`.

## Pull Requests relacionadas

* **PR #5 — Feature/categorias**

  * Implementação do backend da funcionalidade de categorias.
  * Merge `83735c0`.

* **PR #11 — feat(auth): implementa rotas, controllers e testes de autenticação**

  * Implementação da autenticação.
  * Criação de controllers, services, repository, routes e testes.
  * Merge `5f05dc2`.

## Evidências das atividades

* Histórico de atividade do repositório mostrando os commits, branches e merges relacionados às funcionalidades desenvolvidas.
* PR #5 demonstrando a implementação e integração da funcionalidade de categorias.
* PR #11 demonstrando a implementação da autenticação e dos testes automatizados.
* PR #12 demonstrando a criação e integração da documentação das Sprints 1 e 2.
* Arquivos do backend contendo a separação entre `routes`, `controllers`, `services` e `repositories`.
* Testes automatizados presentes em `backend/tests/test_auth_routes.py` e `backend/tests/test_auth_services.py`.
* Execução dos testes automatizados para validação das funcionalidades de autenticação.
* Validação do backend após as alterações e integrações realizadas.
* Histórico de commits utilizado para comprovação das atividades individuais.

## Observações

Nessas duas primeiras Sprints, as contribuições individuais concentraram-se principalmente no desenvolvimento do backend, autenticação, categorias, testes automatizados, organização arquitetural e integração do código.

A implementação de categorias foi realizada na Sprint 1 e posteriormente integrada à `main`. Na Sprint 2, a autenticação foi estruturada em camadas, separando responsabilidades entre rotas, controllers, services e repositories, além da criação de testes automatizados para as principais regras da funcionalidade.
