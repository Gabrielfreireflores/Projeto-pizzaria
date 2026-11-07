# Relatório Individual de Contribuição — Sprint 4
## Identificação do integrante
- **Nome:** Gabriel Freire Flôres
- **RA:** 2840482423010
- **Papel na Sprint 4:** Product Owner


## Atividades realizadas
Integrei o cardápio e o envio de pedidos do frontend aos endpoints e à persistência do backend. Adaptei o contrato do pedido para contato simplificado e retirada sem endereço. Reconciliei a integração da interface interna com a versão do cliente, preservando a autoria dos colegas. Evoluí a seleção das pizzas com modal, segundo sabor, observação e borda vinculada ao item. Implementei ajustes de cadastro, autenticação e consulta dos pedidos da própria conta. Corrigi dados legados, o aceite de pedidos e o carregamento local do cardápio e do perfil. Consolidei as entregas incorporadas à `main`, os resultados de testes atuais e as pendências de aceite.
## Histórias e tarefas sob minha responsabilidade
Relaciono minha atuação ao [Backlog Priorizado](../BackLog.md), sem alterar a sprint alvo original das histórias. Os estados abaixo consideram os critérios de aceite completos, e não apenas a existência de uma tela.

|História ou tarefa|Status real|Minha contribuição e limite|Evidência|
| :-: | :-: | :-: | :-: |
|#4 — Visualizar o cardápio, Must, sprint alvo 2|Parcial|Integrei leitura da API, categorias, preços, descrições e imagens. A consulta filtra `disponivel`, mas não calcula estoque suficiente dos ingredientes, exigido no backlog.|PRs #28, #31 e #32; `frontend/src/services/menu.ts`; `backend/app/repositories/cardapio_repository.py`; E1 e E2|
|#5 — Montar o pedido no carrinho, Must, sprint alvo 2|Concluída nos critérios de quantidade, remoção e total|Evoluí o carrinho anterior, mantendo persistência local, observações, dois sabores e o adicional da borda. A interface calcula o resumo; o backend confirma os preços do banco.|PRs #28 e #31; `frontend/src/hooks/use-cart.tsx`; `frontend/src/services/orders.ts`; E3|
|#6 — Finalizar pedido, Must, sprint alvo 2|Concluída nos critérios documentados|Integrei contato, entrega/retirada, gravação com status inicial Recebido e confirmação. A regra atual exige sessão de cliente antes de confirmar. Retirada dispensa endereço.|PRs #28, #31 e #32; `frontend/src/app/(publico)/checkout/page.tsx`; `backend/app/controllers/pedido_controller.py`; E4, E5 e E6|
|#9 — Acompanhar o pedido, Should, sprint alvo 3|Parcial|Entreguei consulta dos pedidos da própria conta, seus itens e status. A versão atual depende do botão Atualizar e não exibe estimativa de entrega; portanto, não atende integralmente à atualização automática e à previsão previstas no backlog.|PRs #31 e #32; `frontend/src/app/(publico)/meus-pedidos/page.tsx`; E8|
|Integração com #7 e #8 — lista e aceite internos|Concluída no escopo da correção de integração|Corrigi o status corrompido que impedia o aceite e acrescentei regressões. Não atribuo a mim a implementação original da área interna nem do aceite.|PR #32; `2332025`; `backend/tests/test_status_pedidos.py`; E7|
|#1 — Login por perfil, Must, sprint alvo 1|Parcial no conjunto do backlog|Integrei redirecionamento, proteção do checkout e menu da conta. O bloqueio após múltiplas tentativas inválidas não está implementado em `backend/app/services/auth_services.py`.|PRs #29, #31 e #32; `frontend/src/hooks/use-auth.tsx`; `frontend/src/components/shared/requer-funcionario.tsx`|
## Entregas técnicas

