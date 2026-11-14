# Preparação do deploy acadêmico — Etapa 7.1

> Atualização de 13/11/2026: frontend publicado em https://projeto-pizzaria-frontend-seven.vercel.app e backend em https://projeto-pizzaria-backend-xi.vercel.app. A leitura do cardápio direto e via proxy retornou HTTP 200, com 85 produtos; rotas protegidas recusaram visitante com 401. Este guia de preparação permanece como referência; não representa um novo deploy. [Registro E9](evidencias/e9-e10/validacao-2026-11-13.md).

Somente demonstração acadêmica, sem operação comercial. Usar Vercel Hobby,
Neon Free, Upstash Free e Blob Hobby, sem trial Pro, cartão ou upgrade pago.
Esta preparação não publica o projeto nem executa operações nos provedores.

## Estrutura

A publicação usa dois projetos Vercel a partir do mesmo repositório. Estrutura de referência para reprodução autorizada:

| Projeto | Root Directory | Configuração |
| --- | --- | --- |
| Backend | `backend` | Flask, Python 3.13 (`.python-version`), `requirements.txt`, entrada `main.py:app` |
| Frontend | `frontend` | Next.js, Node 22.x, instalar com `npm ci`, build `npm run build` |

Não configurar `python run.py` como Build Command. Não configurar comandos de
migration, seed, `db_admin.py apply` ou `bootstrap` em build, instalação ou startup.
A autodetecção do Flask reconhece `main.py`; não são necessários builders legados
nem rewrites adicionais para a função Flask. Não definir diretório de saída estático
no frontend: manter o padrão Next.js. Não enviar `.env`, `.venv` ou `node_modules`.

O Next encaminha `/api/:path*` ao backend via `BACKEND_URL` HTTPS. O navegador usa
sempre a origem do frontend; não habilitar CORS amplo nem chamar o backend diretamente.
O rewrite antigo `/static/uploads/produtos/:path*` permanece por compatibilidade,
mas arquivos locais não são armazenamento persistente na Vercel. Fotos novas usam Blob;
fotos estáticas em `frontend/public` permanecem disponíveis. Não migrar dados existentes.

## Variáveis de produção

Configurar privadamente no projeto correto, antes do respectivo build:

| Backend | Valor esperado |
| --- | --- |
| `APP_ENV` | `production` |
| `SECRET_KEY` | Aleatória, forte e estável entre instâncias; mínimo 32 caracteres |
| `APP_ORIGINS` | Origem HTTPS exata do frontend, sem caminho; previews só se autorizados explicitamente |
| `DATABASE_URL` | URL Neon pooled do banco inicializado, TLS `sslmode=require`, `channel_binding=require` |
| `DB_CONNECT_TIMEOUT` | `10` |
| `IMAGE_STORAGE` | `blob` |
| `BLOB_READ_WRITE_TOKEN` | Token secreto do store validado |
| `BLOB_STORE_ID` | Identificador real correspondente ao token, não o nome amigável do store |
| `LOGIN_RATE_LIMITER` | `upstash` |
| `UPSTASH_REDIS_REST_URL` | Endpoint HTTPS do Redis validado |
| `UPSTASH_REDIS_REST_TOKEN` | Token REST secreto |
| `LOGIN_RATE_LIMIT` | `10` |
| `LOGIN_GLOBAL_LIMIT` | `100` |
| `LOGIN_WINDOW_SECONDS` | `900` |

| Frontend | Valor esperado |
| --- | --- |
| `BACKEND_URL` | Origem HTTPS do projeto backend, sem caminho ou credenciais |
| `NEXT_PUBLIC_BLOB_HOST` | Host público exato do store: `<identificador>.public.blob.vercel-storage.com` |

`VERCEL=1` é fornecida pela plataforma. Não copiar variáveis `TEST_*` para produção.
Nunca colocar tokens, `SECRET_KEY` ou `DATABASE_URL` em variáveis `NEXT_PUBLIC_*`.
A conta Hobby deve ser a proprietária do store validado. Conferir limites e plano
gratuito nos painéis antes da publicação; consumo excedente pode interromper a demo.

