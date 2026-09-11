-- pizzaria.sql — Pizzaria 
-- PostgreSQL 15+. 
--
-- Integrantes:
-- Marcelo Augusto Oliveira Jose — RA: 2840482423043
-- Christian de Lima — RA: 2840482523031
-- Guilherme Fabiano da Silva Gomes — RA: 2840482423037
-- Gabriel Freire Flores — RA: 2840482423010

CREATE TABLE usuario (
  id_usuario SERIAL PRIMARY KEY,
  email VARCHAR(160) NOT NULL UNIQUE,
  senha VARCHAR(255) NOT NULL,
  ativo BOOLEAN NOT NULL DEFAULT TRUE,
  nome_perfil VARCHAR(80) NOT NULL,
  descricao VARCHAR(500)
);

CREATE TABLE categoria (
  id_categoria SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL UNIQUE,
  descricao VARCHAR(500)
);

CREATE TABLE ingrediente (
  id_ingrediente SERIAL PRIMARY KEY,
  nome VARCHAR(120) NOT NULL UNIQUE,
  quantidade_estoque NUMERIC(12,3) NOT NULL DEFAULT 0,
  unidade_medida VARCHAR(20) NOT NULL,
  CONSTRAINT ck_ingrediente_quantidade_estoque
    CHECK (quantidade_estoque >= 0)
);

CREATE TABLE status (
  id_status SERIAL PRIMARY KEY,
  nome_status VARCHAR(50) NOT NULL UNIQUE
);


CREATE TABLE funcionario (
  id_funcionario SERIAL PRIMARY KEY,
  id_usuario INT NOT NULL UNIQUE
    REFERENCES usuario(id_usuario) ON DELETE CASCADE,
  nome VARCHAR(120) NOT NULL,
  cpf VARCHAR(14) NOT NULL UNIQUE,
  cargo VARCHAR(80) NOT NULL,
  telefone VARCHAR(20)
);

CREATE TABLE cliente (
  id_cliente SERIAL PRIMARY KEY,
  id_usuario INT NOT NULL UNIQUE
    REFERENCES usuario(id_usuario) ON DELETE CASCADE,
  nome VARCHAR(120) NOT NULL,
  cpf VARCHAR(14) NOT NULL UNIQUE,
  telefone VARCHAR(20)
);


CREATE TABLE endereco (
  id_endereco SERIAL PRIMARY KEY,
  id_cliente INT NOT NULL
    REFERENCES cliente(id_cliente) ON DELETE CASCADE,
  cep VARCHAR(9) NOT NULL,
  logradouro VARCHAR(160) NOT NULL,
  numero VARCHAR(20) NOT NULL,
  complemento VARCHAR(100),
  bairro VARCHAR(100) NOT NULL,
  cidade VARCHAR(100) NOT NULL,
  uf CHAR(2) NOT NULL,
  CONSTRAINT ck_endereco_uf CHECK (uf = UPPER(uf))
);

CREATE TABLE produto (
  id_produto SERIAL PRIMARY KEY,
  id_categoria INT NOT NULL
    REFERENCES categoria(id_categoria),
  nome VARCHAR(120) NOT NULL,
  tamanho VARCHAR(30) NOT NULL,
  preco NUMERIC(10,2) NOT NULL,
  disponivel BOOLEAN NOT NULL DEFAULT TRUE,
  CONSTRAINT uq_produto_nome_tamanho UNIQUE (nome, tamanho),
  CONSTRAINT ck_produto_preco CHECK (preco >= 0)
);

CREATE TABLE ingrediente_produto (
  id_ingrediente_produto SERIAL PRIMARY KEY,
  id_produto INT NOT NULL
    REFERENCES produto(id_produto) ON DELETE CASCADE,
  id_ingrediente INT NOT NULL
    REFERENCES ingrediente(id_ingrediente),
  quantidade_necessaria NUMERIC(12,3) NOT NULL,
  CONSTRAINT uq_ingrediente_produto UNIQUE (id_produto, id_ingrediente),
  CONSTRAINT ck_ingrediente_produto_quantidade
    CHECK (quantidade_necessaria > 0)
);

