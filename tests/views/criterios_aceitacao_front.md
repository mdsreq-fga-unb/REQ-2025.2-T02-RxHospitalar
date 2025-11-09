# Critérios de aceitação dos requisitos funcionais (frontend)

Cada pessoa do front ficará responsável pelos testes de um requisito, de preferência o requisito codificado pela pessoa. Cabe a **toda equipe de testes** verificar se há pelo menos 1 teste específico para **cada um** dos critérios de aceitação propostos.

## MVP

### RF01 - Analisar período de estoque
- Permitir configurar período de análise (3, 4, 5 meses, etc.)
- Sugerir quantidade a ser comprada para atingir o estoque ideal
- Destacar na interface produtos com uma cor que deixe evidente os produto que estão com estoque abaixo do limite ideal (4 meses)

### RF02 - Integrar os dados das 4 planilhas principais
- Através de um botão o sistema atualiza os dados automaticamente quando as planilhas forem modificadas.

### RF03 - Consultar Produto por código original do produto
- Consulta utiliza o código original do produto para listar o produto

### RF04 - Consultar Produto pela linha do produto 
- Consulta que utiliza a linha do produto escolhida pelo usuário para listar

### RF05 - Consultar produto por status 
- Consulta que utiliza o status dos produtos escolhido pelo usuário para listar

### RF06 - Consultar por período de estoque específico
- Consulta que utiliza o período do estoque escolhido pelo usuário para listar

### RF03 - 06 (Gerais)
- Permitir a aplicação de múltiplos filtros simultaneamente em uma única busca
- Mostrar resultados em tempo real
- Salvar configurações de filtros frequentes

### RF07 - Sugerir compras inteligentes
- Criar uma sugestão de compra para o usuário quando ele destacar uma célula com um produto marcado como crítico

### RF08 - Consultar principais clientes de cada produto
- Consultar os 5 clientes mais frequentes do produto

### RF09 - Consultar histórico de compras por cliente
- Consultar o histórico das últimas 10 compras por cliente

### RF10 - Consultar performance por vendedor
- Consultar os 5 vendedores que mais venderam no último mês

### RF11 - Consultar padrões de compra e sazonalidade
- Consultar quais meses há maior volume de compras nos últimos 4 meses e quais os clientes que mais compraram em cada mês.

### RF07 - RF11
- Listar principais clientes por produto
- Mostrar média de compra mensal por cliente
- Identificar clientes que pararam de comprar
- Relatórios de vendas por representante

### RF12 - Notificar produtos com baixa saída
- O sistema deve destacar na interface produtos com média de saída do estoque abaixo de 3 meses
- O sistema deve criar notificação para o usuário mostrando quais produtos possuem média de saída do estoque abaixo de 3 meses

### RF13 - Notificar produtos que estão com estoque crítico
- O sistema deve destacar na interface produtos que possuem menos de 1 mês de fornecimento para o estoque
- O sistema deve criar notificação para o usuário mostrando quais produtos possuem menos de 1 mês de fornecimento para o estoque

### RF14 - Notificar produtos zerados no estoque
- O sistema deve destacar na interface produtos que estão zerados no estoque
- O sistema deve criar notificação para o usuário mostrando quais produtos estão zerados no estoque.

### RF15 - Autenticar o usuário
- O sistema ao negar o acesso de um usuário deve exibir de forma visual o acesso negado 

### RF16 - Permitir mudança de senha
- O sistema deve enviar um email seguro para redefinição de senha para o email do cliente
- O sistema deve atualizar a senha do usuário nos sistema
- O sistema deve permitir acesso com a nova senha criada

## Requisitos não funcionais

### RNF01 - Performance
- Tempo de Resposta: Executar a funcionalidade "Análise de Período de Estoque" (RF001). O tempo de resposta, desde o clique até a exibição completa dos resultados na tela, deve ser inferior a 30 segundos.

### RNF03 - Compatibilidade
- Recusação de outros arquivos:Ao tentar importar um arquivo com formato diferente (ex:, .txt) ou um .xlsx com colunas faltando, o sistema deve exibir uma mensagem de erro clara ao usuário, sem travar.

### RNF05 - Confiabilidade
- Fluidez constante do sistema: Durante o período de Teste de Aceitação do Usuário (UAT), com duração de 2 dias úteis, o sistema não deve apresentar nenhuma falha que impeça a conclusão das tarefas pelo usuário.

### RNF06 - Escalabilidade
- Estabilidade do sistema: Com o sistema populado com 1.000 produtos diferentes, os critérios de performance do RNF01 ainda devem ser atendidos.