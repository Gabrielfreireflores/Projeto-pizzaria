# Relatório Individual de Contribuição — Sprint 4

## Identificação do integrante

- **Nome:** Gabriel Freire Flôres.
- **RA:** 2840482423010.
- **Papel formal na Sprint 4:** [PREENCHER: papel na Sprint 4].
- **Atuação técnica documentada:** evolução do frontend do cliente, integração com backend e banco, correções e validação do fluxo de pedidos.
- **Trilha:** B — Cliente real nº 1: Pizzaria do Barriga, Jardinópolis-SP.
- **Equipe:** Marcelo Augusto Oliveira Jose, Christian de Lima e Guilherme Fabiano da Silva Gomes.
- **Período oficial:** [PREENCHER: início e término da Sprint 4].
- **Esforço individual:** [PREENCHER: horas dedicadas à Sprint 4].
- **Verificação deste documento:** 03/11/2026, sobre a `main` em `48b39e7`.

Organizo este registro como contribuição da **Sprint 4**, conforme a orientação do autor. O período oficial ainda precisa ser confirmado: as datas dos commits não substituem o calendário da disciplina. Uso como contexto as entregas de 04/10/2026 já relatadas na Sprint 3; não as apresento como novas implementações da Sprint 4. O recorte de evolução examinado contém commits de 25 a 29/10/2026. Não localizei documento de grupo da Sprint 4; preservei todos os documentos da Sprint 3.

## Resumo da contribuição

Integrei o cardápio e o envio de pedidos do frontend aos endpoints e à persistência do backend.
Adaptei o contrato do pedido para contato simplificado e retirada sem endereço.
Reconciliei a integração da interface interna com a versão do cliente, preservando a autoria dos colegas.
Evoluí a seleção das pizzas com modal, segundo sabor, observação e borda vinculada ao item.
Implementei ajustes de cadastro, autenticação e consulta dos pedidos da própria conta.
Corrigi dados legados, o aceite de pedidos e o carregamento local do cardápio e do perfil.
Consolidei as entregas incorporadas à `main`, os resultados de testes atuais e as pendências de aceite.

## Histórias e tarefas sob minha responsabilidade

Relaciono minha atuação ao [Backlog Priorizado](../BackLog.md), sem alterar a sprint alvo original das histórias. Os estados abaixo consideram os critérios de aceite completos, e não apenas a existência de uma tela.

| História ou tarefa | Status real | Minha contribuição e limite | Evidência |
|---|---|---|---|
| #4 — Visualizar o cardápio, Must, sprint alvo 2 | Parcial | Integrei leitura da API, categorias, preços, descrições e imagens. A consulta filtra `disponivel`, mas não calcula estoque suficiente dos ingredientes, exigido no backlog. | PRs #28, #31 e #32; `frontend/src/services/menu.ts`; `backend/app/repositories/cardapio_repository.py`; E1 e E2 |
| #5 — Montar o pedido no carrinho, Must, sprint alvo 2 | Concluída nos critérios de quantidade, remoção e total | Evoluí o carrinho anterior, mantendo persistência local, observações, dois sabores e o adicional da borda. A interface calcula o resumo; o backend confirma os preços do banco. | PRs #28 e #31; `frontend/src/hooks/use-cart.tsx`; `frontend/src/services/orders.ts`; E3 |
| #6 — Finalizar pedido, Must, sprint alvo 2 | Concluída nos critérios documentados | Integrei contato, entrega/retirada, gravação com status inicial Recebido e confirmação. A regra atual exige sessão de cliente antes de confirmar. Retirada dispensa endereço. | PRs #28, #31 e #32; `frontend/src/app/(publico)/checkout/page.tsx`; `backend/app/controllers/pedido_controller.py`; E4, E5 e E6 |
| #9 — Acompanhar o pedido, Should, sprint alvo 3 | Parcial | Entreguei consulta dos pedidos da própria conta, seus itens e status. A versão atual depende do botão Atualizar e não exibe estimativa de entrega; portanto, não atende integralmente à atualização automática e à previsão previstas no backlog. | PRs #31 e #32; `frontend/src/app/(publico)/meus-pedidos/page.tsx`; E8 |
| Integração com #7 e #8 — lista e aceite internos | Concluída no escopo da correção de integração | Corrigi o status corrompido que impedia o aceite e acrescentei regressões. Não atribuo a mim a implementação original da área interna nem do aceite. | PR #32; `2332025`; `backend/tests/test_status_pedidos.py`; E7 |
| #1 — Login por perfil, Must, sprint alvo 1 | Parcial no conjunto do backlog | Integrei redirecionamento, proteção do checkout e menu da conta. O bloqueio após múltiplas tentativas inválidas não está implementado em `backend/app/services/auth_services.py`. | PRs #29, #31 e #32; `frontend/src/hooks/use-auth.tsx`; `frontend/src/components/shared/requer-funcionario.tsx` |

