# Ata de Retrospectiva — Sprint 1 e Sprint 2

> Documentado em conjunto devido à unificação dos prazos de entrega das duas Sprints.

## Pontos positivos / o que funcionou

- A estrutura inicial do frontend foi criada e a home da visão do cliente foi implementada e validada com sucesso em ambiente local (Sprint 1).
- Na Sprint 2, a jornada completa do cliente (Menu → Carrinho → Checkout → Confirmação) foi implementada de forma incremental, por etapas validadas uma a uma (build aprovado a cada entrega), o que permitiu identificar e corrigir problemas cedo (ex.: arquivo vazio causando erro de build, ajuste de responsividade mobile).
- As interfaces de Login, Cadastro, Sobre e Footer, pendentes da Sprint 1, foram concluídas.
- O vídeo do Hero foi otimizado (de ~21MB para ~600KB) antes de ser incorporado ao produto, evitando impacto negativo de performance.
- A reconciliação da PR #10 (trabalho de outro integrante, reintroduzindo a área de funcionário) foi concluída com sucesso, preservando o conteúdo original da branch e validando o build antes da mesclagem à `main`.
- [INFORMAÇÃO NECESSÁRIA] quanto a outros pontos positivos da equipe como um todo, por não haver registro documental de discussão em equipe sobre estas Sprints.

## Pontos que poderiam ser melhorados

- Houve descompasso entre o planejamento do Backlog para a Sprint 1 (histórias #1, #2 e #3, ligadas a login, categorias e produtos) e o que foi efetivamente entregue nela (estrutura, home, e apenas a interface de login/cadastro, sem categorias/produtos administráveis).
- Houve trabalho paralelo não coordenado: outro integrante (Christian de Lima) desenvolveu, de forma independente, uma versão própria de cadastro/login/área de funcionário (commit `0fd8a98`), que precisou ser revertida (`ccbbdfc`) e, mais tarde, reintroduzida via PR #10 com conflitos de merge.
- A branch `feature/equipe-e-autenticacao` (Christian) ficou desatualizada em relação à `main` por um período prolongado, acumulando divergência que gerou 13 conflitos de rename/delete no momento da reconciliação — sinal de que branches de longa duração deveriam ser sincronizadas com a `main` com mais frequência.
- A `main` do repositório ficou temporariamente desatualizada em relação à branch de trabalho, exigindo processo manual de fetch/merge para sincronização.
- [INFORMAÇÃO NECESSÁRIA] quanto a decisões específicas da equipe sobre redistribuição de tarefas.

## Dificuldades ou impedimentos

- Erro de build causado por um arquivo (`carrinho/page.tsx`) salvo vazio (0 bytes) no ambiente local, identificado e corrigido por diagnóstico manual (verificação de conteúdo do arquivo via terminal).
- Referência local de `origin/main` corrompida/travada (`cannot lock ref`), corrigida com `git update-ref -d` seguido de novo `fetch`.
- Necessidade de reconciliar o histórico da `main` após o revert do trabalho de outro integrante.
- Na reconciliação da PR #10, risco de perda acidental de código funcional (hooks `use-funcionarios.tsx` e `use-produtos.tsx`), que o Git marcou automaticamente para deleção durante o merge sem sinalizar como conflito explícito — exigiu verificação manual cuidadosa antes de commitar.
- [INFORMAÇÃO NECESSÁRIA] quanto a outras dificuldades formalmente registradas pela equipe.

## Aprendizados

- Validar o conteúdo real de arquivos no disco (não apenas assumir que foram salvos) evita erros de build difíceis de diagnosticar à primeira vista.
- Comprimir mídia (vídeo/imagens) antes de subir ao repositório evita impacto de performance no produto final.
- Em merges envolvendo branches de longa duração e divergentes, nem toda perda de arquivo aparece como "conflito" explícito — é necessário conferir manualmente a lista de arquivos deletados/modificados antes de commitar um merge, mesmo quando o Git não acusa erro.
- [INFORMAÇÃO NECESSÁRIA] quanto a aprendizados formalizados coletivamente pela equipe.

## Ações de melhoria para a próxima Sprint

- Implementar as histórias pendentes de gestão de categorias e produtos (Histórias #2 e #3 do Backlog original).
- Coordenar previamente com os demais integrantes antes de iniciar desenvolvimento de funcionalidades sobrepostas (ex.: login/cadastro/área de funcionário), para evitar retrabalho.
- Sincronizar branches de longa duração com a `main` com mais frequência, para reduzir o volume de conflitos acumulados.
- Auditar o conteúdo da área de funcionário introduzida pela PR #10 antes de considerá-la parte das entregas validadas pela equipe.
- [INFORMAÇÃO NECESSÁRIA] quanto a outras ações de melhoria decididas formalmente pela equipe.

## Responsáveis/prazos

[INFORMAÇÃO NECESSÁRIA]
