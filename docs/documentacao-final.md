# Documentação Final — Pizzaria do Barriga

**Deploy definitivo:** https://projeto-pizzaria-frontend-seven.vercel.app
**Backend:** https://projeto-pizzaria-backend-xi.vercel.app
**Repositório:** https://github.com/Gabrielfreireflores/Projeto-pizzaria
**Equipe:** Gabriel Freire Flôres (RA 2840482423010) — Marcelo Augusto Oliveira Jose (RA 2840482423043) — Christian de Lima (RA 2840482523031) — Guilherme Fabiano da Silva Gomes (RA 2840482423037).
**Trilha:** B (Cliente real nº 1). Laboratório de Engenharia de Software, ADS Fatec Ribeirão Preto, 2026/2.
**Consolidação:** 13/11/2026. Uso exclusivamente acadêmico; URL publicada não equivale a aceite do cliente ou autorização comercial.
**Versão examinada:** código local `6619185730be4946b59cba95ae5e3e6f75a26687`; a `main` remota consultada em `fa3cb7f32c6131eadede3e8ced1ef77cb3c6bcce` tem sete commits adicionais, apenas documentais. Não foi verificado o SHA do deployment no painel Vercel; não há tag final inventada.

Este índice reaproveita o relatório integrado pela [PR #35](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/35), a documentação técnica e os registros individuais. A aplicação centraliza cardápio, montagem do pedido e acompanhamento interno, substituindo a transcrição manual; os desvios abaixo permanecem explícitos.
Estrutura conforme o [modelo oficial E10](https://ararauna-lab-es-2026-2.netlify.app/modelos_de_entregas_lab_es#e10), consultado em 13/11/2026. O caminho canônico exigido é este; [relatorio-final.md](relatorio-final.md) mantém o ponto de entrada anterior.

## 1. Índice de artefatos do semestre

| Entrega | Documento | Link |
|---|---|---|
| E1 | Documento de Visão | [Visão](documento-de-visao.md) |
| E2 | Backlog + Termo de Aceite do Projeto | [Backlog original](BackLog.md), [termo inicial E2b](TermoAceite.md) |
| E3 | UML + DER + DDL | [UML original](uml/Uml.md), [UML v2](uml/Uml-v2.md), [DER](der/der.md), [schema](../db/schema.sql), [manifesto](../db/migrations/manifest.json) |
| E4 | README + Protótipo + Plano de Testes | [README](../README.md), [protótipo](Roteiro%20do%20Protótipo%20Navegável%20—%20Pizzaria%20do%20Barriga.md), [plano](plano_de_teste.md) |
| E5 | Sprint 1 | [Relatório](Sprints/sprint-1-relatorio.md), [retrospectiva](Sprints/sprint-1-retrospectiva.md), [evidências](Sprints/sprint-1-evidencias-teste.md) |
| E6 | Sprint 2 | Registro coletivo próprio não localizado; há contribuições individuais conjuntas de Sprints 1–2 abaixo. A equipe deve confirmar/complementar, sem inventar rituais |
| E7 | Sprint 3 | [Relatório](Sprints/sprint-3-relatorio.md), [retrospectiva](Sprints/sprint-3-retrospectiva.md), [evidências](Sprints/sprint-3-evidencias-teste.md) |
| E8 | Sprint 4 | [Relatório](Sprints/sprint-4-relatorio.md), [retrospectiva](Sprints/sprint-4-retrospectiva.md), [evidências](Sprints/sprint-4-evidencias-teste.md); metadados de Review/período dependem da equipe |
| E9 | Relatório de testes + Termo de Aceite do Cliente | [Relatório final de testes](relatorio-testes-final.md), [termo final a assinar](termo-aceite-cliente.md) |
| E10 | Consolidação + manual + apresentação | Este índice, [README final](../README.md), [manual com capturas reais](manual-do-usuario.md), [checklist](evidencias/e9-e10/checklist-entrega.md). Vídeo e roteiro não produzidos por solicitação; apresentação e participação da equipe permanecem externas |

### Contribuições individuais e autoria

| Integrante | Registros e contribuição identificada |
|---|---|
| Gabriel Freire Flôres | [Sprints 1–2](Sprints/sprint-1-%26-2-contribuicao-Gabriel-Freire-Flores.md), [Sprint 3](Sprints/sprint-3-contribuicao-Gabriel-Freire-Flores.md), [Sprint 4](Sprints/sprint-4-contribuição-Gabriel-Freire.md). Integração do cliente, bordas, sacola, reconciliação interna e preparação de infraestrutura; commit `6619185` |
| Marcelo Augusto Oliveira Jose | [Sprints 1–2](Sprints/sprint-1-%26-2-contribuicao-Marcelo-Augusto-Oliveira-Jose.md), [Sprint 3](Sprints/sprint-3-contribuicao-Marcelo-Augusto-Oliveira-Jose.md). Base de cardápio e criação/consulta de pedidos; PR #19, `96d1490`, `d686b22`, reutilizados na integração |
| Christian de Lima | [Sprints 1–2](Sprints/relatorio-individual-sprint-1-2-christian.md), [relatório individual publicado](Sprints/relatorio-individual-sprint-3-4-Christian.md), preservado sem reescrever sua autoria. Área interna, login, equipe, produtos e integração; `c63b253`, PR #29 |
| Guilherme Fabiano da Silva Gomes | [Sprints 1–2](Sprints/Sprint1_2_GuilhermeGomes.md). Base de autenticação, listagem e aceite (`93fa30f`, `8fbcab0`) e merge da PR #20 (`4c9adb6`), conforme histórico citado na Sprint 4 |

Não foram fabricados relatórios individuais ausentes de sprints posteriores nem presença em rituais. A cópia de Christian em `docs/Sprints/` é a referência canônica; existe outra cópia na raiz `docs/` da main remota. Os dois roteiros de protótipo com acentuação Unicode distinta têm conteúdo idêntico: o índice usa o nome com acentos compostos, sem apagar o histórico.

### Rastreabilidade requisito → modelo → código → teste

| Requisito | Modelo relacionado | Código principal | Teste/evidência |
|---|---|---|---|
| H1 — login e perfis | Usuário/Cliente/Funcionário no [UML v2](uml/Uml-v2.md) e [DER](der/der.md) | `backend/app/services/auth_services.py`, `app/security.py`, `app/login_rate_limit.py`; `frontend/src/hooks/use-auth.tsx` | E9 CT01/CT02/CT11; `test_auth_services.py`, `test_infra_services.py`, `test_deploy_security.py` |
| H2/H3 — categoria, produto e receita | Categoria/Produto/Ingrediente, N:N no DER/DDL | `backend/app/schemas/produto_schema.py`, `app/repositories/produto_repository.py`, `app/repositories/categoria_repository.py`; telas internas de produtos | E9 CT03/CT04; `test_produtos.py`; receita obrigatória/ativação de categoria não atendidas |
| H4/H5 — cardápio e sacola | Produto e item do pedido no UML/DDL | `backend/app/repositories/cardapio_repository.py`; `frontend/src/services/menu.ts`, `src/hooks/use-cart.tsx`, `src/components/shared/product-card.tsx` | E9 CT05/CT07/CT10/CT16; leitura e capturas publicadas; estoque não atendido |
| H6 — pedido, contato, borda | Pedido/Endereço/ItemPedido/ItemPedidoBorda no DDL + manifesto | `backend/app/services/pedido_services.py`, `app/schemas/pedido_schema.py`; `frontend/src/app/(publico)/checkout/page.tsx` | E9 CT06/CT10/CT12; SQL de integração não reexecutado em produção |
| H7/H8/H9 — aceite, status e consulta | Status/Pedido e vínculos cliente/funcionário no DER | `backend/app/services/pedido_services.py`, `app/repositories/pedido_repository.py`; telas de pedidos | E9 CT08/CT09; `test_status_pedidos.py`, `test_consulta_pedidos.py`; H9 parcial |
| E1 — relatório agregado / H10 | Dashboard previsto na visão | Não há módulo de consulta agregada de vendas/CSV entregue | Pendente, sem resultado de teste inventado |

## 2. Desvios do escopo original (vs. E2b)

| Item | Mudou? | Justificativa |
|---|---|---|
| E2b 1 / H1 — autenticação | Cliente e Funcionário implementados; Redis acrescentado | Login real informado como validado anteriormente. Bloqueio distribuído agora implementado e testado; afirmações antigas de ausência são históricas |
| E2b 2 / H2 — categorias | Parcial em relação ao backlog | Cadastro existe; categoria não possui campo de ativação. Ativação/desativação do produto não substitui esse critério |
| E2b 3 / H3 — ingredientes obrigatórios | Parcial | Produto tem categoria e associação N:N, mas o validador aceita receita vazia para qualquer categoria. O relato de bebidas sem receita não demonstra obrigatoriedade técnica para pizzas |
| E2b 4 / H4 — disponibilidade por estoque | Parcial | SQL do cardápio usa somente `produto.disponivel`; não calcula estoque suficiente nem baixa ingredientes |
| E2b 5 / H5 — carrinho | Critérios básicos implementados, personalização ampliada | Quantidade, remoção e total; segundo sabor cobra o maior preço e borda acompanha tamanho. Persistência local não é pedido confirmado |
| E2b 6 / H6 — finalização | Login de cliente obrigatório na versão atual | Checkout tem contato, entrega/retirada, pagamento informativo e confirmação. Convidado é legado; não representa o fluxo ativo. Não há pagamento eletrônico real |
| E2b 7 / H7 — tempo real interno | Consulta periódica | A tela interna atualiza a lista periodicamente; não é push/WebSocket. Não foi medida garantia de latência |
| E2b 8 / H8 — aceite | Implementado com autorização e transições ordenadas | Recebido → Em preparação → Saiu para entrega → Entregue. Revisão técnica não alterou pedidos reais |
| E2b 9 / H9 — acompanhamento com estimativa | Parcial | Meus pedidos limita a 50 registros da própria conta, usa Atualizar e não exibe previsão |
| E1 — Gerente distinto | Não entregue como perfil separado | Autorização atual usa Cliente e Funcionário; o cargo de gerente não cria RBAC gerencial distinto. Manual separa tarefas de gestão, sem inventar permissões |
| E1 §6 — consulta agregada / H10 CSV Could | Dashboard/relatório de vendas não entregue; CSV não entregue | H10 referencia equivocadamente H11 (notificações) como dashboard. Falta de prioridade não é evidência de negociação; mínimo acadêmico de consulta agregada exige decisão do professor, não pode ser ocultado |
| E1 — redução do atraso e melhoria de faturamento | Benefícios não medidos com cliente | Não há estudo antes/depois nem homologação que comprove redução de 30 minutos |
| Infraestrutura | Dois projetos Vercel + Neon + Upstash + Blob | Hospedagem acadêmica gratuita; sem operação comercial. Não é autorização para usar Hobby no negócio real |

Não foi encontrada aprovação formal para as reduções de escopo. A E2b original e as histórias foram preservadas; pendências precisam de parecer real do cliente/professor. WhatsApp/e-mail, máquina de cartão, fiscal e GPS não foram implementados como novas funcionalidades nesta finalização.

### Limitações e trabalhos futuros

Concluir critérios parciais somente em etapa autorizada; priorizar a avaliação do requisito agregado da disciplina. Medir cobertura e desempenho; ampliar E2E autenticado e acessibilidade; tratar arquivos Blob órfãos sem apagar imagens compartilhadas. Os cinco avisos de imagens do lint não foram suprimidos. As imagens do cardápio têm [procedência declarada](../frontend/public/produtos/CREDITOS.txt), não são todas fotos reais fornecidas pelo cliente.

## 3. Arquitetura final (resumo)

O navegador acessa Next.js (App Router) na Vercel; rewrites `/api/:path*` encaminham ao Flask publicado em outro projeto Vercel. O Flask usa routes → controllers → services/schemas → repositories → PostgreSQL Neon via psycopg, TLS e URL pooled. Conexões fecham ao fim da operação; importação/startup não executam SQL, migrations ou bootstrap. Entrada serverless `backend/main.py:app`; `run.py` serve apenas ao desenvolvimento local.

Upstash REST guarda contadores de login compartilhados entre instâncias. Vercel Blob público armazena novos uploads autenticados de funcionários; `produto.foto` guarda a URL. Fotos versionadas em `frontend/public` continuam válidas. Armazenamento local não é fallback persistente em produção. O token Blob nunca vai ao navegador; `NEXT_PUBLIC_BLOB_HOST` é apenas hostname público.

Sessões Flask assinadas por chave estável; cookie host-only, Secure em produção, HttpOnly e SameSite=Lax. CSRF exige `X-CSRF-Protection: 1`, valida origem e rejeita cross-site; CORS amplo não habilitado. Limite de imagem 3 MiB e requisição multipart 4 MiB em produção. Login não fica liberado se Redis falhar.

| Camada | Tecnologia/versão verificada |
|---|---|
| Frontend | Next 16.3.4, React 19.3.0, TypeScript 5.9.3, Tailwind 3.4.19 |
| Backend | Python 3.13 (local 3.13.2), Flask 3.1.3, psycopg 3.3.5, Pillow 13.0.0 |
| Serviços | Neon PostgreSQL Free, Upstash Redis REST Free, Vercel Blob Hobby; `vercel-blob` 0.5.1 e `httpx2` 2.16.0 |
| Ferramentas | pytest 9.1.1, pytest-flask 1.3.0, Node local 20.19.4, ESLint 8.57.1 |

O banco já inicializado tem 12 tabelas de aplicação e `_pizzaria_migrations`, conforme validação anterior informada na sessão. O [manifesto](../db/migrations/manifest.json) fixa schema + 001 + 002 + 003 + 004 + 005 bordas + 005 CPF; mantém nomes completos e SHA-256. Os dois 005 não devem ser renumerados. 006/007 não foram necessários à instalação nova; 008 é destrutiva e foi excluída do instalador. Nenhum desses scripts é executado por deploy.

### Resultados finais e infraestrutura

Em 13/11, backend 282 aprovados/43 ignorados; frontend 4 aprovados; build, TypeScript, lint e `pip check` aprovados. Na aplicação publicada, nove consultas HTTP e cinco verificações de navegador passaram; há seis capturas reais no manual. Cardápio retorna 85 produtos em quatro categorias não vazias; isso não contradiz cinco categorias cadastradas anteriormente no banco, pois a API omite categoria vazia.

Neon, login real, Upstash (10/11 tentativas) e Blob (upload, leitura íntegra e exclusão HTTP 404) foram confirmados pelo usuário nas etapas anteriores. Nesta rodada não foram repetidas escritas, login real ou consulta administrativa a esses provedores. Veja [E9](relatorio-testes-final.md) e [registro reproduzível](evidencias/e9-e10/validacao-2026-11-13.md). Não há percentual de cobertura, laudo de segurança ou aceite de cliente inventados.

## 4. Como contribuir/rodar (aponta para o README atualizado)

Ver [README](../README.md) para instalação, variáveis, execução e testes. [Guia de deploy](deploy-academico-vercel.md) documenta origens, serviços gratuitos e limites; [inicialização controlada](../db/README-inicializacao.md) é referência administrativa, não uma instrução para reaplicar SQL no Neon existente.

Revisar alterações em branch e PR com ao menos um integrante; não publicar segredos. Esta finalização não fez commit, push, merge ou deploy. A atualização local de `relatorio-final.md` precisa ser conciliada com a versão que já existe na main em um PR futuro, sem sobrescrever trabalho alheio.

As condições de conclusão acadêmica estão no [checklist E9/E10](evidencias/e9-e10/checklist-entrega.md): termo ainda sem parecer/assinatura, homologação com cliente e capturas autenticadas pendentes; Sprint 2 coletiva não localizada; vídeo, roteiro e apresentação permanecem com a equipe. A documentação não declara E9/E10 integralmente aceitas enquanto esses itens estiverem abertos.
