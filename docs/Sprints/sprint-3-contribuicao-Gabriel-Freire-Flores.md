# Relatório Individual de Contribuição — Sprint 3

**Trilha:** B (Cliente real nº 1)

## Identificação do integrante

- **Nome:** Gabriel Freire Flôres
- **RA:** 2840482423010
- **Papel na Sprint 3:** Frontend do cliente (cardápio, carrinho, checkout e pedido).
- **Papéis anteriores:** Product Owner (Sprint 1); design, marca e front do cliente (Sprint 2).

## Atividades realizadas

### Análise e correção
- Levantamento do estado do frontend contra o escopo (histórias #1, #4, #5 e #6), com lista de problemas e próximas etapas por prioridade.
- Correção de regressão após o merge da PR #10: o `carrinho/page.tsx` estava idêntico ao `checkout/page.tsx` e a tela real do carrinho havia sido perdida. A tela foi restaurada (itens, quantidades, remoção, esvaziar sacola, total e acesso ao checkout).

### Cardápio v2 (história #4)
- Substituição dos dados mock pelo Cardápio v2 oficial da pizzaria (PDF): 31 pizzas salgadas, 5 pizzas doces, 4 bordas e 5 refrigerantes (45 itens), com ingredientes e preços P e G conforme o PDF.
- Estrutura única de dados (`MenuItem`): id por categoria, preços por tamanho e preço único para bebidas, reaproveitada pelos cards e pela seção do cardápio.
- Card com imagem, nome, ingredientes, seletor de tamanho (P e G, com os dois preços visíveis) e botão de adicionar ao pedido.
- Apresentação em categorias (Pizzas Salgadas, Pizzas Doces, Bordas e Bebidas) com faixa de atalhos, priorizando o uso no celular.
- Imagem padrão "Foto em breve" para os itens sem foto (9 dos 45 itens têm foto: 4 pizzas e os 5 refrigerantes; as fotos das demais dependem da pizzaria).

### Personalização do pedido
- Pizza meio a meio (dois sabores da mesma categoria), cobrada pelo preço da metade mais cara (regra de negócio).
- Campo de observação por item (por exemplo, retirar ingredientes). A mesma pizza com observações diferentes fica em linhas separadas na sacola.

### Checkout e pedido (história #6)
- Simplificação do formulário: nome, telefone, rua e número, bairro e forma de pagamento (removidos CEP, UF, cidade e complemento).
- Opção Entrega (somente em Jardinópolis, regra da empresa, com taxa a consultar) ou Retirada.
- Criação do pedido com número, data e status inicial `recebido`, por meio de `services/orders.ts` (localStorage), em formato preparado para o backend (`menuItemId`, `size`, `halfMenuItemId`, `note`, `fulfillment`).
- Confirmação na tela com o número do pedido.

### Manutenção e entrega
- Correção dos links da navbar, que não redirecionavam à home a partir do carrinho e do checkout.
- Atualização para Next.js 16.3.4 e React 19, em commit separado do cardápio.
- Validação por verificação de tipos, `npm run build`, teste manual do fluxo e conferência do pedido gravado no navegador.
- Cuidado no versionamento: apenas arquivos do frontend no commit do cardápio, sem arquivos de ambiente (`backend/.env.example`).
- Elaboração deste relatório e dos acréscimos nos documentos em grupo da Sprint 3.

## Funcionalidades/artefatos produzidos

- Dados e regras do cardápio (`frontend/src/lib/data/products.ts`) e tipos (`frontend/src/types/product.ts`, `frontend/src/types/order.ts`).
- Componentes `product-card.tsx`, `menu-section.tsx` e `navbar.tsx` (`frontend/src/components/shared/`).
- Telas de carrinho e checkout (`frontend/src/app/(publico)/carrinho/page.tsx` e `checkout/page.tsx`).
- Camada de pedidos (`frontend/src/services/orders.ts`).
- Imagem padrão (`frontend/public/produtos/sem-foto.svg`).
- Atualização de dependências (`frontend/package.json` e `package-lock.json`).

## Entregas realizadas

- Jornada de compra do cliente atualizada: Cardápio v2 → sacola → checkout (Entrega ou Retirada) → pedido criado com status `recebido` → confirmação.
- Formato de pedido pronto para integração com o backend.
- Sem integração com backend ou banco de dados: o pedido é gravado apenas no navegador.

## Participação na Sprint

Participação comprovada na implementação técnica do frontend do cliente, em contato e conversas com os demais integrantes da equipe.

## Commits relacionados

Branch `feat/cardapio-v2-pedido`:

- "feat(cliente): cardápio v2, meio a meio, observação, checkout simplificado, retirada e pedido" (`d962689`).
- "chore(deps): atualiza Next.js para 16.3.4 e React para 19" (`f9e9faa`).

## Pull Requests relacionadas

- PR do frontend (branch `feat/cardapio-v2-pedido`): **[INFORMAÇÃO NECESSÁRIA]** quanto ao número e à situação (aberta ou mesclada).
- Dependências do backend (autoria de Marcelo Augusto Oliveira Jose): PR #19 (cardápio) e PR #21 (acompanhamento do pedido). A integração com o frontend está pendente.

## Evidências das atividades

<img width="1908" height="916" alt="image" src="https://github.com/user-attachments/assets/888260d6-1076-44b9-a6c0-d38518e47685" /> — Cardápio v2 no navegador (de preferência na versão celular), mostrando as categorias, o seletor de tamanho P/G e o botão Meio a meio.

<img width="1199" height="597" alt="image" src="https://github.com/user-attachments/assets/8cf32123-e657-469d-a97a-d91a7bf77e94" />
<img width="297" height="542" alt="image" src="https://github.com/user-attachments/assets/5f089993-a990-48e3-8231-a203a176c938" />
<img width="1390" height="770" alt="Captura de tela 2026-10-09 230238" src="https://github.com/user-attachments/assets/a237ba71-33cf-4400-9380-cba47b2ec604" />
<img width="1225" height="646" alt="image" src="https://github.com/user-attachments/assets/72c3acbd-31db-4fd4-95f8-de718828f240" />
— Sacola e checkout: item com observação, opção Entrega/Retirada e a tela de confirmação com o número do pedido.

<img width="1171" height="865" alt="Captura de tela 2026-10-04 140632" src="https://github.com/user-attachments/assets/60d0269e-8434-476b-aa4e-8943afecde3c" /> — DevTools (Application → Local Storage → `pizzaria-orders`) com um pedido de teste, mostrando `status`, `fulfillment`, `items` com `menuItemId`, `size` e `halfMenuItemId`.

<img width="1389" height="725" alt="Captura de tela 2026-10-09 224653" src="https://github.com/user-attachments/assets/12758bbb-a634-4d49-a45b-6abea6a00998" /> — Terminal com `npm run build` aprovado e `git log --oneline` mostrando os commits `d962689` e `f9e9faa`.

## Pendências e dependências

- **Fotos do cardápio:** dependem da pizzaria; 36 dos 45 itens (pizzas, doces e bordas) ainda usam a imagem padrão.
- **Login com perfil e proteção de rota (história #1):** pendente. Pode ser simulado no frontend, mas a autenticação real depende do backend.
- **Acompanhamento do pedido (história #9):** pendente no frontend; depende do endpoint (PR #21) e da definição da estimativa de entrega.
- **Integração com o backend:** consumir `GET /api/v1/cardapio` (mapeando tamanhos P e G) e enviar o pedido. É preciso verificar se o contrato de criação de pedido comporta meio a meio, observação e retirada.
- **Nomenclatura de status:** o frontend usa `recebido`, `em_preparo`, `pronto` e `entregue`; o backend registra "Recebido" e "Em preparação"; a fila do funcionário usa "Em produção", "Pronto" e "Entregue". É necessário alinhar um fluxo único.
- **Qualidade:** o script `next lint` foi removido no Next 16 e há vulnerabilidades no `npm audit`; tratar em PR separada.

## Observações

- Nesta sprint não houve testes automatizados no frontend; a validação foi por build e por teste manual (relato próprio, com as evidências acima).
- O pedido criado no checkout é gravado no localStorage do navegador. Não há persistência em banco nem envio ao backend nesta entrega.
