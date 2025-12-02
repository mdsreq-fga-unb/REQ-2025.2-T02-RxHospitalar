---
sidebar_label: "Ata N.º17 | 24/11"
sidebar_position: 17
---

# ATA N.º17 | 24/11

**Disciplina:** Requisitos de Software  
**Data:** 24/11/2025  
**Horário:** 21:35  
**Local:** Microsoft Teams

---

## Participantes

**Integrantes do Grupo:**
- Amanda de Moura  
- Beatriz Figueiredo dos Santos  
- Davi Marques do Egito Coelho  
- Eduardo Oliveira Valadares  
- Gabriel Augusto Vilarinho Viana Rocha  
- Samuel Rodrigues Viana Lobo  

**Cliente (se participou):**
- Não houve participação do cliente.

**Ausentes:**  
- Sem registros de ausência.

---

## Objetivos da Reunião

- Atualizar o andamento das tarefas da Sprint 6.  
- Discutir a implementação dos filtros e o uso das branches no repositório.  
- Alinhar o diagrama de casos de uso e a preparação para apresentação em aula.

---

## Principais Pontos Abordados

### 1. Implementação dos filtros no frontend

**Discussão:** Foi apresentado o status do componente de filtros no frontend, já desenvolvido e testado em uma branch de front, com alguns problemas de layout ao rodar em outra branch (navbar e planilha em tamanhos diferentes). Debateram-se formas de integrar o componente mantendo a planilha principal e o layout desejado.  

**Justificativa (se houver):** Centralizar o desenvolvimento sobre uma base estável evita retrabalho de interface e conflitos entre branches, além de facilitar a integração com o backend.  

**Decisão:** Criar uma nova branch a partir da branch estável de frontend, integrar nela o componente de filtros e, após ajustes de layout, abrir pull request para revisão e posterior integração às branches principais.

---

### 2. Organização das branches e fluxo de trabalho

**Discussão:** Foram esclarecidas as diferenças de uso entre a branch de frontend e a de experimentação, bem como dúvidas sobre onde desenvolver e testar novos componentes. Discutiu-se que a branch de experimentação está mais voltada para integrações de backend, enquanto o frontend precisa de uma base mais estável para evoluir.  

**Justificativa (se houver):** Um fluxo de branches bem definido reduz conflitos, facilita code review e ajuda a manter uma versão utilizável do sistema para demonstrações e testes.  

**Decisão:** Adotar como padrão a criação de branches de feature a partir da branch de frontend para desenvolvimento da interface, deixando a branch de experimentação focada na integração com o backend e testes mais amplos.

---

### 3. Diagrama de casos de uso e apresentação

**Discussão:** Houve questionamentos sobre a coerência de um caso de uso relacionado a “compartilhar experiências” com a visão do produto, levando o grupo a revisar o documento. Também se conversou sobre como será a apresentação do diagrama em aula e quem ficará responsável por expor o conteúdo.  

**Justificativa (se houver):** Garantir que os casos de uso reflitam fielmente a visão do produto evita inconsistências entre documentação e implementação e contribui para uma apresentação mais clara ao professor.  

**Decisão:** Manter o caso de uso de compartilhamento de experiências, alinhando-o ao texto já presente na visão do produto, e definir Samuel como responsável principal pela apresentação do diagrama, com apoio de Beatriz para complementações durante a exposição.

---

## Próximos Passos (se forem elencados na reunião)

1. Criar branch a partir do frontend e integrar o componente de filtros – responsável: Gabriel.  
2. Ajustar layout e comportamento dos filtros sobre a planilha principal – responsável: Gabriel.  
3. Revisar o documento de visão do produto e o diagrama de casos de uso para garantir coerência – responsáveis: Amanda e Beatriz.  
4. Preparar a apresentação do diagrama de casos de uso para a aula seguinte – responsáveis: Samuel (apresentação) e Beatriz (suporte).

---

## Encaminhamentos Finais

- Reforçado o padrão de uso das branches para organizar melhor o fluxo de desenvolvimento.  
- Confirmada a manutenção do caso de uso de compartilhamento de experiências, com ajustes de texto se necessário.  
- Alinhados responsáveis e estratégia para a apresentação do diagrama em aula, garantindo que o grupo chegue preparado.

---

**Encerramento da reunião:** 22:15  
**Duração:** Aproximadamente 40 minutos  
