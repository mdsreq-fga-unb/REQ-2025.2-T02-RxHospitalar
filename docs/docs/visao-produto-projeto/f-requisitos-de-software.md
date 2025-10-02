---
sidebar_label: "Requisitos de software"
sidebar_position: 6
---

# Requisitos de software do produto

Esta seção descreve os requisitos necessários para o desenvolvimento do software. Ela está dividida em requisitos funcionais e não funcionais, que apresentam as funcionalidades do sistema e as qualidades que ele deve possuir para atender às expectativas dos usuários. 

## 7.1 Requisitos Funcionais
Os requisitos funcionais detalham as funcionalidades específicas que o sistema deve executar para atender às necessidades do negócio.
### **7.1.1 Análise Base do Sistema**

Este grupo de requisitos constitui o núcleo analítico do sistema, automatizando os cálculos fundamentais de gestão de estoque. Sua implementação visa reduzir drasticamente o tempo de análise ([OG1](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OG1)) e automatizar a gestão de estoque com base em regras parametrizáveis ([OG3](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OG3)), atendendo diretamente aos objetivos de diminuir o tempo de análise ([OE01](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE1)) e automatizar cálculos de reposição ([OE05](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE5)).

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

Estes requisitos garantem que os usuários possam explorar os dados centralizados de forma rápida e eficiente. Eles são essenciais para oferecer uma interface intuitiva e acessível ([OG4](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OG4)) e prover insights estratégicos ([OG6](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OG6)), permitindo que o usuário filtre e visualize dados em minutos ([OE04](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE4)) e acesse uma visão analítica do histórico ([OE09](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE9)).

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

Indo além da análise básica, estes requisitos fornecem inteligência de negócio acionável, como sugestões de compra e análise de desempenho. Eles contribuem diretamente para prover insights estratégicos por cliente e vendedor ([OG6](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OG6)) e apoiar a tomada de decisão baseada em dados, realizando os objetivos de oferecer visão analítica do histórico por cliente ([OE09](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE9)) e automatizar sugestões de reposição ([OE05](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE5)).

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

Estes requisitos implementam um sistema de alertas proativo para mitigar riscos operacionais. Eles são fundamentais para notificar proativamente sobre situações críticas ([OG7](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OG7)) e melhorar a confiabilidade e redução de riscos (Impacto 2), viabilizados pelos objetivos de notificar sobre produtos parados ([OE08](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE8)) e permitir a visualização rápida de produtos abaixo do estoque mínimo ([OE06](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE6)).

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

Este grupo assegura a proteção dos dados sensíveis do negócio, um pilar crítico da solução. Ele materializa o objetivo de garantir segurança e controle de acesso ([OG5](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OG5)), atendendo rigorosamente ao objetivo de garantir sigilo e controle de acesso ([OE07](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE7)).

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

## 7.2 Requisitos Não Funcionais

Os requisitos não funcionais especificam os critérios de qualidade do sistema, definindo como ele deve operar em termos de performance, usabilidade, segurança e outras características essenciais.

### 7.2.1 Performance

Esse requisito estabelece tempo de resposta e processamento, garantindo fluidez nas operações. Relaciona-se ao **([OG1](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OG1)) (reduzir tempo de análise)** e ao **([OE01](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE01)) (diminuir em 50% o tempo de análise).**

**RNF01:**

-   **Tempo de Resposta:** Executar a funcionalidade "Análise de Período de Estoque" (RF001). O tempo de resposta, desde o clique até a exibição completa dos resultados na tela, deve ser inferior a 30 segundos.
-   **Tempo de importação:** Realizar o upload de uma planilha .xlsx. O tempo total, desde a submissão do arquivo até a mensagem de conclusão do processamento, deve ser inferior a 10 minutos.
-   **Importação sem quebras:** Após a importação de uma planilha com 1.000 linhas, o número total de registros na tabela de produtos do sistema deve corresponder exatamente ao número de linhas do arquivo original. Uma soma de verificação de uma coluna numérica (ex: quantidade em estoque) no arquivo original deve ser igual à soma da mesma coluna no sistema.

### 7.2.2 Usabilidade

Assegura que a interface seja intuitiva e responsiva (inclusive com modo escuro). Está diretamente ligado ao **([OG4](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OG4)) (oferecer interface intuitiva e acessível)** e ao **([OE02](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE02))/([OE04](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE04)) (interface fácil de usar, filtros dinâmicos e acessíveis em até 5 minutos).**

**RNF02:**

-   **Interface Inclusiva:** A tela principal de análise de dados deve apresentar as informações em um formato que demanda pouco esforço de adaptação para o usuário entender e utilizar o sistema.
-   **Navegação em poucos cliques:** O sistema deve exigir, no máximo, 4 cliques a partir da tela inicial para executar cada tarefa/análise/filtragem.
-   **Reduzir cansaço visual:** O sistema deve possuir uma opção de alternância para um tema "Modo Escuro". Ao ser ativado, o fundo principal da aplicação deve ter uma cor mais escura do que o padrão e os textos devem ter alto contraste.
-   **Adaptação Funcional:** Às adaptações feitas devem propor uma melhor usabilidade, logo o usuário deve realizar um conjunto de fluxos de análise sem treinamento prévio, julgando a facilidade de uso em uma escala de 1 a 5, devendo a nota ser igual ou superior a 4.

### 7.2.3 Compatibilidade

Garante que o sistema seja compatível com planilhas e com o ambiente de uso (Windows). Apoia **([OG2](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OG2)) (centralizar e unificar dados)**, principalmente na integração de fontes conforme **OE03 (centralização das planilhas).**

