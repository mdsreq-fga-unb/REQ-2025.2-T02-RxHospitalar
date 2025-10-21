---
sidebar_label: "User Design"
sidebar_position: 10
---

# ATA N.º3 | 13/10/2025

**Disciplina:** Requisitos de Software  
**Data:** 13/10/2025  
**Horário:** 21:13  
**Local:** Microsoft Teams  
**Evidências:**  
- [Vídeo](https://unbbr.sharepoint.com/:v:/s/BASED/EX4SQperic5IirQ68wNToa0BOkFUqIRXDp2T-A8GKhIFGQ?e=nejpI6&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D)
- [Checklist](https://unbbr.sharepoint.com/:b:/s/BASED/EZyLCRLi71FLigzVsgHhAGkBexsh2h5LZCllD5UJd73q1g?e=ZFYok6)

---

## Participantes

**Integrantes do Grupo:**
- Amanda De Moura
- Beatriz Figueiredo Dos Santos
- Davi Marques Do Egito Coelho
- Gabriel Augusto Vilarinho Viana Rocha
- Samuel Rodrigues Viana Lobo

**Ausentes:** - Eduardo Oliveira Valadares

---

## Objetivos da Reunião
- Realizar retrospectiva sobre a colaboração e comunicação da equipe.
- Validar internamente análises de planilhas e protótipos (User Design).
- Detalhar fluxo de dados e regras de negócio.
- Planejar preenchimento da tabela de Atividades de Engenharia de Requisitos (Entrega da Unidade 2).

---

## Principais Pontos Abordados

### 1. Retrospectiva e Melhoria Contínua
**Discussão:** A equipe realizou uma retrospectiva sobre o andamento do projeto. Foi identificado um consenso sobre a necessidade de melhorar a comunicação assíncrona, pois a maior parte das atividades estava sendo concentrada próximo ao horário das reuniões síncronas 

**Decisão:** A equipe firmou o compromisso de utilizar mais ativamente as ferramentas colaborativas (Discord para atualizações de progresso e Miro para feedbacks assíncronos) para melhorar a visibilidade e o fluxo de trabalho contínuo.

### 2. Análise de Requisitos e Protótipo (User Design)
- **Discussão:** Os membros apresentaram suas análises das planilhas do cliente e dos protótipos de front-end (Figma) associados aos seus épicos.
- **Gabriel (Estoque):** Apresentou protótipos de tela com filtros (tempo, produto, condição) e gráficos (distribuição, giro, curva ABC, sugestão de compra), incluindo visualizações detalhadas para filtros específicos.
- **Beatriz (Regras de Negócio):** Destacou a importância crítica da coluna "Observações" nas planilhas, que contém regras de negócio explícitas (ex: "não comprar", "compra sob encomenda") que devem ser tratadas pela lógica do sistema para evitar sugestões de compra incorretas.
- **Amanda (Vendas/Sazonalidade):** Propôs cruzar "código do vendedor" com "total pago" (para performance) e "código do produto" (para sazonalidade), unificando as análises.

* <img width="763" height="467" alt="image" src="https://github.com/user-attachments/assets/0ba6f91a-ce96-4227-b804-01d5d355cf99" />
* <img width="763" height="467" alt="image" src="https://github.com/user-attachments/assets/f0a44c0a-ebd3-4078-afeb-040f5c77698c" />


**Decisão:** As análises e os protótipos foram validados internamente pela equipe.

### 3. Detalhamento do Fluxo de Dados (Reunião com Cliente)
**Discussão:** Samuel relatou que se reuniu com o cliente (Arthur) e mapeou o fluxo de dados completo, o que representa um avanço significativo no entendimento do problema.
**Lógica Central:** O sistema calculará a "Média de Saída" (da planilha BD 14, baseada na "Data de Giro") e irá compará-la com o "Estoque Atual" (soma de 3 planilhas: Pedido Fora, BD Estoque, BD Consignado).
**Resultado:** A comparação gera os "Meses de Estoque". Se este valor estiver abaixo do ideal (ex: 4 meses), o sistema aciona a "Compra Inteligente".
**Insight Crítico:** O cliente relatou que sua análise atual (baseada em meses fechados) falhou em prever um aumento súbito de demanda (de 1.000 para 5.000 unidades), reforçando a importância do requisito "Consultar principais clientes".

**Decisão:** O fluxo de dados mapeado por Samuel foi validado e será usado como base para o desenvolvimento do backend.

### 4. Planejamento da Entrega (Unidade 2)
**Discussão:** A equipe alinhou a necessidade de preencher a tabela de Atividades de Engenharia de Requisitos para a entrega de terça-feira (14/10). A tarefa consistiu em mapear as Fases do Projeto (Sprints 1 e 2) com as Atividades de RE (Elicitação, Análise, Validação, etc.), as Práticas (Levantamento, Refinamento) e as Técnicas (Brainstorming, Entrevista, Moscow, Prototipagem, Feedback).

**Decisão:** A equipe preencheu a tabela de forma colaborativa durante a reunião, focando nas técnicas efetivamente utilizadas e evidenciáveis. Gabriel ficou responsável por adicionar a tabela ao GitPages.

---

## Próximos Passos
1.  **Atualizar GitPages:** Adicionar a Tabela de Atividades de RE e o cronograma atualizado (Responsável: Gabriel).
2.  **Validar Protótipo com Cliente:** Agendar e realizar o checklist de validação do protótipo com Arthur (Responsáveis: Samuel, Davi e Eduardo [agendar]
3.  **Melhorar Comunicação Assíncrona:** Utilizar ativamente o Discord para atualizações e o Miro para colaboração (Responsável: Todos).
4.  **Disposição das evidências das atividades de E.R:** Estruturar conforme o modelo a tabela de atv. de eng. de requisitos e colocar suas descrições e evidências

---

## Encaminhamentos Finais
- A equipe alinhou as expectativas de comunicação e compromisso com as tarefas assíncronas.
- O protótipo de Estoque foi validado internamente e a lógica de negócio foi detalhada.
- A tabela de Atividades de ER foi estruturada para a entrega de 14/10.

---

**Encerramento da reunião:** 00:56 (14/10/2025)  
**Duração:** Aproximadamente 3h42  
**Responsável pela redação da ata:** Amanda De Moura
