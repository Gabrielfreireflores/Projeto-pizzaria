# Ata de Retrospectiva — Sprint 4

> Atualização documental de 13/11/2026: o conteúdo abaixo preserva a situação histórica de 06/11/2026 e sua autoria. A entrega posterior de Redis, Blob, deploy e testes frontend está no [relatório final E9](../relatorio-testes-final.md) e na [documentação final E10](../documentacao-final.md); referências antigas a essas pendências não são o estado atual. Não foram inventadas datas de Review nem aprovações.

**Trilha:** B (Cliente real nº 1)

Equipe: Gabriel Freire Flôres (RA 2840482423010) — Marcelo Augusto Oliveira Jose (RA 2840482423043) — Christian de Lima (RA 2840482523031) — Guilherme Fabiano da Silva Gomes (RA 2840482423037)

> Registro parcial dos aprendizados da sprint, a complementar pela equipe. As propostas abaixo ainda precisam ser alinhadas pela equipe; não representam decisões de reunião já formalizadas.

## 1. Ações da retrospectiva anterior — foram aplicadas?

| Ação decidida | Aplicada? | Evidência/comentário |
|---|---|---|
| Manter a base sincronizada antes de iniciar novas funcionalidades | Aplicada na integração registrada | Merge da main em `integracao/login-frontend` (`b148d29`) e incorporação pelas PRs #28 a #32; conflitos de contrato resolvidos |
| Manter contratos atualizados junto dos endpoints | Parcial | `backend/DOCS_API.md` foi atualizado no PR #31, mas ainda descreve checkout sem login e consulta automática, superados pelo PR #32 |
| Executar os testes na versão Python prevista | Não nesta validação | Execução de 06/11/2026 usou Python 3.13.2; o README planeja Python 3.14.7. Os testes passaram no ambiente efetivamente usado |
| Integrar os endpoints às telas e validar o fluxo completo | Aplicada na integração; homologação manual consolidada pendente | Cardápio e criação de pedido consomem a API; testes isolados validam cadastro, login, pedido, borda e isolamento entre contas |
| Alinhar a nomenclatura e o fluxo de status do pedido | Aplicada no fluxo de aceite e avanço | Recebido → Em preparação → Saiu para entrega → Entregue; transições inválidas retornam 409. Testes em `test_status_pedidos.py` |
| Confirmar migrations e preenchimento de imagens | Parcial | Migrations 003–008 versionadas e carregadas nos testes isolados; 36 imagens locais de sabores. Não comprova aplicação em todos os ambientes |
| Confirmar prazo estimado de entrega | Pendente | A tela atual de Meus pedidos não exibe estimativa e usa atualização manual; a história #9 segue parcial |
| Obter as fotos dos sabores do cardápio | Parcial em relação à obtenção de fotos reais | Foram incluídas imagens locais com procedência em `frontend/public/produtos/CREDITOS.txt`; não são apresentadas como fotos reais fornecidas pela pizzaria |
| Implementar login com perfil e proteção de rota no frontend | Aplicada no escopo de sessão e redirecionamento | Área interna integrada a partir do trabalho de Christian; checkout exige cliente autenticado. Bloqueio após múltiplas tentativas ainda não implementado |

## 2. O que funcionou bem

- A integração aproveitou o backend de cardápio e criação de pedidos desenvolvido por Marcelo, sem substituir a autoria dessa base. Gabriel adaptou o contrato e conectou as telas à API na PR #28.
- O trabalho de Christian em autenticação, equipe, produtos e pedidos internos (`c63b253`) foi incorporado na integração da PR #29. A reconciliação de Gabriel preservou os contratos do cardápio e removeu duplicações.
- A base de autenticação e aceite desenvolvida por Guilherme foi reutilizada; o histórico registra também seu merge da PR #20 (`4c9adb6`). A correção posterior do aceite preservou a atribuição ao funcionário autenticado.
- A jornada do cliente passou a gravar pedidos no servidor, com entrega ou retirada, observações, preços calculados pelo backend e borda vinculada ao item.
- O cadastro simplificado, o login obrigatório antes da confirmação e a consulta dos próprios pedidos foram integrados nas PRs #31 e #32.
- A organização em commits permitiu identificar as alterações de regra: checkout como convidado na PR #28 e sessão obrigatória na PR #32.
- A execução de 06/11/2026 não apresentou falhas: 145 testes aprovados na suíte padrão e 21 na rodada PostgreSQL isolada. O TypeScript também terminou sem erros.
- Os schemas de teste da rodada adicional foram desfeitos por rollback, permitindo validar SQL e autorização sem manter dados de teste nas tabelas normais.
- O cabeçalho, o menu da conta e a configuração de origens locais foram ajustados; `allowedDevOrigins` contempla localhost e 127.0.0.1.

## 3. O que não funcionou

- A integração encontrou conflitos em `services/menu.ts` e `types/product.ts`, além de `rewrites` e lógica de status duplicados. As correções constam de `b148d29`.
- Um status com acentos corrompidos impedia aceitar pedidos. A migration 007 corrige o nome preservando a chave; a regressão cobre o aceite após o reparo.
- Dados de exemplo continuavam misturados ao cardápio real. A migration 008 remove os dois produtos legados e somente suas dependências previstas; a limpeza exige cuidado em outros ambientes.
- O acesso por 127.0.0.1 deixava cardápio e conta no estado inicial de carregamento. O commit `95047bf` acrescentou as origens locais à configuração do Next.
- O acompanhamento do cliente ainda não atende a todos os critérios da história #9: faltam estimativa de entrega e atualização automática na tela atual.
- A consulta do cardápio filtra produtos disponíveis, mas não verifica estoque suficiente dos ingredientes, previsto no backlog.
- A validação padrão ignorou 43 testes que dependem de PostgreSQL; após executar 21 em isolamento, ainda restam 22 testes antigos de banco não executados nesta rodada.
- A versão Python da validação atual difere da planejada. Não houve novo build de produção nem teste manual completo nesta revisão documental.
- Plano de testes, README e roteiro ainda apresentam pendências da avaliação E4: tabela de estratégia sem cabeçalho, casos de status ausentes do plano, convenções limitadas à documentação e placeholder no roteiro.

## 4. Ações para a próxima sprint

| Ação | Responsável |
|---|---|
| Completar estimativa e atualização automática em Meus pedidos, alinhando a regra com a pizzaria | Backend e frontend — Gabriel e Marcelo (a alinhar) |
| Implementar disponibilidade por estoque e alinhar o cadastro de bebidas sem ingredientes com o backlog | Responsáveis pelo backend, produtos e dados (a alinhar) |
| Validar novamente o fluxo cliente → funcionário → cliente e registrar evidências manuais consolidadas | Gabriel, Christian e responsáveis pelo backend (a alinhar) |
| Validar os 22 testes antigos de banco em ambiente próprio e repetir na versão Python prevista | Responsáveis pelos testes e ambiente (a alinhar) |
| Atualizar contratos e README para login obrigatório, consulta manual e migrations atuais | Gabriel, Marcelo e Christian (a alinhar) |
| Confirmar aplicação das migrations e revisar a limpeza da 008 antes de executá-la em outro ambiente | Responsáveis pelo banco e integração (a alinhar) |
| Atualizar plano de testes, relatório agregado, convenções de funcionalidades e placeholder do roteiro conforme E4 | Equipe (responsáveis a definir) |
| Confirmar período, Sprint Review e homologação com o cliente | Equipe e Product Owner (a alinhar) |
