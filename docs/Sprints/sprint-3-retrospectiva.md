# Ata de Retrospectiva — Sprint 3

**Trilha:** B (Cliente real nº 1)

Equipe: Gabriel Freire Flôres (RA 2840482423010) — Marcelo Augusto Oliveira Jose (RA 2840482423043) — Christian de Lima (RA 2840482523031) — Guilherme Fabiano da Silva Gomes (RA 2840482423037)

> Registro parcial dos aprendizados da sprint, a complementar pela equipe. As propostas abaixo ainda precisam ser alinhadas pela equipe; não representam decisões de reunião já formalizadas.

## 1. Ações da retrospectiva anterior — foram aplicadas?

| Ação decidida | Aplicada? | Evidência/comentário |
|---|---|---|
| Manter a base sincronizada antes de iniciar novas funcionalidades | Aplicada no início do trabalho | Repositório local atualizado e branches separadas para cardápio e acompanhamento |
| Manter contratos atualizados junto dos endpoints | Sim, nas funcionalidades registradas | READMEs de cardápio e acompanhamento com formatos, erros e instruções de integração |
| Executar os testes na versão Python prevista | Sim, para as implementações realizadas | Testes executados com Python 3.14.7 e PostgreSQL temporário |
| Integrar os endpoints às telas e validar o fluxo completo | Pendente neste registro | Escopo implementado somente no backend; contrato entregue para o frontend |
| Manter a base sincronizada antes de iniciar novas funcionalidades (frontend, Gabriel) | Parcial | Branch do frontend criada a partir de uma `main` local desatualizada (28 commits atrás, relativos ao backend); sincronização com a `main` prevista antes de concluir a PR |

## 2. O que funcionou bem

- A separação em routes, controllers, services e repositories manteve o padrão do backend e facilitou implementar as consultas.
- O cardápio foi publicado em uma PR própria, com migração, documentação e 6 testes aprovados.
- O acompanhamento foi desenvolvido em outra branch, com 25 testes aprovados, incluindo proteção dos pedidos de outros clientes.
- Os testes com schemas temporários permitiram validar SQL, migração e leitura de mudança de status sem usar as tabelas compartilhadas como massa de teste.
- A documentação deixou claros os formatos de resposta e o comportamento esperado de atualização periódica no frontend.
- A execução dos testes existentes ajudou a identificar falhas anteriores às novas funcionalidades.
- (Frontend) Dados do cardápio e do pedido isolados em camadas próprias (`lib/data/products.ts` e `services/orders.ts`), deixando localizada a troca futura por chamadas ao backend.
- (Frontend) Entregas em lotes pequenos, com verificação de tipos e build a cada lote, e conferência do pedido gravado no navegador.
- (Frontend) O PDF do Cardápio v2 serviu como fonte única de itens, ingredientes e preços, e as regras de negócio (meio a meio pelo preço da metade mais cara; entrega somente em Jardinópolis) foram incorporadas ao fluxo.

## 3. O que não funcionou

- Problemas no ambiente de execução e nas permissões de publicação interromperam parte do trabalho; o envio de branches precisou ser realizado pelo terminal local.
- A suíte existente não ficou totalmente aprovada: foram encontradas falhas de autenticação, uma rota antiga de categorias nos testes e divergência sobre o funcionário atribuído ao pedido.
- O banco não possuía foto e descrição de produto, exigindo migração e posterior preenchimento para o cardápio retornar esses dados.
- Não havia prazo individual de entrega definido. Foi adotada uma estimativa geral configurável, ainda dependente de alinhamento com a pizzaria.
- A integração das consultas com as telas não foi validada nesta entrega, pois o escopo implementado foi somente backend e contrato.
- (Frontend) Após o merge da PR #10, o `carrinho/page.tsx` ficou idêntico ao `checkout/page.tsx` e a tela do carrinho foi perdida; o problema foi identificado na análise do frontend desta sprint.
- (Frontend) Somente 9 dos 45 itens do cardápio têm foto, e as demais dependem da pizzaria.
- (Frontend) A nomenclatura de status diverge entre frontend (`recebido`, `em_preparo`, `pronto`, `entregue`), backend ("Recebido", "Em preparação") e fila do funcionário ("Em produção", "Pronto", "Entregue").
- (Frontend) A versão do Next.js no `package.json` (14.2.5, com alerta de segurança) divergia da planejada (16.3.4).
- (Frontend) O login com perfil e a proteção de rota permanecem pendentes.
- A correção E4 apontou que o plano de testes não cobre o fluxo de status do pedido, que é a principal regra de negócio do projeto.

## 4. Ações para a próxima sprint

| Ação | Responsável |
|---|---|
| Alinhar e corrigir as falhas existentes de testes sem alterar regras apenas para obter aprovação | Responsáveis pelas funcionalidades (a alinhar) |
| Validar as consultas com a tela do cliente, incluindo sessão, atualização periódica e encerramento após entrega/cancelamento | Responsáveis pelo backend e frontend (a alinhar) |
| Confirmar aplicação da migração 002 e preenchimento de foto e descrição no ambiente compartilhado | Responsáveis pelo backend e dados (a alinhar) |
| Confirmar o prazo estimado e o fuso dos horários gravados no banco | Equipe e pizzaria (a alinhar) |
| Executar novamente a suíte após os merges e registrar o resultado integrado | Responsáveis pelo backend (a alinhar) |
| Atualizar os contratos quando formatos ou regras dos endpoints mudarem | Responsáveis pelos endpoints (a alinhar) |
| Alinhar a nomenclatura e o fluxo de status do pedido entre frontend, backend e área do funcionário | Gabriel, Marcelo e Christian (a alinhar) |
| Integrar o frontend ao `GET /api/v1/cardapio` (tamanhos P e G, fotos) e verificar se a criação de pedido comporta meio a meio, observação e retirada | Gabriel e Marcelo (a alinhar) |
| Obter com a pizzaria as fotos dos sabores do cardápio | Gabriel (a alinhar) |
| Implementar login com perfil e proteção de rota no frontend, simulados até a autenticação do backend | Gabriel (a alinhar) |
| Sincronizar a branch do frontend com a `main` e concluir a PR | Gabriel (a alinhar) |
