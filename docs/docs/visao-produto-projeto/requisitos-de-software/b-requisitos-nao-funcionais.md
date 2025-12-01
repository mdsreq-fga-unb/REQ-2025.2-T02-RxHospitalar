---
sidebar_label: "Requisitos Não Funcionais"
sidebar_position: 1
---

# Requisitos Não Funcionais

Os requisitos não funcionais especificam os critérios de qualidade do sistema, definindo como ele deve operar em termos de performance, usabilidade, segurança e outras características essenciais.  

### Performance  

Esse requisito estabelece tempo de resposta e processamento, garantindo fluidez nas operações. Relaciona-se ao **[OE01](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE1)** (diminuir em 50% o tempo de análise).  

**RNF01 - Performance do Sistema**  
> - **Tempo de Resposta:** Executar a funcionalidade "Análise de Período de Estoque" (RF001). O tempo de resposta, desde o clique até a exibição completa dos resultados na tela, deve ser inferior a 30 segundos.  
> - **Tempo de Importação:** Realizar o upload de uma planilha `.xlsx`. O tempo total, desde a submissão do arquivo até a mensagem de conclusão do processamento, deve ser inferior a 10 minutos.  
> - **Importação sem Quebras:** Após a importação de uma planilha com 1.000 linhas, o número total de registros na tabela de produtos do sistema deve corresponder exatamente ao número de linhas do arquivo original. Uma soma de verificação de uma coluna numérica (ex: quantidade em estoque) no arquivo original deve ser igual à soma da mesma coluna no sistema.  

---

### Usabilidade  

Assegura que a interface seja intuitiva e responsiva (inclusive com modo escuro). Está diretamente ligado a **[OE04](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE4)** (interface fácil de usar, filtros dinâmicos e acessíveis em até 5 minutos).  

**RNF02 - Usabilidade e Experiência do Usuário**  
> - **Interface Inclusiva:** A tela principal de análise de dados deve apresentar as informações em um formato que demande pouco esforço de adaptação para o usuário entender e utilizar o sistema.  
> - **Navegação em Poucos Cliques:** O sistema deve exigir, no máximo, 4 cliques a partir da tela inicial para executar cada tarefa/análise/filtragem.  
> - **Reduzir Cansaço Visual:** O sistema deve possuir uma opção de alternância para um tema escuro. Esse tema deve utilizar fundo em cor mais escura do que o padrão e os textos devem ter alto contraste.  
> - **Adaptação Funcional:** O usuário deve realizar um conjunto de fluxos de análise sem treinamento prévio, julgando a facilidade de uso em uma escala de 1 a 5, devendo a nota ser igual ou superior a 4.  

---

### Compatibilidade  

Garante que o sistema seja compatível com planilhas e com o ambiente de uso (Windows). Apoia principalmente na integração de fontes conforme **[OE03](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE3)** (centralização das planilhas).  

**RNF03 - Compatibilidade com Ambientes e Planilhas**  
> - **Importação sem Quebras:** O sistema deve ser capaz de importar com sucesso um arquivo `.xlsx` ou `.csv` válido, formatado conforme o template esperado.  
> - **Recusa de Arquivos Inválidos:** Ao tentar importar um arquivo em formato diferente (ex: `.txt`) ou um `.xlsx` com colunas faltando, o sistema deve exibir uma mensagem de erro clara ao usuário, sem travar.  
> - **Compatibilidade com OS:** O sistema deve ser compatível com o sistema operacional do ambiente onde vai ser utilizado — Windows.  

---

### Segurança  

Reforça a confidencialidade dos dados, backup e restauração, bem como a conformidade com a **LGPD**. Está totalmente conectado ao     **[OE07](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE7)** (sigilo e controle de acesso).  

