## 🔐 Autenticação/Usuário - Cliente / Funcionário

## Atualização: cliente, acompanhamento e bordas

Aplicar as migrations 001–006 em ordem após `db/schema.sql`, sempre em UTF-8.
A migration 005 cria `item_pedido_borda`, relacionando a borda ao item de pizza,
sem remover produtos ou alterar itens de pedidos antigos. A 006 desativa somente
o produto cujo nome é exatamente `Refrigerante` (ignorando caixa e espaços externos).
O produto e suas referências no histórico permanecem no banco.

### Cadastro e consulta do cliente

`POST /api/v1/clientes` recebe `nome` (nome e sobrenome, até 120 caracteres),
`email` (formato válido, até 160 caracteres, trim e minúsculas), `telefone`
(celular obrigatório, de 10 a 15 dígitos; aceita `+ ( ) . -` e espaços, até 20
caracteres no total) e `senha` (texto não vazio, mantendo a regra existente).
São exatamente quatro campos no formulário; não há confirmação de senha ou endereço.
O campo `cpf`, se enviado, é ignorado. Novos clientes são gravados com CPF NULL;
CPFs existentes e sua restrição de unicidade são preservados. Aplicar também
`db/migrations/005_cliente_cpf_opcional.sql` antes de cadastrar clientes.
O CPF do funcionário e o cliente técnico Convidado não são alterados.
E-mail duplicado retorna 400 com `{"erro": "Usuário já cadastrado com este e-mail."}`.
Falhas internas retornam 503 sem expor SQL. A senha continua armazenada com hash.
Após criar a conta, o formulário faz `POST /api/v1/login` e abre `/meus-pedidos`,
mantendo o comportamento anterior. A resposta 201 mantém `cliente.cpf: null`
por compatibilidade com o formato existente.

`GET /api/v1/meus-pedidos` exige sessão de cliente ativo. Retorna uma lista no
formato da listagem de pedidos, filtrada no SQL pelo cliente associado à sessão.
Não aceita um identificador de cliente enviado pelo navegador como autorização.
Sem sessão retorna 401; funcionário ou cliente inativo recebe 403. A tela consulta
a cada 15 segundos enquanto visível e permite filtrar pelo número do pedido.

Pedidos continuam disponíveis sem login. O contato exige nome e sobrenome e
telefone. Endereço é obrigatório para entrega; retirada dispensa endereço e taxa.
Pedidos de convidado permanecem no cliente técnico e não são transferidos
automaticamente para contas criadas depois.

### Pizza com borda

Cada item de `POST /api/v1/pedidos` pode incluir:

```json
{
  "id_produto": 10,
  "quantidade": 2,
  "observacao": "Borda: Catupiry",
  "bordas": [{"id_produto": 70, "quantidade": 2}]
}
```

Os IDs são ilustrativos. O produto principal deve ser de `Pizzas Salgadas` ou
`Pizzas Doces`; a borda deve estar disponível, pertencer a `Bordas` e ter o mesmo
tamanho. A soma das quantidades das bordas não pode exceder a quantidade de pizzas.
Não se repete o mesmo produto de borda dentro de um item. Linhas de carrinho que
cobram o mesmo produto principal continuam agrupadas, com quantidades e observações
das escolhas preservadas.

Preços de pizza e borda vêm do banco e são gravados como retrato no pedido.
O total inclui pizza, bordas e taxa de entrega. `item_pedido` mantém o subtotal
da pizza; `item_pedido_borda` mantém preço, quantidade e subtotal de cada borda,
com chaves estrangeiras para o item principal e o produto. A listagem devolve
`bordas` dentro de cada item. Itens, bordas, endereço e pedido usam a mesma transação.

---

### 1. Auto-cadastro de Cliente
Cria um novo usuário com o perfil padrão de cliente.

* **URL:** `/auth/api/cadastro/cliente`
* **Método:** `POST`
* **Autenticação:** Nenhuma (Rota pública)

