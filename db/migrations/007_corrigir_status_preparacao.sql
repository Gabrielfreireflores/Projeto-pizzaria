SET client_encoding = 'UTF8';
BEGIN;

-- Repara somente o nome com UTF-8 interpretado como Latin-1; preserva a chave.
UPDATE status
SET nome_status = 'Em preparação'
WHERE nome_status = convert_from(convert_to('Em preparação', 'UTF8'), 'LATIN1')
  AND NOT EXISTS (SELECT 1 FROM status WHERE nome_status = 'Em preparação');

COMMIT;
