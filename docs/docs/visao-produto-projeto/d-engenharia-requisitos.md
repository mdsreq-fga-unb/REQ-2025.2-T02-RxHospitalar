---
sidebar_label: "Engenharia de Requisitos"
sidebar_position: 4
---

# Engenharia de Requisitos

Nesta seção são estabelecidas as atividades da Engenharia de Requisitos (ER), suas práticas e técnicas em alinhamento ao processo de ESW escolhido para o nosso projeto, o RAD. Cada uma das atividades foi descrita a partir de algumas técnicas e práticas que mais estavam alinhadas com a equipe em relação ao projeto. Suas evidências estarão disponíveis em uma ata da reunião que representa o momento no qual executamos tal atividade de Engenharia de Requisitos.  

## Atividades e Técnicas de ER

### Fase 1 - Planejamento de Requisitos

### Elicitação e Descoberta:

- **Entrevista:** Foi feita nesta fase uma primeira reunião da equipe com o cliente com o intuito de entender melhor o negócio e a sua atuação, suas dores, para traçarmos uma solução adequada.
- **Análise de Tarefas:** Ao entender o cenário em que o cliente estava inserido, foi feita dentro da segunda entrevista com o cliente uma análise precisa da sua tarefa de avaliar o período de estoque dos produtos na sua planilha.
- **Brainstorming:** A partir da entrevista, reuniões de brainstorming tendo todos os integrantes da equipe, principalmente a participação do P.O., para melhor organizarmos as ideias gerais do grupo sobre o que poderia ser a nossa solução.

**Resultados gerados:** Visão de Produto, Proposta de Solução, Personas, Lista de Stakeholders, Declaração do Problema

### Análise e Consenso:

- **Análise de priorização MoSCoW**: aplicada durante o refinamento do Backlog para classificação de requisitos em Must, Should, Could e Won’t have e assim ajudar na priorização do MVP.
- **Análise de critérios técnicos**: houve a criação de critérios de avaliação da complexidade técnica numa escala de 1 a 3 sobre a lógica de negócios e algoritmo; complexidade de dados e combinações analíticas; complexidade de interface e experiência do usuário UI/UX.

**Resultado gerado:** Documento de Visão de Produto e Projeto: Consolidação sobre o documento de Visão de Produto e Projeto, nos trazendo uma ideia mais clara sobre o problema do cliente e sobre os objetivos da nossa solução.

#### 4.1.3 Declaração de Requisitos:

* **Especificação de Requisitos:** A partir da especificação inicial dos requisitos, a declaração foi iniciada para auxiliar na clareza do entendimento sobre quais seriam os objetivos e possíveis critérios de aceitação para cada um deles, dado em conta o que inicialmente precisariam ter.
* **Features:** Foram declaradas features de acordo com o fluxo de tarefas parcelado por etapas, primordiais para o trabalho do cliente, que foram analisadas através da observação da explicação do cliente no uso das planilhas até chegar no objetivo final de cada análise.
* **Prompt IA:** A partir do contexto do cliente, do Diagrama de Ishikawa, e dos objetivos da solução, foram avaliados alguns requisitos que poderiam ser utilizados para a solução, alinhados também com as necessidades do cliente.
* **Temas Estratégicos:** Após melhor entendimento do escopo do projeto, foram elencados temas estratégicos que nos guiam de forma mais direta sobre a organização dos requisitos em relação à priorização de cada tema, que possui features correlacionadas.
* **Critérios de aceitação:** cada requisito contém critérios iniciais de aceitação para que seja testável e validado posteriormente.
* **Refinamento dos requisitos:** Foi feito um refinamento em relação aos RF’s e RNF’s do projeto, para que estivessem alinhados com a ideia do que é funcional ou não, o que terá interação do usuário ou não a partir da arquitetura MVC planejada.

**Resultado gerado:** Product Backlog com as nomenclaturas dos Requisitos de Software corretamente declaradas. 

#### 4.1.4 Verificação e Validação de Requisitos:

