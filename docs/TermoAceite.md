# Termo de Aceite do Projeto — Pizzaria do Barriga

**Equipe:** Gabriel Freire Flôres (RA 2840482423010) — Marcelo Augusto Oliveira Jose (RA 2840482423043) — Christian de Lima (RA 2840482523031) — Guilherme Fabiano da Silva Gomes (RA 2840482423037)
**Trilha:** B (Cliente real nº 1)
**Data:** 28/08/2026

## 1. Escopo aceito para o semestre (funcionalidades Must + Should)
1. Login e autenticação de Funcionário 
2. Cadastro de categorias de produtos
3. Cadastro de produtos vinculados a categoria e ingredientes (relacionamento N:N)
4. Visualização do cardápio pelo cliente (produtos disponíveis, por categoria)
5. Montagem de pedido pelo cliente (carrinho com cálculo automático de total)
6. Finalização de pedido pelo cliente com dados de contato/entrega
7. Visualização de pedidos em tempo real pelo funcionário
8. Atualização de status ao receber o pedido pelo funcionário (Recebido → Em preparo)
9. Acompanhamento do status do pedido pelo cliente (Recebido -> Em preparo + estimativa de entrega)

## 2. Critérios de pronto do MVP
- [ ] Cliente consegue visualizar o cardápio e finalizar um pedido sem intervenção de atendente
- [ ] Pedido finalizado pelo cliente aparece automaticamente para o funcionário, sem transcrição manual
- [ ] Funcionário consegue atualizar o status do pedido e o cliente vê essa mudança refletida
- [ ] Autenticação distingue corretamente os perfis Funcionário e Cliente, restringindo acesso conforme permissão
- [ ] Sistema WEB publicado em URL pública, acessível a partir de qualquer dispositivo (responsivo)
- [ ] Repositório Git com README atualizado, refletindo o estado do MVP

## 3. Stack tecnológica definida
| Camada | Tecnologia |
|---|---|
| Frontend | Next.js + TypeScript + Tailwind + shadcn/ui |
| Backend | Python + Flask |
| Banco de dados | PostgreSQL |
| Deploy | Vercel |

## 4. Papéis iniciais da equipe (Sprint 1)
| Integrante | Papel |
|---|---|
| Gabriel Freire Flôres (RA 2840482423010) | Product Owner |
| Marcelo Augusto Oliveira Jose (RA 2840482423043) | Dados |
| Christian de Lima (RA 2840482523031) | Desenvolvedor Frontend |
| Guilherme Fabiano da Silva Gomes (RA 2840482423037) | Dados |

## 5. Aprovação
- Professor: _______________________ Data: ___/___/____