|Entrega|O que foi feito|PR/branch/commit|Arquivos principais|Evidência|
| :-: | :-: | :-: | :-: | :-: |
|Integração de cardápio e pedido|Troquei os dados locais por GET do cardápio e POST de pedido; configurei proxy `/api` e o mapeamento de tamanhos/IDs.|PR #28; `feature/integracao-cliente-backend`; `ea328f1`|`frontend/next.config.mjs`; `frontend/src/lib/api.ts`; `frontend/src/services/menu.ts`; `frontend/src/services/orders.ts`|E1, E5 e E6; diff do commit|
|Retirada e contato simplificado|Adaptei validação e persistência para retirada com endereço nulo e contato no pedido; inicialmente incluí o cliente técnico Convidado.|PR #28; `5520321`|`db/migrations/003_checkout_convidado_retirada.sql`; `backend/app/schemas/pedido_schema.py`; `backend/app/repositories/pedido_repository.py`|E4 e E6; testes de retirada|
|Seed do cardápio v2|Versionei 85 produtos por tamanho, correspondentes a 31 sabores salgados, 5 doces, 4 bordas e 5 bebidas; incluí UTF-8 nas migrations 003 e 004.|PR #28; `ea328f1` e `5520321`|`db/migrations/004_seed_cardapio_v2.sql`; `db/migrations/003_checkout_convidado_retirada.sql`|E12; conferência do SQL e da contagem local|
|Reconciliação com a área interna|Resolvi os conflitos e as duplicações da integração, mantendo os contratos do cardápio e do produto da main.|PR #29; `integracao/login-frontend`; `b148d29`|`frontend/src/services/menu.ts`; `frontend/src/types/product.ts`; `frontend/next.config.mjs`; `backend/app/repositories/pedido_repository.py`; `backend/tests/test_produtos.py`|E11; diff combinado do merge|
|Cards e personalização|Implementei cards expansíveis; evoluí a apresentação para modal responsivo, busca, mistura entre sabores doces/salgados e seleção de borda junto à pizza.|PR #30, `2caf6df`; PR #31, `567e663`|`frontend/src/components/shared/product-card.tsx`; `frontend/src/components/shared/menu-section.tsx`; `frontend/src/types/product.ts`|E2 e E3|
|Bordas persistidas|Acrescentei vínculo da borda ao item, validação de tamanho/disponibilidade e preço confirmado no banco.|PR #31; `fix/validacao-integracao-pedidos`; `567e663`|`db/migrations/005_bordas_por_item.sql`; `backend/app/services/pedido_services.py`; `backend/tests/test_cliente_bordas_integracao.py`|E6; testes de preço e vínculo|
|Cadastro e imagens do cardápio|Simplifiquei cadastro para nome, e-mail, celular e senha; tornei CPF de cliente opcional. Acrescentei 36 imagens locais dos sabores, com procedência registrada, e revisei quatro delas.|PR #31; `7541b92`, `30c148b`, `1875933` e `567e663`|`db/migrations/005_cliente_cpf_opcional.sql`; `frontend/src/app/(publico)/cadastro/page.tsx`; `frontend/public/produtos/CREDITOS.txt`|E2; testes de cadastro e arquivos versionados|
|Aceite e limpeza de exemplos|Reparei o nome do status sem mudar sua chave; removi os dois produtos legados e apenas as dependências previstas na migration.|PR #32; `2332025` e `0c83f32`|`db/migrations/007_corrigir_status_preparacao.sql`; `db/migrations/008_remover_produtos_legados.sql`; `db/schema.sql`|E7 e E12; regressão do fluxo de status|
|Sessão obrigatória e Meus pedidos|Desliguei o uso de Convidado no código, preservei sacola/formulário no retorno do login e limitei a consulta aos 50 pedidos mais recentes da conta.|PR #32; `7479e53`|`backend/app/controllers/pedido_controller.py`; `backend/app/services/pedido_services.py`; `frontend/src/app/(interno)/login/page.tsx`; `frontend/src/app/(publico)/meus-pedidos/page.tsx`|E4 e E8; testes de autorização e isolamento|
|Cabeçalho e menu da conta|Ampliei faixa/logo, alinhei offsets sticky, acrescentei dados permitidos ao `/me` e ações por perfil; visitantes têm Entrar/Cadastrar por mouse ou clique.|PR #32; `8a551a0`, `a7d5555` e `95047bf`|`frontend/src/components/shared/account-menu.tsx`; `frontend/src/components/shared/navbar.tsx`; `frontend/src/app/globals.css`; `backend/app/controllers/auth_controller.py`|E13; `backend/tests/test_menu_conta.py`|
|Inicialização em 127.0.0.1|Autorizei as origens locais de desenvolvimento no Next e acrescentei mensagem/limpeza para busca sem resultados.|PR #32; `95047bf`|`frontend/next.config.mjs`; `frontend/src/components/shared/menu-section.tsx`|E13; configuração versionada|

O relatório da Sprint 3 registra o PDF oficial como fonte do cardápio. Nesta revisão, conferi os dados versionados e a migration 004; não localizei PDF versionado e não afirmo ter reconferido o documento original. Os arquivos de imagem têm procedência em `CREDITOS.txt`; não os apresento como fotografias reais fornecidas pela pizzaria.
## Decisões de projeto e de negócio

