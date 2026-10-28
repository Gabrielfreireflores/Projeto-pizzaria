SET client_encoding = 'UTF8';

BEGIN;
-- Mantém CPFs existentes e a unicidade; novos clientes podem ter CPF NULL.
-- O CPF de funcionario e o cliente técnico Convidado não são alterados.
ALTER TABLE cliente ALTER COLUMN cpf DROP NOT NULL;
COMMIT;
