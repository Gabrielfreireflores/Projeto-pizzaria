## 🔐 Autenticação/Usuário - Cliente / Funcionário

## Atualização: cliente, acompanhamento e bordas

Aplicar as migrations 001–006 em ordem após `db/schema.sql`, sempre em UTF-8.
A migration 005 cria `item_pedido_borda`, relacionando a borda ao item de pizza,
sem remover produtos ou alterar itens de pedidos antigos. A 006 desativa somente
o produto cujo nome é exatamente `Refrigerante` (ignorando caixa e espaços externos).
O produto e suas referências no histórico permanecem no banco.

### Cadastro e consulta do cliente

`POST /api/v1/clientes` recebe `nome` (nome e sobrenome, até 120 caracteres),
`email` (formato válido, até 160 caracteres, trim e minúsculas), `telefone`
(celular obrigatório, de 10 a 15 dígitos; aceita `+ ( ) . -` e espaços, até 20
caracteres no total) e `senha` (texto não vazio, mantendo a regra existente).
São exatamente quatro campos no formulário; não há confirmação de senha ou endereço.
O campo `cpf`, se enviado, é ignorado. Novos clientes são gravados com CPF NULL;
CPFs existentes e sua restrição de unicidade são preservados. Aplicar também
`db/migrations/005_cliente_cpf_opcional.sql` antes de cadastrar clientes.
O CPF do funcionário e o cliente técnico Convidado não são alterados.
E-mail duplicado retorna 400 com `{"erro": "Usuário já cadastrado com este e-mail."}`.
Falhas internas retornam 503 sem expor SQL. A senha continua armazenada com hash.
Após criar a conta, o formulário faz `POST /api/v1/login` e abre `/meus-pedidos`,
mantendo o comportamento anterior. A resposta 201 mantém `cliente.cpf: null`
por compatibilidade com o formato existente.

`GET /api/v1/meus-pedidos` exige sessão de cliente ativo. Retorna uma lista no
formato da listagem de pedidos, filtrada no SQL pelo cliente associado à sessão.
Não aceita um identificador de cliente enviado pelo navegador como autorização.
Sem sessão retorna 401; funcionário ou cliente inativo recebe 403. A tela consulta
a cada 15 segundos enquanto visível e permite filtrar pelo número do pedido.

Pedidos continuam disponíveis sem login. O contato exige nome e sobrenome e
telefone. Endereço é obrigatório para entrega; retirada dispensa endereço e taxa.
Pedidos de convidado permanecem no cliente técnico e não são transferidos
automaticamente para contas criadas depois.

### Pizza com borda

Cada item de `POST /api/v1/pedidos` pode incluir:

```json
{
  "id_produto": 10,
  "quantidade": 2,
  "observacao": "Borda: Catupiry",
  "bordas": [{"id_produto": 70, "quantidade": 2}]
}
```

Os IDs são ilustrativos. O produto principal deve ser de `Pizzas Salgadas` ou
`Pizzas Doces`; a borda deve estar disponível, pertencer a `Bordas` e ter o mesmo
tamanho. A soma das quantidades das bordas não pode exceder a quantidade de pizzas.
Não se repete o mesmo produto de borda dentro de um item. Linhas de carrinho que
cobram o mesmo produto principal continuam agrupadas, com quantidades e observações
das escolhas preservadas.

Preços de pizza e borda vêm do banco e são gravados como retrato no pedido.
O total inclui pizza, bordas e taxa de entrega. `item_pedido` mantém o subtotal
da pizza; `item_pedido_borda` mantém preço, quantidade e subtotal de cada borda,
com chaves estrangeiras para o item principal e o produto. A listagem devolve
`bordas` dentro de cada item. Itens, bordas, endereço e pedido usam a mesma transação.

---

### 1. Auto-cadastro de Cliente
Cria um novo usuário com o perfil padrão de cliente.

* **URL:** `/auth/api/cadastro/cliente`
* **Método:** `POST`
* **Autenticação:** Nenhuma (Rota pública)

#### Corpo da Requisição (Request Body)
```json
{
  "email": "cliente@email.com",
  "senha": "senhaSegura123"
}

201 CREATED
{
  "mensagem": "Usuário do perfil 'perfil_padrao' cadastrado com sucesso.",
  "usuario": {
    "id": 12,
    "email": "cliente@email.com"
  }
}
400 BAD REQUEST
{
  "erro": "Usuário já cadastrado com este e-mail."
}

----------------------------------------------------------------------------------

### 2. Cadastro de Funcionário
Cria um novo usuário com o perfil padrão de funcionário.

* **URL:** `/auth/api/cadastro/funcionario`
* **Método:** `POST`
* **Autenticação:** ADICIONAR AUTENTICACAO - ROTA NAO DEVE SER PUBLICA

#### Corpo da Requisição (Request Body)
```json
{
  "email": "cliente@email.com",
  "senha": "senhaSegura123"
}

201 CREATED
{
  "mensagem": "Usuário do perfil 'perfil_padrao' cadastrado com sucesso.",
  "usuario": {
    "id": 12,
    "email": "cliente@email.com"
  }
}


## 🔐 Categoria
### 1. Criação de categoria
Cria uma nova categoria.

* **URL:** `api/categorias`
* **Método:** `POST`
* **Autenticação:** ADICIONAR AUTENTICACAO - ROTA NAO DEVE SER PUBLICA

#### Corpo da Requisição (Request Body)
```json
{
  "nome": "pizzas"
}

201 CREATED
{
  "mensagem": "Categoria '{nome}' criada com sucesso.",
  "categoria": {
    "id_categoria": 12,
    "nome": "pizzas"
  }
}

----------------------------------------------------------------------------------

### 2. Listar as categorias
Listagem de categoria.

* **URL:** `api/categorias`
* **Método:** `GET`
* **Autenticação:** ADICIONAR AUTENTICACAO - ROTA NAO DEVE SER PUBLICA

200 OK
{
    "categorias": [
        [
            1,
            "pizza"
        ],

        [  
            2,
            "bebidas"
        ]
    ]
}