CREATE TABLE pedido (
  id_pedido SERIAL PRIMARY KEY,
  id_cliente INT NOT NULL
    REFERENCES cliente(id_cliente),
  id_funcionario INT NOT NULL
    REFERENCES funcionario(id_funcionario),
  id_status INT NOT NULL
    REFERENCES status(id_status),
  id_endereco INT NOT NULL
    REFERENCES endereco(id_endereco),
  data_hora_pedido TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  forma_pagamento VARCHAR(40) NOT NULL,
  taxa_entrega NUMERIC(10,2) NOT NULL DEFAULT 0,
  valor_total NUMERIC(12,2) NOT NULL,
  CONSTRAINT ck_pedido_taxa_entrega CHECK (taxa_entrega >= 0),
  CONSTRAINT ck_pedido_valor_total CHECK (valor_total >= 0)
);

CREATE TABLE item_pedido (
  id_item_pedido SERIAL PRIMARY KEY,
  id_pedido INT NOT NULL
    REFERENCES pedido(id_pedido) ON DELETE CASCADE,
  id_produto INT NOT NULL
    REFERENCES produto(id_produto),
  quantidade INT NOT NULL,
  preco_unitario NUMERIC(10,2) NOT NULL,
  subtotal NUMERIC(12,2) NOT NULL,
  observacao VARCHAR(500),
  CONSTRAINT uq_item_pedido_produto UNIQUE (id_pedido, id_produto),
  CONSTRAINT ck_item_pedido_quantidade CHECK (quantidade > 0),
  CONSTRAINT ck_item_pedido_preco_unitario CHECK (preco_unitario >= 0),
  CONSTRAINT ck_item_pedido_subtotal CHECK (subtotal >= 0)
);

CREATE INDEX idx_endereco_id_cliente
  ON endereco(id_cliente);
CREATE INDEX idx_produto_id_categoria
  ON produto(id_categoria);
CREATE INDEX idx_ingrediente_produto_id_ingrediente
  ON ingrediente_produto(id_ingrediente);
CREATE INDEX idx_pedido_id_cliente
  ON pedido(id_cliente);
CREATE INDEX idx_pedido_id_funcionario
  ON pedido(id_funcionario);
CREATE INDEX idx_pedido_id_status
  ON pedido(id_status);
CREATE INDEX idx_pedido_id_endereco
  ON pedido(id_endereco);
CREATE INDEX idx_item_pedido_id_produto
  ON item_pedido(id_produto);


INSERT INTO usuario (email, senha, ativo, nome_perfil, descricao) VALUES
  ('cliente.exemplo@email.com', '$2b$10$hash_de_exemplo_cliente', TRUE,
   'cliente', 'Usuário cliente criado pelo seed'),
  ('funcionario.exemplo@email.com', '$2b$10$hash_de_exemplo_funcionario', TRUE,
   'funcionario', 'Usuário funcionário criado pelo seed');

INSERT INTO cliente (id_usuario, nome, cpf, telefone)
SELECT id_usuario, 'Ana Souza', '123.456.789-00', '(16) 99999-0001'
FROM usuario
WHERE email = 'cliente.exemplo@email.com';

INSERT INTO funcionario (id_usuario, nome, cpf, cargo, telefone)
SELECT id_usuario, 'Bruno Lima', '987.654.321-00', 'Atendente', '(16) 99999-0002'
FROM usuario
WHERE email = 'funcionario.exemplo@email.com';

INSERT INTO endereco
  (id_cliente, cep, logradouro, numero, complemento, bairro, cidade, uf)
SELECT id_cliente, '14150-000', 'Rua das Flores', '100', 'Casa',
       'Centro', 'Serrana', 'SP'
FROM cliente
WHERE cpf = '123.456.789-00';

