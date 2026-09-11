# Pizzaria do Barriga

Projeto de uma aplicação web para pedidos e gestão da Pizzaria do Barriga. O sistema permitirá consultar o cardápio, realizar pedidos e acompanhar seu andamento, além de oferecer uma área interna para os funcionários.

**Deploy:** ainda não publicado — previsão a definir pela equipe.

**Equipe:** Gabriel Freire Flores (RA 2840482423010) — Marcelo Augusto Oliveira Jose (RA 2840482423043) — Christian de Lima (RA 2840482523031) — Guilherme Fabiano da Silva Gomes (RA 2840482423037) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto

## Stack

- Frontend planejado: Next.js 16.3.4 + React 19.3.0 + TypeScript 7.0.2 + Tailwind CSS 4.3.3 + shadcn CLI 4.21.0.
- Backend planejado: Python 3.14.7 + Flask 3.1.3.
- Banco de dados: PostgreSQL 15 ou superior.

## Como rodar localmente

### Pré-requisitos

- Git 2 ou superior: https://git-scm.com/downloads
- Python 3.14.7 com pip e venv: https://www.python.org/downloads/windows/
- PostgreSQL 15 ou superior, incluindo o cliente psql: https://www.postgresql.org/download/windows/

Os comandos abaixo utilizam o CMD do Windows. As ferramentas devem estar disponíveis no PATH, e o serviço do PostgreSQL deve estar iniciado na porta 5432.

### Passo a passo

1. Clone o repositório:

   ```cmd
   git clone https://github.com/Gabrielfreireflores/Projeto-pizzaria.git
   cd Projeto-pizzaria
   ```

2. Crie e ative o ambiente virtual e instale as dependências:

   ```cmd
   python -m venv backend\.venv
   backend\.venv\Scripts\activate.bat
   python -m pip install -r backend\requirements-dev.txt
   ```

   O arquivo de desenvolvimento também instala as dependências de `backend/requirements.txt`.

3. Configure as variáveis de ambiente, copiando `backend/.env.example` para `backend/.env`:

   ```cmd
   copy backend\.env.example backend\.env
   ```

   Edite `backend/.env` e preencha:

   | Variável | Descrição |
   |---|---|
   | `DATABASE_URL` | String de conexão com o PostgreSQL, ex.: `postgresql://postgres:SUA_SENHA@localhost:5432/pizzaria` |

   Não envie o arquivo `.env` com credenciais reais ao GitHub. A leitura dessa variável pela aplicação será implementada junto ao backend; os comandos SQL abaixo utilizam parâmetros explícitos.

4. Crie um banco vazio e execute o schema:

   ```cmd
   psql -h localhost -p 5432 -U postgres -d postgres -v ON_ERROR_STOP=1 -c "CREATE DATABASE pizzaria;"
   psql -h localhost -p 5432 -U postgres -d pizzaria -v ON_ERROR_STOP=1 -f "db/schema.sql"
   ```

   Informe a senha do usuário `postgres` quando solicitada. Execute o script uma única vez em um banco vazio.

5. O seed já está incluído em `db/schema.sql`; não há migrations ou comandos adicionais de carga. Os usuários de exemplo possuem hashes fictícios, sem credenciais válidas para login.

6. A inicialização da aplicação ainda não está disponível: o backend não foi implementado e a interface está em prototipação no Figma. Nesta versão, é possível preparar o banco e instalar as dependências.

7. Ainda não há URL local da aplicação. O protótipo em desenvolvimento pode ser acessado em [Figma — Pizzaria do Barriga](https://www.figma.com/design/hd8egMUs65MPhKonVAZqMm/Pizzaria-do-Barriga).

## Estrutura do repositório

```text
/backend    — dependências Python e modelo de configuração .env.example
/db         — schema.sql com criação das tabelas e seed
/docs       — documento de visão, termo de aceite, backlog, UML e DER
```

## Convenções da equipe

- Branches: `docs/nome-curto` para documentação, a partir de `main`, seguindo o padrão utilizado em `docs/entrega-e4-readme`.
- Commits: `docs: descrição da alteração` para documentação, seguindo o padrão utilizado nesta entrega.
- Toda PR exige revisão de ao menos 1 integrante antes do merge.

## Testes

A preparação do banco de dados, a instalação das dependências Python e a conexão com o PostgreSQL foram testadas por Marcelo Augusto Oliveira Jose, integrante do grupo. O comando `python -m pip check` não identificou conflitos de dependências.

## Licença / Uso acadêmico

Projeto desenvolvido para a disciplina de Laboratório de Engenharia de Software — ADS, Fatec Ribeirão Preto, 2026.
