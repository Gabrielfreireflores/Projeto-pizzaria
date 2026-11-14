# Pizzaria do Barriga

Projeto de uma aplicação web para pedidos e gestão da Pizzaria do Barriga. O sistema permitirá consultar o cardápio, realizar pedidos e acompanhar seu andamento, além de oferecer uma área interna para os funcionários.

> **Atualização de 13/11/2026:** o texto original abaixo foi preservado. As informações atuais de deploy, versões, execução e testes estão em [Novidades e estado atual](#novidades-e-estado-atual--13112026).

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



4. Crie um banco vazio e execute o schema:

   ```cmd
   psql -h localhost -p 5432 -U postgres -d postgres -v ON_ERROR_STOP=1 -c "CREATE DATABASE pizzaria;"
   psql -h localhost -p 5432 -U postgres -d pizzaria -v ON_ERROR_STOP=1 -f "db/schema.sql"
   ```

   Informe a senha do usuário `postgres` quando solicitada. Execute o script uma única vez em um banco vazio.

5. O seed já está incluído em `db/schema.sql`.

6. Para inicializar a aplicação backend com os endpoints execute:
   ``` python run.py ```
   OBS: Endpoints ainda sendo desenvolvidos.

   FrontEnd em desenvolvimento.

8. Ainda não há URL local da aplicação. O protótipo em desenvolvimento pode ser acessado em [Figma — Pizzaria do Barriga](https://www.figma.com/design/hd8egMUs65MPhKonVAZqMm/Pizzaria-do-Barriga).

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

## Novidades e estado atual — 13/11/2026

As seções anteriores foram mantidas como registro original do projeto. As informações de deploy, versões e execução abaixo atualizam aquele planejamento.

### Aplicação publicada e entregas finais

- **Frontend:** https://projeto-pizzaria-frontend-seven.vercel.app
- **Backend:** https://projeto-pizzaria-backend-xi.vercel.app
- [Documentação final E1–E10](docs/documentacao-final.md), [relatório de testes E9](docs/relatorio-testes-final.md), [Termo de Aceite do Cliente](docs/termo-aceite-cliente.md), [Manual do Usuário com capturas reais](docs/manual-do-usuario.md) e [checklist das entregas](docs/evidencias/e9-e10/checklist-entrega.md).
- Demonstração exclusivamente acadêmica, sem operação comercial nesta hospedagem. Assinatura, homologação com cliente, capturas internas e atividades externas continuam pendentes; vídeo e roteiro não foram produzidos.

### Funcionalidades acrescentadas e integrações

- Cardápio integrado à API, busca, modal responsivo, sabores mistos, borda vinculada à pizza e sacola persistida no navegador.
- Checkout com login de cliente obrigatório, contato, entrega/retirada, pagamento informativo e confirmação. Funcionário consulta pedidos, aceita e avança status; gerencia produtos e equipe.
- Dois projetos Vercel Hobby; o Next encaminha `/api` ao Flask. PostgreSQL Neon Free, limitador de login Upstash Free e imagens Vercel Blob Hobby.
- Sessões, CSRF e autorização por perfil; cookies seguros em produção e validação de conteúdo das imagens. Preservar `httpx2`, dependência real do adaptador Blob. Limite de imagem: 3 MiB; requisição completa em produção: 4 MiB.
- Limitações reais: categorias sem ativação, disponibilidade sem cálculo de estoque, receita opcional, acompanhamento do cliente manual sem estimativa, sem Gerente separado e sem relatório/dashboard de vendas/CSV. A aprovação dos desvios depende do cliente/professor; o escopo inicial não foi alterado para ocultá-los.

### Versões efetivamente verificadas

O planejamento da seção Stack foi preservado. Na validação atual: Python **3.13.2** (backend declara 3.13), Flask 3.1.3, psycopg 3.3.5, Node 20.19.4, Next.js 16.3.4, React 19.3.0, TypeScript 5.9.3 e Tailwind 3.4.19. As versões TypeScript 7, Tailwind 4 e Python 3.14 citadas anteriormente não são as usadas nesta bateria.

### Complementos para executar a versão atual

Os comandos originais em CMD continuam registrados acima. Para a versão atual, usar Python 3.13 e configurar também uma `SECRET_KEY` de desenvolvimento, além de `DATABASE_URL`. Copiar `frontend/.env.example` para `frontend/.env.local` e manter `BACKEND_URL=http://127.0.0.1:5000`. Nunca versionar os arquivos reais de ambiente.

**Banco novo:** o schema isolado não instala todo o cardápio atual. Usar o [procedimento controlado](db/README-inicializacao.md) e seu manifesto explícito. Não reaplicar schema/seeds no Neon já inicializado, não renumerar os dois arquivos 005 e não executar a migration 008 na instalação nova. Não há inicialização SQL automática no startup ou deploy.

Após configurar um banco já inicializado, no PowerShell a partir da raiz:

```powershell
Set-Location backend
& ./.venv/Scripts/python.exe run.py
```

Em outro terminal, a partir da raiz:

```powershell
Set-Location frontend
npm.cmd ci
npm.cmd run dev
```

A interface local está em http://127.0.0.1:3000 e o backend em http://127.0.0.1:5000. `npm.cmd` evita o bloqueio de `npm.ps1` em algumas instalações Windows. A primeira conta de funcionário é criada por administração explícita, sem rota pública ou criação automática. Cadastro pela tela grava no banco configurado: usar somente ambiente autorizado.

### Testes automatizados e build

Em PowerShell separado, a partir da raiz, sem usar o Neon para testes de escrita:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHON_DOTENV_DISABLED = '1'
$env:DATABASE_URL = ''
$env:TEST_DATABASE_URL = ''
$env:TEST_NEXT_PROXY = ''
$env:APP_ENV = 'development'
$env:VERCEL = '0'
$env:LOGIN_RATE_LIMITER = 'disabled'
$env:IMAGE_STORAGE = 'local'
$env:SECRET_KEY = 'somente-testes-locais-sem-credenciais'
Push-Location backend
& ./.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider
Pop-Location
Push-Location frontend
node --test tests/deploy-config.test.mjs
npm.cmd run lint
node node_modules/typescript/bin/tsc --noEmit --incremental false
$env:BACKEND_URL = 'http://127.0.0.1:5000'
npm.cmd run build
Pop-Location
```

O build precisa acessar as fontes públicas do Google. Depois do build com backend local e portas 5000/3107 livres, definir `TEST_NEXT_PROXY=1` e repetir pytest habilita o teste local de proxy, com login e serviços simulados. Ele encerra os servidores ao finalizar.

Em 13/11/2026: **282 aprovados / 43 ignorados** no backend com proxy opt-in e **4 aprovados** no frontend; build e TypeScript aprovados; lint com zero erros e cinco avisos existentes. Sem o proxy opt-in: 281 aprovados / 44 ignorados. Os ignorados dependem de PostgreSQL de teste. Não há workflow CI versionado nesta revisão. Os resultados não substituem nem se somam aos testes históricos de Marcelo registrados acima. [Evidências e comandos](docs/evidencias/e9-e10/validacao-2026-11-13.md).

### Estrutura e publicação

A estrutura ganhou `frontend/`, os adaptadores de serviços e a documentação E9/E10. As imagens do manual estão em `docs/evidencias/e9-e10/imagens/`. [Guia atualizado de deploy e variáveis](docs/deploy-academico-vercel.md).

As convenções originais de revisão por PR permanecem. Preservar autoria e comentários; não publicar sem autorização, pois o push pode disparar previews. Não incluir `.env`, cookies, tokens, dumps ou artefatos de build. Manter somente planos gratuitos, sem trial pago, cartão ou upgrade automático.