INSERT INTO categoria (nome, descricao) VALUES
  ('Pizzas', 'Pizzas disponíveis no cardápio'),
  ('Bebidas', 'Bebidas disponíveis no cardápio');

INSERT INTO produto (id_categoria, nome, tamanho, preco, disponivel)
SELECT id_categoria, 'Pizza de Muçarela', 'Grande', 49.90, TRUE
FROM categoria
WHERE nome = 'Pizzas';

INSERT INTO produto (id_categoria, nome, tamanho, preco, disponivel)
SELECT id_categoria, 'Refrigerante', '2 litros', 12.00, TRUE
FROM categoria
WHERE nome = 'Bebidas';

INSERT INTO ingrediente (nome, quantidade_estoque, unidade_medida) VALUES
  ('Massa de pizza', 20.000, 'unidade'),
  ('Molho de tomate', 10.000, 'litro'),
  ('Muçarela', 15.000, 'kg');

INSERT INTO ingrediente_produto
  (id_produto, id_ingrediente, quantidade_necessaria)
SELECT p.id_produto, i.id_ingrediente, 1.000
FROM produto p
CROSS JOIN ingrediente i
WHERE p.nome = 'Pizza de Muçarela'
  AND p.tamanho = 'Grande'
  AND i.nome = 'Massa de pizza';

INSERT INTO ingrediente_produto
  (id_produto, id_ingrediente, quantidade_necessaria)
SELECT p.id_produto, i.id_ingrediente, 0.200
FROM produto p
CROSS JOIN ingrediente i
WHERE p.nome = 'Pizza de Muçarela'
  AND p.tamanho = 'Grande'
  AND i.nome = 'Molho de tomate';

INSERT INTO ingrediente_produto
  (id_produto, id_ingrediente, quantidade_necessaria)
SELECT p.id_produto, i.id_ingrediente, 0.350
FROM produto p
CROSS JOIN ingrediente i
WHERE p.nome = 'Pizza de Muçarela'
  AND p.tamanho = 'Grande'
  AND i.nome = 'Muçarela';

INSERT INTO status (nome_status) VALUES
  ('Recebido'),
  ('Em preparação'),
  ('Saiu para entrega'),
  ('Entregue'),
  ('Cancelado');

INSERT INTO pedido
  (id_cliente, id_funcionario, id_status, id_endereco,
   data_hora_pedido, forma_pagamento, taxa_entrega, valor_total)
SELECT c.id_cliente, f.id_funcionario, s.id_status, e.id_endereco,
       CURRENT_TIMESTAMP, 'PIX', 5.00, 66.90
FROM cliente c
CROSS JOIN funcionario f
CROSS JOIN status s
JOIN endereco e ON e.id_cliente = c.id_cliente
WHERE c.cpf = '123.456.789-00'
  AND f.cpf = '987.654.321-00'
  AND s.nome_status = 'Recebido';

INSERT INTO item_pedido
  (id_pedido, id_produto, quantidade, preco_unitario, subtotal, observacao)
SELECT pe.id_pedido, pr.id_produto, 1, 49.90, 49.90, 'Sem azeitonas'
FROM pedido pe
JOIN cliente c ON c.id_cliente = pe.id_cliente
CROSS JOIN produto pr
WHERE c.cpf = '123.456.789-00'
  AND pr.nome = 'Pizza de Muçarela'
  AND pr.tamanho = 'Grande';

INSERT INTO item_pedido
  (id_pedido, id_produto, quantidade, preco_unitario, subtotal, observacao)
SELECT pe.id_pedido, pr.id_produto, 1, 12.00, 12.00, NULL
FROM pedido pe
JOIN cliente c ON c.id_cliente = pe.id_cliente
CROSS JOIN produto pr
WHERE c.cpf = '123.456.789-00'
  AND pr.nome = 'Refrigerante'
  AND pr.tamanho = '2 litros';

COMMIT;
