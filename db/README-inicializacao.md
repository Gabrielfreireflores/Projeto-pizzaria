# Inicialização controlada — Neon Free (Etapa 3.1)

Procedimento preparado localmente. **Nenhum banco foi inicializado nesta etapa.**
Destina-se à demonstração acadêmica, sem pedidos reais, serviços pagos ou cartão.

## Antes de qualquer acesso

1. Autorizar separadamente o acesso ao projeto correto; conferir Free, cotas,
   espaço e recursos gratuitos de recuperação no painel. `--confirm-free-plan`
   é uma declaração manual: PostgreSQL não informa o plano de cobrança.
2. Confirmar host **direto** do projeto, banco `neondb` e schema `public` vazio.
   Não usar a URL pooled para manutenção; ela permanece apropriada ao Flask.
3. Configurar `DATABASE_URL` somente no ambiente seguro do processo administrativo,
   com TLS (`sslmode=require&channel_binding=require` no Neon). Nunca passar a URL
   ou senha como argumento de linha de comando, registrar no Git ou exibir no chat.
   Nenhum arquivo `.env` real é alterado pelo comando.
4. Usar Python/dependências já previstos em `backend/requirements.txt`. Não há
   ferramenta adicional, criação automática de conta ou execução no startup Flask.
5. Garantir backup/dump verificável fora do provedor antes de operar sobre dados
   existentes. Este instalador **não adota** banco existente sem histórico.

## Manifesto e controles

`db/migrations/manifest.json` fixa nomes completos, ordem e SHA-256 de:

1. `db/schema.sql`
2. `db/migrations/001_pedido_contato.sql`
3. `db/migrations/002_produto_cardapio.sql`
4. `db/migrations/003_checkout_convidado_retirada.sql`
5. `db/migrations/004_seed_cardapio_v2.sql`
6. `db/migrations/005_bordas_por_item.sql`
7. `db/migrations/005_cliente_cpf_opcional.sql`

006 e 007 não são necessárias ao seed novo correto. **008 é preservada, mas
excluída do instalador**; não existe opção para executar arquivos arbitrários.
Qualquer manutenção destrutiva dependerá de revisão e autorização próprias.

Checksum: SHA-256 do texto UTF-8 com CRLF normalizado para LF, incluindo comentários
e a quebra final. Troca de checkout Windows/Linux não altera o digest. Não atualizar
o manifesto para esconder divergências de arquivos já aplicados.

O executor valida os wrappers auditados e retira BEGIN/COMMIT apenas da cópia em
memória. Executa tudo numa **única transação**, incluindo o histórico em
`public._pizzaria_migrations` (nome completo, SHA-256, posição e `applied_at` com fuso).
Qualquer erro interrompe a sequência e reverte a instalação inteira. O arquivo
schema mantém seu próprio BEGIN/COMMIT para uso fora desse executor; se houver
execução manual excepcional, exigir parada no primeiro erro, como ON_ERROR_STOP
no psql, e controle transacional equivalente. Não combinar executores.

Instalação integral já registrada e verificada é ignorada, sem reaplicar seed.
Histórico parcial, desconhecido, modificado ou com estrutura ausente é recusado:
não há retomada/adaptação automática. Lock administrativo impede concorrência;
esperas por locks têm limite de 5 s e cada comando tem timeout de 60 s.

## Comandos futuros — não executados nesta etapa

Em `backend/`, usando o ambiente virtual. Substituir `HOST_DIRETO` pelo host público
exato do projeto, sem protocolo, credenciais ou `-pooler`:

```powershell
.\.venv\Scripts\python.exe db_admin.py plan
.\.venv\Scripts\python.exe db_admin.py check --host HOST_DIRETO --database neondb --connect --confirm-free-plan
.\.venv\Scripts\python.exe db_admin.py apply --host HOST_DIRETO --database neondb --execute --confirm-free-plan
.\.venv\Scripts\python.exe db_admin.py bootstrap --host HOST_DIRETO --database neondb --execute --confirm-free-plan
```

Somente `plan` é offline. `check` abre futuramente uma transação somente leitura:
confere host/banco/schema, PostgreSQL 15+, TLS, permissões, objetos e histórico.
`apply` e `bootstrap` exigem também a frase exata mostrada no terminal **antes de
conectar**. O destino é verificado novamente antes das escritas.

Bootstrap solicita os dados e senha com confirmação oculta; recusa terminal sem
entrada segura, e-mail duplicado (sem distinguir caixa) e CPF duplicado (sem
pontuação). Reutiliza validação da equipe e hash Werkzeug, criando usuário e
funcionário na mesma transação. Só permite o primeiro funcionário ativo com hash
compatível, depois do manifesto completo. Não corrige/sobrescreve os exemplos
inválidos do seed nem abre rota HTTP. Novos funcionários posteriores usam a equipe.
Uma falha pode consumir número de sequência, mas não deve deixar conta parcial;
não tentar corrigir lacunas de IDs com reset de sequências.

## Validação e interrupção

Antes de liberar a demonstração: conferir 12 tabelas de negócio, 85 produtos,
5 categorias, 5 status e ausência de pedidos iniciais; após bootstrap, validar
login e fluxos em homologação autorizada. `check` não substitui esse teste funcional.

Interromper diante de checksum divergente, destino/objetos inesperados, histórico
parcial, falta de permissão/TLS/cota, erro SQL ou falha na verificação final.
Rollback desfaz a transação atual; comandos apply e bootstrap são transações
separadas. Não reaplicar arquivos ou limpar objetos às cegas. Uma restauração,
exclusão ou nova tentativa sobre estado desconhecido exige nova autorização.
