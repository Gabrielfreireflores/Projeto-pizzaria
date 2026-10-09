-- Aplicar após schema.sql, tanto em banco novo quanto existente.
-- Não atribuir funcionário arbitrário antes de o pedido ser aceito.
BEGIN;
ALTER TABLE pedido ALTER COLUMN id_funcionario DROP NOT NULL;
-- Campos opcionais para registros antigos; obrigatórios no service para novos pedidos.
ALTER TABLE pedido ADD COLUMN IF NOT EXISTS nome_contato VARCHAR(120);
ALTER TABLE pedido ADD COLUMN IF NOT EXISTS telefone_contato VARCHAR(20);
INSERT INTO status (nome_status) VALUES ('Recebido')
ON CONFLICT (nome_status) DO NOTHING;
COMMIT;
