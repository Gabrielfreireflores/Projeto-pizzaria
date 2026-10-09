# Evidências de Teste — Sprint 3

**Trilha:** B (Cliente real nº 1)

> Registro parcial das validações realizadas durante o desenvolvimento, a complementar pela equipe.

| Funcionalidade/cenário testado | Objetivo do teste | Procedimento realizado | Resultado esperado | Resultado obtido | Status | Evidência disponível | Observações |
|---|---|---|---|---|---|---|---|
| Consulta de cardápio — H04-01 | Consultar produtos disponíveis por categoria | Cliente HTTP Flask, mocks e PostgreSQL temporário | HTTP 200 com categorias e produtos disponíveis | Cenários aprovados na suíte de 6 testes | Aprovado na versão testada | `test_cardapio.py`, PR #19 | Não calcula disponibilidade por estoque |
| Campos e cardápio vazio | Validar foto, descrição, preço e ausência de produtos | Consulta com dados preenchidos, campos nulos e todos os produtos indisponíveis | Preço com duas casas, campos preservados e lista vazia com HTTP 200 | Retornos conferidos | Aprovado | `test_cardapio.py` | Dados legados podem retornar foto e descrição nulas |
| Migração de cardápio | Verificar compatibilidade e reaplicação | Aplicação da migração 002 duas vezes no schema temporário | Colunas criadas sem duplicação e produtos preservados | Testes de integração aprovados | Aprovado | `test_cardapio.py`, `002_produto_cardapio.sql` | Não comprova aplicação ao banco compartilhado |
| Falha de banco no cardápio | Evitar exposição de detalhes internos | Simulação de erro de conexão/configuração | HTTP 503 com mensagem genérica | Resposta conforme contrato | Aprovado | `test_cardapio.py` | Cenário simulado |
| Autorização no acompanhamento — história #9 | Restringir consulta ao cliente ativo dono do pedido | Sessões inválidas, cliente inativo, perfil de funcionário e outro cliente | HTTP 401/403 ou 404 conforme o caso | Cenários aprovados na suíte de 25 testes | Aprovado na versão testada | `test_acompanhamento.py`, PR #21 | Pedido alheio e inexistente retornam a mesma mensagem |
| Status e encerramento | Retornar estados e indicar término do acompanhamento | Consultas com os estados do enum de pedido | Status correto; entregue/cancelado sem estimativa nem próxima consulta | Respostas conferidas | Aprovado | `test_acompanhamento.py` | Não testa a API de alteração pelo funcionário |
| Estimativa de entrega | Verificar prazo, estabilidade e indicação de atraso | Testes com prazo padrão, prazo configurado, dados antigos e configuração inválida | Previsão baseada na criação, atraso sem mudar status e erro genérico para configuração inválida | Cenários aprovados | Aprovado | `test_acompanhamento.py` | Prazo padrão de 60 minutos precisa de alinhamento operacional |
| Leitura de mudança de status | Refletir mudança na próxima consulta | Alteração de Recebido para Em preparação no banco temporário entre dois GETs | Segundo GET retorna novo status e preserva previsão | Mudança refletida | Aprovado | Teste `test_banco_reflete_mudanca_e_preserva_previsao` | Valida backend; não houve atualização automática de tela |
| Cache e falha de banco no acompanhamento | Evitar cache e vazamento de detalhes | Inspeção dos cabeçalhos e simulação de erro | `Cache-Control: no-store` e erro 503 genérico | Resultados conferidos | Aprovado | `test_acompanhamento.py` | Sessão simulada pelo cliente de testes Flask |
| Regressão de produtos e pedidos | Identificar interferência das novas funcionalidades | Execução conjunta com os testes existentes em cada branch | Suíte sem regressões causadas pelas novas consultas | Cardápio: 96 aprovados e 2 falhas; acompanhamento: 115 aprovados e 2 falhas | Pendências preexistentes | Saídas de pytest registradas no desenvolvimento e PRs #19/#21 | Falhas na rota antiga de categorias e na expectativa de funcionário nulo no pedido |

## Observações gerais

- Cardápio: `6 passed in 1.16s`. Acompanhamento: `25 passed in 1.66s`.
- Verificações conjuntas: `2 failed, 96 passed in 10.51s` e `2 failed, 115 passed in 9.92s`. As contagens incluem testes existentes e não representam uma execução única; não somar os totais.
- Ambiente: Python 3.14.7 e PostgreSQL. Os testes de integração das novas funcionalidades criaram e removeram schemas temporários próprios.
- As duas falhas de regressão já foram reproduzidas sem o registro do cardápio. Não foram corrigidas nesta entrega. A execução da suíte completa também apresentou falhas de autenticação.
- Não foi medido percentual de cobertura. Os resultados não comprovam deploy, integração com telas, login real pelo navegador ou aplicação de migrações no banco compartilhado.
- Referências: [PR #19](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/19), [PR #21](https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/21) e [relatório individual](sprint-3-contribuicao-Marcelo-Augusto-Oliveira-Jose.md).
