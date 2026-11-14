# Relatório de Entrega — Sprint 4 — Pizzaria do Barriga

> Atualização documental de 13/11/2026: o conteúdo abaixo preserva a situação histórica de 06/11/2026 e sua autoria. A entrega posterior de Redis, Blob, deploy e testes frontend está no [relatório final E9](../relatorio-testes-final.md) e na [documentação final E10](../documentacao-final.md); referências antigas a essas pendências não são o estado atual. Não foram inventadas datas de Review nem aprovações.

**Período:** a preencher pela equipe.
**Sprint Review:** a preencher pela equipe.

**Trilha:** B (Cliente real nº 1)

Equipe: Gabriel Freire Flôres (RA 2840482423010) — Marcelo Augusto Oliveira Jose (RA 2840482423043) — Christian de Lima (RA 2840482523031) — Guilherme Fabiano da Silva Gomes (RA 2840482423037)

> Registro parcial das entregas da Sprint 4, a complementar pela equipe. Situação conferida em 06/11/2026, com a main remota em `635c0ea`; o último merge funcional é a PR #32 (`48b39e7`).

## 1. Planejado vs. entregue

| História (E2) | Planejada para esta sprint? | Entregue? | Observação |
|---|---|---|---|
| #4 — H04-01 Consulta de cardápio | Continuidade da entrega anterior | Integrada à tela; critérios parciais | Backend de Marcelo (PR #19) consumido pelo frontend integrado por Gabriel (PR #28). Agrupamento, preços, descrições e imagens disponíveis; estoque de ingredientes ainda não participa do filtro |
| #5 — Montagem do pedido | Evolução da história da Sprint 2 | Entregue nos critérios de quantidade, remoção e total | Carrinho persistido no navegador, personalização, meio a meio pelo maior preço e borda vinculada à pizza. PRs #28 e #31 |
| #6 — Finalização do pedido | Continuidade e integração | Entregue nos critérios documentados | Nome, telefone e endereço para entrega; retirada sem endereço; pedido persistido com status Recebido e confirmação. Login de cliente obrigatório antes de confirmar no PR #32 |
| #7 — Lista interna de pedidos | Continuidade da integração interna | Implementada e integrada | Base de Guilherme e área interna de Christian; lista usa a API e consulta a cada 15 segundos. Gabriel realizou a reconciliação e ajustes posteriores |
| #8 — Aceite e fluxo de status | Continuidade e correção da integração | Implementado e coberto por regressão | Aceite atribui funcionário autenticado. Ordem Recebido → Em preparação → Saiu para entrega → Entregue; tentativa inválida retorna 409. Reparo de dados na migration 007 |
| #9 — Acompanhamento pelo cliente | Continuidade da história da Sprint 3 | Parcial | Meus pedidos filtra os pedidos da conta, exibe itens e status; consulta até 50 mais recentes. Atualização manual, sem estimativa na tela atual |
| #1 — Login por perfil | Evolução da história da Sprint 1 | Parcial no conjunto do backlog | Sessão, redirecionamento, proteção interna e gate do checkout integrados. Bloqueio após múltiplas tentativas inválidas ainda não implementado |
| #3 — Gestão de produtos integrada | Continuidade da área interna | Implementada, com divergência documental | Trabalho de Christian integrado à API, com ajustes de Gabriel em layout, descrição, fotos e duplicidade. Código aceita ingredientes opcionais; backlog ainda exige ao menos um ingrediente |

**Artefatos de apoio entregues:**

- Migrations 003 e 004 para retirada/contato simplificado e seed dos 85 produtos por tamanho.
- Migrations `005_bordas_por_item.sql` e `005_cliente_cpf_opcional.sql`, ambas necessárias apesar do mesmo prefixo; migration 006 para desativação inicial do Refrigerante legado.
- Migrations 007 e 008 para reparo do status e limpeza dos dois produtos de exemplo e suas dependências previstas.
- Testes de autenticação, bordas, isolamento de contas, menu da conta e transições de status; contratos em `backend/DOCS_API.md`, com trechos ainda sujeitos a atualização após a mudança de login.
- Imagens locais para 36 sabores e arquivo de procedência `frontend/public/produtos/CREDITOS.txt`; cabeçalho responsivo, logo circular, busca e menu da conta.

