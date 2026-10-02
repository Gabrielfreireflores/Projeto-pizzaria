# H03-05 — Contrato da API de Produto

Versão documentada: 02/10/2026. Contrato conferido com routes, controllers,
services e schema da branch `feature/consulta-produtos-criacao-pedidos`.

Este documento define o que o frontend envia e o que recebe. Os exemplos são
ilustrativos: IDs devem corresponder aos registros do banco utilizado.

## 1. Endpoints e autenticação

Base local: `http://127.0.0.1:5000`.

| Método | Endpoint recomendado | Finalidade | Acesso |
|---|---|---|---|
| POST | `/api/v1/produtos` | Cadastrar produto e sua receita | Funcionário ativo autenticado |
| GET | `/api/v1/produtos` | Listar produtos | Público |

Os caminhos `/produtos` e `/api/produtos` são aliases para os mesmos métodos,
corpos e respostas. Utilizar `/api/v1/produtos` nas novas integrações.

No POST, enviar `Content-Type: application/json`. A autenticação utiliza cookie
de sessão Flask assinado, contendo `id_usuario`. Não enviar usuário/perfil no
JSON para tentar autenticar; não existe suporte a Bearer token nestas rotas.
O backend exige usuário ativo, perfil funcionario/Funcionário e registro
correspondente na tabela funcionario.

A criação da sessão depende da implementação do login. Na versão documentada,
o PR #11 ainda não fornece o fluxo HTTP completo de login/sessão. Sem uma sessão
válida, o POST retorna 401 mesmo que o JSON esteja correto. O frontend deverá
reutilizar o cookie fornecido pelo login; CORS e envio de cookies entre origens
devem ser configurados na integração, pois não foram implementados neste cartão.

## 2. Request de criação

`POST /api/v1/produtos`

```json
{
  "nome": "Pizza de Calabresa",
  "tamanho": "Grande",
  "preco": "49.90",
  "id_categoria": 1,
  "disponivel": true,
  "ingredientes": [
    {"id_ingrediente": 1, "quantidade_necessaria": "1.000"},
    {"id_ingrediente": 2, "quantidade_necessaria": "0.200"}
  ]
}
```

| Campo | Tipo JSON | Obrigatório | Regra |
|---|---|---|---|
| `nome` | string | Sim | Não vazio após remover espaços nas extremidades; até 120 caracteres |
| `tamanho` | string | Sim | Não vazio após remover espaços nas extremidades; até 30 caracteres |
| `preco` | string decimal ou number | Sim | De 0 a 99999999.99, representável com até 2 casas decimais |
| `id_categoria` | integer | Sim | De 1 a 2147483647; categoria deve existir |
| `disponivel` | boolean | Não | Padrão true; enviar true/false, sem aspas |
| `ingredientes` | array de objetos | Sim | Pelo menos um objeto; não repetir id_ingrediente |
| `ingredientes[].id_ingrediente` | integer | Sim | De 1 a 2147483647; ingrediente deve existir |
| `ingredientes[].quantidade_necessaria` | string decimal ou number | Sim | Maior que zero, até 999999999.999, representável com até 3 casas decimais |

Recomenda-se enviar decimais como strings com ponto, conforme o exemplo, para
preservar precisão. Vírgula decimal, NaN, Infinity e booleanos não são aceitos
como números. IDs não aceitam strings (`"1"`), booleanos ou números fracionários.
Preço zero é permitido. Zeros decimais extras que não alteram o valor são
normalizados: `"49.900"` pode ser representado e retornado como `"49.90"`.

`id_produto` é gerado pelo banco e não deve ser enviado. Campos não reconhecidos
são ignorados pela implementação atual; não são persistidos. Não existem campos
de foto ou descrição neste contrato. Nome e tamanho são normalizados apenas
com remoção de espaços nas extremidades, sem conversão para minúsculas.

## 3. Formato da categoria e dos ingredientes

### No cadastro