## Segurança e armazenamento

Sessão assinada com cookie host-only, `Secure`, `HttpOnly`, `SameSite=Lax` e `Path=/`.
O proxy deve preservar `Set-Cookie`, cookies e `Origin`. Requisições de escrita usam
`X-CSRF-Protection: 1` e a allowlist `APP_ORIGINS`. Respostas de API usam `no-store`.
Não desabilitar CSRF, Redis ou cookies seguros para contornar configuração incorreta.

Imagens: máximo 3 MiB por arquivo, JPG/PNG/WebP validados pelo Pillow. Requisição
completa em produção: máximo 4 MiB (4.194.304 bytes), incluindo campos e multipart,
abaixo dos 4,5 MB da Vercel. O limite global continua 10 MiB no desenvolvimento.
O cadastro e a edição exibem o mesmo limite de arquivo. Campos excessivamente grandes
podem ser recusados pelo parser mesmo com imagem pequena. Falhas retornam erro e não
utilizam disco local como alternativa em produção. Upload exige funcionário ativo.

Limpeza automática de imagens antigas NÃO foi adicionada. Substituir foto ou excluir
produto pode deixar arquivos antigos no Blob. Não apagar apenas porque uma URL foi
substituída: ela pode estar compartilhada ou ainda referenciada. Uma implementação futura
precisa confirmar commit no PostgreSQL, ausência de referências e pertencimento ao store
e prefixo autorizados; falhas devem poder ser reconciliadas sem reverter dados já salvos.
Por enquanto, usar limpeza individual expressamente autorizada e monitorar a cota.

## Verificações antes e depois da publicação autorizada

1. Confirmar plano Hobby e uso acadêmico, variáveis e origens reais, cotas e ausência
   de comandos administrativos nos Build/Install Commands do painel.
2. Validar que Deployment Protection do backend permite chamadas do proxy Next.
   Não inserir segredo de bypass na URL nem desabilitar proteções sem avaliar o efeito.
3. Executar testes locais sem `TEST_DATABASE_URL`, `npm run lint` e `npm run build`.
   `httpx2` é dependência real do adaptador e deve ser preservado.
4. Somente após autorização, publicar backend e frontend com as raízes acima.
   Se o backend precisar da origem do frontend antes do primeiro build, reservar os nomes
   dos projetos e configurar suas origens estáveis antes da publicação.
5. Validar HTTPS, cardápio, login manual, cookie seguro, `/api/v1/me`, acesso de funcionário,
   bloqueio de origem não autorizada e logout. Não criar pedidos/produtos para esse teste.
   Um teste funcional que grave dados ou novos Blobs exige autorização específica.
6. Se houver falha, voltar ao deployment anterior. Rollback de aplicação não restaura
   dados ou objetos; não executar SQL, seed ou migrations para tentar corrigir um deploy.

Limitações da validação local: SDK e psycopg foram verificados no Windows/Python 3.13;
o ambiente Python Linux e suas versões exatas no painel não foram reinspecionados nesta revisão, embora o backend publicado tenha respondido corretamente às leituras.
O frontend foi compilado localmente com Node 20.19.4; a versão 22.x recomendada para
o painel ainda requer validação na plataforma. O lint usa as dependências já existentes,
sem atualização de versões nem instalação nesta etapa.

Neon, login real, Upstash e Blob foram validados nas etapas anteriores conforme resultados informados pelo usuário. O arquivo sintético Blob foi excluído e a ausência confirmada com HTTP 404. Nenhuma operação de escrita nos provedores foi repetida na bateria final. A troca/substituição de fotos ainda pode deixar objetos antigos; não executar limpeza ampla. Para estado atual da entrega e homologação pendente, consultar [documentação final](documentacao-final.md).

Referências oficiais consultadas:
- https://vercel.com/docs/frameworks/backend/flask
- https://vercel.com/docs/functions/limitations
- https://vercel.com/docs/plans/hobby
- https://vercel.com/docs/vercel-blob/usage-and-pricing