#### Corpo da Requisição (Request Body)
```json
{
  "email": "cliente@email.com",
  "senha": "senhaSegura123"
}

201 CREATED
{
  "mensagem": "Usuário do perfil 'perfil_padrao' cadastrado com sucesso.",
  "usuario": {
    "id": 12,
    "email": "cliente@email.com"
  }
}
400 BAD REQUEST
{
  "erro": "Usuário já cadastrado com este e-mail."
}

----------------------------------------------------------------------------------

### 2. Cadastro de Funcionário
Cria um novo usuário com o perfil padrão de funcionário.

* **URL:** `/auth/api/cadastro/funcionario`
* **Método:** `POST`
* **Autenticação:** ADICIONAR AUTENTICACAO - ROTA NAO DEVE SER PUBLICA

#### Corpo da Requisição (Request Body)
```json
{
  "email": "cliente@email.com",
  "senha": "senhaSegura123"
}

201 CREATED
{
  "mensagem": "Usuário do perfil 'perfil_padrao' cadastrado com sucesso.",
  "usuario": {
    "id": 12,
    "email": "cliente@email.com"
  }
}


## 🔐 Categoria
### 1. Criação de categoria
Cria uma nova categoria.

* **URL:** `api/categorias`
* **Método:** `POST`
* **Autenticação:** ADICIONAR AUTENTICACAO - ROTA NAO DEVE SER PUBLICA

