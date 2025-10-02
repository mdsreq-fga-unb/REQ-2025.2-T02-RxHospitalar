---
sidebar_label: "Requisitos de software"
sidebar_position: 6
---

# Requisitos de software do produto

Esta seção descreve os requisitos necessários para o desenvolvimento do software. Ela está dividida em requisitos funcionais e não funcionais, que apresentam as funcionalidades do sistema e as qualidades que ele deve possuir para atender às expectativas dos usuários. 

## 7.1 Requisitos Funcionais
Os requisitos funcionais detalham as funcionalidades específicas que o sistema deve executar para atender às necessidades do negócio.
### **7.1.1 Análise Base do Sistema**

Este grupo de requisitos constitui o núcleo analítico do sistema, automatizando os cálculos fundamentais de gestão de estoque. Sua implementação visa reduzir drasticamente o tempo de análise ([OG1](https://docs.google.com/document/d/1ObKkLQiQ6n5fSmXcMj0E3VsbUX4fnFBW7WjJGxMA8vg/edit?tab=t.0#bookmark=id.mfwlj63l2hz2)) e automatizar a gestão de estoque com base em regras parametrizáveis ([OG3](https://docs.google.com/document/d/1ObKkLQiQ6n5fSmXcMj0E3VsbUX4fnFBW7WjJGxMA8vg/edit?tab=t.0#bookmark=id.weaxijen9b55)), atendendo diretamente aos objetivos de diminuir o tempo de análise ([OE01](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE1)) e automatizar cálculos de reposição ([OE05](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE5)).

**RF01** - Analisar período de estoque (CORE)

**Descrição**: O sistema deve calcular automaticamente o período de estoque (em meses) para cada

Produto inserido nas tabelas, considerando:

- Estoque atual
- Produtos em consignação
- Pedidos pendentes de entrega
- Média de saída dos últimos 4 meses (configurável)

**Critérios de aceitação**:

- O sistema deve calcular o período de estoque baseado na fórmula: (Estoque Total / Média de Saída)
- Permitir configurar período de análise (3, 4, 5 meses, etc.)
- Destacar na interface produtos com uma cor que deixe evidente os produto que estão com estoque abaixo do limite ideal (4 meses)
- Sugerir quantidade a ser comprada para atingir o estoque ideal

### **7.1.2 Filtros avançados**

Estes requisitos garantem que os usuários possam explorar os dados centralizados de forma rápida e eficiente. Eles são essenciais para oferecer uma interface intuitiva e acessível ([OG4](https://docs.google.com/document/d/1ObKkLQiQ6n5fSmXcMj0E3VsbUX4fnFBW7WjJGxMA8vg/edit?tab=t.0#bookmark=id.9ccn3zvu7c6d)) e prover insights estratégicos ([OG6](https://docs.google.com/document/d/1ObKkLQiQ6n5fSmXcMj0E3VsbUX4fnFBW7WjJGxMA8vg/edit?tab=t.0#bookmark=id.lxzjgld3hly7)), permitindo que o usuário filtre e visualize dados em minutos ([OE04](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE4)) e acesse uma visão analítica do histórico ([OE09](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE9)).

**RF02** - Integrar os dados das 4 planilhas principais

**Descrição**: O sistema deve importar e centralizar dados de múltiplas fontes:

- Base de dados de faturamento (relatório 14)
- Planilha de estoque atual
- Planilha de pedidos pendentes ("pedido fora")
- Planilha de produtos consignados

**Critérios de aceitação**:

- O sistema aceita dados via upload de planilhas Excel
- Através de um botão o sistema atualiza os dados automaticamente quando as planilhas forem carregadas

**RF03** - Filtrar produto por código original do produto

Critérios de aceitação:

- Filtro que utiliza o código original do produto para listar

**RF04** - Filtrar produto pela linha do produto (prioritário)

**Critérios de aceitação**:

- Filtro que utiliza a linha do produto escolhida pelo usuário para listar

**RF05** - Filtrar produto por status (ativo, parado, etc.)  (prioritário)

**Critérios de aceitação**:

- Filtro que utiliza o status dos produtos escolhido pelo usuário para listar

**RF06** - Filtrar por período de estoque (abaixo/acima de X meses)

**Critérios de aceitação**:

- Filtro que utiliza o período do estoque escolhido pelo usuário para listar

**Critérios de aceitação gerais**:

- Interface deve permitir ao usuário aplicar filtros em poucos cliques
- Permitir a aplicação de múltiplos filtros simultaneamente em uma única busca
- Mostrar resultados em tempo real
- Salvar configurações de filtros frequentes

### **7.1.3 Análises Avançadas**

Indo além da análise básica, estes requisitos fornecem inteligência de negócio acionável, como sugestões de compra e análise de desempenho. Eles contribuem diretamente para prover insights estratégicos por cliente e vendedor ([OG6](https://docs.google.com/document/d/1ObKkLQiQ6n5fSmXcMj0E3VsbUX4fnFBW7WjJGxMA8vg/edit?tab=t.0#bookmark=id.lxzjgld3hly7)) e apoiar a tomada de decisão baseada em dados, realizando os objetivos de oferecer visão analítica do histórico por cliente ([OE09](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE9)) e automatizar sugestões de reposição ([OE05](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE5)).

**RF07** - Sugerir compras inteligentes

**Descrição**: O sistema deve gerar sugestões automáticas de compra baseadas na análise de estoque:

**Critérios de aceitação**:

- Calcular quantidade sugerida para atingir meta de estoque
- Considerar unidades por caixa na sugestão
- Calcular valor total da compra sugerida
- Destacar na interface produtos críticos (estoque zerado ou muito baixo)
- Criar uma sugestão de compra para o usuário quando ele destacar uma célula com um produto marcado como crítico

**RF08** - Listar principais clientes de cada produto

**Descrição**: o sistema deve listar os principais clientes de cada produto, ou seja, quais clientes compram mais quais produtos.

**Critérios de aceitação**:

- Listar os 5 clientes mais frequentes do produto

**RF09** - Listar histórico de compras por cliente

**Descrição**: o sistema deve listar o histórico de compras de cada cliente.

**Critérios de aceitação**:

- Listar o histórico das últimas 10 compras por cliente

**RF10** - Listar performance por vendedor

**Descrição**: o sistema deve listar os vendedores em relação a quem mais vende.

**Critérios de aceitação**:

- Listar os 5 vendedores que mais venderam no último mês

**RF11** - Listar padrões de compra e sazonalidade

**Descrição**: o sistema deve listar os padrões de compra dos clientes e a sazonalidade das compras, ou seja, quais meses vendem mais e quais clientes são recorrentes.

**Critérios de aceitação**:

- Listar quais meses há maior volume de compras nos últimos 6 meses e quais os clientes que mais compraram em cada mês.

**Critérios de aceitação gerais**:

- Listar principais clientes por produto
- Mostrar média de compra mensal por cliente
- Identificar clientes que pararam de comprar
- Relatórios de vendas por representante

### **7.1.4 Notificação sobre produtos em estado crítico**

Estes requisitos implementam um sistema de alertas proativo para mitigar riscos operacionais. Eles são fundamentais para notificar proativamente sobre situações críticas ([OG7](https://docs.google.com/document/d/1ObKkLQiQ6n5fSmXcMj0E3VsbUX4fnFBW7WjJGxMA8vg/edit?tab=t.0#bookmark=id.iaaq90w6xtya)) e melhorar a confiabilidade e redução de riscos (Impacto 2), viabilizados pelos objetivos de notificar sobre produtos parados ([OE08](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE8)) e permitir a visualização rápida de produtos abaixo do estoque mínimo ([OE06](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE6)).

**RF12** - Notificar produtos com baixa saída

**Critérios de aceitação**:

- O sistema deve destacar na interface produtos com média de saída do estoque abaixo de 3 meses
- O sistema deve criar notificação para o usuário mostrando quais produtos possuem média de saída do estoque abaixo de 3 meses

**RF13** - Notificar produtos que estão com estoque crítico

**Critérios de aceitação**:

- O sistema deve destacar na interface produtos que possuem menos de 1 mês de fornecimento para o estoque
- O sistema deve criar notificação para o usuário mostrando quais produtos possuem menos de 1 mês de fornecimento para o estoque

**RF14** - Notificar produtos zerados no estoque

**Critérios de aceitação**:

- O sistema deve destacar na interface produtos que estão zerados no estoque
- O sistema deve criar notificação para o usuário mostrando quais produtos estão zerados no estoque.

### **7.1.5 Autorização de Acesso**

Este grupo assegura a proteção dos dados sensíveis do negócio, um pilar crítico da solução. Ele materializa o objetivo de garantir segurança e controle de acesso ([OG5](https://docs.google.com/document/d/1ObKkLQiQ6n5fSmXcMj0E3VsbUX4fnFBW7WjJGxMA8vg/edit?tab=t.0#bookmark=id.bfdm3gcoohe0)), atendendo rigorosamente ao objetivo de garantir sigilo e controle de acesso ([OE07](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE7)).

**RF15** - Permitir somente acesso autorizado

**Descrição**: O sistema deve realizar uma autenticação de login para permitir acesso somente com as informações corretas.

**Critérios de aceitação**:

- Listar os 5 clientes mais frequentes do produto

**RF16** - Permitir mudança de senha

**Descrição**: O sistema deve permitir o usuário mudar a senha de acesso ao sistema

**Critérios de aceitação**:

- O sistema deve enviar um e-mail seguro para redefinição de senha para o e-mail do cliente
- O sistema deve atualizar a senha do usuário nos sistema
- O sistema deve permitir acesso com a nova senha criada

### Análise Base do Sistema

[coming soon]


## Requisitos não Funcionais
