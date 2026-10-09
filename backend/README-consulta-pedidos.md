# H03-04, H06-02 e H06-03

Implementação local de consulta de produtos, criação de pedido e status inicial.
Segue o padrão de funções e aliases da história 3 e a separação de controllers
proposta pelo PR #11. Não faz merge do PR nem altera os arquivos de categorias/auth.

## Camadas

- `routes`: registra o endpoint e chama o controller.
- `controllers`: lê JSON/sessão, chama services e traduz erros para HTTP.
- `services`: autorização, validação, preço/total e escolha do status inicial.
- `schemas`: valida e normaliza os dados de entrada.
- `repositories`: SQL parametrizado e gerenciamento de conexão/transação.
- `models/status_pedido.py`: enum dos status existentes no banco.

O cadastro anterior de produtos continua disponível, com o tratamento HTTP
movido de routes para `produto_controller.py`, preservando as respostas.
No `app/__init__.py` só foram acrescentados import e registro de `pedido_bp`.
`database.py`, `run.py` e as funções da história 2 não foram alterados.

## GET /api/v1/produtos

Aliases: `GET /produtos` e `GET /api/produtos`. Consulta pública, sem dados pessoais.
Retorna 200 e `{"produtos": [...]}`; catálogo vazio retorna `{"produtos": []}`.

Exemplo de um produto:

```json
{
  "id_produto": 1,
  "nome": "Pizza de Muçarela",
  "tamanho": "Grande",
  "preco": "49.90",
  "disponivel": true,
  "categoria": {"id_categoria": 1, "nome": "Pizzas"},
  "ingredientes": [
    {"id_ingrediente": 1, "nome": "Massa de pizza", "quantidade_necessaria": "1.000", "unidade_medida": "unidade"}
  ]
}
```

Retorna todos os produtos, inclusive indisponíveis, com a flag armazenada no
modelo. Produto legado sem receita retorna lista de ingredientes vazia. Uma
consulta com JOIN reúne tudo, sem consultar ingredientes separadamente por produto.
Não calcula disponibilidade por estoque; isso pertence à história do cardápio.

## POST /api/v1/pedidos

Exige sessão Flask assinada com `id_usuario` de cliente ativo e um registro na
tabela `cliente` ligado a esse usuário. Não aceita id_cliente do payload como
identidade. É compatível com os perfis `cliente` do seed e `Cliente` do PR #11.

```json
{
  "contato": {"nome": "Ana Souza", "telefone": "(16) 99999-0001"},
  "endereco": {
    "cep": "14150-000",
    "logradouro": "Rua das Flores",
    "numero": "100",
    "complemento": "Casa",
    "bairro": "Centro",
    "cidade": "Serrana",
    "uf": "SP"
  },
  "forma_pagamento": "PIX",
  "itens": [
    {"id_produto": 1, "quantidade": 2, "observacao": "Sem azeitonas"},
    {"id_produto": 2, "quantidade": 1}
  ]
}
```

- Nome, telefone, endereço, forma de pagamento e 1 a 100 itens são obrigatórios.
- Quantidades devem ser inteiros positivos; produtos repetidos são rejeitados.
- Complemento e observação são opcionais. Os limites respeitam as colunas SQL.
- Produtos devem existir e ter `disponivel = true`.
- Preços vêm exclusivamente de `produto.preco`, usando Decimal; totais e preços
  recebidos no payload são ignorados. O backend calcula subtotal e valor_total.
- Taxa de entrega vem de `app.config['TAXA_ENTREGA']`; padrão `0.00`, pois não
  existe tabela de fretes no projeto. Configure-a no servidor quando a equipe
  definir a regra. `taxa_entrega` do payload também é ignorada.
- Status do cliente é ignorado. O serviço sempre usa `StatusPedido.RECEBIDO`,
  busca seu ID pelo nome `Recebido` no banco e responde `status: "RECEBIDO"`.
- O funcionário fica NULL até a aceitação do pedido. Nenhum funcionário é
  selecionado arbitrariamente nem recebido do cliente.
- Nome e telefone são guardados no pedido; um novo endereço é criado e vinculado
  ao cliente para preservar a entrega desse pedido, sem editar endereços antigos.
