---
sidebar_label: "Ata N.º14 | 18/11"
sidebar_position: 14
---

# ATA N.º14 | 18/11

**Disciplina:** Requisitos de Software  
**Data:** 18/11/2025  
**Horário:** 21:00  
**Local:** Microsoft Teams

---

## Participantes

**Integrantes do Grupo:**
- Amanda de Moura  
- Beatriz Figueiredo dos Santos  
- Eduardo Oliveira Valadares  
- Samuel Rodrigues Viana Lobo  
- Davi Marques do Egito Coelho (moderação)

**Cliente:**  
- Não participou nesta reunião

**Ausentes:**  
- Gabriel Augusto Vilarinho Viana Rocha  

---

## Objetivos da Reunião
- Planejamento de sprint para reta final do projeto  
- Atualização de status dos requisitos e desenvolvimento  
- Alinhamento sobre integração front/back  
- Ajustes no processo de versionamento e branches  
- Organização das próximas entregas formais (casos de uso, dashboards, testes, etc.)

---

## Principais Pontos Abordados

### 1. Situação acadêmica e atualização de Samuel
**Discussão:**  
Samuel relatou que precisou priorizar outras disciplinas devido a provas e atrasos, o que o afastou temporariamente das tarefas do projeto.  
**Decisão:**  
Retomar as atividades e atualização frequente no Discord.

---

### 2. Branches e fluxo de desenvolvimento
**Discussão:**  
Decidido que o repositório terá branches para funcionalidades, e não apenas por área (front/back).  
A branch `developer` será utilizada como base estável para integração.  
**Decisão:**  
- Cada requisito terá sua própria branch derivada da branch principal de cada camada (`experiment` para back e equivalente no front).  
- Integrações serão feitas via pull requests com revisão.

---

### 3. Progresso dos Requisitos RF
**Samuel (RF07 – Compras Inteligentes):**  
- Falta finalizar comparação entre planilhas de estoque e vendas.  
- Já acessa planilha de estoque e falta implementar lógica de síntese.

**Amanda e Beatriz (Front – Importação e Dashboard):**  
- Parte da importação e exibição de dados já pode subir para branch `developer`.

**Davi (RF01 e correlatos):**  
- Testes acima de 87%, meta continuar ampliando cobertura.

**Eduardo (RF05 e RF06):**  
- Início atrasado devido a provas, retomando agora.

---

### 4. Integração e necessidade de entregar software funcional
**Discussão:**  
Professor exige **software funcional até 02/12**, com fechamento de alterações no Projects após essa data.  
**Decisão:**  
Priorizar:
- Integração funcional front + back  
- Requisitos centrais funcionando antes da entrega final

---

### 5. Ajustes no planejamento e documentação
**Discussão:**  
Necessário apresentar:
- Estudos de caso  
- Diagramas de Casos de Uso  
- Evidências de Engenharia de Requisitos e Software  
- Histórico de progresso (prints do GitHub Project)

**Decisão:**  
- Davi montou checklist para acompanhamento  
- Material de referência do monitor Ian será utilizado  
- Gabriel responsável por consolidar definições de dashboards e requisitos de visualização

---

### 6. Dashboard – Consulta de Principais Clientes (RF08)
**Discussão:**  
Beatriz apresentou proposta inicial de exibição via gráfico. Debate sobre:  
- O que é mais relevante ao cliente: frequência, quantidade, faturamento, datas  
- Como manejar situações em que datas não estão presentes nas planilhas

Samuel informou que, conforme cliente, a data exata não é sempre relevante – faturamento por mês costuma ser o suficiente.  
**Decisão:**  
- Gráfico inicial será de barras com os 5 clientes que mais compraram  
- Dados mínimos:
  - Nome do cliente  
  - Quantidade de compras  
  - Faturamento gerado  
  - Se aplicável: datas de compra  
- Samuel gravará conversas futuras com Arthur para evitar retrabalho

---

### 7. Testes
**Discussão:**  
- Back-end seguirá com TDD  
- Front ainda precisa iniciar estrutura de testes  

**Decisão:**  
- Davi apoiará equipe do front com exemplo inicial  
- Integrações e testes não serão separados em branches distintas para evitar retrabalho

---

### 8. Manutenibilidade no GitHub
**Discussão:**  
- Necessário aprimorar organização e verificar compliance com critérios de qualidade  
- Novos PRs deverão exigir revisão e checklist de confirmação

**Decisão:**  
- Implementar workflow de linting  
- Revisão automatizada será configurada até 22/11

---

## Próximos Passos

1. **Samuel**  
   - Finalizar lógica do RF07  
   - Gravar conversas e repassar ao grupo  
   - Ajustar dados e filtros do RF08

2. **Beatriz e Amanda**  
   - Subir progresso atual do front para `developer`  
   - Criar testes básicos para telas iniciais

3. **Eduardo**  
   - Retomar RF05 e RF06 analisando trabalhos já implementados

4. **Davi**  
   - Melhorar cobertura de testes do RF01  
   - Configurar lint e workflows  
   - Consolidar checklist de acompanhamento

5. **Gabriel**
   - Consolidar definição dos dashboards e parâmetros exigidos

---

## Encaminhamentos Finais
- Realizar atualizações regulares no Discord para manter visibilidade do progresso.  
- Evitar retrabalho alinhando requisitos sempre que surgir dúvida com o cliente.  
- Priorizar integração e funcionamento completo até 02/12.

---

**Encerramento da reunião:** 22:15 
**Duração:** Aproximadamente 1h15  
**Responsável pela redação da ata:** Gabriel Augusto V. V. Rocha