A categoria é uma referência simples: `"id_categoria": 1`. Não enviar um objeto
categoria nem seu nome. O endpoint não cria categorias automaticamente.

Cada ingrediente é referenciado pelo ID, junto à quantidade usada na receita:

```json
{"id_ingrediente": 3, "quantidade_necessaria": "0.350"}
```

A unidade é a que já está cadastrada no ingrediente. Por exemplo, `0.350` para
um ingrediente cuja unidade seja `kg` significa 0,350 kg. Não enviar nomes como
`["calabresa", "muçarela"]`; não enviar unidade para alterar o ingrediente.
Este endpoint não cria ingredientes nem desconta estoque.

### Na consulta

A categoria e os ingredientes são expandidos com seus dados descritivos:

```json
{
  "categoria": {"id_categoria": 1, "nome": "Pizzas"},
  "ingredientes": [
    {
      "id_ingrediente": 3,
      "nome": "Muçarela",
      "quantidade_necessaria": "0.350",
      "unidade_medida": "kg"
    }
  ]
}
```

## 4. Response de criação

Sucesso: **201 Created**, corpo JSON com o produto criado diretamente, sem
envelope `produto` ou `produtos`:

```json
{
  "id_produto": 3,
  "nome": "Pizza de Calabresa",
  "tamanho": "Grande",
  "preco": "49.90",
  "id_categoria": 1,
  "disponivel": true,
  "ingredientes": [
    {"id_ingrediente": 1, "quantidade_necessaria": "1.000"},
    {"id_ingrediente": 2, "quantidade_necessaria": "0.200"}
  ]
}
```

- IDs são inteiros; disponibilidade é booleano.
- Preço retorna como string com 2 casas; quantidade como string com 3 casas.
- O retorno do POST não contém os nomes da categoria/ingredientes nem unidades.
  Para obtê-los, usar a consulta GET.
- Produto e associações são salvos em uma transação. Uma falha desfaz o cadastro.
- Mesmo nome e tamanho já cadastrados retornam 409. Tamanhos diferentes permitem
  produtos com o mesmo nome.

## 5. Consulta

`GET /api/v1/produtos` não recebe corpo nem exige sessão. Não há parâmetros
implementados para paginação, pesquisa, filtro ou ordenação personalizada.

Sucesso: **200 OK**.

```json
{
  "produtos": [
    {
      "id_produto": 1,
      "nome": "Pizza de Muçarela",
      "tamanho": "Grande",
      "preco": "49.90",
      "disponivel": true,
      "categoria": {"id_categoria": 1, "nome": "Pizzas"},
      "ingredientes": [
        {
          "id_ingrediente": 3,
          "nome": "Muçarela",
          "quantidade_necessaria": "0.350",
          "unidade_medida": "kg"
        }
      ]
    },
    {
      "id_produto": 2,
      "nome": "Refrigerante",
      "tamanho": "2 litros",
      "preco": "12.00",
      "disponivel": false,
      "categoria": {"id_categoria": 2, "nome": "Bebidas"},
      "ingredientes": []
    }
  ]
}
```

Catálogo vazio também retorna 200:

```json
{"produtos": []}
```

Produtos são ordenados por id_produto crescente; ingredientes, por id_ingrediente
crescente. Cada produto aparece uma vez. A lista inclui produtos indisponíveis:
`disponivel` reflete a flag do banco, sem calcular estoque de ingredientes.
Produtos legados sem receita podem retornar `ingredientes: []`, embora o POST
exija pelo menos um ingrediente em novos cadastros.

Não existe, nesta entrega, `GET /produtos/{id}`, edição ou exclusão de produtos.

## 6. Erros

Erros tratados pelos controllers retornam um objeto com uma mensagem em `erro`:

```json
{"erro": "Informe ao menos um ingrediente."}
```

