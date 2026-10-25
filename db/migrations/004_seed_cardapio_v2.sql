-- Cardápio v2 (gerado a partir de frontend/src/lib/data/products.ts).
-- Aplicar após as migrations 002 e 003. Idempotente: reexecutar atualiza preço/descrição.
-- Aplicar SET client_encoding = 'UTF8';
-- Convenções lidas pelo frontend (frontend/src/services/menu.ts):
--   * categorias: 'Pizzas Salgadas', 'Pizzas Doces', 'Bordas', 'Bebidas';
--   * tamanhos: 'Pequena' (P) e 'Grande' (G); bebidas usam 'Único';
--   * bordas se chamam 'Borda <sabor>' (o nome da pizza pode repetir, ex.: Mussarela).

SET client_encoding = 'UTF8';

BEGIN;

INSERT INTO categoria (nome, descricao) VALUES
  ('Pizzas Salgadas', 'Pizzas salgadas'),
  ('Pizzas Doces', 'Pizzas doces'),
  ('Bordas', 'Bordas recheadas'),
  ('Bebidas', 'Bebidas')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO produto (id_categoria, nome, tamanho, preco, disponivel, descricao)
SELECT c.id_categoria, v.nome, v.tamanho, v.preco, TRUE, v.descricao
FROM (VALUES
  ('Pizzas Salgadas', 'Mussarela', 'Pequena', 30.00, 'mussarela, tomate'),
  ('Pizzas Salgadas', 'Mussarela', 'Grande', 45.00, 'mussarela, tomate'),
  ('Pizzas Salgadas', 'Calabresa', 'Pequena', 30.00, 'cebola, calabresa, mussarela, tomate'),
  ('Pizzas Salgadas', 'Calabresa', 'Grande', 45.00, 'cebola, calabresa, mussarela, tomate'),
  ('Pizzas Salgadas', 'Bauru', 'Pequena', 30.00, 'presunto, mussarela, tomate'),
  ('Pizzas Salgadas', 'Bauru', 'Grande', 45.00, 'presunto, mussarela, tomate'),
  ('Pizzas Salgadas', 'Marguerita', 'Pequena', 30.00, 'mussarela, parmesão, manjericão, tomate'),
  ('Pizzas Salgadas', 'Marguerita', 'Grande', 45.00, 'mussarela, parmesão, manjericão, tomate'),
  ('Pizzas Salgadas', 'Milho', 'Pequena', 30.00, 'mussarela, milho, tomate'),
  ('Pizzas Salgadas', 'Milho', 'Grande', 45.00, 'mussarela, milho, tomate'),
  ('Pizzas Salgadas', 'Milho c/ Catupiry', 'Pequena', 35.00, 'mussarela, milho, catupiry'),
  ('Pizzas Salgadas', 'Milho c/ Catupiry', 'Grande', 50.00, 'mussarela, milho, catupiry'),
  ('Pizzas Salgadas', 'Frango c/ Catupiry', 'Pequena', 35.00, 'frango, mussarela, catupiry'),
  ('Pizzas Salgadas', 'Frango c/ Catupiry', 'Grande', 50.00, 'frango, mussarela, catupiry'),
  ('Pizzas Salgadas', 'Caipira', 'Pequena', 35.00, 'mussarela, frango, milho, catupiry'),
  ('Pizzas Salgadas', 'Caipira', 'Grande', 50.00, 'mussarela, frango, milho, catupiry'),
  ('Pizzas Salgadas', 'Americana', 'Pequena', 35.00, 'frango, bacon, mussarela, cheddar'),
  ('Pizzas Salgadas', 'Americana', 'Grande', 50.00, 'frango, bacon, mussarela, cheddar'),
  ('Pizzas Salgadas', 'Calabresa c/ Catupiry', 'Pequena', 35.00, 'calabresa, mussarela, catupiry'),
  ('Pizzas Salgadas', 'Calabresa c/ Catupiry', 'Grande', 50.00, 'calabresa, mussarela, catupiry'),
  ('Pizzas Salgadas', 'Quatro Queijos', 'Pequena', 35.00, 'mussarela, catupiry, parmesão, provolone'),
  ('Pizzas Salgadas', 'Quatro Queijos', 'Grande', 50.00, 'mussarela, catupiry, parmesão, provolone'),
  ('Pizzas Salgadas', 'Portuguesa', 'Pequena', 35.00, 'presunto, palmito, ervilha, ovo, tomate, cebola, mussarela'),
  ('Pizzas Salgadas', 'Portuguesa', 'Grande', 50.00, 'presunto, palmito, ervilha, ovo, tomate, cebola, mussarela'),
  ('Pizzas Salgadas', 'Paulista', 'Pequena', 35.00, 'presunto, palmito, ervilha, mussarela, cebola, tomate, bacon'),
  ('Pizzas Salgadas', 'Paulista', 'Grande', 50.00, 'presunto, palmito, ervilha, mussarela, cebola, tomate, bacon'),
  ('Pizzas Salgadas', 'Chefinho', 'Pequena', 35.00, 'calabresa, frango, milho, mussarela, catupiry'),
  ('Pizzas Salgadas', 'Chefinho', 'Grande', 50.00, 'calabresa, frango, milho, mussarela, catupiry'),
  ('Pizzas Salgadas', 'Palmito', 'Pequena', 35.00, 'palmito, mussarela, tomate'),
  ('Pizzas Salgadas', 'Palmito', 'Grande', 50.00, 'palmito, mussarela, tomate'),
  ('Pizzas Salgadas', 'Bacon', 'Pequena', 35.00, 'bacon, mussarela, tomate'),
  ('Pizzas Salgadas', 'Bacon', 'Grande', 50.00, 'bacon, mussarela, tomate'),
  ('Pizzas Salgadas', 'Brócolis', 'Pequena', 30.00, 'brócolis, mussarela, cebola, tomate, alho frito'),
  ('Pizzas Salgadas', 'Brócolis', 'Grande', 48.00, 'brócolis, mussarela, cebola, tomate, alho frito'),
  ('Pizzas Salgadas', 'Brócolis c/ Catupiry', 'Pequena', 35.00, 'mussarela, brócolis, catupiry, bacon'),
  ('Pizzas Salgadas', 'Brócolis c/ Catupiry', 'Grande', 50.00, 'mussarela, brócolis, catupiry, bacon'),
  ('Pizzas Salgadas', 'Lombo', 'Pequena', 35.00, 'mussarela, lombo, catupiry'),
  ('Pizzas Salgadas', 'Lombo', 'Grande', 50.00, 'mussarela, lombo, catupiry'),
  ('Pizzas Salgadas', 'Atum', 'Pequena', 30.00, 'mussarela, atum, cebola'),
  ('Pizzas Salgadas', 'Atum', 'Grande', 48.00, 'mussarela, atum, cebola'),
  ('Pizzas Salgadas', 'Mineira', 'Pequena', 35.00, 'presunto, mussarela, milho, catupiry'),
  ('Pizzas Salgadas', 'Mineira', 'Grande', 50.00, 'presunto, mussarela, milho, catupiry'),
  ('Pizzas Salgadas', 'Baiana', 'Pequena', 30.00, 'calabresa, ovo, cebola, pimenta, mussarela'),
  ('Pizzas Salgadas', 'Baiana', 'Grande', 48.00, 'calabresa, ovo, cebola, pimenta, mussarela'),
  ('Pizzas Salgadas', 'Mexicana', 'Pequena', 35.00, 'mussarela, cebola, bacon, alho frito, tomate, parmesão'),
  ('Pizzas Salgadas', 'Mexicana', 'Grande', 50.00, 'mussarela, cebola, bacon, alho frito, tomate, parmesão'),
  ('Pizzas Salgadas', 'Pizzaiolo', 'Pequena', 35.00, 'mussarela, presunto, catupiry, tomate, palmito'),
  ('Pizzas Salgadas', 'Pizzaiolo', 'Grande', 50.00, 'mussarela, presunto, catupiry, tomate, palmito'),
  ('Pizzas Salgadas', 'Frango & Cheddar', 'Pequena', 35.00, 'mussarela, frango, cheddar'),
  ('Pizzas Salgadas', 'Frango & Cheddar', 'Grande', 50.00, 'mussarela, frango, cheddar'),
  ('Pizzas Salgadas', 'À Moda da Casa', 'Pequena', 30.00, 'calabresa, ovo, milho, tomate, mussarela'),
  ('Pizzas Salgadas', 'À Moda da Casa', 'Grande', 48.00, 'calabresa, ovo, milho, tomate, mussarela'),
  ('Pizzas Salgadas', 'Brócolis & Bacon', 'Pequena', 30.00, 'brócolis, mussarela, bacon'),
  ('Pizzas Salgadas', 'Brócolis & Bacon', 'Grande', 48.00, 'brócolis, mussarela, bacon'),
  ('Pizzas Salgadas', 'Toscana c/ Catupiry', 'Pequena', 35.00, 'calabresa moída, catupiry, cebola, mussarela'),
  ('Pizzas Salgadas', 'Toscana c/ Catupiry', 'Grande', 50.00, 'calabresa moída, catupiry, cebola, mussarela'),
  ('Pizzas Salgadas', 'Toscana c/ Cheddar', 'Pequena', 35.00, 'calabresa moída, mussarela, cheddar'),
  ('Pizzas Salgadas', 'Toscana c/ Cheddar', 'Grande', 50.00, 'calabresa moída, mussarela, cheddar'),
  ('Pizzas Salgadas', 'Dois queijos', 'Pequena', 30.00, 'mussarela, catupiry'),
  ('Pizzas Salgadas', 'Dois queijos', 'Grande', 48.00, 'mussarela, catupiry'),
  ('Pizzas Salgadas', 'Calabresa Paulistana', 'Pequena', 30.00, 'calabresa, cebola'),
  ('Pizzas Salgadas', 'Calabresa Paulistana', 'Grande', 45.00, 'calabresa, cebola'),
  ('Pizzas Doces', 'Chocolate', 'Pequena', 30.00, 'chocolate, granulado'),
  ('Pizzas Doces', 'Chocolate', 'Grande', 50.00, 'chocolate, granulado'),
  ('Pizzas Doces', 'Chocolate c/ Morango', 'Pequena', 30.00, 'chocolate, morango, leite condensado'),
  ('Pizzas Doces', 'Chocolate c/ Morango', 'Grande', 50.00, 'chocolate, morango, leite condensado'),
  ('Pizzas Doces', 'Prestígio', 'Pequena', 30.00, 'chocolate, coco ralado, leite condensado'),
  ('Pizzas Doces', 'Prestígio', 'Grande', 50.00, 'chocolate, coco ralado, leite condensado'),
  ('Pizzas Doces', 'Banana', 'Pequena', 30.00, 'banana, canela e leite condensado'),
  ('Pizzas Doces', 'Banana', 'Grande', 45.00, 'banana, canela e leite condensado'),
  ('Pizzas Doces', 'Banana Chok', 'Pequena', 30.00, 'banana e chocolate'),
  ('Pizzas Doces', 'Banana Chok', 'Grande', 50.00, 'banana e chocolate'),
  ('Bordas', 'Borda Catupiry', 'Pequena', 8.00, NULL),
  ('Bordas', 'Borda Catupiry', 'Grande', 15.00, NULL),
  ('Bordas', 'Borda Cheddar', 'Pequena', 8.00, NULL),
  ('Bordas', 'Borda Cheddar', 'Grande', 15.00, NULL),
  ('Bordas', 'Borda Mussarela', 'Pequena', 8.00, NULL),
  ('Bordas', 'Borda Mussarela', 'Grande', 15.00, NULL),
  ('Bordas', 'Borda Chocolate', 'Pequena', 8.00, NULL),
  ('Bordas', 'Borda Chocolate', 'Grande', 15.00, NULL),
  ('Bebidas', 'Coca-Cola 2L', 'Único', 15.00, NULL),
  ('Bebidas', 'Fanta Laranja 2L', 'Único', 13.00, NULL),
  ('Bebidas', 'Sprite Limão 2L', 'Único', 13.00, NULL),
  ('Bebidas', 'Jaboti 2L', 'Único', 8.00, NULL),
  ('Bebidas', 'Coca-Cola Lata 350ml', 'Único', 6.00, NULL)
) AS v(categoria, nome, tamanho, preco, descricao)
JOIN categoria c ON c.nome = v.categoria
ON CONFLICT ON CONSTRAINT uq_produto_nome_tamanho DO UPDATE
  SET preco = EXCLUDED.preco,
      descricao = EXCLUDED.descricao,
      id_categoria = EXCLUDED.id_categoria;

COMMIT;
