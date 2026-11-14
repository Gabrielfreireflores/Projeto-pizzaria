## 1. Estratégia

Revisão final: 13/11/2026. [Resultados executados E9](relatorio-testes-final.md) e [comandos/evidências](evidencias/e9-e10/validacao-2026-11-13.md). Os cenários abaixo são plano; aprovação efetiva depende do registro da execução, não da intenção.

| Tipo | Escopo | Ferramentas | Execução / situação real |
|---|---|---|---|
| Unitário | Validações, preços, perfis e regras isoladas | pytest | Local, com mocks quando necessário |
| Integração simulada | Rotas Flask, serviços, SDKs e falhas | pytest, pytest-flask, transporte HTTP simulado | Sem banco/provedores remotos; não equivale a SQL real |
| Integração PostgreSQL | N:N, pedido, borda e isolamento de contas | pytest + banco exclusivamente de teste | Opt-in `TEST_DATABASE_URL`; proibido usar Neon publicado. 43 casos ignorados na bateria final |
| Frontend automatizado | Proxy configurado, domínios permitidos e imagens | Node test runner | 4 testes existentes; não representa E2E completo |
| Proxy local | Cookies, métodos, CSRF, JSON e multipart | pytest + Next/Flask em loopback | Opt-in após build local; negócio e login simulados |
| Funcional publicado sem escrita | Cardápio, modal, sacola local, acesso sem sessão e responsividade | GET HTTP + Chrome headless | Rodada de 13/11, perfil temporário e bloqueio de escrita remota |
| Aceitação | Fluxo completo cliente → funcionário → cliente e critérios E2b | Navegador + cliente/PO | Pendente de sessão autorizada e registro de participantes/parecer |

A execução automática por commit/PR era planejada; não há workflow CI versionado nesta revisão. Não declarar CI ou proteção de branch como configurados sem evidência. Falha do Redis deve bloquear login, e indisponibilidade Blob não deve causar fallback para disco em produção.

## 2. Critério de bloqueio de merge
O Pull Request será bloqueado e não poderá ser mesclado se:
(a) Falha na esteira: Algum teste automatizado existente quebrar durante a execução.
(b) Falta de cobertura: Novas funcionalidades ou regras de negócio forem enviadas sem a criação dos testes unitários correspondentes.
(c) Falta de revisão (Code Review): Não houver aprovação formal de pelo menos um desenvolvedor da equipe (revisão por pares) validando a lógica.
(d) Falta de contexto: A descrição do PR estiver vazia ou não explicar de forma clara o motivo e o impacto das alterações realizadas.
(e) Débito técnico: O código apresentar problemas de legibilidade, complexidade desnecessária.



## 3. Casos de teste planejados (cresce a cada sprint)

| ID | História (E2) | Cenário | Entrada | Resultado esperado | Prioridade |
|---|---|---|---|---|---|
| CT01 | História 1: Login | Múltiplas tentativas de login com senha incorreta. | E-mail correto e senha incorreta enviada sucessivas vezes. | O sistema deve aplicar o bloqueio após as múltiplas tentativas inválidas. | Alta (Must) |
| CT02 | História 1: Login | Autenticação bem-sucedida de perfis distintos. | E-mail e senha válidos de um Cliente e, posteriormente, de um Funcionário. | Redirecionamento correto para a área correspondente ao perfil logado. | Alta (Must) |
| CT03 | História 2: Categorias | Tentativa de cadastrar categoria duplicada. | Nome de categoria que já consta como cadastrado. | Erro de validação informando que o nome da categoria deve ser único. | Alta (Must) |
| CT04 | História 3: Produtos | Cadastro de produto com valor inválido. | Preenchimento do formulário com o campo de preço contendo o valor "-15.00". | O sistema deve rejeitar o cadastro, visto que o preço não pode ser negativo. | Alta (Must) |
| CT05 | História 5: Carrinho | Inclusão de itens e conferência matemática. | Adição de itens e alteração de quantidade na interface do carrinho. | O sistema permite alterar quantidades e calcula o valor total automaticamente. | Alta (Must) |
| CT06 | História 6: Finalizar pedido | Submissão de pedido sem os dados obrigatórios. | Formulário enviado deixando o campo telefone em branco. | Sistema exibe erro indicando que nome, telefone e endereço são obrigatórios. | Alta (Must) |
| CT07 | História 4: Cardápio | Agrupamento, preço e disponibilidade. | Leitura pública e retorno simulado da API. | Produtos disponíveis agrupados; estoque insuficiente é critério original ainda não implementado. | Alta (Must) |
| CT08 | Histórias 7/8: Lista e status | Aceitar com funcionário e tentar pular etapas. | Sessões/perfis simulados; transições válidas e inválidas. | Aceite atribui responsável; saltos e retornos recusados com 409. | Alta (Must) |
| CT09 | História 9: Meus pedidos | Isolamento por conta e acesso anônimo. | Sessão própria e GET sem sessão. | Somente próprios pedidos; anônimo 401. Previsão e atualização automática continuam pendentes. | Média (Should) |
| CT10 | Histórias 3/5/6: Personalização | Segundo sabor e borda vinculada. | Pizza, sabores, borda de tamanho válido/inválido. | Maior preço do sabor, borda adicional do mesmo tamanho, integridade do vínculo. | Alta |
| CT11 | Segurança transversal | CSRF, origem, cookies, upload inválido e erros. | Requisições sem proteção, imagem falsa, arquivo >3 MiB, multipart >4 MiB em produção. | Rejeição antes de gravar; mensagens sem segredos; cookie seguro em produção. | Alta |
| CT12 | Banco e instalador | Histórico, checksums, ordem e rollback. | Banco simulado e manifesto dos sete SQL. | Dois 005 distintos; 008 excluída; importação sem conexão nem SQL automático. | Alta |
| CT13 | Armazenamento | SDK, indisponibilidade e limpeza compensatória. | Transporte Blob simulado, falhas de upload e de persistência. | Sem sobrescrita/fallback; limpar somente novo arquivo quando aplicável. Não apagar fotos antigas automaticamente. | Alta |
| CT14 | Deploy/proxy | Configuração HTTPS, Set-Cookie e multipart. | Testes Node, proxy opt-in, build, TypeScript e lint. | Configuração inválida recusada; fluxo local aprovado. | Alta |
| CT15 | Disponibilidade publicada | Páginas, catálogo e ausência de sessão. | Somente GET, sem login e sem envio de pedido. | Páginas/cardápio 200; consultas protegidas 401. | Alta |
| CT16 | Interface publicada | Renderização, modal, sacola e móvel. | Perfil temporário sem credenciais; 390 × 844 e desktop. | Sacola local preservada e sem overflow horizontal no cenário medido. | Alta |

## 4. Rastreabilidade e limites

Cada CT é relacionado às áreas e aos arquivos de teste na seção 2 da [E9](relatorio-testes-final.md). Modelo: [UML v2](uml/Uml-v2.md), [DER](der/der.md) e [DDL](../db/schema.sql); requisitos: [backlog](BackLog.md) e [E2b](TermoAceite.md). Código: `backend/app/` e `frontend/src/`, detalhado no índice final. Os critérios originais de ativação de categoria, estoque, receita obrigatória e acompanhamento com estimativa não foram removidos para ajustar o plano à implementação.

Não usar credenciais reais em testes automatizados; não criar compras ou alterar dados publicados sem autorização. Cobertura de linhas, carga e aceite com cliente não foram medidos/concluídos nesta revisão. Resultados de sprints distintas não se somam como se fossem a mesma bateria.