## Entregas técnicas

| Entrega | O que foi feito | PR/branch/commit | Arquivos principais | Evidência |
|---|---|---|---|---|
| Integração de cardápio e pedido | Troquei os dados locais por GET do cardápio e POST de pedido; configurei proxy `/api` e o mapeamento de tamanhos/IDs. | PR #28; `feature/integracao-cliente-backend`; `ea328f1` | `frontend/next.config.mjs`; `frontend/src/lib/api.ts`; `frontend/src/services/menu.ts`; `frontend/src/services/orders.ts` | E1, E5 e E6; diff do commit |
| Retirada e contato simplificado | Adaptei validação e persistência para retirada com endereço nulo e contato no pedido; inicialmente incluí o cliente técnico Convidado. | PR #28; `5520321` | `db/migrations/003_checkout_convidado_retirada.sql`; `backend/app/schemas/pedido_schema.py`; `backend/app/repositories/pedido_repository.py` | E4 e E6; testes de retirada |
| Seed do cardápio v2 | Versionei 85 produtos por tamanho, correspondentes a 31 sabores salgados, 5 doces, 4 bordas e 5 bebidas; incluí UTF-8 nas migrations 003 e 004. | PR #28; `ea328f1` e `5520321` | `db/migrations/004_seed_cardapio_v2.sql`; `db/migrations/003_checkout_convidado_retirada.sql` | E12; conferência do SQL e da contagem local |
| Reconciliação com a área interna | Resolvi os conflitos e as duplicações da integração, mantendo os contratos do cardápio e do produto da main. | PR #29; `integracao/login-frontend`; `b148d29` | `frontend/src/services/menu.ts`; `frontend/src/types/product.ts`; `frontend/next.config.mjs`; `backend/app/repositories/pedido_repository.py`; `backend/tests/test_produtos.py` | E11; diff combinado do merge |
| Cards e personalização | Implementei cards expansíveis; evoluí a apresentação para modal responsivo, busca, mistura entre sabores doces/salgados e seleção de borda junto à pizza. | PR #30, `2caf6df`; PR #31, `567e663` | `frontend/src/components/shared/product-card.tsx`; `frontend/src/components/shared/menu-section.tsx`; `frontend/src/types/product.ts` | E2 e E3 |
| Bordas persistidas | Acrescentei vínculo da borda ao item, validação de tamanho/disponibilidade e preço confirmado no banco. | PR #31; `fix/validacao-integracao-pedidos`; `567e663` | `db/migrations/005_bordas_por_item.sql`; `backend/app/services/pedido_services.py`; `backend/tests/test_cliente_bordas_integracao.py` | E6; testes de preço e vínculo |
| Cadastro e imagens do cardápio | Simplifiquei cadastro para nome, e-mail, celular e senha; tornei CPF de cliente opcional. Acrescentei 36 imagens locais dos sabores, com procedência registrada, e revisei quatro delas. | PR #31; `7541b92`, `30c148b`, `1875933` e `567e663` | `db/migrations/005_cliente_cpf_opcional.sql`; `frontend/src/app/(publico)/cadastro/page.tsx`; `frontend/public/produtos/CREDITOS.txt` | E2; testes de cadastro e arquivos versionados |
| Aceite e limpeza de exemplos | Reparei o nome do status sem mudar sua chave; removi os dois produtos legados e apenas as dependências previstas na migration. | PR #32; `2332025` e `0c83f32` | `db/migrations/007_corrigir_status_preparacao.sql`; `db/migrations/008_remover_produtos_legados.sql`; `db/schema.sql` | E7 e E12; regressão do fluxo de status |
| Sessão obrigatória e Meus pedidos | Desliguei o uso de Convidado no código, preservei sacola/formulário no retorno do login e limitei a consulta aos 50 pedidos mais recentes da conta. | PR #32; `7479e53` | `backend/app/controllers/pedido_controller.py`; `backend/app/services/pedido_services.py`; `frontend/src/app/(interno)/login/page.tsx`; `frontend/src/app/(publico)/meus-pedidos/page.tsx` | E4 e E8; testes de autorização e isolamento |
| Cabeçalho e menu da conta | Ampliei faixa/logo, alinhei offsets sticky, acrescentei dados permitidos ao `/me` e ações por perfil; visitantes têm Entrar/Cadastrar por mouse ou clique. | PR #32; `8a551a0`, `a7d5555` e `95047bf` | `frontend/src/components/shared/account-menu.tsx`; `frontend/src/components/shared/navbar.tsx`; `frontend/src/app/globals.css`; `backend/app/controllers/auth_controller.py` | E13; `backend/tests/test_menu_conta.py` |
| Inicialização em 127.0.0.1 | Autorizei as origens locais de desenvolvimento no Next e acrescentei mensagem/limpeza para busca sem resultados. | PR #32; `95047bf` | `frontend/next.config.mjs`; `frontend/src/components/shared/menu-section.tsx` | E13; configuração versionada |

