---
sidebar_label: "Requisitos Funcionais"
sidebar_position: 1
---

# Requisitos Funcionais

Os requisitos funcionais detalham as funcionalidades específicas que o sistema deve executar para atender às necessidades do negócio.

---

### Análise Base do Sistema

Este grupo de requisitos constitui o núcleo analítico do sistema, automatizando os cálculos fundamentais de gestão de estoque. Sua implementação visa reduzir drasticamente o tempo de análise e automatizar a gestão de estoque com base em regras parametrizáveis diretamente aos objetivos de diminuir o tempo de análise ([OE01](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE1))  
e automatizar cálculos de reposição ([OE05](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE5)).

O **RF01** está relacionado ao **[OE05](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE5)** e o **RF02** está relacionado ao **[OE03](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE3)**.

**RF01 - Analisar período de estoque (CORE)**  

> **Descrição**: O sistema deve calcular automaticamente o período de estoque (em meses) para cada produto inserido nas tabelas, considerando:  
> - Estoque atual  
> - Produtos em consignação  
> - Pedidos pendentes de entrega  
> - Média de saída dos últimos 4 meses (configurável)  
>
> **Objetivo Específico (OE) Relacionado:** [OE05](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE5)  
>
> **Critérios de aceitação**:
> - O sistema deve calcular o período de estoque baseado na fórmula: (Estoque Total / Média de Saída)
> - Permitir configurar período de análise (3, 4, 5 meses, etc.)
> - Através de um botão o sistema atualiza os dados automaticamente a última versão do arquivo de dados


---

**RF02 - Integrar os dados das 4 planilhas principais**  

> **Descrição**: O sistema deve importar e centralizar dados de múltiplas fontes:
> - Base de dados de faturamento (relatório 14)
> - Planilha de estoque atual
> - Planilha de pedidos pendentes ("pedido fora")
> - Planilha de produtos consignados  
>
> **Objetivo Específico (OE) Relacionado:** [OE03](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE3)  
>
> **Critérios de aceitação**:
> - O sistema possui compatibilidade com as planilhas Excel
> - Através de um botão o sistema atualiza os dados automaticamente quando as planilhas forem modificadas

---

### Consultas Diretas

Este grupo de requisitos está conectado ao ([OE04](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE4)), na funcionalidade que permite ao usuário consultar seus produtos através de diferentes chaves de pesquisa.

**RF03 - Consultar Produto por código original do produto**

> **Critérios de aceitação:**
> - Consulta utiliza o código original do produto para listar o produto  
>
> **Objetivo Específico (OE) Relacionado:** [OE04](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE4) 

**RF04 - Consultar Produto pela linha do produto (prioritário)**  

> **Critérios de aceitação:**
> - Consulta que utiliza a linha do produto escolhida pelo usuário para listar  
>
> **Objetivo Específico (OE) Relacionado:** [OE04](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE4)

**RF05 - Consultar produto por status (ativo, parado, etc.) (prioritário)**  

> **Critérios de aceitação:**
> - Consulta que utiliza o status parado dos produtos para listar para o usuario produtos que estão sem movimentação de vendas há pelo menos 6 meses
  
> **Objetivo Específico (OE) Relacionado:** [OE04](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE4)  

**RF06 - Consultar por período de estoque específico (por X quantidade de meses)**  

> **Critérios de aceitação:**
> - Consulta que utiliza o período do estoque escolhido pelo usuário para listar  
>
> **Objetivo Específico (OE) Relacionado:** [OE04](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE4)  

---

### Análises Avançadas

Indo além da análise básica, estes requisitos fornecem inteligência de negócio acionável, como sugestões de compra e análise de desempenho. Eles contribuem diretamente para prover insights estratégicos por cliente e vendedor, e apoiar a tomada de decisão baseada em dados, realizando os objetivos de oferecer visão analítica do histórico por cliente ([OE09](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE9)) e automatizar sugestões de compra ([OE05](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE5)).

**RF07 - Sugerir compras inteligentes**

> **Descrição**: O sistema deve gerar sugestões automáticas de compra baseadas na análise de estoque.  
>
> **Objetivo Específico (OE) Relacionado:** [OE05](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE5)  
>
> **Critérios de aceitação**:
> - Calcular quantidade sugerida para atingir meta de estoque
> - Considerar unidades por caixa na sugestão
> - Calcular valor total da compra sugerida
> - Destacar na interface produtos críticos (estoque zerado ou muito baixo)

**RF08 - Consultar principais clientes de cada produto**

> **Descrição**: O sistema deve listar os principais clientes de cada produto (quais clientes compram mais quais produtos).  
>
> **Objetivo Específico (OE) Relacionado:** [OE09](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE9) 
>
> **Critérios de aceitação:**
> - Consultar os 5 clientes mais frequentes do produto  
> - Mostrar média de compra mensal por cliente

**RF09 - Consultar histórico de compras por cliente**

