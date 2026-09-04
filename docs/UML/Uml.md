# Diagramas UML — Pizzaria do Barriga

**Equipe:** Gabriel Freire Flôres (RA 2840482423010) — Marcelo Augusto Oliveira Jose (RA 2840482423043) — Christian de Lima (RA 2840482523031) — Guilherme Fabiano da Silva Gomes (RA 2840482423037)
**Trilha:** B (Cliente real nº 1)



## 1. Diagrama de Casos de Uso

```mermaid
flowchart LR
    Cliente((Cliente))
    Funcionario((Funcionário))

    UC1[Fazer login]
    UC2[Visualizar cardápio]
    UC3[Montar pedido no carrinho]
    UC4[Finalizar pedido]
    UC5[Cadastrar categoria]
    UC6[Cadastrar produto]
    UC7[Visualizar pedidos em tempo real]
    UC8[Aceitar pedido]
    UC9[Acompanhar status do pedido]

    Cliente --> UC1
    Cliente --> UC2
    Cliente --> UC3
    Cliente --> UC4
    Cliente --> UC9

    Funcionario --> UC1
    Funcionario --> UC5
    Funcionario --> UC6
    Funcionario --> UC7
    Funcionario --> UC8

    UC3 -.include.-> UC2
    UC4 -.include.-> UC3
```

## 2. Diagrama de Classes

```mermaid
classDiagram
    class Usuario {
        -id: Integer
        -email: String
        -senha: String
        -nome: String
        -tentativasLoginInvalidas: Integer
        -contaBloqueada: Boolean
        +getId(): Integer
        +getNome(): String
        +alteraSenha(novaSenha: String): void
        +contaTentativasInvalidas(): Integer
        +bloqueiaConta(): void
        +autenticaUsuario(): void
    }

    class Funcionario {
        -id: Integer
    }

    class Cliente {
        -cpf: String
        -telefone: String
        +alteraTelefone(novoTelefone: String): void
    }

    class Produto {
        -id: Integer
        -nome: String
        -preco: decimal
        -ativo: boolean
        +getId(): Integer
        +getNome(): String
        +getPreco(): decimal
        +isAtivo(): boolean
        +alteraPreco(novoPreco: decimal): void
        +ativar(): void
        +desativar(): void
    }

    class Categoria {
        -id: Integer
        -nome: String
        -ativo: boolean
        +getId(): Integer
        +getNome(): String
        +isAtivo(): boolean
        +ativar(): void
        +desativar(): void
    }

    class Ingrediente {
        -id: Integer
        -nome: String
        -disponivel: boolean
        +getId(): Integer
        +getNome(): String
    }

    class Pedido {
        -id: Integer
        -dataHoraPedido: DateTime
        -formaPagamento: String
        -taxaEntrega: decimal
        -valorTotal: decimal
        +getId(): Integer
        +alteraStatus(novoStatus: String)
    }

    class ItemPedido {
        -id: Integer
        -quantidade: Integer
        -precoUnitario: decimal
        -precoTotal: decimal
        -observacao: String
        +calculaTotal(): decimal
        +alterarQuantidade(novaQuantidade: Integer): void
        +exibirObservacao(): String
    }

    class Status {
        -id: Integer
        -descricao: String
        -ordem: Integer
        +getOrdem(): Integer
        +getDescricao(): String
    }

    class Endereco {
        -id: Integer
        -rua: String
        -bairro: String
        -cidade: String
        -cep: String
        -numeroCasa: String
        -referencia: String
        +getId(): Integer
        +exibeEndereco(): String
        +adicionarReferencia(): String
    }

    class IngredienteProduto {
        -id: Integer
        -quantidadeNecessaria: decimal
    }

    Usuario <|-- Funcionario
    Usuario <|-- Cliente

    Categoria "1" --> "0..*" Produto
    Produto "1" --> "0..*" IngredienteProduto
    Ingrediente "1" --> "0..*" IngredienteProduto
    Cliente "1" --> "0..*" Endereco
    Cliente "1" --> "0..*" Pedido
    Funcionario "1" --> "0..*" Pedido
    Pedido "1" --> "1..*" ItemPedido
    Produto "1" --> "0..*" ItemPedido
    Status "1" --> "0..*" Pedido
    Endereco "1" --> "0..*" Pedido
```

## 3. Rastreabilidade

| Caso de uso | História(s) relacionada(s) (E2) |
|---|---|
| Visualizar cardápio | #4 |
| Montar pedido no carrinho | #5 |
| Finalizar pedido | #6 |
