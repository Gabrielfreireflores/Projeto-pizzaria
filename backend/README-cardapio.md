# Consulta de cardápio — H04-01

`GET /api/v1/cardapio` é público e retorna apenas produtos com `disponivel = TRUE`,
agrupados por categoria. Categorias sem produtos disponíveis são omitidas.
A ordenação é por nome de categoria e de produto, com IDs como desempate.
A disponibilidade usa o cadastro; não calcula estoque de ingredientes.

## Banco de dados

Aplicar `db/migrations/002_produto_cardapio.sql` antes de usar o endpoint.
Para instalação nova, executar primeiro `db/schema.sql`. A migração pode ser
reaplicada e não altera os produtos existentes.

Os novos campos `foto` (URL ou caminho da imagem) e `descricao` são opcionais.
Produtos antigos retornam `null` nesses campos até que sejam preenchidos no banco.
O cadastro atual continua compatível; upload de imagens e edição desses campos
pela API não fazem parte desta consulta. A migração não é aplicada automaticamente.

## Resposta 200

```json
{
  "categorias": [
    {
      "id_categoria": 1,
      "nome": "Pizzas",
      "produtos": [
        {
          "id_produto": 1,
          "nome": "Pizza de Muçarela",
          "tamanho": "Grande",
          "preco": "49.90",
          "foto": "/imagens/mucarela.jpg",
          "descricao": "Pizza com molho de tomate e muçarela"
        }
      ]
    }
  ]
}
```

Preço é uma string decimal com duas casas. Cardápio vazio retorna
`{"categorias": []}` com HTTP 200. Falha de banco ou migração ausente retorna
HTTP 503 com `{"erro": "Não foi possível consultar o cardápio."}`.

## Testes

Na raiz do projeto: `backend\.venv\Scripts\python.exe -m pytest backend/tests/test_cardapio.py -q`.
Para os testes de integração, definir `TEST_DATABASE_URL` com um banco PostgreSQL
onde o usuário possa criar schemas. Os testes criam e removem somente um schema
temporário próprio; não aplicam a migração às tabelas compartilhadas.
