---
sidebar_label: "Ata N.º22 | 29/11"
sidebar_position: 22
---

# ATA N.º22 | 29/11

**Disciplina:** Requisitos de Software  
**Data:** 29/11/2025  
**Horário:** 19:10  
**Local:** Microsoft Teams

---

## Participantes

**Integrantes do Grupo:**
- Amanda de Moura  
- Beatriz Figueiredo dos Santos  
- Davi Marques do Egito Coelho  
- Gabriel Augusto Vilarinho Viana Rocha  
- Samuel Rodrigues Viana Lobo  

**Cliente (se participou):**
- Não houve participação direta do cliente.

**Ausentes:**  
- Eduardo Oliveira Valadares  

---

## Objetivos da Reunião

- Alinhar a mudança de entendimento e escopo do requisito 11 (sazonalidade e clientes que mais compram). 
- Atualizar o status dos requisitos 8, 9, 10 e integrações na branch de experimentação. 
- Verificar pendências de documentação (evidências de engenharia de software, feedback do cliente, checklists em PRs). 

---

## Principais Pontos Abordados

### 1. Atualização do requisito 11 (sazonalidade)

**Discussão:** Samuel explicou que, após conversa com o cliente, o requisito 11 passou a ser entendido como duas funcionalidades dentro do mesmo requisito: análise da saída de uma linha de produtos ao longo dos meses (sazonalidade) e listagem dos clientes que mais compram essa linha. Constatou-se que a descrição atual no documento não refletia bem essa separação e ainda mencionava apenas quatro meses, enquanto o cliente deseja um panorama mais amplo para planejamento. 

**Justificativa (se houver):** A correção garante alinhamento entre documentação, critérios de aceitação e objetivo real do cliente, evitando divergências na avaliação da funcionalidade de análises avançadas. 

**Decisão:** Manter o requisito 11 como um único requisito funcional, detalhando que ele realiza duas ações (sazonalidade por linha e clientes que mais compram) e atualizar imediatamente descrição e critérios de aceitação no documento de requisitos, considerando todos os meses disponíveis e o fluxo “ao selecionar uma linha, exibir comportamento ao longo do tempo e principais clientes”. 

---

### 2. Andamento dos requisitos 8, 9, 10 e integrações

**Discussão:** Davi informou que finalizou os requisitos 8, 9 e 10, abriu pull request para a branch de experimentação e incluiu testes com dados reais, tornando a suíte de testes mais confiável, embora um pouco mais lenta. Ele também relatou ajustes em evidências de engenharia de software (prints de miro, retrospectivas, protótipo, etc.) e plano de abrir PR de integração do requisito 8 assim que o PR atual for revisado e aprovado. 

**Justificativa (se houver):** Concluir requisitos pendentes e garantir testes com dados próximos aos reais aumenta a qualidade das entregas e prepara o terreno para integração com o dashboard e validação final. 

**Decisão:** Davi seguirá avaliando o diagrama do grupo parceiro (Berkanan), finalizará a parte de documentação de engenharia de software e, após aprovação do PR de análises avançadas, abrirá PR para integração na branch principal, destravando os próximos passos de front e dashboards. 

---

### 3. Documentação, feedbacks e checklists de PR

**Discussão:** Davi solicitou acesso a um documento com anotações de feedback do cliente sobre o protótipo funcional, para registrar evidências no GitHub Pages, acordando com Amanda que mesmo o documento sem anotações já é suficiente para demonstrar o processo de coleta de feedback. Amanda também chamou atenção para a ausência de marcações em checklists obrigatórios e opcionais em um PR de Samuel, o que prejudica a rastreabilidade de critérios de aceitação atendidos. Samuel reconheceu que parte dos critérios (principalmente do requisito 7) não estava totalmente implementada, comentando que voltou a revisar descrição e checklists para refletir melhor o estado atual da funcionalidade. 

**Justificativa (se houver):** Evidências de feedback e checklists completos são fundamentais para comprovar o uso de boas práticas de engenharia de requisitos e rastreabilidade, itens avaliados explicitamente na disciplina. 

**Decisão:** Amanda ficará responsável por localizar e compartilhar o documento de feedback do protótipo para uso nas evidências. Samuel revisará os checklists dos PRs relacionados a análises avançadas, ajustando descrições e marcações de acordo com o que de fato foi implementado, e retornará ao requisito 7 para tentar cobrir critérios de aceitação ainda não contemplados, se o tempo permitir. 

---

## Próximos Passos (se forem elencados na reunião)

1. Atualizar no documento de requisitos a descrição e critérios de aceitação do requisito 11, refletindo sazonalidade por linha e clientes que mais compram – responsável: Samuel. 
2. Localizar e enviar ao grupo o documento de feedback do protótipo do cliente para uso nas evidências de engenharia de software – responsável: Amanda. 
3. Finalizar a avaliação do diagrama do grupo Bercanan e complementar evidências de engenharia de software (prints, protótipo, retrospectivas) – responsável: Davi. 
4. Revisar e atualizar checklists de PRs de análises avançadas, em especial os relacionados ao requisito 7, e ajustar descrições conforme critérios de aceitação – responsável: Samuel. 
5. Após aprovação do PR atual, abrir PR de integração do requisito 8 na branch principal, iniciando ajustes de front e dashboards – responsável: Davi. 

---

## Encaminhamentos Finais

- Reforçada a necessidade de manter documento de requisitos sempre alinhado com o entendimento mais recente do cliente, especialmente em funcionalidades complexas como análise de sazonalidade. 
- Destacada a importância de checklists de PR bem preenchidos para evidenciar o atendimento a critérios de aceitação e facilitar a avaliação da disciplina. 
- Registrado que o grupo está entrando na fase de fechamento da sprint, com foco em integração, ajustes finos e consolidação de evidências de engenharia de software. 

---

**Encerramento da reunião:** 19:43  
**Duração:** Aproximadamente 33 minutos  
