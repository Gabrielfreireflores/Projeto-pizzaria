# Registro da bateria final — 13/11/2026

Fuso de referência: America/Sao_Paulo. Código local `6619185730be4946b59cba95ae5e3e6f75a26687`, sem mudança funcional nesta bateria. Main remota consultada pelo conector GitHub: `fa3cb7f32c6131eadede3e8ced1ef77cb3c6bcce`, com diferenças apenas em documentação. Não foi feito fetch, merge, commit, push ou deploy nesta tarefa.

## Ambiente e isolamento

Windows; Python 3.13.2; Node 20.19.4; Next 16.3.4; React 19.3.0; TypeScript 5.9.3; Tailwind 3.4.19; ESLint 8.57.1. Segredos não foram lidos de `.env` nem expostos. Os testes locais usaram `PYTHON_DOTENV_DISABLED=1`, `PYTHONDONTWRITEBYTECODE=1`, `DATABASE_URL` e `TEST_DATABASE_URL` vazias, `APP_ENV=development`, `VERCEL=0`, `LOGIN_RATE_LIMITER=disabled`, `IMAGE_STORAGE=local` e chave de sessão exclusiva de teste.

## Comandos e resultados reais

| Execução | Diretório / comando | Resultado |
|---|---|---|
| Backend padrão | `backend`: `.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider --tb=short`, `TEST_NEXT_PROXY` vazio | 281 passed, 44 skipped, 4.34 s |
| Backend com proxy local | Mesmo comando, `TEST_NEXT_PROXY=1`, após build com `BACKEND_URL=http://127.0.0.1:5000` | 282 passed, 43 skipped, 10.07 s |
| Dependências | `backend`: `.venv/Scripts/python.exe -B -m pip check` | No broken requirements found |
| Frontend | `frontend`: `node --test tests/deploy-config.test.mjs` | 4 passaram, 0 falhas |
| ESLint | `frontend`: `node node_modules/eslint/bin/eslint.js src --ext .ts,.tsx` | Exit 0; 0 erros, 5 avisos de `<img>` |
| TypeScript | `frontend`: `node node_modules/typescript/bin/tsc --noEmit --incremental false` | Exit 0 |
| Build de produção | `frontend`: `node node_modules/next/dist/bin/next build` | Exit 0, 16 páginas geradas; rotas dinâmicas de edição preservadas |

O primeiro build foi impedido pelo bloqueio de saída para Google Fonts. Repetição com acesso às fontes públicas foi aprovada, sem mudar fonte, dependência ou funcionalidade. Nenhuma migration, seed ou bootstrap foi executada. Os dois resultados de pytest são execuções alternativas da mesma suíte: não somar 281 + 282. A bateria final considera 282 aprovados e 43 ignorados; os quatro testes Node são distintos.

O teste `test_next_proxy.py` iniciou Flask/Next apenas em loopback, usando mocks de autenticação e repositories. Ele testa login fictício, cookie, métodos HTTP, CSRF e multipart com arquivos temporários locais; encerra os servidores ao finalizar. Não representa login real no Neon.

## Disponibilidade publicada — somente GET sem sessão

| URL/caminho | Resultado |
|---|---|
| `https://projeto-pizzaria-frontend-seven.vercel.app/` | 200, HTML |
| Frontend `/login` | 200, HTML |
| Frontend `/cadastro` | 200, HTML |
| Frontend `/carrinho` | 200, HTML |
| Frontend `/api/v1/cardapio` | 200, JSON, `Cache-Control: no-store`, 85 produtos / 4 categorias não vazias |
| Frontend `/api/v1/me` | 401 |
| Frontend `/api/v1/meus-pedidos` | 401 |
| Frontend `/api/v1/pedidos` | 401 |
| `https://projeto-pizzaria-backend-xi.vercel.app/api/v1/cardapio` | 200, JSON, `no-store`, 85 produtos / 4 categorias não vazias |

Não foi consultada tabela diretamente, coletado hash de senha ou exportado pedido de cliente. A categoria vazia não aparece na API, embora a inicialização anterior tenha cinco categorias. As consultas de catálogo demonstram integração publicada Flask/Neon no caminho de leitura; não medem disponibilidade contínua ou desempenho.

## Navegador real publicado

Chrome headless instalado no Windows, perfil temporário vazio, controle via protocolo local do navegador. Interceptação configurada para permitir somente GET/HEAD/OPTIONS; requisições de escrita seriam abortadas. Nenhuma tentativa de escrita remota ocorreu. O site publicado foi usado; não se trata de mock ou protótipo.

| Verificação | Resultado |
|---|---|
| Cardápio renderiza produtos após leitura da API | Passou |
| Produto abre modal com segundo sabor e borda | Passou |
| Adicionar uma pizza à sacola e navegar preserva o item no armazenamento local do perfil temporário | Passou |
| Visitante em `/funcionario` é redirecionado para `/login` | Passou |
| Tela móvel 390 × 844 sem overflow horizontal | Passou |

Capturas inspecionadas visualmente, sem dados pessoais: [cardápio desktop](imagens/cardapio-desktop.png), [modal](imagens/produto-modal.png), [sacola](imagens/carrinho.png), [login](imagens/login.png), [cadastro](imagens/cadastro.png), [cardápio móvel](imagens/cardapio-mobile.png). Desktop: 1440 × 1000. A sacola não foi confirmada nem enviada; o perfil do navegador era exclusivo do teste. Capturas autenticadas e homologação do fluxo de escrita em produção não foram realizadas.

## Evidências anteriores informadas pelo usuário — não repetidas

- Neon: 12 tabelas da aplicação + histórico, sete SQL registrados, cinco categorias, 85 produtos, cinco status; bootstrap administrativo e login real aprovados.
- Upstash: dez tentativas sintéticas permitidas, 11ª bloqueada, 898 segundos restantes, sem erro. Não é um novo teste HTTP de Retry-After nesta bateria.
- Blob: upload de PNG, GET 200, MIME correto, bytes íntegros; exclusão posterior exclusivamente autorizada confirmada pelo usuário com HTTP 404. Não existe arquivo sintético pendente a excluir nesta tarefa.

Esses resultados são declarações anteriores da sessão, sem inventar datas de execução ou repetir operações. Não são comprovantes de aceite do cliente.

## Arquivos locais desta finalizacao

Lista inclui novos documentos e capturas; nenhum arquivo funcional ou SQL foi alterado.

```text
README.md
backend/DOCS_API.md
docs/BackLog.md
docs/Roteiro do Protótipo Navegável — Pizzaria do Barriga.md
docs/Roteiro do Protótipo Navegável — Pizzaria do Barriga.md
docs/Sprints/relatorio-individual-sprint-3-4-Christian.md
docs/Sprints/sprint-4-evidencias-teste.md
docs/Sprints/sprint-4-relatorio.md
docs/Sprints/sprint-4-retrospectiva.md
docs/deploy-academico-vercel.md
docs/documentacao-final.md
docs/evidencias/e9-e10/imagens/cadastro.png
docs/evidencias/e9-e10/imagens/cardapio-desktop.png
docs/evidencias/e9-e10/imagens/cardapio-mobile.png
docs/evidencias/e9-e10/imagens/carrinho.png
docs/evidencias/e9-e10/checklist-entrega.md
docs/evidencias/e9-e10/imagens/login.png
docs/evidencias/e9-e10/imagens/produto-modal.png
docs/evidencias/e9-e10/validacao-2026-11-13.md
docs/manual-do-usuario.md
docs/plano_de_teste.md
docs/relatorio-final.md
docs/relatorio-testes-final.md
docs/termo-aceite-cliente.md
```