## 2. Incremento funcional demonstrável

O cliente consulta o cardápio pela API, escolhe tamanho, segundo sabor, observação e borda, revisa a sacola e confirma o pedido após login. A API calcula preços e grava o contato, os itens e as bordas; retirada não exige endereço. A consulta Meus pedidos deriva o cliente da sessão e não permite selecionar outra conta pelo navegador.

Na área interna, o funcionário autenticado consulta pedidos e aceita os que estão em Recebido. O aceite grava o funcionário responsável e muda para Em preparação. As próximas etapas são Saiu para entrega e Entregue; saltos ou retornos de etapa são rejeitados. A tela interna consulta novos pedidos automaticamente; a tela do cliente usa o botão Atualizar.

A base do backend de consulta e criação de pedidos é de Marcelo; a listagem e o aceite originais são de Guilherme; Christian implementou a integração da área interna, autenticação e gestão (`c63b253`). Gabriel realizou a integração do cliente, a reconciliação da área interna e as correções das PRs #28 a #32. O merge da PR #20, de autenticação, foi realizado por Guilherme em 16/10/2026 (`4c9adb6`). As bases anteriores são creditadas como trabalho reutilizado, sem atribuir novas implementações sem registro.

- **Link do deploy:** não registrado neste registro.
- **GIF/vídeo de demonstração:** não registrado neste registro.
- **Como reproduzir localmente:** preparar o PostgreSQL, aplicar o schema em banco vazio e as migrations em ordem, incluindo os dois arquivos 005; revisar a 008 antes de aplicá-la a dados existentes. Iniciar o backend com `python run.py` em `backend/` e o frontend com `npm run dev` em `frontend/`. Abrir `http://127.0.0.1:3000`, criar conta de cliente e concluir um pedido. A conta de funcionário precisa ter credenciais válidas configuradas no ambiente.

### Incremento do frontend do cliente (Gabriel Freire Flôres)

O fluxo passou da gravação apenas no navegador para envio à API e persistência no PostgreSQL. Foram acrescentados modal de pizza, borda no item, mistura de sabores doces e salgados, busca, cadastro com quatro campos, login obrigatório na confirmação e consulta dos próprios pedidos. A sacola e o formulário são preservados ao retornar do login. O cabeçalho foi ampliado, o logo ficou circular e o menu oferece Entrar/Cadastrar para visitantes e ações por perfil para usuários autenticados.

