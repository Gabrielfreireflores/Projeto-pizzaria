-- Aplicar após schema.sql e migrations 001/002 (idempotente).
-- aplicar  SET client_encoding = 'UTF8';
-- Suporta o checkout simplificado do frontend do cliente:
--   * pedido de retirada, sem endereço;
--   * pedido feito sem cadastro/login (cliente técnico "Convidado").

SET client_encoding = 'UTF8';

BEGIN;

ALTER TABLE pedido ALTER COLUMN id_endereco DROP NOT NULL;
ALTER TABLE pedido ADD COLUMN IF NOT EXISTS tipo_entrega VARCHAR(10) NOT NULL DEFAULT 'entrega';

ALTER TABLE pedido DROP CONSTRAINT IF EXISTS ck_pedido_tipo_entrega;
ALTER TABLE pedido ADD CONSTRAINT ck_pedido_tipo_entrega
  CHECK (tipo_entrega IN ('entrega', 'retirada'));

ALTER TABLE pedido DROP CONSTRAINT IF EXISTS ck_pedido_endereco_entrega;
ALTER TABLE pedido ADD CONSTRAINT ck_pedido_endereco_entrega
  CHECK (tipo_entrega = 'retirada' OR id_endereco IS NOT NULL);

-- Conta técnica dona dos pedidos feitos sem login. A senha '!' não é um hash
-- válido, então ninguém consegue autenticar com ela. O nome e o telefone reais
-- de cada pedido ficam em pedido.nome_contato / pedido.telefone_contato.
INSERT INTO usuario (email, senha, ativo, nome_perfil, descricao)
VALUES ('convidado@pizzariadobarriga.local', '!', TRUE, 'cliente',
        'Conta técnica para pedidos sem cadastro (não faz login)')
ON CONFLICT (email) DO NOTHING;

INSERT INTO cliente (id_usuario, nome, cpf, telefone)
SELECT id_usuario, 'Cliente Convidado', '000.000.000-00', NULL
FROM usuario
WHERE email = 'convidado@pizzariadobarriga.local'
ON CONFLICT DO NOTHING;

COMMIT;