#### Corpo da Requisição (Request Body)
```json
{
  "nome": "pizzas"
}

201 CREATED
{
  "mensagem": "Categoria '{nome}' criada com sucesso.",
  "categoria": {
    "id_categoria": 12,
    "nome": "pizzas"
  }
}

----------------------------------------------------------------------------------

### 2. Listar as categorias
Listagem de categoria.

* **URL:** `api/categorias`
* **Método:** `GET`
* **Autenticação:** ADICIONAR AUTENTICACAO - ROTA NAO DEVE SER PUBLICA

200 OK
{
    "categorias": [
        [
            1,
            "pizza"
        ],

        [  
            2,
            "bebidas"
        ]
    ]
}

# Preparação de deploy — Etapa 1

- Entrada serverless: `backend/main.py` exporta `app`; local: `python run.py`.
- Instalar `requirements.txt` (Python 3.13). Pillow valida conteúdo, formato,
  tamanho (5 MB), dimensões e arquivos truncados antes de gravar a imagem.
- Escritas (`POST`, `PUT`, `PATCH`, `DELETE`) exigem `X-CSRF-Protection: 1`.
  Os dois clientes HTTP do Next enviam o cabeçalho. Formulários externos são
  rejeitados; CORS permanece fechado. Clientes de API também devem enviá-lo.
- `POST /api/categorias` exige funcionário ativo. O cadastro legado em
  `/auth/api/cadastro/funcionario` está bloqueado; usar `/api/v1/funcionarios`
  com sessão de funcionário ativo para o cadastro legítimo da equipe.
- `APP_ENV=production` ou `VERCEL=1` exige `SECRET_KEY` estável com pelo menos
  32 caracteres e variedade de caracteres. Gerar uma única vez com
  `python -c "import secrets; print(secrets.token_urlsafe(32))"` e guardar no
  ambiente do backend, nunca no Git ou no frontend.
- `APP_ORIGINS`: origens exatas do frontend, separadas por vírgula; HTTPS em
  produção. Cadastrar previews explicitamente, sem curingas.
- Cookies: HttpOnly, SameSite=Lax, Path=/, sem Domain; Secure em produção e
  HTTP permitido localmente. O navegador acessa apenas o domínio do Next por
  `/api`; o proxy encaminha cookies, métodos, cabeçalhos e Set-Cookie. Não
  chamar o domínio Flask diretamente no navegador nem habilitar CORS aberto.
- Frontend: configurar `BACKEND_URL` HTTPS antes do build na Vercel. Não usar
  prefixo `NEXT_PUBLIC_`. Banco: `DATABASE_URL` somente no backend, com TLS
  conforme o provedor; a Etapa 1 não executa migrations nem configura banco.
- `IMAGE_STORAGE=local` no desenvolvimento. Em produção, usar `disabled`
  enquanto o serviço persistente não estiver definido: operações sem nova
  foto continuam disponíveis; upload retorna erro genérico sem gravar disco.
  O contrato `save(content, extension) -> (url, key)` / `delete(key)` permite
  acrescentar Cloudinary ou Blob depois. Nenhuma imagem existente é migrada,
  substituída ou apagada por esta preparação; edição sem foto mantém a atual.
- Bloqueios externos: escolher serviço de imagens, credenciais, URLs HTTPS e
  PostgreSQL hospedado; validar tudo no ambiente de homologação. O adaptador
  externo e sua leitura de imagens ainda não estão implementados.
- Pendente antes de exposição pública: limitação distribuída de tentativas de
  login (plataforma ou armazenamento compartilhado). Um contador em memória
  não oferece proteção consistente em múltiplas funções serverless.
- Testes: `python -m pytest -q -p no:cacheprovider`; configuração Next:
  `node --test tests/deploy-config.test.mjs` em `frontend/`. O teste real do
  proxy é opt-in (`TEST_NEXT_PROXY=1`), requer build local e portas 5000/3107
  livres; usa serviços simulados sem banco e encerra os servidores ao terminar.

# Infraestrutura — Etapa 2 (08/11/2026)

**Escopo confirmado: demonstração acadêmica, sem operação comercial e sem pedidos
reais.** Esta seção atualiza as pendências registradas na Etapa 1. Não houve
provisionamento, deploy, conexão remota ou execução de SQL nesta preparação.

| Serviço | Limites gratuitos consultados | Decisão e proteção contra cobrança |
|---|---|---|
| [Vercel Hobby](https://vercel.com/docs/plans/hobby) | 4 CPU-h, 1 milhão de invocações, 100 GB de transferência/mês | Somente demonstração pessoal não comercial; ao atingir cotas, aceitar pausa. Não ativar Pro, trial, serviços pagos nem cadastrar cartão |
| [Neon Free](https://neon.com/pricing) | Sem prazo/cartão; 100 CU-h, 1 GB de PostgreSQL e 5 GB de transferência por projeto/mês | Selecionar Free; cotas pausam compute ou impedem crescimento, sem upgrade automático |
| [Vercel Blob Hobby](https://vercel.com/docs/vercel-blob/usage-and-pricing) | 1 GB, 10 GB de transferência, 10 mil operações simples e 2 mil avançadas/mês | Store público apenas para fotos do cardápio; cota excedida bloqueia acesso, sem cobrança adicional Hobby |
| [Upstash Redis Free](https://upstash.com/pricing/redis) | 250 MB, 500 mil comandos/mês, 10 GB de banda | Conta Free normal, sem cartão e sem Pay-as-you-go; não usar banco temporário não reivindicado de 3 dias. Cota/falha bloqueia login com 503 |

Os planos são gratuitos recorrentes dentro das cotas, não capacidade ilimitada
nem garantia de disponibilidade ou permanência contratual. Confirmar Free e
ausência de cartão/add-ons no painel antes de qualquer configuração futura.
Não contornar limites com múltiplas contas. Revisar consumo: a tela da cozinha
consulta a cada 15 s e pode manter o PostgreSQL ativo; não deixar aberta fora
das demonstrações. A adequação das cotas depende da carga real observada.

**Uso comercial:** Hobby não autoriza a operação da pizzaria, conforme as
[regras oficiais](https://vercel.com/docs/limits/fair-use-guidelines). Trocar
o escopo para pedidos reais exige nova decisão de hospedagem. Alternativas
avaliadas: [Netlify Free](https://www.netlify.com/blog/introducing-netlify-free-plan/)
aceita projetos comerciais, sem cartão e com pausa por cota (300 créditos/mês),
mas não substitui diretamente o Flask; [Render Free](https://render.com/docs/free)
tem suspensão após 15 minutos, recomenda não usar em produção e pode exigir
verificação de cartão. Não foi escolhido como garantia de infraestrutura R$ 0.
[Cloudinary Free](https://cloudinary.com/documentation/developer_onboarding_faq_free_plan)
é alternativa para fotos em produção, sem cartão, com 25 créditos mensais;
excesso pode suspender a conta. Não há adaptador Cloudinary nesta etapa.

**PostgreSQL:** `DATABASE_URL` pode ser direta ou pooled; preferir a URL pooled
Neon (`-pooler`) na aplicação e TLS `sslmode=require&channel_binding=require`.
Produção rejeita modos sem TLS; Neon exige channel binding por padrão. Para
validação de certificado, configurar `sslmode=verify-full` e confiança da CA
adequada ao runtime. `DB_CONNECT_TIMEOUT` (1–30 s; padrão 10) prevalece sobre
a URL. Não há pool persistente nem conexão na importação; transações e fechamento
dos repositórios são preservados. Prepared statements automáticos desativados
para compatibilidade com transaction pooling. Usar URL direta na manutenção.

**Fotos:** `IMAGE_STORAGE=local` mantém desenvolvimento independente; `blob`
usa o [SDK Python oficial](https://vercel.com/docs/vercel-blob/python-sdk-reference),
API síncrona, timeout 10 s e credenciais explícitas `BLOB_READ_WRITE_TOKEN` e
`BLOB_STORE_ID` somente no backend. Token/store ausentes falham sem escrita local.
UUID, `allow_overwrite=False`, Pillow e namespace `pizzaria/produtos/` preservados.
No frontend, configurar apenas `NEXT_PUBLIC_BLOB_HOST`, o host público exato do
store (sem token), antes do build. Imagens anteriores continuam disponíveis.
Exclusão de compensação atua somente na nova imagem cujo cadastro falhou; falha
do provedor não apaga registros. Timeout/erro de compensação pode deixar objeto
órfão para revisão futura. Não enviar dados privados ao store público.
A Vercel limita payloads de funções a [4,5 MB](https://vercel.com/docs/functions/limitations):
o limite local de imagem de 5 MB foi preservado; usar fotos menores na demo.

**Login:** `LOGIN_RATE_LIMITER=disabled` somente local; `upstash` utiliza
`UPSTASH_REDIS_REST_URL` e `UPSTASH_REDIS_REST_TOKEN`. Produção não permite bypass:
ausência, erro ou cota do serviço retorna 503 antes de verificar a senha.
`LOGIN_RATE_LIMIT=10`, `LOGIN_GLOBAL_LIMIT=100`, `LOGIN_WINDOW_SECONDS=900`:
contam todas as tentativas válidas de entrada, inclusive sucessos, em janela
com TTL. Um único EVAL valida e incrementa conta e limite global atomicamente.
Conta usa HMAC-SHA256, sem e-mail/IP/senha em texto nas chaves. Não confiar em
`X-Forwarded-For`: o limite global contém rotação de contas, mas pode bloquear
temporariamente outros usuários sob ataque. Excesso retorna 429 e Retry-After;
tentativas bloqueadas não prolongam a janela. Sem CAPTCHA/MFA ou contador local
como proteção de produção. Testes de concorrência usam fake, não Redis remoto.

**Configuração futura:** manter dois projetos com raízes `frontend` e `backend`,
`main.py`, HTTPS, proxy `/api`, CSRF e cookies existentes. Antes do build,
definir `BACKEND_URL`, host Blob e `APP_ORIGINS`; manter `SECRET_KEY` estável.
Usar subdomínios gratuitos dos provedores, sem compra de domínio ou add-ons.
Não compartilhar tokens/arquivos .env no Git ou chat.

**Migrations futuras:** usar banco vazio isolado e snapshot/backup; revisar
o [procedimento da Etapa 3.1](../db/README-inicializacao.md). O manifesto inicial
inclui `schema.sql`, 001, 002, 003, 004 e **ambos** 005. 006/007 são desnecessárias
ao banco novo e a 008 destrutiva está excluída. `backend/db_admin.py` registra
nome completo, SHA-256 e data numa transação única; recusa histórico divergente
e nunca executa automaticamente ao iniciar o Flask.

**Pendente:** configurar as contas Free e credenciais somente em etapa autorizada,
validar cotas/elegibilidade no painel e testar integração real em homologação.
A homologação não está pronta apenas por os testes com mocks passarem.