|Decisão|Justificativa e limite verificável|
| :-: | :-: |
|Manter o meio a meio pelo maior preço|Preservei a regra já documentada na Sprint 3 e implementada por `precoMeioAMeio` em `frontend/src/lib/data/products.ts`, que usa o maior preço das metades. O valor cobrado corresponde ao produto da metade mais cara.|
|Permitir combinação doce/salgada|A versão atual permite ambos os tipos no segundo sabor, em `product-card.tsx`. Não atribuo motivo comercial adicional sem registro.|
|Relacionar borda à pizza|O vínculo em `item_pedido_borda` permite guardar quantidade e preço da borda separadamente do preço da pizza; a validação exige o mesmo tamanho.|
|Mudar de Convidado para login obrigatório|No PR #28, o pedido sem sessão usava a conta técnica. No PR #32, passei a exigir login para associar o pedido ao cliente autenticado e permitir consulta isolada por conta. A migration 003 e seu registro técnico foram preservados. Não registro essa opção antiga como regra vigente.|
|Manter a sacola local e o pedido no servidor|A chave `pizzaria-barriga:cart:v2` preserva a montagem no navegador. A confirmação é enviada à API, que calcula preços e grava o pedido; não confundo persistência da sacola com persistência do pedido.|
|Oferecer entrega local ou retirada|O relatório da Sprint 3 registra entrega somente em Jardinópolis; o schema usa essa cidade como padrão e dispensa endereço na retirada. A API ainda aceita cidade informada no payload: não afirmo que exista bloqueio geográfico completo.|
|Registrar pagamento sem cobrar online|O checkout informa dinheiro, Pix ou cartão como preferência. A própria interface declara que não há cobrança online.|
|Encerrar o uso de exemplos legados|A migration 006 primeiro desativou Refrigerante; a 008 passou a remover esse exemplo e a Pizza de Muçarela Grande, seus itens e somente pedidos afetados que ficarem vazios. Não é exclusão geral do histórico.|
## Integração com o trabalho dos colegas
Reconheço a autoria de Marcelo no backend de consulta/criação de pedidos (`96d1490`) e no cardápio por categoria (`d686b22`, PR #19). Minha contribuição foi adaptar contratos e ligar o fluxo do cliente a essa base; não reivindico a criação original desses endpoints.

Reconheço a implementação da área interna, autenticação e gestão trazida por Christian em `c63b253`. A `main` contém esse commit por meio da integração posterior; o histórico de merges identifica a PR #29 para a branch `integracao/login-frontend`. Também reconheço o trabalho de Guilherme na listagem e no aceite originais (`8fbcab0`).

No merge `b148d29`, o Git registra conflitos em `frontend/src/services/menu.ts` e `frontend/src/types/product.ts`. Comparei as versões do merge com `9560bc4`: elas são iguais às da main daquele momento. O diff combinado comprova a retirada de um `rewrites` duplicado em `next.config.mjs`, a remoção do bloco de transição indevidamente duplicado no repository e o ajuste dos testes para ingredientes opcionais. Minha atuação nesse ponto foi de reconciliação, sem substituir a autoria das funcionalidades internas.

Os documentos de grupo da Sprint 3 são registros parciais anteriores, com situação consultada em 09/10/2026. Quando indicam integração pendente, descrevem aquele estágio. Registro aqui as incorporações posteriores, preservando os textos de grupo e sem declarar retroativamente que as funcionalidades já estavam integradas naquela data.
## Qualidade e testes
Executei as verificações abaixo em **03/11/2026**. Estes são resultados atuais sobre a base `48b39e7`, não uma reprodução dos números históricos das capturas de outubro.

|Verificação executada|Resultado real|Alcance e limite|
| :-: | :-: | :-: |
|`cd backend` e `.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider`|**145 passed, 43 skipped**, sem falhas, em 2,65 s|A suíte inclui os testes de status. Sem `TEST_DATABASE_URL`, os testes que exigem PostgreSQL são ignorados; não trato os 43 como aprovados.|
|PostgreSQL adicional: `pytest` restrito a `tests/test_cliente_bordas_integracao.py` e `tests/test_integracao_auth_pedidos.py`, com `TEST_DATABASE_URL` derivada do ambiente sem exibir credenciais|**21 passed**, sem falhas, em 10,12 s|Schemas exclusivos dentro de transação, desfeitos por rollback. Validei SQL, migrations, sessão, cadastro, bordas e isolamento. Esses 21 estavam ignorados na execução anterior; restam 22 testes antigos de banco não executados.|
|`cd frontend` e `node_modules/.bin/tsc.cmd --noEmit --incremental false`|Código de saída **0**, sem diagnósticos|Verificação de tipos; não equivale a build, teste de navegador ou medição de performance.|
|Consulta somente de leitura ao PostgreSQL local: `SELECT count(*) FROM produto`|**85 produtos**|Confirma o banco de desenvolvimento consultado nesta data, não outros ambientes. Não reapliquei migrations nesse banco durante esta documentação.|
|Conferência de Git e autoria|Commits citados resolvidos por `git cat-file`; incorporação conferida por `git merge-base --is-ancestor`; PRs identificadas nas mensagens de merge|A checagem não comprova homologação do cliente nem período oficial da sprint.|

Não executei build, testes manuais no navegador ou análise de desempenho nesta revisão documental. Não somei execuções repetidas da mesma suíte. O total distinto aprovado nas duas execuções de backend foi **166**, com os **22 testes antigos de banco** ainda não executados. A disponibilidade do banco foi confirmada pela execução isolada e pela consulta de leitura, não presumida a partir do `.env`.


## Dificuldades e como foram superadas
- **Integração de versões distintas:** resolvi os conflitos explícitos do merge `b148d29` e preservei os contratos do cliente presentes na main.
- **Acentuação e dados antigos:** as migrations 003/004 declaram `SET client_encoding = 'UTF8'`; a 007 trata especificamente o status com UTF-8 interpretado como Latin-1. As capturas antigas mostram corrupção, mas o Git não registra o comando original de importação: não afirmo como comprovada a causa operacional exata dessa carga.
- **Hash inválido em conta de exemplo:** acrescentei tratamento de `ValueError`/`TypeError` em `backend/app/services/auth_services.py` no PR #31, retornando erro de credenciais em vez de expor o formato interno. Não documento senha, hash nem ajuste de credencial local.
- **Carregamento e perfil sem interação em 127.0.0.1:** o commit `95047bf` inclui `allowedDevOrigins` para os hosts locais. O resultado visual final deve ser acompanhado da evidência E13; não uso a captura antiga de carregamento como prova da correção.
- **Mudanças de regra durante a integração:** distingui o checkout como convidado do login obrigatório posterior e mantive testes de autorização compatíveis com a regra atual.


## Evidências das atividades
Reservo `img/sprint-4/` como pasta relativa a este documento. O modelo das Sprints 1/2 utiliza imagens hospedadas externamente; adoto aqui a pasta local solicitada, com `.gitkeep`, sem copiar ou gerar imagens. Os links abaixo são nomes sugeridos para as capturas que o autor ainda deve inserir. Capturas de erro ou de versões antigas podem servir de contexto, mas não substituem demonstrações do estado corrigido. Não incluo capturas com credenciais de ambiente.

<img width="692" height="537" alt="Captura de tela 2026-10-25 135604" src="https://github.com/user-attachments/assets/8c6ef877-c615-4b1a-a01d-35261b3c64e9" />
<img width="686" height="522" alt="Captura de tela 2026-10-25 140307" src="https://github.com/user-attachments/assets/04815bd3-abb6-4142-aad8-49a854ff292c" />
<img width="715" height="523" alt="Captura de tela 2026-10-25 140327" src="https://github.com/user-attachments/assets/47c3eba9-7b54-44f1-a4f6-4f351fdfb763" />
<img width="1505" height="526" alt="Captura de tela 2026-10-25 142518" src="https://github.com/user-attachments/assets/87a59f54-0d67-4050-be7f-6bb3904146f3" />
<img width="677" height="151" alt="Captura de tela 2026-10-25 143724" src="https://github.com/user-attachments/assets/0256e02a-22de-4879-90e8-b96521ae7944" />
<img width="1572" height="841" alt="image" src="https://github.com/user-attachments/assets/d487e7d6-c4d5-4c98-8177-697f7d2bd0a9" />
<img width="761" height="252" alt="image" src="https://github.com/user-attachments/assets/205d3c02-59a4-4ea4-a75c-0b07e0d9d38d" />
<img width="1143" height="757" alt="image" src="https://github.com/user-attachments/assets/517e7237-d36d-4513-8570-9f7bd5f9607b" />
<img width="775" height="392" alt="image" src="https://github.com/user-attachments/assets/383aa78a-3ca3-4667-8d42-164a98a39d17" />
<img width="1770" height="845" alt="image" src="https://github.com/user-attachments/assets/d5c9209d-d395-47b1-a1f7-e015b3d9d893" />
<img width="1912" height="870" alt="image" src="https://github.com/user-attachments/assets/80cb8a5e-6d65-41c4-8afd-bb8576cf3aaf" />
<img width="7" height="2" alt="image" src="https://github.com/user-attachments/assets/7cfce286-1d21-4b1c-be49-657679888718" />



## Uso de ferramentas de apoio
Uso de inteligência artificial para a geração de código, acelerando o processo de desenvolvimento.
