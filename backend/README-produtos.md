# História 3 — cadastro de produtos

Implementação alinhada ao merge `83735c0` da história 2. A fábrica em
`app/__init__.py` carrega categorias e produtos. Os módulos de categorias,
`app/database.py` e `run.py` foram preservados.

## Organização

- `app/repositories/produto_repository.py`: SQL parametrizado, conexão com
  `get_connection()`, commit, rollback e fechamento da conexão. Sem decisões
  sobre autorização ou validação de campos.
- `app/services/produto_services.py`: autorização de funcionário ativo,
  chamada das validações e tradução dos conflitos do banco para erros de negócio.
- `app/schemas/produto_schema.py`: funções de validação chamadas pelo serviço.
- `app/routes/produto_routes.py`: Blueprint, leitura de JSON/sessão e respostas HTTP.
- `app/__init__.py`: fábrica compartilhada, configuração e registro dos Blueprints.
- `produtos_app.py`: compatibilidade com o comando de inicialização anterior.

Os nomes de arquivos, imports `from app...`, funções e acesso ao banco seguem
o padrão de categorias. A transação fica no repository, como na história 2;
isso é controle de persistência, não regra de negócio. Produto e ingredientes
são inseridos na mesma transação e uma falha desfaz o cadastro inteiro.

## Executar (PowerShell, a partir da raiz)

Instale as dependências existentes em `backend/requirements-dev.txt` se necessário.
Configure `DATABASE_URL` e uma `SECRET_KEY` privada em `backend/.env` (não versionar).
A conexão usa a mesma variável de ambiente e função da história 2.

```powershell
cd backend
.\.venv\Scripts\python.exe run.py
```

Essa inicialização oferece `/categorias` e `/produtos` na mesma aplicação.
`/api/produtos` continua disponível como compatibilidade com a primeira versão.
O `run.py` carrega as duas funcionalidades pela fábrica compartilhada.
O comando anterior com `--app produtos_app:create_app` também continua válido.

## Cadastro

`POST /produtos`, com JSON:

```json
{
  "nome": "Pizza de Calabresa",
  "tamanho": "Grande",
  "preco": "54.90",
  "id_categoria": 1,
  "ingredientes": [
    {"id_ingrediente": 1, "quantidade_necessaria": "1.000"},
    {"id_ingrediente": 2, "quantidade_necessaria": "0.200"}
  ]
}
```

Exige sessão assinada com `id_usuario`, fornecida pelo futuro login da história 1.
Não há login nem acesso liberado artificialmente nesta entrega. Usuário precisa
estar ativo, ter perfil funcionario e registro correspondente em funcionario.
Categoria e ingredientes precisam existir. Ingredientes não podem se repetir;
preço aceita zero, mas não negativo; quantidades devem ser positivas. Tamanho
é obrigatório conforme o schema existente. Cadastro não baixa estoque.

Resposta 201: produto com seu id e valores decimais como strings. Falhas retornam
`{"erro": "mensagem"}` com 400 (dados inválidos), 401 (sem sessão), 403 (sem
permissão), 409 (nome/tamanho duplicados) ou 503 (problema de banco).

## Testes (a partir da raiz)

```powershell
.\backend\.venv\Scripts\python.exe -m pytest backend/tests/test_produtos.py -q
```

Sem `TEST_DATABASE_URL`, integração é ignorada. Para executar todos, configure
essa variável com um banco exclusivo de testes PostgreSQL 15+ com permissão
de criar schemas. Os testes criam e removem apenas schemas de nome aleatório.
Não use dados reais. O teste usa monkeypatch para direcionar `DATABASE_URL`
ao schema temporário e restaura a variável ao finalizar.

Pendências: implementar login e frontend. Nenhuma migração foi necessária.
