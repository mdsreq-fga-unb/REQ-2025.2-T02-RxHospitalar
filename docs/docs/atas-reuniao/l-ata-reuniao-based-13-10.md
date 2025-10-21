<img width="1445" height="749" alt="image" src="https://github.com/user-attachments/assets/4b9b962a-5c8e-495a-908f-3aef34070e24" />---
sidebar_label: "User Design"
sidebar_position: 11
---

# ATA N.º3 | 13/10/2025

**Disciplina:** Requisitos de Software  
**Data:** 13/10/2025  
**Horário:** 21:13  
**Local:** Microsoft Teams
[**Evidência**](https://unbbr.sharepoint.com/:v:/s/BASED/EX4SQperic5IirQ68wNToa0BOkFUqIRXDp2T-A8GKhIFGQ?e=nejpI6&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D)

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
- Planejar preenchimento da tabela de Atividades de Engenharia de Requisitos (Entrega Unidade 2).

---

## Principais Pontos Abordados

### 1. Retrospectiva e Melhoria Contínua
[cite_start]**Discussão:** A equipe realizou uma retrospectiva sobre o andamento do projeto[cite: 2112]. [cite_start]Foi identificado um consenso sobre a necessidade de melhorar a comunicação assíncrona, pois a maior parte das atividades estava sendo concentrada próximo ao horário das reuniões síncronas [cite: 2113-2115, 2129-2130, 2132-2136].

[cite_start]**Decisão:** A equipe firmou o compromisso de utilizar mais ativamente as ferramentas colaborativas (Discord para atualizações de progresso e Miro para feedbacks assíncronos) para melhorar a visibilidade e o fluxo de trabalho contínuo [cite: 2142-2146, 2164-2173].

### 2. Análise de Requisitos e Protótipo (User Design)
[cite_start]**Discussão:** Os membros apresentaram suas análises das planilhas do cliente e os protótipos de front-end (Figma) associados aos seus épicos [cite: 2195-2197, 2258-2260, 2427-2430].
* [cite_start]**Gabriel (Estoque):** Apresentou protótipos de tela com filtros (tempo, produto, condição) e gráficos (distribuição, giro, curva ABC, sugestão de compra), incluindo visualizações detalhadas para filtros específicos [cite: 2217-2241].
* [cite_start]**Beatriz (Regras de Negócio):** Destacou a importância crítica da coluna "Observações" nas planilhas, que contém regras de negócio explícitas (ex: "não comprar", "compra sob encomenda") que devem ser tratadas pela lógica do sistema para evitar sugestões de compra incorretas [cite: 2261-2267, 2315-2322].
* [cite_start]**Amanda (Vendas/Sazonalidade):** Propôs cruzar "código do vendedor" com "total pago" (para performance) e "código do produto" (para sazonalidade), unificando as análises [cite: 2431-2432, 2438-2441, 2448-2450].

* <img width="1845" height="858" alt="image" src="https://github.com/user-attachments/assets/0ba6f91a-ce96-4227-b804-01d5d355cf99" />
* <img width="1445" height="749" alt="image" src="https://github.com/user-attachments/assets/f0a44c0a-ebd3-4078-afeb-040f5c77698c" />


**Decisão:** As análises e os protótipos foram validados internamente pela equipe.

### 3. Detalhamento do Fluxo de Dados (Reunião com Cliente)
[cite_start]**Discussão:** Samuel relatou que se reuniu com o cliente (Arthur) e mapeou o fluxo de dados completo, o que representa um avanço significativo no entendimento do problema [cite: 2211-2212, 2520-2521].
* [cite_start]**Lógica Central:** O sistema calculará a "Média de Saída" (da planilha BD 14, baseada na "Data de Giro") e irá compará-la com o "Estoque Atual" (soma de 3 planilhas: Pedido Fora, BD Estoque, BD Consignado) [cite: 2537-2539, 2544-2545, 2584, 2596-2598].
* **Resultado:** A comparação gera os "Meses de Estoque". [cite_start]Se este valor estiver abaixo do ideal (ex: 4 meses), o sistema aciona a "Compra Inteligente"[cite: 2599].
* [cite_start]**Insight Crítico:** O cliente relatou que sua análise atual (baseada em meses fechados) falhou em prever um aumento súbito de demanda (de 1.000 para 5.000 unidades), reforçando a importância do requisito "Consultar principais clientes" [cite: 2638-2645].

**Decisão:** O fluxo de dados mapeado por Samuel foi validado e será usado como base para o desenvolvimento do backend.

### 4. Planejamento da Entrega (Unidade 2)
[cite_start]**Discussão:** A equipe alinhou a necessidade de preencher a tabela de Atividades de Engenharia de Requisitos para a entrega de terça-feira (14/10) [cite: 2756-2757]. [cite_start]A tarefa consistiu em mapear as Fases do Projeto (Sprints 1 e 2) com as Atividades de RE (Elicitação, Análise, Validação, etc.), as Práticas (Levantamento, Refinamento) e as Técnicas (Brainstorming, Entrevista, Moscow, Prototipagem, Feedback) [cite: 2776-2782, 2843-2846].

[cite_start]**Decisão:** A equipe preencheu a tabela de forma colaborativa durante a reunião, focando nas técnicas efetivamente utilizadas e evidenciáveis [cite: 3192-3221]. [cite_start]Gabriel ficou responsável por adicionar a tabela ao GitPages [cite: 4081-4082, 4085].

---

## Próximos Passos
1.  [cite_start]**Atualizar GitPages:** Adicionar a Tabela de Atividades de RE e o cronograma atualizado (Responsável: Gabriel)[cite: 4085].
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