**RNF03:**

-   **Importação sem quebras:** O sistema deve ser capaz de importar com sucesso um arquivo .xlsx .csv válido, ou outro arquivo de planilhas, e formatado conforme o template esperado.
-   **Recusação de outros arquivos:** Ao tentar importar um arquivo com formato diferente (ex., .txt) ou um .xlsx com colunas faltando, o sistema deve exibir uma mensagem de erro clara ao usuário, sem travar.
-   **Funcionamento sem gargalos no OS do cliente:** O sistema deve ser compatível com o sistema operacional do ambiente onde vai ser utilizado - Windows.

### 7.2.4 Segurança

Reforça a confidencialidade dos dados, backup e restauração, bem como a conformidade com a LGPD. Está totalmente conectado ao **OG5 (garantir segurança e controle de acesso)** e ao **OE07 (sigilo e controle de acesso).**

**RNF04:**

-   **Acesso autorizado:** O sistema deve ter um sistema de autenticação para garantir somente acesso autorizado.
-   **Dados criptografados:** Os arquivos de dados gerados ou utilizados pelo sistema (onde ficam as informações consolidadas de clientes, preços e estoque) devem ser armazenados de forma criptografada. O teste consiste em tentar abrir o arquivo de dados (.db, .dat, .json, etc.) com um editor de texto e verificar que o conteúdo é ilegível (caracteres aleatórios), em vez de texto plano.
-   **Arquivo de Backup:** A aplicação deve ter uma funcionalidade que, quando acionada (ou de forma automática ao fechar), cria uma cópia do arquivo de dados principal em uma pasta de backup pré-definida. O teste consiste em verificar se o arquivo de backup foi criado na pasta correta com um timestamp (data e hora) no nome.
-   **Restauração Local:** O sistema deve ter uma função "Restaurar Backup", que consiste em executar a função de restauração a partir do último backup e verificar se a aplicação volta a funcionar com os dados do momento do backup.
-   **Conformidade com LGPD:** O sistema ao ser acionado para excluir algum dado deve descartar este dado do sistema, garantindo que após apagar os dados, ao buscar por eles a pesquisa não irá encontrar estes dados.

### 7.2.5 Confiabilidade

Garante a estabilidade do sistema em operação sem falhas críticas. Apoia a consecução de **([OG3](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OG3))** e **([OG7](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OG7))**, ao assegurar consistência nas análises e notificações (indiretamente relacionado a OE06 e OE08).

**RNF05:**

-   **Fluidez constante do sistema:** Durante o período de Teste de Aceitação do Usuário (UAT), com duração de 2 dias úteis, o sistema não deve apresentar nenhuma falha que impeça a conclusão das tarefas pelo usuário.

### 7.2.6 Escalabilidade

Estabelece critérios para suportar crescimento de usuários e dados sem perda de desempenho. Relaciona-se a **([OG2](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OG2)) (centralizar dados de forma sustentável)** e **([OG3](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OG3)) (automatizar gestão de estoque).**

**RNF06:**

-   **Estabilidade do sistema:** Com o sistema populado com 1.000 produtos diferentes, os critérios de performance do RNF01 ainda devem ser atendidos.
-   Utilizando uma ferramenta de teste de carga (como o JMeter), simular 5 usuários realizando consultas simultâneas na funcionalidade de filtro. O tempo de resposta médio não deve exceder 15 minutos (uma degradação aceitável em relação ao teste com um único usuário).

### 7.2.7 Manutenibilidade

Define práticas para manter e evoluir o sistema, incluindo revisão de código, testes, documentação e integração de novos requisitos. Apoia transversalmente todos os OGs, especialmente OG2, OG3 e OG5, e conecta-se a OE05/OE07.

**RNF07:**

-   **Incremento de novos Requisitos Funcionais:** Nenhuma nova funcionalidade pode ser integrada ao ramo principal do código sem a aprovação de pelo menos um outro membro da equipe. A revisão deve seguir um checklist que verifica a clareza do código e a existência de comentários em trechos complexos e os testes unitários.
-   **Cobertura de Testes:** Utilizar uma ferramenta de análise de cobertura de testes (ex: coverage.py para Python). A cobertura de testes unitários para os módulos de regras de negócio (cálculos de estoque, sugestões, etc.) deve ser de, no mínimo, 90%.
-   **Revisão Automatizada do código:** Antes de ser aceito no projeto principal, o código deve passar por uma ferramenta de linting, como Pylint, sem apresentar erros.
-   **Documentação da instalação:** O projeto deve apresentar um Readme que seja descritivo e instrutivo para o usuário realizar seus primeiros passos para executar o sistema me muito esforço.
-   **Documentação do Produto:** Para cada funcionalidade deve haver um guia de como o usuário pode executar e identificar os resultados de cada pesquisa feita no sistema. Além de também explicar o conjunto de ferramentas, botões e caminhos obrigatórios que o usuário deve fazer para ter uma boa execução do sistema (relacionado ao RF01).

### 7.2.8 Manter histórico de notificações

Assegura rastreabilidade e auditoria das notificações geradas. Está conectado a **([OG6](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OG6)) (prover insights estratégicos)** e **([OG7](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OG7)) (notificar situações críticas)**, além de reforçar **([OE08](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE08)) (alertas automáticos sobre produtos de baixo giro ou parados).**

**RNF08:**

-   **Descrição:** O sistema deve manter histórico de notificações por 15 dias para análise de rastreabilidade do produto para o cliente dispondo na interface as notificações que foram geradas através dos requisitos da categoria: **Notificação sobre produtos em estado crítico.**
