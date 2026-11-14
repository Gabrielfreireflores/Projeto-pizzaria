# Relatório de Testes Executados — Pizzaria do Barriga

**Data da bateria final:** 13/11/2026 (America/Sao_Paulo).
**Equipe:** Gabriel Freire Flôres (RA 2840482423010) — Marcelo Augusto Oliveira Jose (RA 2840482423043) — Christian de Lima (RA 2840482523031) — Guilherme Fabiano da Silva Gomes (RA 2840482423037).
**Trilha:** B (Cliente real nº 1).
**Escopo testado:** fluxo de cliente e funcionário do [Termo E2b](TermoAceite.md), com os desvios explicitados na [documentação final](documentacao-final.md#2-desvios-do-escopo-original-vs-e2b). Não significa aceite integral dos critérios ainda parciais.
**Modelo oficial:** [E9 — Relatório de Testes Executados](https://ararauna-lab-es-2026-2.netlify.app/modelos_de_entregas_lab_es#e9), consultado em 13/11/2026.

## 1. Resumo executivo

| Métrica | Valor |
|---|---|
| Total de casos de teste automatizados coletados | 329: backend 325 + frontend 4 |
| Passaram | 286: backend 282 + frontend 4 |
| Falharam | 0 na execução final dos testes |
| Ignorados | 43, dependem de PostgreSQL de teste; não executados contra o Neon |
| Cobertura automatizada (linhas/branches) | Não medida; quantidade de testes não é percentual de cobertura |
| Verificações públicas HTTP adicionais | 9 aprovadas; separadas dos 329 casos automatizados locais |
| Verificações adicionais no navegador publicado | 5 aprovadas; separadas da suíte local |
| Build / TypeScript / ESLint / dependências Python | Aprovados; lint com 5 avisos existentes de `<img>` |

Estratégia: regressão unitária e integração Flask em memória; repositories, Redis e Blob simulados quando necessário; proxy Next → Flask real em loopback, com serviços de negócio simulados. O frontend dispõe de quatro testes de configuração; isso não representa uma suíte completa de componentes ou E2E. As cinco verificações adicionais usaram Chrome headless no site publicado, com perfil temporário vazio e bloqueio de requisições remotas de escrita. A sacola alterada pertence somente ao navegador de teste; nenhum pedido foi enviado.

Ambiente: Windows, Python 3.13.2, Node 20.19.4, Next 16.3.4, React 19.3.0, TypeScript 5.9.3, Tailwind 3.4.19. O backend declara Python 3.13. Versões efetivas obtidas do ambiente/lockfile, não das antigas previsões do README. Comandos, resultados e limites estão no [registro da bateria](evidencias/e9-e10/validacao-2026-11-13.md).

## 2. Casos de teste — visão consolidada

Os IDs CT01–CT06 preservam o [plano E4](plano_de_teste.md); os demais completam sua rastreabilidade. Cada linha agrupa cenários, não equivale a um teste pytest nem deve ser somada novamente à seção 1.

| ID | Área | Tipo | Resultado | Observação |
|---|---|---|---|---|
| CT01 | H1 — limitação de login | Unitário/integração simulada | Passou | `test_infra_services.py`: atomicidade, expiração, concorrência e falha fechada. Validação real Upstash anterior informada: 10 permitidas, 11ª bloqueada, 898 s restantes; não repetida nesta rodada |
| CT02 | H1 — sessão e perfis | Unitário + proxy local | Passou | `test_auth_routes.py`, `test_auth_services.py`, `test_menu_conta.py`, `test_next_proxy.py`; login real administrativo foi confirmado pelo usuário nas etapas anteriores, sem novas credenciais nesta rodada |
| CT03 | H2 — categoria duplicada e autorização | Unitário/rota simulada | Passou no escopo executado | `test_deploy_security.py`; UNIQUE no DDL. Ativação/desativação de categoria não implementada; H2 permanece parcial |
| CT04 | H3 — preço, campos e receita | Unitário/rota simulada | Passou no escopo implementado | `test_produtos.py`; ingredientes são opcionais no validador atual, diferente do backlog. N:N existe; testes PostgreSQL ignorados nesta rodada |
| CT05 | H5 — carrinho | Navegador real público + proxy local | Passou no cenário executado | Modal, inclusão de uma pizza e persistência após navegação; captura real da sacola. Não foi executada uma compra real nem toda combinação de quantidades/sabores |
| CT06 | H6 — dados obrigatórios e autorização | Unitário/rota simulada | Passou | `test_consulta_pedidos.py`, `test_cadastro_simplificado.py`; criação SQL de pedido não repetida em produção |
| CT07 | H4 — cardápio por categoria | Unitário + GET publicado | Passou no escopo implementado | `test_cardapio.py`; proxy e backend retornaram 85 produtos em 4 categorias não vazias. Não comprova estoque de ingredientes |
| CT08 | H7/H8 — lista, aceite e transições | Unitário/integração simulada | Passou | `test_status_pedidos.py`: responsável autenticado, ordem das transições e conflitos HTTP 409. Não alterados pedidos publicados |
| CT09 | H9 — pedidos da própria conta | Unitário + GET sem sessão publicado | Passou no escopo implementado | `test_menu_conta.py`, `test_consulta_pedidos.py`; acesso anônimo HTTP 401. Tela usa Atualizar, sem estimativa: H9 parcial |
| CT10 | H3/H5/H6 — bordas e sabores | Unitário + navegador público | Parcial na bateria | Modal exibe segundo sabor e borda; regressões locais de preço/tamanho. SQL de bordas e isolamento pertence aos 43 testes PostgreSQL ignorados |
| CT11 | Segurança | Unitário/integração simulada | Passou | `test_deploy_security.py`: CSRF, origem, perfil ativo, cookies, erros sanitizados, MIME/conteúdo e limites 3 MiB/4 MiB |
| CT12 | Banco e instalador | Simulado/estático | Passou | `test_db_admin.py`, `test_infra_services.py`: checksums, dois 005, exclusão de 008, rollback, TLS e importação sem conexão. Nenhum SQL executado remotamente |
| CT13 | Blob | SDK com transporte simulado | Passou | `test_infra_services.py`; upload/leitura real e posterior exclusão HTTP 404 foram confirmados pelo usuário antes desta rodada, não repetidos |
| CT14 | Proxy, imagens e build | Node + proxy local + build | Passou | 4 testes em `frontend/tests/deploy-config.test.mjs`; `test_next_proxy.py` verifica métodos, cookies, CSRF e multipart sem banco |
| CT15 | Disponibilidade e acesso público | HTTP real publicado | Passou | `/`, `/login`, `/cadastro`, `/carrinho` HTTP 200; cardápio direto e via proxy 200; `/me`, `/meus-pedidos`, `/pedidos` sem sessão 401 |
| CT16 | Interface publicada | Navegador real público | Passou | Cardápio, modal com sabores/borda, sacola, redirecionamento interno para login e largura móvel de 390 px sem overflow horizontal |

**Histórico reaproveitado:** [Sprint 1](Sprints/sprint-1-evidencias-teste.md), [Sprint 3](Sprints/sprint-3-evidencias-teste.md) e [Sprint 4](Sprints/sprint-4-evidencias-teste.md). A Sprint 4 registra 145 aprovados/43 ignorados em 06/11 e uma rodada PostgreSQL isolada de 21 aprovados. Não somar baterias históricas aos números atuais nem tratar esses testes de banco como executados hoje. Não foi localizado documento coletivo específico de evidências da Sprint 2.

## 3. Bugs encontrados nesta bateria

| # | Descrição | Severidade | Status |
|---|---|---|---|
| 1 | Build inicial não conseguiu baixar Fraunces/Public Sans devido ao bloqueio de rede do ambiente | Impedimento de ambiente | Resolvido permitindo somente o download público; build repetido com sucesso, sem mudar o código |
| 2 | README descrevia deploy inexistente e versões planejadas incompatíveis com o ambiente | Média — documentação | Corrigido no README e na documentação final |
| 3 | Relatório final remoto marcava Sprint 4 como pendente e recomendava renumerar migrations já aplicadas | Média — documentação | Corrigido no índice canônico; manifesto preservado, sem renumeração |
| 4 | Plano afirmava CI automático sem workflow versionado, e documentação antiga não reconhecia Redis/testes frontend | Média — documentação | Plano revisado; registros históricos preservados com aviso e referência à E9 |
| 5 | Critérios originais não integralmente atendidos: categoria ativa, estoque, ingredientes obrigatórios, estimativa/atualização do cliente, gerente e consulta agregada | Limitação de aceite; impacto a avaliar com professor/cliente | Explicitados na documentação final e termo; não escondidos nem implementados como novas funcionalidades |

Não houve falha funcional nova comprovada nos cenários executados. Isso não atesta ausência de bugs, teste de carga, auditoria completa OWASP/LGPD, compatibilidade com todos os aparelhos ou aceite integral.

## 4. Testes de aceitação com cliente/PO

**Não comprovados nesta bateria.** A verificação técnica automatizada do site não contou com cliente/PO e não substitui homologação. O login administrativo real e os testes Neon/Redis/Blob anteriores foram relatados pelo usuário; não há neste relatório assinatura do cliente nem homologação completa de pedido em produção.

- Data da sessão de aceite: ____________________.
- Cliente/PO e participantes efetivos, com nome completo/RA quando integrantes: ____________________.
- Cenários propostos para execução autorizada: comparar os nove itens da E2b, revisar o pedido como cliente, aceitar como funcionário e conferir o acompanhamento; registrar especialmente as ressalvas de estoque e previsão. Escritas de homologação precisam de autorização específica.
- Resultado e evidências de participação: ____________________.
- Parecer e assinatura: preencher somente no [Termo de Aceite do Cliente](termo-aceite-cliente.md).