O relatório da Sprint 3 registra o PDF oficial como fonte do cardápio. Nesta revisão, conferi os dados versionados e a migration 004; não localizei PDF versionado e não afirmo ter reconferido o documento original. Os arquivos de imagem têm procedência em `CREDITOS.txt`; não os apresento como fotografias reais fornecidas pela pizzaria.

## Decisões de projeto e de negócio

| Decisão | Justificativa e limite verificável |
|---|---|
| Manter o meio a meio pelo maior preço | Preservei a regra já documentada na Sprint 3 e implementada por `precoMeioAMeio` em `frontend/src/lib/data/products.ts`, que usa o maior preço das metades. O valor cobrado corresponde ao produto da metade mais cara. |
| Permitir combinação doce/salgada | A versão atual permite ambos os tipos no segundo sabor, em `product-card.tsx`. Não atribuo motivo comercial adicional sem registro. |
| Relacionar borda à pizza | O vínculo em `item_pedido_borda` permite guardar quantidade e preço da borda separadamente do preço da pizza; a validação exige o mesmo tamanho. |
| Mudar de Convidado para login obrigatório | No PR #28, o pedido sem sessão usava a conta técnica. No PR #32, passei a exigir login para associar o pedido ao cliente autenticado e permitir consulta isolada por conta. A migration 003 e seu registro técnico foram preservados. Não registro essa opção antiga como regra vigente. |
| Manter a sacola local e o pedido no servidor | A chave `pizzaria-barriga:cart:v2` preserva a montagem no navegador. A confirmação é enviada à API, que calcula preços e grava o pedido; não confundo persistência da sacola com persistência do pedido. |
| Oferecer entrega local ou retirada | O relatório da Sprint 3 registra entrega somente em Jardinópolis; o schema usa essa cidade como padrão e dispensa endereço na retirada. A API ainda aceita cidade informada no payload: não afirmo que exista bloqueio geográfico completo. |
| Registrar pagamento sem cobrar online | O checkout informa dinheiro, Pix ou cartão como preferência. A própria interface declara que não há cobrança online. |
| Encerrar o uso de exemplos legados | A migration 006 primeiro desativou Refrigerante; a 008 passou a remover esse exemplo e a Pizza de Muçarela Grande, seus itens e somente pedidos afetados que ficarem vazios. Não é exclusão geral do histórico. |

