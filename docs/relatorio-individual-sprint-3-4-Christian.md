# Relatório Individual de Contribuição — Projeto-pizzaria — Christian de Lima

**Sprint:** 1-4 · **RA:** 2840482523031
**Papel nesta sprint:** Atuação em frontend e integração

## 1. O que fiz

| Item | Branch/PR | Status |
|---|---|---|
| Frontend em Next.js (App Router, TypeScript, Tailwind) na pasta `frontend/src/app/(interno)` | `feature/login-frontend` | Funcionando |
| Login integrado entre frontend e backend (conta de cliente e de funcionário) | `feature/login-frontend` | Funcionando |
| CRUD de equipe (funcionários), com cadastro dos membros que acessam os pedidos | `feature/equipe-e-autenticacao` | Integrado e funcionando |
| Área do funcionário: cadastro de produtos com ingredientes, edição e exclusão | `feature/equipe-e-autenticacao` | Funcionando |
| Tela de pedidos do funcionário com atualização de status | `feature/login-frontend` | Funcionando |

**Decisões de projeto na área do funcionário:**

- A foto do produto é enviada por upload de arquivo escolhido no computador.
- A bebida é cadastrada só com tamanho e preço, sem ingredientes.
- Pizza e sobremesa exibem os ingredientes.

## 2. Rituais que participei

- [ ] Dailies/weeklies ([x] de [y])
- [ ] Sprint Review
- [ ] Retrospectiva
- [X] Trelo

## 3. PRs de colegas que revisei

| PR | Autor | Comentário resumido |
|---|---|---|
|integracao/login-frontend| Gabriel Freire | Avaliei o código da integração com a parte de crientes |
|fix/validacao-integracao-pedidos| Gabriel Freire | Avaliei quais erros estavam acontecendo e o que foi feito para acertá-los |

## 4. Dificuldades e o que aprendi

- **Conexão com o banco:** Tive problemas para conectar a aplicação ao PostgreSQL local. Rodei o script, mas precisava configurar o `psql` na minha máquina para criar o banco de dados do projeto. Aprendi que o banco precisa existir antes de a aplicação conectar pelo `DATABASE_URL` e que o ambiente local (como o `psql`) deve estar configurado antes de rodar os scripts do projeto.
- **Trabalho em grupo no Git:** trabalhei em branches separadas, sem enviar para a `main` antes da hora, e precisei trazer as atualizações do colega para minha branch (30/10). Aprendi que isolar o trabalho em branches evita quebrar a `main` e que sincronizar a minha branch com as mudanças do grupo com frequência reduz conflitos na hora do merge.
