# Acompanhamento de pedido — história 9

## Consulta do cliente

`GET /api/v1/pedidos/{id_pedido}/acompanhamento`

Requer a sessão de login do cliente (`id_usuario`). O ID do pedido é o retornado
pelo POST de criação. Somente o dono, com perfil cliente ativo, pode consultar.
Não enviar ID de usuário ou cliente no corpo: a identidade vem da sessão.

Resposta HTTP 200 (exemplo):

```json
{
  "id_pedido": 1,
  "status": "EM_PREPARACAO",
  "status_descricao": "Em preparação",
  "data_hora_pedido": "2026-10-09T18:00:00+00:00",
  "estimativa_entrega": {
    "prazo_minutos": 60,
    "previsao_entrega": "2026-10-09T19:00:00+00:00",
    "atrasada": false
  },
  "finalizado": false,
  "atualizar_em_segundos": 10
}
```

Estados: `RECEBIDO` (solicitado), `EM_PREPARACAO`, `SAIU_PARA_ENTREGA`,
`ENTREGUE` e `CANCELADO`. Nos dois últimos, `finalizado` é true e
`estimativa_entrega` e `atualizar_em_segundos` são null.

## Estimativa

Configurar `PRAZO_ESTIMADO_ENTREGA_MINUTOS=60` no ambiente ou na configuração
Flask. Aceita inteiro de 1 a 1440 minutos; padrão 60. Trata-se de prazo estimado
total, contado desde a criação, não de tempo restante nem promessa de entrega.
O valor inicial de 60 minutos deve ser alinhado à operação da pizzaria.
A previsão não é deslocada a cada consulta. Quando ultrapassada, `atrasada`
fica true, sem alterar o status. Alterar a configuração recalcula as estimativas
dos pedidos abertos, pois não existe previsão individual persistida nesta entrega.

O schema atual usa timestamp sem fuso. A consulta interpreta a data armazenada
como horário de `America/Sao_Paulo`, seguindo o ambiente local do projeto, e
retorna ISO 8601 com fuso. O servidor PostgreSQL deve gravar os horários locais
nesse mesmo fuso; confirmar essa configuração antes de usar em outro ambiente.

## Atualização automática no frontend

1. Ao finalizar a compra, guardar `id_pedido` da resposta do POST.
2. Consultar este GET com o cookie da sessão (`credentials: 'include'`).
3. Exibir `status_descricao` e a previsão convertida para o horário do cliente.
4. Após cada resposta, agendar a próxima consulta em `atualizar_em_segundos`.
   Usar agendamento após concluir a requisição, evitando consultas sobrepostas.
5. Parar quando `finalizado` for true ou ao sair da tela; cancelar a requisição
   pendente ao desmontar o componente.
6. Em 401 pedir login; em 403/404 interromper. Em 503 ou erro de rede, manter
   o último estado com indicação de falha e tentar novamente com intervalo maior.

Cada GET lê o estado atual no banco e retorna `Cache-Control: no-store`.
Assim, uma mudança feita pelo funcionário aparece na próxima consulta.
Não há WebSocket, SSE, notificações ou tela implementados nesta entrega.
Frontend em origem diferente ainda depende de CORS e cookies configurados pela equipe.

## Erros

| HTTP | Resposta |
|---|---|
| 401 | `{"erro": "Autenticação necessária."}` |
| 403 | `{"erro": "É necessário ter um cadastro de cliente ativo."}` |
| 404 | `{"erro": "Pedido não encontrado."}` — mesmo retorno para pedido de outro cliente |
| 503 | `{"erro": "Não foi possível consultar o pedido."}` |

## Escopo e validação

Sem nova migração. O endpoint não modifica pedidos e não depende do cardápio.
A atualização de status pelo funcionário e suas transições pertencem à história 8.
Os testes simulam essa alteração no banco isolado e verificam a leitura seguinte.

Executar `backend\.venv\Scripts\python.exe -m pytest backend/tests/test_acompanhamento.py -q`
na raiz. Definir `TEST_DATABASE_URL` para testes PostgreSQL: eles criam schemas
temporários próprios e os removem ao terminar, preservando as tabelas existentes.