- **Branch:** `feature/integracao-cliente-backend` (PR #28), `integracao/login-frontend` (PRs #29/#30), `fix/validacao-integracao-pedidos` (PR #31) e `feat/cabecalho-menu-conta` (PR #32).
- **Como reproduzir localmente:** com frontend e backend iniciados, montar a sacola, entrar como cliente e percorrer dados, pagamento e confirmação. Conferir o pedido em Meus pedidos; aceitar com funcionário e consultar novamente pelo botão Atualizar. A sacola usa `pizzaria-barriga:cart:v2`; o pedido confirmado é gravado no servidor.
- **Link do deploy / vídeo de demonstração:** não registrados.

## 3. Backlog atualizado

- #4: integração visual e API incorporada nas PRs #28/#31; permanece pendente o cálculo da disponibilidade pelo estoque de ingredientes.
- #5: quantidade, remoção, total e persistência da sacola implementados; meio a meio cobra a metade mais cara, com observação e borda no item.
- #6: criação real de pedido, entrega/retirada e confirmação incorporadas; login de cliente tornou-se obrigatório na PR #32, substituindo o uso de Convidado no código.
- #7/#8: área interna integrada, lista automática, aceite e ordem de status implementados; correção do status corrompido e testes de regressão incorporados.
- #9: consulta dos próprios pedidos entregue parcialmente; não registrar como concluída enquanto faltarem atualização automática e estimativa na tela atual. O commit `534da12`, do acompanhamento com previsão de Marcelo, não é ancestral da main examinada.
- #1: autenticação e redirecionamento por perfil integrados; o critério de bloqueio por múltiplas tentativas continua pendente.
- Esses registros descrevem código e PRs confirmados, sem substituir a atualização do board ou a homologação da equipe.

## 4. Evidências de teste

- Em 06/11/2026, a suíte padrão retornou **145 passed, 43 skipped**, sem falhas, em 2,94 s.
- A rodada adicional restrita a `test_cliente_bordas_integracao.py` e `test_integracao_auth_pedidos.py`, com PostgreSQL em transação isolada, retornou **21 passed**, sem falhas, em 13,84 s. Esses casos estavam ignorados na execução padrão; restam 22 testes antigos de banco não executados.
- A verificação `tsc --noEmit --incremental false` terminou com código de saída zero. Ambiente verificado: Python 3.13.2 e Node 20.19.4; não confundir com as versões planejadas no README.
- Detalhes em [Evidências de teste da Sprint 4](sprint-4-evidencias-teste.md). Não houve novo build de produção nem nova execução manual completa nesta revisão documental.
- O [relatório individual de Gabriel](sprint-4-contribuição-Gabriel-Freire.md) registra a validação de 03/11/2026 e capturas de desenvolvimento; os números de datas diferentes não são somados. Capturas antigas de falhas não comprovam a correção final.

## 5. Retrospectiva e contribuição individual

- [Retrospectiva da Sprint 4](sprint-4-retrospectiva.md).
- [Relatório individual — Gabriel Freire Flôres](sprint-4-contribuição-Gabriel-Freire.md), publicado no GitHub em `635c0ea` e salvo localmente sem alterações.
- Gabriel: `5520321` e `ea328f1` (contrato e integração), `b148d29` (reconciliação), `2caf6df` (cards), `567e663` (bordas e integração), `7479e53` (login obrigatório), `8a551a0`/`a7d5555`/`95047bf` (conta e cabeçalho).
- Christian: `f7bebd8`, `aaf8984` e `c63b253` (HTTP, cliente de API, área interna e integração). Incorporação confirmada pela PR #29 (`56c0182`).
- Marcelo: base de consulta e criação em `96d1490`, cardápio em `d686b22` e PR #19, reutilizados pela integração desta sprint. Não foi localizado novo relatório individual dele para a Sprint 4 na main consultada.
- Guilherme: base de autenticação, listagem e aceite em `93fa30f` e `8fbcab0`, reutilizada; merge da PR #20 em `4c9adb6`. Não foi localizado relatório individual dele para a Sprint 4 na main consultada.

## 6. Riscos/impedimentos para a próxima sprint

- Completar estimativa e atualização automática de Meus pedidos e alinhar o prazo com a pizzaria.
- Implementar disponibilidade por estoque; alinhar backlog e código quanto a ingredientes opcionais para bebidas.
- Validar os 22 testes antigos de banco em ambiente próprio e repetir as verificações na versão Python prevista.
- Atualizar `backend/DOCS_API.md` e README para refletir login obrigatório, atualização manual e migrations atuais.
- Revisar a execução da migration 008 em outros ambientes; não tratar sua limpeza como exclusão geral do histórico. Aplicar ambos os arquivos 005.
- Confirmar as pendências da avaliação E4: plano de testes, casos de status documentados, relatório agregado, convenções de funcionalidades e placeholder do roteiro.
- Registrar homologação manual consolidada, período oficial, Sprint Review e evidências dos demais integrantes.
