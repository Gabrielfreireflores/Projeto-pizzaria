


```mermaid

    USUARIO ||--o| FUNCIONARIO: "é um"
    USUARIO ||--o| CLIENTE: "é um"

    CLIENTE ||--|{ ENDERECO: "cadastra"
    PEDIDO }o--|| ENDERECO: "entregue"
    CLIENTE ||--o{ PEDIDO: "realiza"
    
    FUNCIONARIO ||--o{ PEDIDO: "supervisiona"
    
    STATUS ||--o{ PEDIDO: "classifica"

    CATEGORIA ||--|{ PRODUTO: "pertence a"
    PRODUTO ||--o{ INGREDIENTE_PRODUTO: "composto por"
    INGREDIENTE ||--o{ INGREDIENTE_PRODUTO: "usado em"

    PEDIDO ||--|{ ITEM_PEDIDO: "contém"
    PRODUTO ||--o{ ITEM_PEDIDO: "inserido em"
```    

    USUARIO {
        int id_usuario PK
        string email
        string senha
        boolean ativo
        string nome_perfil
        string descricao
    }
    
    FUNCIONARIO {
        int id_funcionario PK
        int id_usuario FK
        string nome
        string cpf
        string cargo
        string telefone
    }

    CLIENTE {
        int id_cliente PK
        int id_usuario FK
        string nome
        string cpf
        string telefone
    }

    ENDERECO {
        int id_endereco PK
        int id_cliente FK
        string cep
        string logradouro
        string numero
        string complemento
        string bairro
        string cidade
        string uf
    }

    CATEGORIA {
        int id_categoria PK
        string nome
        string descricao
    }
    
    PRODUTO {
        int id_produto PK
        int id_categoria FK
        string nome
        string tamanho
        double preco
        boolean disponivel
    }
    
    INGREDIENTE {
        int id_ingrediente PK
        string nome
        double quantidade_estoque 
        string unidade_medida
    }
    
    INGREDIENTE_PRODUTO {
        int id_ingrediente_produto PK
        int id_produto FK
        int id_ingrediente FK
        double quantidade_necessaria
    }
    
    STATUS {
        int id_status PK
        string nome_status
    }
    
    PEDIDO {
        int id_pedido PK
        int id_cliente FK
        int id_funcionario FK 
        int id_status FK
        int id_endereco FK
        datetime data_hora_pedido
        string forma_pagamento
        double taxa_entrega
        double valor_total
    }
    
    ITEM_PEDIDO {
        int id_item_pedido PK
        int id_pedido FK
        int id_produto FK
        int quantidade
        double preco_unitario
        double subtotal
        string observacao
    }