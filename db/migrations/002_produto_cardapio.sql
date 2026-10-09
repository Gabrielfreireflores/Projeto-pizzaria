-- Executar após schema.sql em instalações novas, ou no banco existente.
-- Campos opcionais preservam a compatibilidade com o cadastro de produtos.
BEGIN;
ALTER TABLE produto ADD COLUMN IF NOT EXISTS foto TEXT;
ALTER TABLE produto ADD COLUMN IF NOT EXISTS descricao TEXT;
COMMIT;
