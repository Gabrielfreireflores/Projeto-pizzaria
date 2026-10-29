SET client_encoding = 'UTF8';
BEGIN;

-- Alvos por nome/tamanho, incluindo a grafia legada com encoding corrompido.
DO $$
DECLARE
  produtos_legados integer[];
  pedidos_afetados integer[];
BEGIN
SELECT array_agg(id_produto) INTO produtos_legados FROM produto
WHERE (nome, tamanho) IN (('Pizza de Muçarela', 'Grande'),
                         ('Refrigerante', '2 litros'))
   OR (nome = convert_from(convert_to('Pizza de Muçarela', 'UTF8'), 'LATIN1')
       AND tamanho = 'Grande');
SELECT array_agg(DISTINCT id_pedido) INTO pedidos_afetados FROM item_pedido
WHERE id_produto = ANY(produtos_legados);

DELETE FROM item_pedido_borda
WHERE id_item_pedido IN (SELECT id_item_pedido FROM item_pedido
                        WHERE id_produto = ANY(produtos_legados));
DELETE FROM item_pedido WHERE id_produto = ANY(produtos_legados);
DELETE FROM pedido
WHERE id_pedido = ANY(pedidos_afetados)
  AND NOT EXISTS (SELECT 1 FROM item_pedido i WHERE i.id_pedido = pedido.id_pedido);
DELETE FROM produto WHERE id_produto = ANY(produtos_legados);
DELETE FROM categoria WHERE nome = 'Pizzas'
  AND NOT EXISTS (SELECT 1 FROM produto p WHERE p.id_categoria = categoria.id_categoria);

END $$;

COMMIT;
