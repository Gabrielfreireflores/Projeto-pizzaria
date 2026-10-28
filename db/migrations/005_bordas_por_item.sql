-- Aplicar após as migrations 001 a 004. Preserva produtos e pedidos existentes.
SET client_encoding = 'UTF8';
BEGIN;
CREATE TABLE IF NOT EXISTS item_pedido_borda (
  id_item_pedido INT NOT NULL REFERENCES item_pedido(id_item_pedido),
  id_produto INT NOT NULL REFERENCES produto(id_produto),
  quantidade INT NOT NULL CHECK (quantidade > 0),
  preco_unitario NUMERIC(10,2) NOT NULL CHECK (preco_unitario >= 0),
  subtotal NUMERIC(12,2) NOT NULL CHECK (subtotal >= 0),
  PRIMARY KEY (id_item_pedido, id_produto)
);
COMMIT;