* Após a declaração inicial, os requisitos foram verificados e atualizados a partir de feedbacks de outro grupo da matéria e do professor, como nomenclatura dos mesmos.
* **Testes de aceitação:** realizados à medida que os protótipos foram feitos para verificar se os critérios de aceitação foram atendidos.
* **Análise de priorização MoSCoW:** aplicada durante o refinamento do Backlog para classificação de requisitos em *Must*, *Should*, *Could* e *Won’t have* e assim ajudar na priorização do MVP.
* **Análise de critérios técnicos:** Houve a criação de Critérios de Avaliação Técnica em relação à complexidade técnica numa escala de 1 a 3 sobre a lógica de negócios e algoritmo; complexidade de dados, combinações analíticas, complexidade de interface e experiência do usuário UI/UX;

**Resultado gerado:**  Análise da priorização dos requisitos com base na complexidade e valor de negócio.

#### 4.1.5 Verificação e Validação de Requisitos && Análise e Consenso:

* **Validação de Requisitos e Negociação:** Durante a reunião com o cliente para a validação do MVP houve um conflito sobre a complexidade e valor de negócio dos requisitos do tema: Análises Avançadas, os quais julgávamos de maior complexidade.
* **Análise de Domínio de Requisito:** A partir de uma reunião de validação com o cliente sobre o MVP, entendemos com mais profundidade as regras de negócio e como elas impactaram nos requisitos que havíamos declarado para a solução.
* **Feedback:** Após melhor explicação e visão do cliente, entendemos que eles não tinham uma complexidade elevada, mas tinham um alto impacto no valor de negócio para o cliente, o que ficou em consenso geral, que os RF’s presentes neste tema seriam desenvolvidos, após a construção de requisitos mais simples, acordando que ele fará parte do MVP.

**Resultado gerado:** Feedback do cliente em relação ao escopo do MVP, valor de negócio e priorização

#### 4.1.6 Organização e Atualização:

* **Feedbacks:** Após comentário do professor ao nosso *pitch* do projeto foram realizadas atualizações sobre a rastreabilidade dos requisitos do MVP, alinhando com os O.E’S do produto elencado inicialmente junto às características da solução.
* **Priorização de Requisitos:** Após o feedback do cliente e a avaliação a partir da rastreabilidade dos requisitos, foi atualizado o tema de Análises Avançadas no MVP.
* **Refinamento dos requisitos:** Foi feito um refinamento em relação aos RF’s e RNF’s do projeto, para que estivessem alinhados com a ideia do que é funcional ou não, o que terá interação do usuário ou não a partir da arquitetura MVC planejada.

**Resultado gerado:** Backlog do MVP atualizado, alinhado com a rastreabilidade dos O.E’S do produto, da avaliação técnica e valor de negócio do cliente.


### Fase 2 - User Design

#### 4.1.7 Representação de Requisitos:

* **Prototipagem:** a materialização dos requisitos foi por meio de [Figma](https://www.figma.com/design/Xk5sSYqw2tHww9UCYAKv7k/BASED--RX-Hospitalar?node-id=0-1&p=f&t=G1ZNAtvqbZ1XNQvB-0) para melhor verificação e validação posteriormente.

**Resultado gerado:** Protótipo de baixa e média fidelidade

#### 4.1.8 Análise e Consenso:

* **Inspeção de protótipos:** Foram utilizados os protótipos de média fidelidade para melhor análise dos requisitos em relação à interação do usuário e organização da manipulação de dados no *backend* da aplicação, de acordo com o que cada página iria exibir, alinhado com o que foi acordado no Backlog com o objetivo de domínio de cada requisito.

**Resultado gerado:** Protótipo Analisado, consenso da equipe sobre os primeiros RF a serem implementados com base nos protótipos

#### 4.1.9 Verificação e Validação de Requisitos:

* **Walkthrough:** Foi realizado um *walkthrough* no protótipo para simular a jornada de interação do usuário. Essa técnica nos permitiu percorrer o fluxo de tarefas e validar se a sequência de passos para executar as funcionalidades principais era lógica e simples de ser executada pelo usuário.
* **Decomposição Funcional:** Através da inspeção, cada tela e interação foram analisadas detalhadamente. A decomposição funcional foi aplicada para quebrar as tarefas maiores em passos menores, verificando a consistência e a clareza de cada etapa do processo.

**Resultado:** Protótipo verificado: Clareza da equipe em relação ao passo a passo seguido pelo usuário para executar os primeiros RF’s.

#### 4.1.10 Declaração de Requisitos:

* **Decomposição Funcional:** Utilizamos das funcionalidades representadas no protótipo para traçar como seria a interação do usuário com a aplicação e especificar melhor quais eram os resultados que deveriam aparecer para o usuário por meio de uma de nossas reuniões.

* **Histórias de Usuário:** Através de uma reunião com o cliente foram coletadas ass histórias de usuário do projeto para assim conectá-las aos RF’s e OE’s aos quais estavam relacionados para assim mapear a rastreabilidade do projeto.

**Resultado gerado:** Product Backlog populado com a US’s  

#### 4.1.11 Organização e Atualização de Requisitos: 

* **Histórias de Usuário:** Foi realizado no board do Miro da equipe a relação entre os RF’s e OE’S do projeto às US coletadas com o cliente.

**Resultado gerado:** Mapa de Rastreabilidade e Mapa de Relações entre Requisito  

#### 4.1.12 Validação: 

* **Protótipo de Alta Fidelidade:** Para validação da concepção da aplicação foi realizada uma validação através do protótipo de alta fidelidade gerada pela equipe com foco na interação do usuário com a inteface, para além de visualizar os componentes, procurando garantir mais conexão do cliente com a proposta final do do que será o projeto antes da fase de construção.  

* **Feedback:** Através de um formulário com  critérios de aceitação específicos sobre cada para do protótipo foram deixados checklists e espaços livre para comentários e sugestões em que o cliente poderia preencher rapidamente para coletarmos este feedback antes de iniciarmos a implementação.

**Resultado gerado:** [Formulário com o checklist da  validação do cliente e comentários adicionais sobre o protótipo de alta fidelidade](https://docs.google.com/document/d/1DuWLgI8KOPhmYx1iw2JULCNu_puY95xGvxx-HQFFgos/edit?usp=sharing)

### Fase 3 - Construção

#### 4.1.13 Verificação:

* **Definition of Ready (DoR):**  Foram utilizados para garantir que as novas construções a serem feitas estejam alinhadas com  idea da concepção do produto representada pelo protótipo, não causando implementação que fujam muito do escopo que foi validado, conforme conversado com o cliente.  

* **Revisão:** Durante todo processo de construção ao adicionar uma nova funcionalidade ou alteração considerável no código é preciso passar pela revisão de pelo menos um outro membro da equipe (realizando um Pull Request), que irá garantir a não quebra das funcionalidades já implementadas, o funcionamento esperado do que está sendo implementado, e também o alinhamento da implementação do requisito em relação ao (DoD).

**Resultado gerado:** Implementação alinhada aos DoD, DoR, Qualidade de Requisitos (testes), através do TDD, Resultados da Revisão de pelo menos um outro memebro (Pull Request).  

#### 4.1.14 Análise e Consenso && Organização e Atualização:

* **Backlog do Produto:**  Backlog de Requisitos: Através de uma nova análise dos requisitos no backlog e do MoSCoW gerado pelal equipe foi trago em uma das nossas reuniões semanais dada a produtividade da equipe, perspectiva de entrega do produto e também da maior priorização dos requisitos de Análises Avançadas foi votada a retirada dos requisitos da categoria de Notificações do MVP. Para além disso, também tivemos atualizações referentes aos requisitos RF11 e RF05 advindas do cliente.


* **Negociação:**   Foi tida uma conversa através do nosso grupo no whatsapp com o cliente para abordar sobre a possível mudança de escopo do MVP dado a produtividade da equipe em relação ao tempo de desenvolvimento necessário que os requisitos mais prioritários da categoria de Análises Avançadas estava maior do que o esperado. Dado os argumentos e explicação sincerada da proposta de mudança do MVP e análise das prioridades em relação ao que era mais necessário para o cliente a proposta de mundaça foi entendida com clareza e aceita com sucesso.


**Resultado gerado:** MVP Backlog Atualizado e Requisitos com espeficações mais definidas alinhadas com a necessidade do cliente.  

#### 4.1.15 Validação:

* **Feedback:** Através do Sistema Executável gerado, foi possivel coletar o primerio feedback do cliente em relação a V1 do projeto. Com o uso de critérios de valiadção específicos para os requisitos propostos naquela fase utilizando um formulário, foi coletado as impressões do usúario sobre o uso da aplicação e os resultados gerado para que fosse possível melhorias, caso necessário.

**Resultado gerado:** [Feedback do cliente sobre a implementação dos requisitos RF02, RF03, RF04, RF15](https://docs.google.com/document/u/6/d/1Rl8c0sF_EulcMqKozSS-cp1m0hZfKLWszexWU68Aw6Q/edit)  

### Fase 4 - Transição

#### 4.1.16 Verificação:

* **Revisão:**  Durante todo processo de construção ao adicionar uma nova funcionalidade ou alteração considerável no código é preciso passar pela revisão de pelo menos um outro membro da equipe (realizando um Pull Request), que irá garantir a não quebra das funcionalidades já implementadas, a integração entre as implementações do backend e frontend com o funcionamento esperado definido pelos critérios de aceitação alinhado ao (DoD).



* **Análise da Qualidade de Requisitos:** Por estarmos utilizando o TDD no nosso processo de desenvolvimento, os testes automatizaos em relação aos código do backend estão sendo realizado para garantir a confiabilidade necessária, dada a cobertura de teste que foi deferida para este projeto, garantido a sua funcionalidade dentro dos resultados esperados.


**Resultado gerado:** Qualidade de Requisitos, Resultados da Revisão e Executável Funcional do Projeto    

---

## 4.2 Engenharia de Requisitos e o RAD

Aqui, as atividades da ER, suas práticas e técnicas devem ser mapeadas, a partir das fases (etapas) do RAD, para a condução do projeto. As evidências de cada uma das atividades estão linkadas através do nome da atividade às atas realizadas pelos membros da equipe.

| Abordagem | Atividades ER | Prática | Técnica | Resultado |
| :--- | :--- | :--- | :--- | :--- |
| **Fase 1 - Planejamento de Requisitos** | | | | |
| | [Elicitação e Descoberta](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/atas-reuniao/a-ata-reuniao-based-06-09) | Descoberta sobre o negócio e dor do cliente | Entrevista e Análise de Tarefas | Entendimento sobre o negócio e contexto do cliente, Declaração do Problema, Personas |
| | [Análise e Consenso](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/atas-reuniao/b-ata-reuniao-based-09-09) | Discussões em Equipe, Reuniões com a equipe | Brainstorming, Análise de Personas, Análise de Concorrentes | Declaração do Problema, Lista de Necessidades, Personas, Proposta de Solução, Documento de Visão do Produto e Projeto |
| | [Declaração dos Requisitos](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/atas-reuniao/e-ata-reuniao-based-18-09) | Registro dos Requisitos | Brainstorming, Análise de Domínio de Requisito, Especificação de Requisitos | Lista de Requisitos (RFs) e Lista de Requisitos não funcionais (RNFs), BackLog do Produto e Requisitos de Software com nomenclaturas corrigidas |
| | [Verificação e Validação](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/atas-reuniao/f-ata-reuniao-based-22-09) | Verificação dos Requisitos && Refinamento dos requisitos && Priorização dos Requisitos | Reuniões, Feedbacks, MoSCoW, Critérios de Avaliação Técnica | BackLog do MVP priorizado |
| | [Verificação e Validação](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/atas-reuniao/i-ata-reuniao-based-04-10) | Validação de Requisitos && Resolução de Conflito (Valor e Acordo) | Negociação, Reunião, Feedbacks, Análise de Domínio de Requisito | MVP validado pelo cliente, e consenso sobre os primeiros requisitos a serem implementados |
| | [Organização e Atualização](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/atas-reuniao/i-ata-reuniao-based-04-10) | Priorização de Requisitos | Feedbacks do professor sobre rastreabilidade e da validação do cliente | Backlog do MVP atualizado, alinhado com o Mapa de Rastreabilidade dos O.E’S do produto |
| **Fase 2 - User Design** | | | | |
| | [Representação](https://www.figma.com/design/Xk5sSYqw2tHww9UCYAKv7k/BASED--RX-Hospitalar?node-id=0-1&p=f&t=yfklc8zNh3fXNjdj-0) | Criação de Protótipos | Prototipagem | Protótipo de baixa e média fidelidade |
| | [Análise e Consenso](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/atas-reuniao/k-ata-reuniao-based-11-10) | Refinamento dos requisitos | Protótipos, Inspeção, Análise de Objetivo de Domínio | Protótipo Analisado: Consenso da equipe sobre os primeiros RF a serem implementados com base nos protótipos |
| | [Verificação e Validação](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/atas-reuniao/l-ata-reuniao-based-13-10/) | Verificação da jornada de interação do usuário em relação ao fluxo de tarefas | Walkthrough, Decomposição funcional | Protótipo verificado: Clareza da equipe em relação ao passo a passo seguido pelo usuário para executar os primeiros RF’s |
| | [Declaração](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/atas-reuniao/l-ata-reuniao-based-13-10/) | Especificações da interação do usuário + Adição das histórias de usuário ao projeto | Prótipos, Decomposição funcional + Reunião, Histórias de Usuário | Primeiros RF’s do backlog do MVP a serem desenvolvidos com mais especificações em relação ao UI + Product Backlog populado com a conexão entre os RF’s e as US’s |  
| | [Organização e Atualização]() | Adequação dos RF’s e OE’S do projeto às US coletadas com o cliente | User History e Reunião | Mapa de Rastreabilidade & Mapa de Relações entre Requisito |  
| | [Verificação e Validação](https://unbbr.sharepoint.com/:b:/s/BASED/EZyLCRLi71FLigzVsgHhAGkBTbnJggljLuo3WdDzIhUDjw?e=Qlp6jI) | Validação do Protótipo de Alta fidelidade | Prótipos, Feedback e Checklist | Protótipo validado pelo cliente + [Feedback do cliente](https://docs.google.com/document/d/1DuWLgI8KOPhmYx1iw2JULCNu_puY95xGvxx-HQFFgos/edit?usp=sharing) |   
| **Fase 3 - Construção** | | | | |  
| | Verificação | Garantir que os requisitos a srem implementados estavam dentro da ideia do protótipo | Definition of Ready (DoR),Definition of Done (DoD), Revisão, Qualidade dos Requisitos | DoD, DoR, Qualidade de Requisitos (testes), Resultados da Revisão, Requisitos orientados à testes, com a revisão de pelo menos outro dev |  
| | Análise e Consenso && Organização e Atualização | Conversa com o cliente para validar a mudança de escopo do MVP // Atualização de especificações de  Requisitos e do MVP | Negociação // Backlog de Requisitos, Votação, MoSCoW | MVP Backlog Atualizado e Requisitos com espeficações mais definidas alinhadas com a necessidade do cliente |  
| | Validação | Validação do cliente em relação a entrega da V1 do projeto | Sistema Executável, Feedback e Checklist de Validação | Protótipo validado pelo cliente + [Feedback do cliente](https://docs.google.com/document/u/6/d/1Rl8c0sF_EulcMqKozSS-cp1m0hZfKLWszexWU68Aw6Q/edit) |  
| **Fase 4 - Transição** | | | | |  
| | Verificação | Garantir Alinhamento do projeto em relação a integração do backend com o frontend e criação do executável do projeto | Definition of Done (DoD), Revisão, Análise de Qualidade de Requisitos | Qualidade de Requisitos, Resultados da Revisão e  Executável Funcional do Projeto |  


