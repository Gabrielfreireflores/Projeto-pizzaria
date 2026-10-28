-- Mantém o produto e suas referências em pedidos antigos.
SET client_encoding = 'UTF8';
BEGIN;
UPDATE produto SET disponivel = FALSE
WHERE lower(trim(nome)) = 'refrigerante';
COMMIT;