| HTTP | Operação | Situação / mensagem |
|---|---|---|
| 400 | POST | JSON malformado ou tipo de conteúdo inadequado: `Envie um objeto JSON válido.` |
| 400 | POST | Corpo é lista, texto ou null: `Envie um objeto JSON.` |
| 400 | POST | Campos inválidos; ver mensagens abaixo |
| 400 | POST | `Categoria ou ingrediente inexistente.` |
| 401 | POST | `Autenticação necessária.` |
| 403 | POST | `Acesso exclusivo de funcionário ativo.` |
| 409 | POST | `Já existe produto com esse nome e tamanho.` |
| 503 | POST | `Não foi possível cadastrar o produto.` |
| 503 | GET | `Não foi possível listar os produtos.` |

### Mensagens de validação

| Campo/caso | Mensagem |
|---|---|
| Nome ausente, vazio ou longo | `nome é obrigatório e deve ter até 120 caracteres.` |
| Tamanho ausente, vazio ou longo | `tamanho é obrigatório e deve ter até 30 caracteres.` |
| Categoria inválida | `id_categoria deve ser um inteiro positivo válido.` |
| ID de ingrediente inválido | `id_ingrediente deve ser um inteiro positivo válido.` |
| Lista ausente/vazia ou de tipo incorreto | `Informe ao menos um ingrediente.` |
| Item que não é objeto | `Cada ingrediente deve ser um objeto.` |
| Ingrediente repetido | `Não repita ingredientes no mesmo produto.` |
| Disponibilidade não booleana | `disponivel deve ser booleano.` |
| Preço ausente/formato inválido | `preco deve ser um número válido.` |
| Preço negativo, não finito ou acima do limite | `preco está fora do intervalo permitido.` |
| Preço com precisão excessiva | `preco deve ter no máximo 2 casas decimais.` |
| Quantidade ausente/formato inválido | `quantidade_necessaria deve ser um número válido.` |
| Quantidade zero | `quantidade_necessaria deve ser maior que zero.` |
| Quantidade negativa, não finita ou acima do limite | `quantidade_necessaria está fora do intervalo permitido.` |
| Quantidade com precisão excessiva | `quantidade_necessaria deve ter no máximo 3 casas decimais.` |

O backend retorna a primeira falha encontrada, não uma lista de erros por campo.
Sem sessão, 401 vem antes da leitura do JSON. Após validar o formato JSON, a
permissão do funcionário é verificada antes das validações de campos. Uma falha
de banco nessa etapa pode retornar 503 antes da validação do formulário.
Não assumir que respostas padrão do Flask para rota inexistente/método não
permitido (404/405) possuem esse mesmo envelope JSON.

## 7. Como conferir no Postman

1. Crie a variável `base_url` com `http://127.0.0.1:5000`.
2. Crie uma requisição GET para `{{base_url}}/api/v1/produtos`, sem body.
3. Crie uma requisição POST para a mesma URL; selecione Body → raw → JSON e
   cole o exemplo da seção 2, usando IDs existentes.
4. Para sucesso no POST, será necessário o cookie de uma sessão de funcionário
   criada pelo futuro login. Sem ele, o resultado esperado atualmente é 401.
5. Depois da integração do login, confira 201 para cadastro válido, 409 ao
   repetir nome/tamanho e 400 para preço negativo ou ingredientes vazios.

Os testes automatizados usam o cliente Flask e simulam uma sessão assinada para
validar os cenários autenticados. Não existe endpoint para liberar autenticação
artificialmente no Postman.

## 8. Critérios do cartão

- Request de criação: seção 2.
- Response: seção 4.
- Consulta: seção 5.
- Formato dos ingredientes: seção 3.
- Formato da categoria: seção 3.
- Erros de validação: seção 6.

Fontes: `backend/app/routes/produto_routes.py`,
`backend/app/controllers/produto_controller.py`,
`backend/app/services/produto_services.py`,
`backend/app/schemas/produto_schema.py` e
`backend/app/repositories/produto_repository.py`.
