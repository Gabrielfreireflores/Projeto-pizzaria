## 🔐 Autenticação/Usuário - Cliente / Funcionário

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