## Integração com o trabalho dos colegas

Reconheço a autoria de Marcelo no backend de consulta/criação de pedidos (`96d1490`) e no cardápio por categoria (`d686b22`, PR #19). Minha contribuição foi adaptar contratos e ligar o fluxo do cliente a essa base; não reivindico a criação original desses endpoints.

Reconheço a implementação da área interna, autenticação e gestão trazida por Christian em `c63b253`. A `main` contém esse commit por meio da integração posterior; o histórico de merges identifica a PR #29 para a branch `integracao/login-frontend`. Também reconheço o trabalho de Guilherme na listagem e no aceite originais (`8fbcab0`).

No merge `b148d29`, o Git registra conflitos em `frontend/src/services/menu.ts` e `frontend/src/types/product.ts`. Comparei as versões do merge com `9560bc4`: elas são iguais às da main daquele momento. O diff combinado comprova a retirada de um `rewrites` duplicado em `next.config.mjs`, a remoção do bloco de transição indevidamente duplicado no repository e o ajuste dos testes para ingredientes opcionais. Minha atuação nesse ponto foi de reconciliação, sem substituir a autoria das funcionalidades internas.

Os documentos de grupo da Sprint 3 são registros parciais anteriores, com situação consultada em 09/10/2026. Quando indicam integração pendente, descrevem aquele estágio. Registro aqui as incorporações posteriores, preservando os textos de grupo e sem declarar retroativamente que as funcionalidades já estavam integradas naquela data.

## Qualidade e testes

Executei as verificações abaixo em **03/11/2026**. Estes são resultados atuais sobre a base `48b39e7`, não uma reprodução dos números históricos das capturas de outubro.

| Verificação executada | Resultado real | Alcance e limite |
|---|---|---|
| `cd backend` e `.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider` | **145 passed, 43 skipped**, sem falhas, em 2,65 s | A suíte inclui os testes de status. Sem `TEST_DATABASE_URL`, os testes que exigem PostgreSQL são ignorados; não trato os 43 como aprovados. |
| PostgreSQL adicional: `pytest` restrito a `tests/test_cliente_bordas_integracao.py` e `tests/test_integracao_auth_pedidos.py`, com `TEST_DATABASE_URL` derivada do ambiente sem exibir credenciais | **21 passed**, sem falhas, em 10,12 s | Schemas exclusivos dentro de transação, desfeitos por rollback. Validei SQL, migrations, sessão, cadastro, bordas e isolamento. Esses 21 estavam ignorados na execução anterior; restam 22 testes antigos de banco não executados. |
| `cd frontend` e `node_modules/.bin/tsc.cmd --noEmit --incremental false` | Código de saída **0**, sem diagnósticos | Verificação de tipos; não equivale a build, teste de navegador ou medição de performance. |
| Consulta somente de leitura ao PostgreSQL local: `SELECT count(*) FROM produto` | **85 produtos** | Confirma o banco de desenvolvimento consultado nesta data, não outros ambientes. Não reapliquei migrations nesse banco durante esta documentação. |
| Conferência de Git e autoria | Commits citados resolvidos por `git cat-file`; incorporação conferida por `git merge-base --is-ancestor`; PRs identificadas nas mensagens de merge | A checagem não comprova homologação do cliente nem período oficial da sprint. |

Não executei build, testes manuais no navegador ou análise de desempenho nesta revisão documental. Não somei execuções repetidas da mesma suíte. O total distinto aprovado nas duas execuções de backend foi **166**, com os **22 testes antigos de banco** ainda não executados. A disponibilidade do banco foi confirmada pela execução isolada e pela consulta de leitura, não presumida a partir do `.env`.

**Registro manual da sprint:** [PREENCHER: datas, cenários e resultados dos testes manuais da Sprint 4].

## Dificuldades e como foram superadas

- **Integração de versões distintas:** resolvi os conflitos explícitos do merge `b148d29` e preservei os contratos do cliente presentes na main.
- **Acentuação e dados antigos:** as migrations 003/004 declaram `SET client_encoding = 'UTF8'`; a 007 trata especificamente o status com UTF-8 interpretado como Latin-1. As capturas antigas mostram corrupção, mas o Git não registra o comando original de importação: não afirmo como comprovada a causa operacional exata dessa carga.
- **Hash inválido em conta de exemplo:** acrescentei tratamento de `ValueError`/`TypeError` em `backend/app/services/auth_services.py` no PR #31, retornando erro de credenciais em vez de expor o formato interno. Não documento senha, hash nem ajuste de credencial local.
- **Carregamento e perfil sem interação em 127.0.0.1:** o commit `95047bf` inclui `allowedDevOrigins` para os hosts locais. O resultado visual final deve ser acompanhado da evidência E13; não uso a captura antiga de carregamento como prova da correção.
- **Mudanças de regra durante a integração:** distingui o checkout como convidado do login obrigatório posterior e mantive testes de autorização compatíveis com a regra atual.

## Pendências, riscos e dívida técnica

1. Não considero a história #9 integralmente entregue: faltam atualização automática e estimativa na tela atual de Meus pedidos.
2. O filtro de disponibilidade do cardápio não valida estoque de ingredientes; falta parte do aceite da história #4.
3. O meio a meio registra os nomes das metades na observação e cobra o ID do sabor mais caro; não existe relação própria para consultar cada metade estruturalmente no banco. As bordas, por sua vez, já têm vínculo próprio.
4. O cadastro de produtos aceita ingredientes opcionais, necessário ao fluxo de bebidas, enquanto o backlog ainda exige ao menos um ingrediente para produto. Essa divergência deve ser alinhada, sem afirmar que o documento foi atualizado.
5. A cidade padrão não implementa validação geográfica estrita; também permanece o CEP técnico padrão `00000-000` em `backend/app/schemas/pedido_schema.py`.
6. O bloqueio de login após múltiplas tentativas não está implementado no service atual, apesar de previsto na história #1.
7. Há dois arquivos de migration com prefixo 005, ambos versionados e necessários. A migration 008 é destrutiva para os exemplos identificados e deve ser revisada antes de execução em outro ambiente.
8. O script `lint` ainda chama `next lint`, apesar da dependência Next 16. Não executei auditoria de vulnerabilidades nesta revisão e não atribuo quantidade de vulnerabilidades sem medição.
9. O README mantém instruções anteriores à integração atual, e o roteiro ainda contém placeholder. Os 22 testes antigos de banco não foram executados nesta revisão; não declaro cobertura completa.

## Plano de correção da avaliação E4

Registro somente o plano e o estado que encontrei, sem implementar alterações no README, plano de testes, roteiros ou documentos do grupo. A nota e o documento da devolutiva não constam dos arquivos consultados: [PREENCHER: confirmar nota e referência da devolutiva E4].

| Correção solicitada | Ação | Responsável | Arquivo(s) | Status |
|---|---|---|---|---|
| Plano com título, identificação e cabeçalho na estratégia | Acrescentar título do documento, identificação da equipe/versão e linha de cabeçalho/separador à tabela de estratégia. A versão atual começa em `## 1. Estratégia` e contém linhas sem cabeçalho. | [PREENCHER: responsável pelo plano de testes E4] | `docs/plano_de_teste.md` | Pendente |
| Casos de transição de status, inclusive inválidos | Mapear os testes já existentes aos casos documentados e complementar as lacunas propostas abaixo. O código já cobre transições válidas, salto de etapa, retorno e alteração de pedido entregue, mas esses casos não constam na tabela CT01–CT06 do plano. | [PREENCHER: responsável pelos casos de status E4] | `backend/tests/test_status_pedidos.py`; `backend/tests/test_cliente_bordas_integracao.py`; `docs/plano_de_teste.md` | Em andamento |
| Relatório agregado dos testes | Consolidar casos, ambiente, data, resultados e ignorados no documento de evidências definido pela equipe para a entrega E4. Minha tabela individual acima não substitui a revisão do relatório de grupo. | [PREENCHER: responsável pelo relatório agregado E4] | `docs/Sprints/sprint-3-evidencias-teste.md`, documento existente a revisar pela equipe | Pendente |
| Convenções de branch/commit de funcionalidades | Documentar prefixos para funcionalidades e correções e exemplos de fluxo de PR. O README atual descreve apenas `docs/nome-curto` e commits `docs:`. | [PREENCHER: responsável pelas convenções no README E4] | `README.md` | Pendente |
| Remover placeholder do roteiro | Substituir o campo `[url do Figma/Penpot, com acesso de visualização liberado]` pelo link definitivo; verificar os dois arquivos de roteiro com grafias Unicode diferentes. | [PREENCHER: responsável pelo roteiro E4] | `docs/Roteiro do Protótipo Navegável — Pizzaria do Barriga.md`; `docs/Roteiro do Protótipo Navegável — Pizzaria do Barriga.md` | Pendente |

### Casos propostos para a correção, sem implementação nesta tarefa

| Caso proposto | Resultado esperado | Situação no código examinado |
|---|---|---|
| Funcionário ativo aceita Recebido → Em preparação | HTTP 200 e atribuição ao funcionário autenticado | Coberto por `test_aceite_atribui_funcionario_autenticado` e regressão SQL de aceite |
| Em preparação → Saiu para entrega | HTTP 200, responsável preservado | Coberto por `test_transicao_valida_preserva_responsavel` |
| Saiu para entrega → Entregue | HTTP 200, responsável preservado | Coberto pelo mesmo teste parametrizado |
| Pular etapas: Recebido → Entregue ou Em preparação → Entregue | HTTP 409, sem atualização | Coberto por `test_transicao_invalida_retorna_409_sem_atualizar` |
| Voltar etapa: Saiu para entrega → Em preparação | HTTP 409, sem atualização | Coberto pelo teste de transição inválida |
| Alterar pedido Entregue → Saiu para entrega | HTTP 409, sem atualização | Coberto pelo teste de transição inválida |
| Alterar pedido Entregue → Recebido | HTTP 409, sem atualização | Comportamento previsto pelas regras; caso específico a acrescentar aos testes e ao plano |
| Cliente ou funcionário inativo tenta aceitar | HTTP 403, sem alteração | Coberto por `test_alteracao_exige_funcionario_ativo` |

## Retrospectiva individual

Consigo sustentar pelo histórico que separei integração, alterações de contrato e correções em commits revisáveis, reunidos nas PRs #28 a #32. A reconciliação de conflitos e os testes de isolamento ajudaram a manter verificáveis os limites entre a tela do cliente e a operação interna.

Como oportunidade técnica, identifico a necessidade de aproximar backlog, plano de testes, README e código: os exemplos de estoque, acompanhamento automático e ingredientes obrigatórios mostram critérios que ainda não correspondem integralmente à implementação.

- **Minha avaliação pessoal sobre o que funcionou:** [PREENCHER: aprendizado pessoal e práticas que funcionaram na Sprint 4].
- **Minha avaliação pessoal sobre o que melhorar:** [PREENCHER: dificuldade pessoal e ação de melhoria para a próxima sprint].

## Evidências das atividades

Reservo `img/sprint-4/` como pasta relativa a este documento. O modelo das Sprints 1/2 utiliza imagens hospedadas externamente; adoto aqui a pasta local solicitada, com `.gitkeep`, sem copiar ou gerar imagens. Os links abaixo são nomes sugeridos para as capturas que o autor ainda deve inserir. Capturas de erro ou de versões antigas podem servir de contexto, mas não substituem demonstrações do estado corrigido. Não incluo capturas com credenciais de ambiente.

| ID | Nome de arquivo a usar | Legenda e afirmação a comprovar |
|---|---|---|
| E1 | `e01-cardapio-do-banco.png` | Resposta do GET público com categorias e produtos; comprova a leitura do backend. |
| E2 | `e02-pizza-modal-borda.png` | Cardápio atual e modal com tamanho, segundo sabor e borda; comprova a interface integrada. |
| E3 | `e03-sacola-meio-a-meio.png` | Sacola com meio a meio, observação, borda, quantidade e total; comprova a montagem do pedido. |
| E4 | `e04-checkout-login.png` | Checkout após login, com contato e entrega/retirada; comprova o fluxo autenticado. |
| E5 | `e05-confirmacao-pedido.png` | Confirmação com número do pedido; comprova o retorno de criação à tela. |
| E6 | `e06-pedido-persistido.png` | Consulta SQL do mesmo pedido e seus itens/bordas, sem dados pessoais; comprova a persistência. |
| E7 | `e07-funcionario-aceite.png` | Pedido aceito na área interna, com Em preparação; comprova o resultado do aceite. |
| E8 | `e08-meus-pedidos.png` | Conta de cliente com o próprio pedido e botão Atualizar; comprova consulta isolada e atualização manual. |
| E9 | `e09-pytest.png` | Terminais das duas execuções de 03/11/2026: 145 aprovados/43 ignorados e 21 aprovados na rodada isolada. |
| E10 | `e10-tsc.png` | Comando de tipos concluído, incluindo código de saída zero; comprova a verificação estática. |
| E11 | `e11-prs-mergeadas.png` | Histórico com merges #28–#32 e PR #28 integrada; comprova a incorporação e as datas, sem atribuir autoria de colegas a mim. |
| E12 | `e12-migrations-e-produtos.png` | Migrations 007/008 e consulta da contagem de 85 produtos, sem credenciais; comprova a correção versionada e o estado local consultado. |
| E13 | `e13-cabecalho-menu-conta.png` | Cabeçalho circular e menu Entrar/Cadastrar em 127.0.0.1, com cardápio carregado; comprova o estado final da interface. |

![E1 - Cardápio consultado no backend](img/sprint-4/e01-cardapio-do-banco.png)
<!-- INSERIR PRINT: GET /api/v1/cardapio com categorias e produtos disponíveis. -->

![E2 - Modal de pizza com borda](img/sprint-4/e02-pizza-modal-borda.png)
<!-- INSERIR PRINT: modal atual exibindo tamanho, segundo sabor e borda da pizza. -->

![E3 - Sacola com personalização](img/sprint-4/e03-sacola-meio-a-meio.png)
<!-- INSERIR PRINT: pizza meio a meio com observação, borda, quantidade e total. -->

![E4 - Checkout autenticado](img/sprint-4/e04-checkout-login.png)
<!-- INSERIR PRINT: checkout após login com dados fictícios de contato e entrega/retirada. -->

![E5 - Confirmação com número](img/sprint-4/e05-confirmacao-pedido.png)
<!-- INSERIR PRINT: confirmação do pedido com o identificador retornado pela API. -->

![E6 - Pedido persistido](img/sprint-4/e06-pedido-persistido.png)
<!-- INSERIR PRINT: consulta SQL relacionando pedido, itens e bordas; ocultar dados pessoais. -->

![E7 - Aceite na área interna](img/sprint-4/e07-funcionario-aceite.png)
<!-- INSERIR PRINT: pedido após Aceitar pedido, com status Em preparação na área interna. -->

![E8 - Consulta dos próprios pedidos](img/sprint-4/e08-meus-pedidos.png)
<!-- INSERIR PRINT: cliente autenticado consultando o próprio pedido, com Atualizar visível. -->

![E9 - Resultados atuais de pytest](img/sprint-4/e09-pytest.png)
<!-- INSERIR PRINT: resultados das duas rodadas de backend descritas neste documento. -->

![E10 - Verificação de tipos](img/sprint-4/e10-tsc.png)
<!-- INSERIR PRINT: execução de tsc e código de saída zero, sem confundir com build. -->

![E11 - Histórico de integração](img/sprint-4/e11-prs-mergeadas.png)
<!-- INSERIR PRINT: PR #28 integrada e histórico de merges #29, #30, #31 e #32. -->

![E12 - Migrations e contagem local](img/sprint-4/e12-migrations-e-produtos.png)
<!-- INSERIR PRINT: migrations 007/008 e SELECT count(*) FROM produto retornando 85; sem credenciais. -->

![E13 - Cabeçalho e menu funcionando](img/sprint-4/e13-cabecalho-menu-conta.png)
<!-- INSERIR PRINT: menu Entrar/Cadastrar e cardápio carregado no endereço 127.0.0.1; não usar o estado antigo travado. -->

## Uso de ferramentas de apoio

[PREENCHER: seguir a política da disciplina sobre declaração de ferramentas de apoio]

## Referências verificadas

- Base examinada: `main`, merge `48b39e7`, de 29/10/2026. Verifiquei existência dos commits e ancestralidade, além da autoria de Gabriel Freire/Gabriel Freire Flores pelo e-mail de commits do projeto.
- Contexto anterior da Sprint 3: [relatório individual](sprint-3-contribuicao-Gabriel-Freire-Flores.md), [relatório do grupo](sprint-3-relatorio.md), [retrospectiva](sprint-3-retrospectiva.md) e [evidências de teste](sprint-3-evidencias-teste.md). Não alterei esses arquivos.
- Base de autoria dos colegas: Marcelo, `96d1490` e `d686b22`; Christian, `c63b253`; Guilherme, `8fbcab0`. O commit `534da12`, de acompanhamento com estimativa, não é ancestral da main examinada; não o incluo como funcionalidade entregue por mim.

| PR | Branch indicada no merge | Data do merge no Git | Merge e commits de referência |
|---|---|---|---|
| [#17](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/17) | `feat/cardapio-v2-pedido` | 04/10/2026 | `ddfcda4`; `d962689`. Contexto da Sprint 3. |
| [#18](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/18) | `feat/cardapio-v2-pedido` | 04/10/2026 | `bfb43f3`; `f9e9faa`. Contexto da Sprint 3. |
| [#19](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/19) | `feature/consulta-cardapio` | 09/10/2026 | `db3417f`; `d686b22`. Backend de Marcelo, contexto de integração. |
| [#28](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/28) | `feature/integracao-cliente-backend` | 25/10/2026 | `9560bc4`; `5520321`; `ea328f1`. |
| [#29](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/29) | `integracao/login-frontend` | 26/10/2026 | `56c0182`; `b148d29`; incorporação de `c63b253`. |
| [#30](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/30) | `integracao/login-frontend` | 27/10/2026 | `f6c990e`; `2caf6df`. |
| [#31](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/31) | `fix/validacao-integracao-pedidos` | 28/10/2026 | `f025544`; `7541b92`; `30c148b`; `1875933`; `567e663`. |
| [#32](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/32) | `feat/cabecalho-menu-conta` | 29/10/2026 | `48b39e7`; `2332025`; `0c83f32`; `7479e53`; `8a551a0`; `a7d5555`; `95047bf`. |

Não localizei merge identificado como PR #27 nas mensagens de merge da main; referencio a integração efetiva pelo commit de Christian e pela PR #29, sem inventar um merge próprio para esse número.

## Marcadores pendentes de preenchimento

1. [PREENCHER: papel na Sprint 4]
2. [PREENCHER: início e término da Sprint 4]
3. [PREENCHER: horas dedicadas à Sprint 4]
4. [PREENCHER: datas, cenários e resultados dos testes manuais da Sprint 4]
5. [PREENCHER: confirmar nota e referência da devolutiva E4]
6. [PREENCHER: responsável pelo plano de testes E4]
7. [PREENCHER: responsável pelos casos de status E4]
8. [PREENCHER: responsável pelo relatório agregado E4]
9. [PREENCHER: responsável pelas convenções no README E4]
10. [PREENCHER: responsável pelo roteiro E4]
11. [PREENCHER: aprendizado pessoal e práticas que funcionaram na Sprint 4]
12. [PREENCHER: dificuldade pessoal e ação de melhoria para a próxima sprint]
13. [PREENCHER: seguir a política da disciplina sobre declaração de ferramentas de apoio]
