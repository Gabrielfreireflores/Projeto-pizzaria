# Documento de Visão — Aplicação Web para Pedidos e Gestão da Pizzaria do Barriga

**Equipe:** Gabriel Freire Flôres (RA 2840482423010) — Marcelo Augusto Oliveira Jose (RA 2840482423043) — Christian de Lima (RA 2840482523031) — Guilherme Fabiano da Silva Gomes (RA 2840482423037)

**Trilha:** B (Cliente real nº 1)

**Origem do problema:** Cliente real — Pizzaria do Barriga / Jardinópolis - SP

**Data:** 21/08/2026

## 1. Problema

A pizzaria está em fase de crescimento e seu atendimento é realizado principalmente via WhatsApp, tendo uma atendente como responsável por esse canal de comunicação para realização dos pedidos. Atualmente, o processo de efetuação dos pedidos é realizado manualmente, utilizando papel e caneta.

Por se tratar de um processo manual, surgem algumas dificuldades em horários de maior movimento: **(1)** atraso na passagem do pedido para a cozinha; **(2)** possíveis erros na escrita devido ao alto volume de informações recebidas simultaneamente, podendo ocasionar erros na especificação dos pedidos; **(3)** insatisfação do cliente devido à demora no retorno ou ao recebimento de pedidos incorretos; **(4)** concentração de diversas operações — atendimento via mensagem, presencial e telefone — em uma única pessoa, ocasionando gargalos; **(5)** falta de controle centralizado sobre os pedidos realizados, status de pagamento e faturamento; e **(6)** em média, os problemas decorrentes das situações apresentadas geram um atraso de aproximadamente 30 minutos no tempo de entrega.

## 2. Público-alvo e perfis de usuário

| Perfil | Quem é | O que faz no sistema |
|---|---|---|
| Funcionário | Atendente/colaborador responsável pelo recebimento e acompanhamento dos pedidos. | Visualiza e confirma pedidos, atualiza seus status, consulta informações e auxilia no atendimento. |
| Gerente | Responsável pela gestão da pizzaria. | Gerencia produtos, categorias e ingredientes, consulta relatórios de vendas e acompanha os pedidos. |

## 3. Visão da solução

O sistema será uma aplicação web para centralizar o processo de realização e gerenciamento de pedidos da pizzaria. O cliente poderá consultar o cardápio, selecionar os produtos desejados e finalizar o pedido pelo próprio site, reduzindo a dependência do atendimento via WhatsApp.

Os funcionários terão acesso a uma área interna na qual poderão acompanhar os pedidos de forma mais rápida e organizada. A gerência terá uma visão mais ampla do negócio, com acesso a relatórios, produtos, pedidos e outras informações relevantes para o controle das operações.

## 4. Objetivos do MVP

- **Antes:** o pedido depende de transcrição manual até chegar à cozinha, atrasando seu encaminhamento. **Depois:** o pedido é encaminhado de forma estruturada pelo sistema, eliminando a transcrição manual e reduzindo o tempo até chegar à cozinha.
- **Antes:** as informações do pedido são anotadas por um atendente, sujeitas a erros de interpretação no alto volume. **Depois:** as informações são inseridas pelo próprio cliente diretamente na aplicação e chegam à equipe da pizzaria de forma estruturada, reduzindo erros de interpretação.
- **Antes:** o acompanhamento dos pedidos e das informações de vendas é feito de forma manual e descentralizada. **Depois:** o acompanhamento é centralizado e automatizado, com integridade dos dados garantida e relatórios confiáveis para o controle das operações do comércio.

## 5. Fora de escopo

- Automação completa da cozinha ou integração com equipamentos utilizados na produção.
- Integração com aplicativos de terceiros, como iFood e outros marketplaces.
- Integração direta com máquinas de cartão ou sistemas de pagamento.
- Aplicativo mobile nativo para Android/iOS, sendo o acesso mobile realizado por meio da aplicação web responsiva.
- Sistema próprio de entregadores e rastreamento GPS em tempo real.
- Emissão de documentos fiscais.

## 6. Requisitos mínimos do §3 do Manual — como este projeto cobre cada um

| Requisito mínimo | Como este projeto cobre |
|---|---|
| Autenticação com 2+ perfis | Sistema de autenticação com perfis de **Funcionário** e **Gerente**, cada um com permissões específicas. |
| 6+ entidades com relacionamento N:N | O sistema contará com entidades como Usuário, Perfil, Produto, Categoria, Ingrediente, Pedido e ItemPedido, Cliente, StatusPedido. O relacionamento N:N poderá ocorrer, por exemplo, entre Produto e Ingrediente, por meio de uma entidade associativa. |
| Regra de negócio não trivial | Controle da disponibilidade dos produtos com base nos ingredientes em estoque e validação do fluxo de status dos pedidos. |
| Consulta agregada (relatório/dashboard) | Dashboard e relatórios com informações como quantidade de pedidos, faturamento, produtos mais vendidos e vendas por período. |
| Validações em interface e banco | Validação de campos obrigatórios, valores, quantidades, dados dos pedidos e regras de integridade no banco de dados. |
| Deploy público por URL | Deploy planejado na Vercel, a confirmar na E4. |
| Repositório Git com README | Repositório GitHub contendo o código-fonte, documentação e README do projeto. |

**Repositório:** `https://github.com/Gabrielfreireflores/Projeto-pizzaria/`

## 7. Riscos identificados

| Risco | Impacto | Mitigação |
|---|---|---|
| Escopo maior que a capacidade da equipe no semestre | Atraso ou entrega incompleta do MVP. | Priorizar as funcionalidades essenciais e definir claramente o que ficará fora do escopo. |
| Mudanças nos requisitos durante o desenvolvimento | Retrabalho e atraso nas Sprints. | Validar os requisitos e o fluxo principal com o responsável pela pizzaria antes do desenvolvimento e registrar as mudanças. |
| Dificuldade na integração dos módulos do sistema | Falhas no fluxo de realização e recebimento dos pedidos. | Definir as responsabilidades de cada componente e realizar testes de integração durante o desenvolvimento. |

# Uso de Inteligência Artificial

A Inteligência Artificial foi utilizada como ferramenta auxiliar durante o planejamento e desenvolvimento do projeto, principalmente para apoiar a organização das ideias, definição do escopo, identificação de requisitos, levantamento de riscos e avaliação das funcionalidades propostas. A ferramenta foi utilizada como apoio à equipe, sem substituir as decisões e validações realizadas pelos integrantes do projeto.