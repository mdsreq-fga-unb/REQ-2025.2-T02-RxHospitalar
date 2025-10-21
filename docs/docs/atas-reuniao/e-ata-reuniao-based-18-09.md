---
sidebar_label: "Declaração dos Requisitos"
sidebar_position: 5
---
# ATA N.º5 | 18/09  

**Disciplina:** Requisitos de Software  
**Atividade de Engenharia de Requisitos:** Declaração dos Requisitos
**Data:** 18/09/2025  
**Horário de início:** 21:00  
**Local:** Microsoft Teams
[**Evidência:**](https://unbbr.sharepoint.com/:v:/s/BASED/EcecFTlLaX5Hq4UOwGJp0VQBuc4ZfW79XYq5GVsVkmftGA?e=ich7zC&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D) 

---

## Participantes  

**Integrantes do Grupo:**  
- Amanda de Moura  
- Beatriz Figueiredo dos Santos  
- Eduardo Oliveira Valadares  
- Samuel Rodrigues Viana Lobo  

**Cliente:**  
- Arthur Ribeiro  

**Ausentes:**  
- Gabriel Augusto Vilarinho Viana Rocha  

---

## Objetivos da Reunião  
- Compreender melhor o processo atual do Arthur de análise e gestão de estoque  
- Identificar as principais necessidades para reconstruirmos os passos que tomaremos na construção do projeto (Declaração e Refinamento dos Requisitos)

---

## Principais Pontos Abordados  

### 1. Análise de Tarefas do Cliente ("As-Is")  
**Discussão:** O processo de gestão de Arthur é centrado em planilhas Excel (BD - 14, BD Estoque, PEDIDO FORA, BD - CONSIGNADO) atualizadas a partir de dados de um sistema interno. Foram identificados desafios como o processo ser muito manual, a baixa eficiência por precisar cruzar múltiplas planilhas, e o alto risco de erros devido à manipulação de fórmulas.  

**Justificativa:** Compreender o fluxo de trabalho atual é fundamental para identificar os pontos de melhoria e definir os requisitos da nova solução.  

**Decisão:** Foi decidido que os dados da planilha *"BD - CONSIGNADO"* serão desconsiderados na fase inicial do projeto.  

---

### 2. Levantamento de Requisitos e Funcionalidades Desejadas ("To-Be")  
**Discussão:** O objetivo principal é automatizar a análise para manter um estoque médio de 4 meses. As funcionalidades essenciais incluem:  
- análise rápida de produtos por linha  
- análise detalhada por SKU com os principais clientes  
- cálculos automatizados (média de saída, estoque atual, pedidos em aberto)  
- filtros avançados e processamento automático de preços  

**Justificativa:** As funcionalidades listadas visam automatizar tarefas manuais, reduzir erros e agilizar a tomada de decisão sobre a gestão de estoque.  

**Decisão:** A sugestão de Beatriz, de que o sistema processe as informações de preço de forma automática, foi aceita por Arthur.  

---

### 3. Requisitos Não-Funcionais e Preferências  
**Discussão:** Foi discutida a preferência por uma aplicação desktop, embora uma solução web bem estruturada seja uma alternativa viável. Também foi apontada a necessidade de o sistema possuir um método de atualização de dados a partir das extrações do sistema interno da empresa.  

**Justificativa:** Alinhar as expectativas técnicas e de usabilidade do cliente com as possibilidades de desenvolvimento.  

**Decisão:** As preferências foram anotadas para guiar a escolha da arquitetura da solução.  

---

### 4. Esboço do MVP  
**Discussão:** Foi acordado que o foco inicial do projeto (MVP) poderá ser a entrega da funcionalidade principal que calcula e exibe o período de estoque de cada produto.  

**Justificativa:** Priorizar a funcionalidade de maior impacto para permitir uma análise rápida dos itens mais críticos e entregar valor ao cliente o mais cedo possível.  

**Decisão:** O escopo do MVP está focado no cálculo e exibição do período de estoque por produto.  

---

## Próximos Passos  
1. Agendar uma reunião presencial com Arthur.  
   - **Responsável:** A equipe  
   - **Justificativa:** Permitir que a equipe visualize o processo de uso das planilhas em tempo real para aprofundar o entendimento dos desafios e fluxos de trabalho.  

---

## Encaminhamentos Finais  
- Foi avaliado o escopo do MVP, focado na automação do cálculo de estoque, e introduzida a possibilidade de uma próxima reunião presencial para observação detalhada do processo atual do cliente.  

---

**Encerramento da reunião:** 22:40  
**Duração:** Aproximadamente 1h40  
**Responsável pela redação da ata:** Eduardo  
