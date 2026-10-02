# Ata de Retrospectiva — Sprint 1 e Sprint 2

> Documentado em conjunto devido à unificação dos prazos de entrega das duas Sprints.

Equipe: Gabriel Freire Flôres (RA 2840482423010) — Marcelo Augusto Oliveira Jose (RA 2840482423043) — Christian de Lima (RA 2840482523031) — Guilherme Fabiano da Silva Gomes (RA 2840482423037) Trilha: B (Cliente real nº 1)

## 1. Ações da retrospectiva anterior — foram aplicadas?

| Ação decidida | Aplicada? | Evidência/comentário |
|---|---|---|
| — | — | Não há registro de retrospectiva anterior formalizada para estas Sprints. |

## 2. O que funcionou bem

- A estrutura inicial do frontend foi criada e a home da visão do cliente foi implementada e validada com sucesso em ambiente local (Sprint 1).
- Na Sprint 2, a jornada completa do cliente (Menu → Carrinho → Checkout → Confirmação) foi implementada de forma incremental, por etapas validadas uma a uma, com build aprovado a cada entrega. Isso permitiu identificar e corrigir problemas antecipadamente, como arquivo vazio causando erro de build e ajustes de responsividade mobile.
- As interfaces de Login, Cadastro, Sobre e Footer, pendentes da Sprint 1, foram concluídas.
- O vídeo do Hero foi otimizado, reduzindo seu tamanho de aproximadamente 21 MB para 600 KB antes de ser incorporado ao produto, evitando impacto negativo de performance.
- A reconciliação da PR #10, relacionada ao trabalho de outro integrante e à reintrodução da área de funcionário, foi concluída com sucesso, preservando o conteúdo original da branch e validando o build antes da mesclagem à `main`.

## 3. O que não funcionou

- Houve descompasso entre o planejamento do Backlog para a Sprint 1 (histórias #1, #2 e #3, relacionadas a login, categorias e produtos) e o que foi efetivamente entregue. Foram concluídas a estrutura, a home e as interfaces de login/cadastro, enquanto categorias e produtos administráveis não foram concluídos nessa Sprint.
- A `main` do repositório ficou temporariamente desatualizada em relação à branch de trabalho, exigindo um processo manual de fetch/merge para sincronização.
- Durante a reconciliação da PR #10, houve risco de perda acidental de código funcional, envolvendo os hooks `use-funcionarios.tsx` e `use-produtos.tsx`. O Git marcou os arquivos para deleção sem apresentar um conflito explícito, exigindo verificação manual antes do commit.
- 

## 4. Ações para a próxima sprint

| Ação | Responsável |
|---|---|
| Manter o build como etapa de validação após cada implementação ou alteração relevante. | Equipe |
| Verificar manualmente arquivos modificados ou removidos durante merges antes de realizar o commit. | Equipe |
| Manter a `main` sincronizada com as branches de desenvolvimento para reduzir conflitos e necessidade de sincronizações manuais. | Equipe |
| Priorizar a conclusão das funcionalidades que ficaram pendentes do planejamento da Sprint 1. | Equipe |