- Endereço, pedido e itens são gravados na mesma conexão/transação. Uma falha
  desfaz tudo. Produtos são bloqueados para leitura durante a transação para
  evitar alteração concorrente de preço/disponibilidade antes da confirmação.
- Não baixa estoque, cobra pagamento, atribui funcionário ou muda status depois
  do cadastro; essas funcionalidades não fazem parte destes cartões.

Resposta 201 contém id_pedido, id_status, status, data_hora_pedido, contato,
endereco, forma_pagamento, taxa_entrega, valor_total e itens com preços/subtotais.
Decimais são strings JSON. Erros: 400 (payload/produto inválido), 401 (sem sessão),
403 (sem cliente ativo), 503 (banco/configuração indisponível), com `{"erro": "..."}`.

## Migração necessária

Em banco novo, execute `db/schema.sql` primeiro. Em banco existente, não repita
o schema/seed: execute somente a migração abaixo, na raiz do repositório:

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -h localhost -p 5432 -U postgres -d pizzaria -W -v ON_ERROR_STOP=1 -f "db/migrations/001_pedido_contato.sql"
```

A migração permite funcionário ainda não atribuído, adiciona nome_contato e
telefone_contato e garante o status Recebido. É transacional e pode ser reaplicada.
Pedidos anteriores continuam válidos, com contato NULL nos novos campos.
Ela não foi aplicada automaticamente às tabelas atuais; somente a schemas de testes.

## Testes

Na raiz, `python -m pytest backend/tests -q` executa as validações e os testes
HTTP; sem `TEST_DATABASE_URL`, os testes PostgreSQL são ignorados. Para executar
tudo carregando uma conexão explicitamente autorizada de desenvolvimento/testes:

```powershell
.\backend\.venv\Scripts\python.exe -c "import os, pytest; from dotenv import load_dotenv; load_dotenv('backend/.env'); os.environ['TEST_DATABASE_URL'] = os.environ['DATABASE_URL']; raise SystemExit(pytest.main(['backend/tests', '-q', '--tb=short']))"
```

Cada teste de integração usa um schema aleatório, com o schema/seed oficial e
a migração. Remove apenas esse schema ao finalizar. Não imprime credenciais.
A migração é executada duas vezes nos testes para verificar reaplicação.

## Integração com o PR #11

Analisado no commit `ec571278f6f9d421a572fc2b7fbd48562123cb9f` em 02/10/2026.
PR: https://github.com/Gabrielfreireflores/Projeto-pizzaria/pull/11

- As novas rotas usam `app.controllers`, no mesmo formato proposto pelo PR.
- Os perfis Cliente/Funcionário do PR e cliente/funcionario do seed são aceitos
  nas respectivas autorizações, ainda exigindo registro na tabela correspondente.
- O PR cadastra usuario, mas não cria os dados obrigatórios de cliente/funcionario
  nem expõe uma rota de login que preencha `session['id_usuario']`. Esses pontos
  ainda dependem da história 1/onboarding. Não criamos registros com CPF fictício.
- A fábrica continua com a assinatura original `create_app()`. A configuração
  da SECRET_KEY e da sessão deve ser integrada pela história de autenticação.
  Apenas declarar SECRET_KEY no .env não a copia para app.config automaticamente.
  Os testes configuram uma chave exclusiva para testes e simulam a sessão.
- O PR está aberto e informado como não mergeável. Ao resolver `app/__init__.py`,
  manter categoria_bp, produto_bp, pedido_bp e acrescentar auth_bp do PR.
- No diff analisado, `categoria_controller.py` contém `Except` com inicial
  maiúscula; `categoria_routes.py` possui imports/chamadas de controllers
  inconsistentes; `usuario_repository.py` usa a coluna `descricao_perfil`, mas
  o schema atual possui `descricao`. Esses pontos devem ser corrigidos no PR
  pelo responsável antes de testar a aplicação combinada.

Não foi feito merge nem aplicada uma cópia do PR. Os testes locais verificam
compatibilidade de estrutura e perfis, não validam o funcionamento completo do PR.