> **Descrição**: O sistema deve listar o histórico de compras de cada cliente.  
>
> **Objetivo Específico (OE) Relacionado:** [OE09](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE9)  
>
> **Critérios de aceitação:**
> - Consultar o histórico das últimas 10 compras por cliente

**RF10 - Consultar performance por vendedor**

> **Descrição**: O sistema deve listar os vendedores em relação a quem mais vende.  
>
> **Objetivo Específico (OE) Relacionado:** [OE09](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE9)  
>
> **Critérios de aceitação:**
> - Consultar os 5 vendedores que mais venderam no último mês

**RF11 - Consultar padrões de compra e sazonalidade**

> **Descrição**: O sistema deve listar os padrões de compra dos clientes e a sazonalidade das compras, ou seja, quais meses vendem mais e quais clientes são recorrentes.  
>
> **Objetivo Específico (OE) Relacionado:** [OE09](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE9) 
>
> **Critérios de aceitação:**
> - Consultar quais meses há maior volume de compras nos últimos 4 meses e quais os clientes que mais compraram em cada mês.

---

### Notificação sobre produtos em estado crítico

Estes requisitos implementam um sistema de alertas proativo para mitigar riscos operacionais.  
Eles são fundamentais para notificar proativamente sobre situações críticas e melhorar a confiabilidade e redução de riscos, viabilizados pelos objetivos de notificar sobre produtos parados ([OE08](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE8)) e permitir a visualização rápida de produtos abaixo do estoque mínimo ([OE06](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE6)).

**RF12 - Notificar produtos com baixa saída**

> **Critérios de aceitação:**
> - O sistema deve destacar na interface produtos com média de saída do estoque abaixo de 3 meses
> - O sistema deve criar notificação para o usuário mostrando quais produtos possuem média de saída do estoque abaixo de 3 meses  
>
> **Objetivo Específico (OE) Relacionado:** [OE08](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE8)  

**RF13 - Notificar produtos que estão com estoque crítico**

> **Critérios de aceitação:**
> - O sistema deve destacar na interface produtos que possuem menos de 1 mês de fornecimento para o estoque
> - O sistema deve criar notificação para o usuário mostrando quais produtos possuem menos de 1 mês de fornecimento para o estoque  
>
> **Objetivo Específico (OE) Relacionado:** [OE08](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE8)  

**RF14 - Notificar produtos zerados no estoque**

> **Critérios de aceitação:**
> - O sistema deve destacar na interface produtos que estão zerados no estoque
> - O sistema deve criar notificação para o usuário mostrando quais produtos estão zerados no estoque  
>
> **Objetivo Específico (OE) Relacionado:** [OE08](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE8) 

---

### Autorização de Acesso

Este grupo assegura a proteção dos dados sensíveis do negócio, um pilar crítico da solução.  
Ele materializa o objetivo de garantir segurança e controle de acesso ([OE07](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE7)).

**RF15 - Autenticar o usuário**

> **Descrição**: O sistema deve realizar uma autenticação com um sistema de login para permitir acesso somente com as credenciais aceitas.  
>
> **Objetivo Específico (OE) Relacionado:** [OE07](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE7)  
>
> **Critérios de aceitação:**
> - O sistema deve permitir acesso ao sistema ao usuário que inseriu as credenciais de usuário e senha válidos (que tem cadastro de permissão no sistema)
> - O sistema deve negar acesso ao sistema ao usuário que inseriu credenciais inválidas (sem permissão)
> - O sistema ao negar o acesso de um usuário deve exibir de forma visual o acesso negado

**RF16 - Permitir mudança de senha**

> **Descrição**: O sistema deve permitir o usuário mudar a senha de acesso ao sistema.  
>
> **Objetivo Específico (OE) Relacionado:** [OE07](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE7) 
>
> **Critérios de aceitação:**
> - O sistema deve enviar um e-mail seguro para redefinição de senha para o e-mail do cliente
> - O sistema deve atualizar a senha do usuário no sistema
> - O sistema deve permitir acesso com a nova senha criada

---

### Tabela de Requisitos Funcionais  

| ID    | Nome                                       |
|-------|--------------------------------------------|
| RF01  | Analisar Período de Estoque                |
| RF02  | Integrar os Dados das 4 Planilhas          |
| RF03  | Consultar Produto por Código               |
| RF04  | Consultar Produto pela Linha               |
| RF05  | Consultar Produto por Status               |
| RF06  | Consultar por Período de Estoque           |
| RF07  | Sugerir Compras Inteligentes               |
| RF08  | Consultar Principais Clientes do Produto   |
| RF09  | Consultar Histórico de Compras por Cliente |
| RF10  | Consultar Performance por Vendedor         |
| RF11  | Consultar Padrões de Compra e Sazonalidade |
| RF12  | Notificar Produtos com Baixa Saída         |
| RF13  | Notificar Produtos com Estoque Crítico     |
| RF14  | Notificar Produtos Zerados                 |
| RF15  | Autenticar o Usuário                       |
| RF16  | Permitir Mudança de Senha                  |
