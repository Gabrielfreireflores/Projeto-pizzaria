# Pizzaria do Barriga

Aplicação web acadêmica para cardápio, pedidos e acompanhamento interno da Pizzaria do Barriga, Jardinópolis-SP. O MVP tem perfis Cliente e Funcionário; esta hospedagem não realiza operação comercial.

**Frontend publicado:** https://projeto-pizzaria-frontend-seven.vercel.app

**Backend publicado:** https://projeto-pizzaria-backend-xi.vercel.app

**Equipe:** Gabriel Freire Flôres (RA 2840482423010) — Marcelo Augusto Oliveira Jose (RA 2840482423043) — Christian de Lima (RA 2840482523031) — Guilherme Fabiano da Silva Gomes (RA 2840482423037). Laboratório de Engenharia de Software, ADS Fatec Ribeirão Preto, 2026/2; Trilha B, cliente real nº 1.

## Entregas e estado do MVP

- [Índice E1–E10](docs/documentacao-final.md), [relatório E9](docs/relatorio-testes-final.md), [termo final a assinar](docs/termo-aceite-cliente.md), [manual com capturas reais](docs/manual-do-usuario.md).
- Cardápio, busca, modal responsivo, sabores mistos, borda vinculada à pizza e sacola persistida no navegador.
- Checkout exige login de cliente; contato, entrega/retirada, pagamento informativo e confirmação. Funcionário consulta pedidos, aceita e avança status; gerencia produtos e equipe.
- Limitações: categorias sem ativação, disponibilidade sem estoque de ingredientes, receita opcional, acompanhamento do cliente manual sem estimativa, sem Gerente separado e sem relatório/dashboard de vendas/CSV. A aprovação dessas diferenças depende do cliente/professor; o escopo original foi preservado.
- [Checklist E9/E10](docs/evidencias/e9-e10/checklist-entrega.md): homologação, assinatura, capturas internas e atividades externas pendentes. Vídeo e roteiro não produzidos nesta revisão.

## Stack e arquitetura

Next.js 16.3.4, React 19.3.0, TypeScript 5.9.3 e Tailwind 3.4.19 no ambiente/lockfile verificados. Python **3.13** (local 3.13.2), Flask 3.1.3 e psycopg 3.3.5. Node local validado: 20.19.4. Versões de produção e variáveis: [guia de deploy](docs/deploy-academico-vercel.md).

Dois projetos Vercel Hobby (`frontend/` e `backend/`); Next encaminha `/api` ao Flask. PostgreSQL Neon Free, limitador distribuído Upstash Free e imagens Vercel Blob Hobby. O navegador usa o domínio do frontend, sem CORS amplo. Preservar `httpx2`, dependência real do adaptador Blob. Manter somente planos gratuitos, sem trial pago, cartão ou upgrade automático.

## Como rodar localmente

Pré-requisitos: Git, Python 3.13, Node compatível com Next 16 e PostgreSQL 15+ **local e descartável** se for necessário inicializar banco. Não apontar testes de escrita para o Neon publicado. Os comandos usam PowerShell; `npm.cmd` evita bloqueios de `npm.ps1` em algumas instalações Windows.

```powershell
git clone https://github.com/Gabrielfreireflores/Projeto-pizzaria.git
Set-Location Projeto-pizzaria
py -3.13 -m venv backend/.venv
& ./backend/.venv/Scripts/python.exe -m pip install -r backend/requirements-dev.txt
Copy-Item backend/.env.example backend/.env
Copy-Item frontend/.env.example frontend/.env.local
```

Preencher privadamente `DATABASE_URL` e uma `SECRET_KEY` de desenvolvimento no backend. Usar `APP_ENV=development`, `IMAGE_STORAGE=local` e `LOGIN_RATE_LIMITER=disabled` somente no desenvolvimento. No frontend: `BACKEND_URL=http://127.0.0.1:5000`. Nunca versionar os ambientes reais; tokens ficam no backend.

**Banco novo:** seguir [inicialização controlada](db/README-inicializacao.md) e o manifesto explícito. O schema isolado não instala todo o cardápio atual. Comandos administrativos exigem confirmação e destino verificado: não executá-los contra o Neon já inicializado, não reaplicar seeds, não renumerar os dois 005 e não executar a migration 008 na instalação nova. Não há inicialização SQL automática no Flask ou build.

Após configurar um banco já inicializado, iniciar o backend:

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

Abrir http://127.0.0.1:3000; backend em http://127.0.0.1:5000. O primeiro funcionário é criado por administração explícita conforme o guia, nunca por rota pública ou startup. Cadastro de cliente grava no banco configurado: usar somente ambiente autorizado.

## Testes e build seguros

Em PowerShell separado, a partir da raiz e sem credenciais remotas de teste:

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

O build precisa acessar fontes públicas do Google. Após build com backend local e portas 5000/3107 livres, o proxy pode ser testado definindo `TEST_NEXT_PROXY=1` e repetindo pytest. Ele usa login/negócio simulados, sem PostgreSQL, e encerra os servidores locais ao finalizar.

Em 13/11/2026: **282 passaram / 43 ignorados** no backend com proxy opt-in; **4 passaram** no frontend; build/TypeScript aprovados e lint com zero erros e cinco avisos existentes. Sem proxy: 281 passaram / 44 ignorados. Os ignorados dependem de PostgreSQL de teste. Não há workflow CI versionado nesta revisão. [Comandos e evidências](docs/evidencias/e9-e10/validacao-2026-11-13.md).

## Estrutura, contribuição e uso acadêmico

`backend/`: API/administração; `frontend/`: interface; `db/`: schema/migrations/manifesto; `docs/`: E1–E10, modelos, contratos, sprints e evidências. [Protótipo Figma](https://www.figma.com/design/hd8egMUs65MPhKonVAZqMm/Pizzaria-do-Barriga).

Preservar autoria e comentários; trabalhar em branch e PR com revisão de ao menos um integrante. Não publicar sem autorização: pushes podem disparar previews. Não incluir `.env`, cookies, tokens, dumps ou artefatos de build. O termo E2 permanece histórico e o parecer final do cliente não foi preenchido pela equipe.

Projeto acadêmico de 2026. Vercel Hobby restrito à demonstração, sem pedidos comerciais reais; não há licença comercial declarada neste repositório.