**RNF04 - Segurança**  
> - **Acesso Autorizado:** O sistema deve ter autenticação para garantir somente acesso autorizado.  
> - **Dados Criptografados:** Os arquivos de dados gerados ou utilizados pelo sistema (informações consolidadas de clientes, preços e estoque) devem ser armazenados de forma criptografada. O teste consiste em tentar abrir o arquivo com um editor de texto e verificar que o conteúdo é ilegível (caracteres aleatórios).  
> - **Arquivo de Backup:** A aplicação deve possuir funcionalidade que, quando acionada (ou de forma automática ao fechar), cria uma cópia do arquivo de dados principal em uma pasta de backup pré-definida, com timestamp no nome.  
> - **Restauração Local:** O sistema deve ter uma função “Restaurar Backup” que permita retornar os dados ao último estado salvo.  
> - **Conformidade com LGPD:** O sistema, ao excluir algum dado, deve garantir descarte definitivo. Após a exclusão, a busca por esse dado não deve retornar resultados.  

---

### Confiabilidade  

Garante a estabilidade do sistema em operação sem falhas críticas. Apoia a consecução ao assegurar consistência nas análises(indiretamente relacionado a **[OE06](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE6)** e **[OE08](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE8)**).  

**RNF05 - Confiabilidade Operacional**  
> - **Fluidez Constante do Sistema:** Durante o período de Teste de Aceitação do Usuário (UAT), com duração de 2 dias úteis, o sistema não deve apresentar nenhuma falha que impeça a conclusão das tarefas pelo usuário.  

---

### Escalabilidade  

Estabelece critérios para suportar crescimento de usuários e dados sem perda de desempenho.  

**RNF06 - Escalabilidade de Usuários e Dados**  
> - **Estabilidade do Sistema:** Com o sistema populado com 1.000 produtos diferentes, os critérios de performance do RNF01 ainda devem ser atendidos.  
> - **Teste de Carga:** Utilizando uma ferramenta (como JMeter), simular 5 usuários realizando consultas simultâneas na funcionalidade de filtro. O tempo de resposta médio não deve exceder 15 minutos (degradação aceitável em relação ao teste com um único usuário).  

---

### Manutenibilidade  

Define práticas para manter e evoluir o sistema, incluindo revisão de código, testes, documentação e integração de novos requisitos. 

**RNF07 - Manutenibilidade e Evolução**  
> - **Incremento de Requisitos Funcionais:** Nenhuma nova funcionalidade pode ser integrada ao ramo principal sem aprovação de pelo menos um outro membro da equipe.  
> - **Cobertura de Testes:** Utilizar ferramenta de análise de cobertura (ex: `coverage.py` para Python). A cobertura de testes unitários dos módulos de regras de negócio deve ser ≥ 80%.  
> - **Revisão Automatizada do Código:** Antes de aceito no projeto, o código deve passar por uma ferramenta de linting (ex: Pylint), sem erros.  
> - **Documentação da Instalação:** O projeto deve conter um **Readme** descritivo e instrutivo para os primeiros passos do usuário.  
> - **Documentação do Produto:** Cada funcionalidade deve ter um guia explicando como executar e interpretar resultados, além de descrever botões e fluxos obrigatórios para boa execução.  

---

### Manter Histórico de Notificações  

Assegura rastreabilidade e auditoria das notificações geradas. Está conectado a **[OE08](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#OE8)** (alertas automáticos sobre produtos de baixo giro ou parados).  

**RNF08 - Histórico de Notificações**  
> - **Descrição:** O sistema deve manter histórico de notificações por 15 dias para análise de rastreabilidade do produto. As notificações devem estar disponíveis na interface para o cliente, incluindo aquelas geradas pelos requisitos da categoria **Notificação sobre produtos em estado crítico**.  

---

### Tabela de Requisitos Não Funcionais  

A tabela abaixo apresenta a lista dos **Requisitos Não Funcionais (RNF)** definidos no projeto, com seus respectivos IDs e nomes resumidos.  

| ID    | Nome                                    |
|-------|-----------------------------------------|
| RNF01 | Performance do Sistema                  |
| RNF02 | Usabilidade e Experiência do Usuário    |
| RNF03 | Compatibilidade com Ambientes e Planilhas |
| RNF04 | Segurança           |
| RNF05 | Confiabilidade Operacional              |
| RNF06 | Escalabilidade de Usuários e Dados      |
| RNF07 | Manutenibilidade e Evolução             |
| RNF08 | Histórico de Notificações               |