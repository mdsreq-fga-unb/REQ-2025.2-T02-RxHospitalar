# Critérios de aceitação dos requisitos funcionais (backend)

Cada pessoa do back ficará responsável pelos testes de um requisito. Cabe a **toda equipe de testes** verificar se há pelo menos 1 teste específico para **cada um** dos critérios de aceitação propostos.

## MVP

### RF01 - Analisar período de estoque
- O sistema deve calcular o período de estoque baseado na fórmula: (Estoque Total / Média de Saída)
- Permitir configurar período de análise (3, 4, 5 meses, etc.)
- Sugerir quantidade a ser comprada para atingir o estoque ideal

### RF02 - Integrar os dados das 4 planilhas principais
- O sistema possui compatibilidade com as planilhas Excel
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
- Calcular quantidade sugerida para atingir meta de estoque
- Considerar unidades por caixa na sugestão
- Calcular valor total da compra sugerida
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
- O sistema deve criar notificação para o usuário mostrando quais produtos possuem média de saída do estoque abaixo de 3 meses

### RF13 - Notificar produtos que estão com estoque crítico
- O sistema deve criar notificação para o usuário mostrando quais produtos possuem menos de 1 mês de fornecimento para o estoque

### RF14 - Notificar produtos zerados no estoque
- O sistema deve criar notificação para o usuário mostrando quais produtos estão zerados no estoque.

### RF15 - Autenticar o usuário
- O sistema deve permitir acesso ao sistema ao usuário que inseriu as credenciais de usuário e senha válidos (que tem cadastro de permissão no sistema)
- O sistema deve negar acesso ao sistema ao usuário que inseriu as credenciais de usuário e senha inválidos (que não tem cadastro de permissão no sistema)

### RF16 - Permitir mudança de senha
- O sistema deve enviar um email seguro para redefinição de senha para o email do cliente
- O sistema deve atualizar a senha do usuário nos sistema
- O sistema deve permitir acesso com a nova senha criada

## Requisitos não funcionais

### RNF01 - Performance
- Tempo de Resposta: Executar a funcionalidade "Análise de Período de Estoque" (RF001). O tempo de resposta, desde o clique até a exibição completa dos resultados na tela, deve ser inferior a 30 segundos.
- Tempo de importação:  Realizar o upload de uma planilha .xlsx. O tempo total, desde a submissão do arquivo até a mensagem de conclusão do processamento, deve ser inferior a 10 minutos.
- Importação sem quebras: Após a importação de uma planilha com 1.000 linhas, o número total de registros na tabela de produtos do sistema deve corresponder exatamente ao número de linhas do arquivo original. Uma soma de verificação de uma coluna numérica (ex: quantidade em estoque) no arquivo original deve ser igual à soma da mesma coluna no sistema.

### RNF03 - Compatibilidade
- Importação sem quebras: O sistema deve ser capaz de importar com sucesso um arquivo .xlsx, .csv  válido, ou outro arquivo de planilhas, e formatado conforme o template esperado.
- Recusação de outros arquivos:Ao tentar importar um arquivo com formato diferente (ex:, .txt) ou um .xlsx com colunas faltando, o sistema deve exibir uma mensagem de erro clara ao usuário, sem travar.
- Funcionamento sem gargalos no OS do cliente: O sistema deve ser compatível com o sistema operacional do ambiente onde vai ser utilizado - Windows

### RNF04 - Segurança
- Acesso autorizado: O sistema deve ter um sistema de autenticação para garantir somente acesso autorizado
- Dados criptografados: Os arquivos de dados gerados ou utilizados pelo sistema (onde ficam as informações consolidadas de clientes, preços e estoque) devem ser armazenados de forma criptografada. O teste consiste em tentar abrir o arquivo de dados (.db, .dat, .json, etc.) com um editor de texto e verificar que o conteúdo é ilegível (caracteres aleatórios), em vez de texto plano.
- Conformidade com LGPD: O sistema ao ser acionado para excluir algum dado deve descartar este dado do sistema, garantindo que após apagar os dados, ao buscar por eles a pesquisa não irá encontrar estes dados.

### RNF05 - Confiabilidade
- Fluidez constante do sistema: Durante o período de Teste de Aceitação do Usuário (UAT), com duração de 2 dias úteis, o sistema não deve apresentar nenhuma falha que impeça a conclusão das tarefas pelo usuário.

### RNF06 - Escalabilidade
- Estabilidade do sistema: Com o sistema populado com 1.000 produtos diferentes, os critérios de performance do RNF01 ainda devem ser atendidos.

### RNF07 - Manutenibilidade
- Incremento de novos Requisitos Funcionais: Nenhuma nova funcionalidade pode ser integrada ao ramo principal do código sem a aprovação de pelo menos um outro membro da equipe. A revisão deve seguir um checklist que verifica a clareza do código e a existência de comentários em trechos complexos e os testes unitários.
- Cobertura de Testes: Utilizar uma ferramenta de análise de cobertura de testes (ex: coverage.py para Python). A cobertura de testes unitários para os módulos de regras de negócio (cálculos de estoque, sugestões, etc.) deve ser de, no mínimo, 90%.
- Revisão Automatizada do código: Antes de ser aceito no projeto principal, o código deve passar por uma ferramenta de linting, como Pylint, sem apresentar erros. 
- Documentação da instalação: O projeto deve apresentar um Readme que seja descritivo e instrutivo para o usuário realizar seus primeiros passos para executar o sistema me muito esforço
- Documentação do Produto: Para cada funcionalidade deve haver um guia de como o usuário pode executar e identificar os resultados de cada pesquisa feita no sistema. Além de também explicar o conjunto de ferramentas, botões e caminhos obrigatórios que o usuário deve fazer para ter uma boa execução do sistema ( relacionado ao RF01)
