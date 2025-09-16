---
sidebar_label: "Estratégias de Engenharia de Software"
sidebar_position: 3
---
# Estratégias de Engenharia de Software

### 3.1 Estratégia priorizada


- **Abordagem:** Híbrido ( Dirigido a plano + Ágil )
- **Ciclo de Vida:** Adaptativo
- **Processo:** Scrum + XP
  
 
### 3.2 Quadro comparativo


|  Características  |            SCRUM + RAD           |             SCRUM+XP           |
|-------------------|----------------------------------|--------------------------------|
| Abordagem Geral   | Iterativo e incremental, prototipagem e desenvolvimento rápido   | Iterativo incremental, TDD (dirigido por testes), feedback contínuo e entregas frequentes.              |
| Foco em Arquitetura   | Arquitetura focada na prototipação rápida e reutilização de componentes | Menor foco inicialmente, mas evoluindo conforme a necessidade e tempo.    |
| Estrutura de Processos  | Estrutura Scrum (sprints, daily e backlog de produto) e fases do RAD: planejamento de requisitos, prototipação (user design), construção, implementação final    | Estrutura Scrum (sprints, daily e backlog de produto) e fases do  XP: planejamento de requisitos (user stories), planejamento de release, iteração (código, integração, testes), validação (small releases), release final. |
| Flexibilidade de Requisitos  | Alta: requisitos definidos que podem mudar de acordo com o feedback do cliente  | Alta: aborda os requisitos como variáveis, histórias de usuários. |
| Colaboração com Cliente  | Alta: feedback contínuo em relação a protótipos. | Alta: cliente responsável por validar pequenas entregas. |
| Complexidade do Processo  | Moderada: orientada a protótipo, modularização permite que partes do projeto sejam divididas em equipes RAD | Moderada: Práticas Scrum e XP exigem organização e participação da equipe. |
|  Qualidade Técnica  | Foco em protótipos e entregas rápidas pode comprometer a qualidade do código. Sem práticas fortes de testes automatizados. |Alta: Prioriza testes automatizados, integração contínua, refatoração. |
|  Práticas de Desenvolvimento  | Construção rápida de protótipos, iterações rápidas com foco em design de usuário. | TDD, pair programming, integração contínua. |
|  Adaptação ao Projeto da RX Hospitalar  | Ideal para um cenário com foco em protótipos | Ideal para um cenário extremamente dinâmico, garantido qualidade de código. |
|  Documentação  | Representação informal (protótipos) pode substituir partes da documentação formal. Documentação mínima. | Documentação mínima, apenas o necessário para o cliente e equipe. |
|  Controle de Qualidade  | Feito no ciclo de prototipagem via retorno do usuário | Testes automatizados. |
|  Escalabilidade  | Apresenta limitações para sistemas de grande escala, melhor para projetos de baixa complexidade | Boa em times pequenos e médios, difícil em times muito grandes. |
|  Suporte a Equipes de Desenvolvimento  | A equipe deve ser muito comprometida, deve haver regras claras. Uso do Scrum para organização formal.| Práticas XP ajudam na colaboração e manutenção da qualidade em equipes pequenas/médias. |



### 3.3 Justificativa

Considerando a necessidade de alinhar características do software a ser desenvolvido com o nível de maturidade da equipe BASED, o processo ScrumXP se mostrou mais oportuno, pelos seguintes fatores:

#### 1. Aprendizagem Contínua

O ScrumXP, por meio de práticas interativas e colaborativas, favorece o desenvolvimento técnico e o crescimento da equipe. Diferentemente do RAD, que foca em prototipação rápida, o ScrumXP promove evolução das habilidades ao longo de todo o projeto. Ideal para equipes de baixa experiência.

#### 2. Controle de Qualidade

A aplicação de práticas do XP, tais como Test-Driven Development (TDD), testes automatizados e integração contínua, assegura maior confiabilidade ao código. Essa abordagem reduz a ocorrência de falhas e garante maior qualidade em comparação ao RAD, onde a prototipação pode deixar lacunas de qualidades a depender do nível de experiência da equipe.

#### 3. Práticas XP + Scrum

O uso de práticas como pair programming, em conjunto com a estrutura do Scrum (reuniões diárias e retrospectivas), promove colaboração contínua, alinhamento de expectativas e maior eficiência na comunicação. Assim, contribuindo para o aumento de produtividade e redução de riscos organizacionais.

#### 4. Releases e Validação Contínua

As entregas incrementais e frequentes permitem validação contínua do produto pelo cliente, garantindo que o produto atenda suas demandas e necessidades reais. Essa prática reduz o risco de retrabalho na entrega final. Em contrapartida, o RAD utiliza de validação de protótipos, que, a depender da experiência técnica, pode não refletir a complexidade real do sistema.


