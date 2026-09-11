## 1. Estratégia
|Unitário| Regras de negócio isoladas, como garantir que o preço do produto não seja negativo e o cálculo automático do valor total do carrinho|PyTest|Automaticamente a cada novo commit ou abertura de Pull Request (CI).
|Integração| Validação dos relacionamentos do banco de dados e rotas, como a ligação N:N entre Produto e Ingrediente | PyTest, pytest-flask |  Na esteira de CI/CD, antes da aprovação do Pull Request para a branch principal.
|Manuais| Fluxos completos de usabilidade, como montar o pedido e verificar se o status inicial foi registrado como "Recebido" | Postman, WEB | Ao final de cada Sprint, antes da entrega das histórias (ex: Sprint 1 e 2)

## 2. Critério de bloqueio de merge
O Pull Request será bloqueado e não poderá ser mesclado se:
(a) Falha na esteira: Algum teste automatizado existente quebrar durante a execução.
(b) Falta de cobertura: Novas funcionalidades ou regras de negócio forem enviadas sem a criação dos testes unitários correspondentes.
(c) Falta de revisão (Code Review): Não houver aprovação formal de pelo menos um desenvolvedor da equipe (revisão por pares) validando a lógica.
(d) Falta de contexto: A descrição do PR estiver vazia ou não explicar de forma clara o motivo e o impacto das alterações realizadas.
(e) Débito técnico: O código apresentar problemas de legibilidade, complexidade desnecessária.



## 3. Casos de teste planejados (cresce a cada sprint)

| ID | História (E2) | Cenário | Entrada | Resultado esperado | Prioridade |
|---|---|---|---|---|---|
| CT01 | História 1: Login | Múltiplas tentativas de login com senha incorreta. | E-mail correto e senha incorreta enviada sucessivas vezes. | O sistema deve aplicar o bloqueio após as múltiplas tentativas inválidas. | Alta (Must) |
| CT02 | História 1: Login | Autenticação bem-sucedida de perfis distintos. | E-mail e senha válidos de um Cliente e, posteriormente, de um Funcionário. | Redirecionamento correto para a área correspondente ao perfil logado. | Alta (Must) |
| CT03 | História 2: Categorias | Tentativa de cadastrar categoria duplicada. | Nome de categoria que já consta como cadastrado. | Erro de validação informando que o nome da categoria deve ser único. | Alta (Must) |
| CT04 | História 3: Produtos | Cadastro de produto com valor inválido. | Preenchimento do formulário com o campo de preço contendo o valor "-15.00". | O sistema deve rejeitar o cadastro, visto que o preço não pode ser negativo. | Alta (Must) |
| CT05 | História 5: Carrinho | Inclusão de itens e conferência matemática. | Adição de itens e alteração de quantidade na interface do carrinho. | O sistema permite alterar quantidades e calcula o valor total automaticamente. | Alta (Must) |
| CT06 | História 6: Finalizar pedido | Submissão de pedido sem os dados obrigatórios. | Formulário enviado deixando o campo telefone em branco. | Sistema exibe erro indicando que nome, telefone e endereço são obrigatórios. | Alta (Must) |
