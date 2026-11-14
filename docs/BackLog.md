# Backlog Priorizado — Pizzaria do Barriga

**Equipe:** Gabriel Freire Flôres (RA 2840482423010) — Marcelo Augusto Oliveira Jose (RA 2840482423043) — Christian de Lima (RA 2840482523031) — Guilherme Fabiano da Silva Gomes (RA 2840482423037)
**Trilha:** B (Cliente real nº 1)

| # | História | Critérios de aceite | Prioridade (MoSCoW) | Estimativa | Sprint alvo |
|---|---|---|---|---|---|
| 1 | Como funcionário ou cliente, quero fazer login no sistema, para que apenas pessoas autorizadas acessem a área interna. | - Login por e-mail e senha<br>- Bloqueio após múltiplas tentativas inválidas<br>- Redireciona para a área correspondente ao perfil (Funcionário/Cliente) | Must | 3 | Sprint 1 |
| 2 | Como funcionário, quero cadastrar categorias de produtos (ex.: pizzas, bebidas, sobremesas), para que o cardápio fique organizado. | - Nome da categoria obrigatório e único<br>- Categoria pode ser ativada/desativada | Must | 2 | Sprint 1 |
| 3 | Como funcionário, quero cadastrar produtos vinculados a uma categoria e aos seus ingredientes, para que o cardápio reflita o que é realmente produzido. | - Produto exige nome, preço, categoria e ao menos um ingrediente<br>- Relacionamento N:N entre Produto e Ingrediente<br>- Preço não pode ser negativo | Must | 5 | Sprint 1 |
| 4 | Como cliente, quero visualizar o cardápio da pizzaria com fotos, descrições e preços, para que eu decida o que pedir sem falar com um atendente. | - Lista apenas produtos disponíveis (com estoque de ingredientes suficiente)<br>- Produtos agrupados por categoria | Must | 3 | Sprint 2 |
| 5 | Como cliente, quero montar meu pedido adicionando produtos a um carrinho, para que eu possa revisar antes de confirmar. | - Permite alterar quantidade e remover itens<br>- Calcula o valor total automaticamente | Must | 5 | Sprint 2 |
| 6 | Como cliente, quero finalizar meu pedido informando meus dados de contato e entrega, para que a pizzaria receba as informações corretas. | - Campos obrigatórios: nome, telefone, endereço<br>- Pedido é criado com status inicial "Recebido"<br>- Cliente recebe confirmação na tela | Must | 5 | Sprint 2 |
| 7 | Como funcionário, quero visualizar em tempo real os pedidos recebidos, para que eu não dependa de anotações em papel. | - Lista atualiza automaticamente sem precisar recarregar a página<br>- Exibe itens, observações e status de cada pedido | Must | 5 | Sprint 3 |
| 8 | Como funcionário, quero aceitar o pedido solicitado. | - Funcionário consegue confirmar o recebimento do pedido<br>- Transição de status segue ordem definida, sem pular etapas | Must | 5 | Sprint 3 |
| 9 | Como cliente, quero acompanhar o status do meu pedido após finalizá-lo, para que eu saiba quando ele ficará pronto. | - Exibe que o pedido foi solicitado, em preparo e recebe uma estimativa de entrega<br>- Atualiza automaticamente conforme o funcionário altera o status | Should | 3 | Sprint 3 |
| 10 | Como funcionário, quero exportar o relatório de vendas em CSV, para que eu envie os dados para contabilidade ou análise externa. | - Exporta os mesmos dados exibidos no dashboard do item 11 | Could | 3 | Sprint 4 |
| 11 | Como cliente, quero receber notificação por WhatsApp/e-mail quando meu pedido mudar de status, para não precisar ficar atualizando a página. | Fora de escopo neste semestre — ver Documento de Visão, seção 5 | Won't | — | — |
| 12 | Como funcionário, quero integrar o sistema a máquinas de cartão para pagamento automático, para eliminar a conferência manual. | Fora de escopo neste semestre — ver Documento de Visão, seção 5 | Won't | — | — |

## Conferência final de implementação — 13/11/2026

As histórias, critérios, prioridades e sprints originais acima foram preservados. A situação final não substitui a aprovação do escopo: veja [desvios E10](documentacao-final.md#2-desvios-do-escopo-original-vs-e2b), [testes E9](relatorio-testes-final.md) e [termo final a preencher](termo-aceite-cliente.md).

| História | Situação técnica e limite |
|---|---|
| H1 | Cliente/Funcionário, sessão e redirecionamento implementados; limitação distribuída Upstash acrescentada. Não há Gerente separado |
| H2 | Cadastro e unicidade; ativação/desativação de categoria ausente |
| H3 | Categoria, preço e N:N implementados; validador permite receita vazia, contrariando o critério original |
| H4 | Cardápio por categoria e disponibilidade manual; estoque de ingredientes não é calculado |
| H5 | Quantidades, remoção, total e persistência da sacola implementados; sabores/bordas ampliam o fluxo |
| H6 | Contato, entrega/retirada e confirmação implementados; versão atual exige cliente autenticado |
| H7/H8 | Lista periódica, responsável e transições ordenadas implementados e cobertos por testes locais |
| H9 | Parcial: próprios pedidos e Atualizar; sem previsão ou atualização automática na tela do cliente |
| H10 | CSV não entregue. A referência original ao dashboard do item 11 é inconsistente: H11 trata de notificações. Não foi criada nem renumerada história para ocultar isso |
| H11/H12 | Permanecem fora de escopo; nenhum envio automático ou cobrança integrada foi acrescentado |

O requisito de consulta agregada da visão permanece não atendido pelo dashboard planejado. A aceitação da redução depende do professor/cliente e não foi presumida. Os resultados atuais de Redis/frontend não reescrevem as evidências históricas das sprints.
