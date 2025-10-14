---
sidebar_label: "Engenharia de Requisitos"
sidebar_position: 4
---

# Engenharia de Requisitos

A partir das informações apresentadas na seção 3, deste documento, devem ser estabelecidas as atividades da Engenharia de Requisitos (ER), suas práticas e técnicas em alinhamento ao processo de ESW informado. Inicialmente, cada uma das 6 atividades da ER deve ser associadas às técnicas que serão utilizadas no projeto em desenvolvimento durante a disciplina.
## Atividades e Técnicas de ER

### Elicitação e Descoberta:

- **Brainstorming**: uso durante reuniões de refinamento do Backlog para gerar ideias e identificar requisitos e restrições do sistema.
- **Reunião com o cliente**: reuniões com o cliente para validação de requisitos e o funcionamento destes.

### Análise e Consenso:

- **Análise de priorização MoSCoW**: aplicado durante o refinamento do Backlog para classificação de requisitos em Must, Should, Could e Won’t have e assim ajudar na priorização do MVP.
- **Análise de critérios técnicos**: houve a criação de critérios de avaliação da complexidade técnica numa escala de 1 a 3 sobre a lógica de negócios e algoritmo; complexidade de dados e combinações analíticas; complexidade de interface e experiência do usuário UI/UX.

### Declaração de Requisitos:

- **Critérios de aceitação**: cada requisito contém critérios de aceitação para que seja testável e validado posteriormente.

### Representação de Requisitos:

- **Product Backlog**: o Backlog será usado para representar os requisitos organizados por prioridade.
- **Prototipagem**: a materialização dos requisitos será por meio dos protótipos feitos em cada fase.

### Verificação e Validação de Requisitos:

- **Testes de aceitação**: realizados à medida em que os protótipos foram feitos para verificar se os critérios de aceitação foram atendidos.
- **Inspeção de protótipos**: à medida em que os protótipos estiverem feitos, o cliente fará a validação acerca do protótipo e se ele corresponde às expectativas e ao que foi acordado no Backlog.

### Organização e Atualização de Requisitos:

- **Refinamento do Backlog**: à medida em que o andamento do projeto avança, os requisitos serão revisados e atualizados conforme o feedback do cliente e a capacidade técnica da equipe.
- **Rastreabilidade de requisitos**: Por meio de um quadro Kanban no Github Projects, será feito o acompanhamento da evolução dos requisitos a serem feitos, sendo feitos e concluído.

## Engenharia de Requisitos e o RAD + Scrum

Aqui, as atividades da ER, suas práticas e técnicas devem ser mapeadas, a partir das fases (etapas) do processo estabelecido pela equipe, para a condução do projeto. Essas informações devem ser apresentadas em uma tabela conforme indicado, a seguir (exemplo).

| Fase do RAD                  | Atividades ER              | Prática                              | Técnica                                                              | Resultado Esperado                                      |
|------------------------------|----------------------------|--------------------------------------|----------------------------------------------------------------------|---------------------------------------------------------|
| Joint Requirements Planning (JRP) Sprint 1 | Elicitação e Descoberta    | Levantamento de Requisitos           | Brainstorming // Entrevista // Documento de Visão de Produto         | Visão de Produto e Projeto                              |
|                              | Declaração de Requisitos   | Registro dos Requisitos              | Brainstorming // Especificação de Requisitos                         | Lista de Requisitos (RFs) e Lista de Requisitos não funcionais (RNFs) BackLog do Produto |
|                              | Análise e Consenso         | Refinamento dos requisitos           | Lean Inception e Reuniões                                            | BackLog do MVP validado pelo cliente                    |
|                              | Verificação e Validação    | Validação de Requisitos              | Reuniões // Descrição dos requisitos // Critérios de aceitação       | Funcionalidades verificadas com o cliente e feedback coletado |
|                              | Organização e Atualização  | Priorização de Requisitos            | MoSCoW // Critérios de Avaliação Técnica                             | Backlog atualizado e alinhado com os objetivos da sprint em andamento |
| Joint Application Design (JAD) Sprint 2 | Representação              | Criação de Protótipos                | Prototipagem                                                         | Protótipos que orientam a equipe                        |
|                              | Verificação e Validação    | Verificação de Requisitos            | Revisão dos Requisitos Funcionais                                    | Requisitos Funcionais validados em relação aos OE's     |
|                              | Organização e Atualização  | Atualização dos Requisitos do MVP    | Feedback                                                             | MVP atualizado e alinhado                               |
|                              | Análise e Consenso         | Refinamento e Esclarecimento de alguns Requisitos Funcionais | Especificação dos Requisitos com base nos casos de uso // Prototipagem | Especificação de Requisitos (RFs) Com o Backlog ajustado conforme consenso com o cliente |