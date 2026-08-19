# Documento de Visão — [Aplicação Web para pedidos e gestão da Pizzaria do Barriga]

**Equipe:** Gabriel Freire Flôres (RA 2840482423010) — Milene Fernanda Araujo Pereira (RA 2840482423044) — Marcelo Augusto Oliveira Jose (RA 2840482423043) — Christian de Lima (RA 2840482523031) - Guilherme Fabiano da Silva Gomes (RA 2840482423037)

**Trilha:** B (Cliente real nº 1)

**Origem do problema:** Cliente real - Pizzaria do Barriga / Jardinópolis - SP

**Data:** 21/08/2026

## 1. Problema

A Pizzaria está em fase de crescimento, o seu atendimento é realizado via Whatsapp, sendo uma atendente e este o único canal de comunicação para realização dos pedidos. O processo de efetuação de pedidos é realizado manualmente utilizando papel e caneta. Por se tratar de processos manuais, isso gera algumas dores em horários com maior pico de movimento: (1) Atraso na passagem do pedido para a cozinha; (2) Possíveis erros na escrita por conta do alto volume de informações chegando ao mesmo tempo, podendo ocasionar errata no pedido de Pizza; (3) Insatisfação do cliente com demora de retorno ou pedido errado; (4) muitas operações {atendimento via mensagem, presencial, via telefonema} destinadas a uma pessoa ocasionando gargalo; (5) Falta de controle nos pedidos efetuados, status de pagamento, ganhos totais; (6) Em média, problemas advindos das causas apresentadas acima geram um atraso de 30 minutos no tempo de entrega;

## 2. Público-alvo e perfis de usuário

| Perfil | Quem é | O que faz no sistema |
|---|---|---|
| Funcionário | Atendente/Colaborador, responsável pelo recebimento e acompanhamento dos pedidos | Visualiza, confirma pedidos, atualiza status, consulta informações e auxilia em atendimentos 

| Gerente | Responsável pela gestão | gerencia produtos, categorias, ingredientes, consulta relatórios de vendas e acompanha pedidos 

## 3. Visão da solução

O sistema será uma aplicação web para centralizar o processo de realização e gerenciamento de pedidos da pizzaria. O cliente pode consultar cardápio, selecionar as pizzas que deseja e finalizar o atendimento pelo próprio site, sem depender do atendimento via Whatsapp. Os funcionários terão acesso a uma aplicação interna na qual poderão acompanhar o quadro de pedidos de forma mais rápida e a gerência tem um controle e visão melhor do negócio, ele terá acesso a relatórios, produtos, pedidos entre outros.

## 4. Objetivos do MVP (o que o semestre entrega)

- Reduzir o tempo médio entre a realização do pedido e seu encaminhamento para a cozinha, elimininando a transcrição manual dos pedidos.

- Reduzir a ocorrência de erros de interpretação dos pedidos, permitindo que as informações já sejam aplicadas pelo cliente diretamente na aplicação, chegando para a equipe da pizzaria os dados já estruturados.

- Centralizar o acompanhamento de pedidos e informações de vendas, automazindo processos e garantindo integridade dos dados, garantindo relatórios confiáveis e melhor controle das operações do comércio.

## 5. Fora de escopo (explicitamente)

- Automação completa da cozinha ou integração com equipamentos da mesma.

- Integração com aplicativos de terceiros, como iFood e outros marketplaces.

- Integração direta com máquinas de cartão ou sistemas de pagamento.

- Aplicativo mobile nativo para Android/iOS, sendo o acesso mobile realizado pela aplicação web responsiva.

- Sistema próprio de entregadores e rastreamento GPS em tempo real.

- Emissão de documentos fiscais.

## 6. Requisitos mínimos do §3 do Manual — como este projeto cobre cada um
| Requisito mínimo | Como este projeto cobre |
|---|---|
| Autenticação com 2+ perfis | Sistema de autenticação com perfis de Funcionário e Gerente, cada um com permissões específicas. 

| 6+ entidades com relacionamento N:N |  Usuário, Funcionário, Gerente, Produto, Categoria, Ingrediente, Pedido, ItemPedido o relacionamento N:N ocorre em por exemplo Produto e Ingrediente. 

| Regra de negócio não trivial | Controle de disponibilidade dos produtos baseado nos ingredientes em estoque e validação d fluxo de status dos pedidos. 

| Consulta agregada (relatório/dashboard) | Dashboard/relatórios com informações como quantidade de pedidos, faturamento, produtos mais vendidos e vendas por período. 

| Validações em interface e banco | Validação de campos obrigatórios, valores, quantidades, dados de pedido e regras de integridade no banco de dados. 

| Deploy público por URL | Deploy planejado na Vercel (a confirmar na E4) 

| Repositório Git com README | https://github.com/Gabrielfreireflores/Projeto-pizzaria/ |

## 7. Riscos identificados
| Risco | Impacto | Mitigação |
|---|---|---|
| Escopo maior que a capacidade da equipe no semestre | Ataso ou entrega incompleta do MVP | Priorizar funcionalidades essenciais e definir claramente o que ficará fora do escopo.

| Mudança nos requisitos durante o desenvolvimento | Retrabalho e atraso nas Sprints | Validação dos requisitos e do fluxo principal com o responsável pela pizzaria antes do desenvolvimento e registrar as mudanças.

| Dificuldade na integração dos módulos do sistema | Falhas no fluxo de realização e recebimento de pedidos | Definir as responsabilidades de cada componente e realizar testes na integração e implementação de cada um.

# Uso de Inteligência Artificial

A Inteligência Artificial foi utilizada como ferramenta auxiliar durante o planejamento e desenvolvimento do projeto, principalmente para apoiar a organização das ideias, definição do escopo, identificação de requisitos, levantamento de riscos e avaliação das funcionalidades propostas. A ferramenta foi utilizada como apoio à equipe, sem substituir as decisões e validações realizadas pelos integrantes do projeto.