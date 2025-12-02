---
sidebar_label: "Ata N.º19 | 26/11"
sidebar_position: 19
---

# ATA N.º19 | 26/11

**Disciplina:** Requisitos de Software  
**Data:** 26/11/2025  
**Horário:** 21:33  
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

- Atualizar o status de desenvolvimento do dashboard (filtros, gráficos e integração com a planilha).  
- Alinhar a estratégia de teste com o cliente Arthur usando o executável.  
- Verificar o andamento do requisito 7 e das especificações de casos de uso.

---

## Principais Pontos Abordados

### 1. Progresso do dashboard e filtros

**Discussão:** Gabriel apresentou o estado atual do dashboard de estoque, com o menu, área de gráficos e componente de filtros já visível, mas ainda utilizando dados mocados para linhas e sublinhas. Comentou que falta conectar o componente à planilha real e ajustar detalhes visuais (como cantos arredondados e tamanho da área de gráficos).  

**Justificativa (se houver):** A conexão direta com a planilha é essencial para que filtros e gráficos reflitam os dados reais do cliente, permitindo testes significativos e evolução do MVP.  

**Decisão:** Gabriel continuará priorizando a integração dos filtros com a planilha (linhas e sublinhas reais) e, assim que essa conexão estiver funcional, incluirá o primeiro gráfico planejado na área de gráficos, reorganizando a tela para acomodar os quatro gráficos previstos.

---

### 2. Tela de importação e teste com o cliente

**Discussão:** Amanda relembrou a tela de importação da planilha que havia desenvolvido e questionou se ela foi aproveitada no layout atual. Também reforçou o combinado de gerar um executável para envio ao Arthur, de forma que ele possa testar os filtros e verificar na planilha se os dados filtrados aparecem corretamente.  

**Justificativa (se houver):** Utilizar a tela de importação já construída e disponibilizar um executável para o cliente permite validar mais cedo o fluxo de consulta direta e filtragem, reduzindo riscos antes da entrega final.  

**Decisão:** Ficou acordado que a tela de importação será incorporada ao novo layout (abaixo da área de gráficos) e que, após a conexão filtros–planilha estar estável, o grupo avançará na montagem do executável para envio ao Arthur, mesmo que esse envio ocorra próximo ao final da sprint.

---

### 3. Requisito 7 e especificações de casos de uso

**Discussão:** Samuel relatou a continuidade da comunicação com o Arthur para obtenção de dados mais adequados ao requisito 7 (sugestão de compra inteligente) e explicou que, enquanto aguardava a nova planilha, gerou dados mocados estruturados para avançar na lógica. Comentou que o requisito é robusto e que ainda estava ajustando detalhes de cálculo. Amanda indicou que depende da finalização do requisito 7 para concluir testes no frontend e mencionou que está adicionando comentários e ajustes no diagrama de casos de uso, preparando-se para focar na especificação de um caso específico.  

**Justificativa (se houver):** A conclusão do requisito 7 é fundamental para alimentar o frontend com dados consistentes e para viabilizar funcionalidades de sugestão de compra, enquanto as especificações de casos de uso são exigência direta da disciplina para a próxima aula.  

**Decisão:** Samuel seguirá ajustando o requisito 7 e fará commit com código e prints de resultados para que o grupo visualize a estrutura dos dados. Amanda continuará a correção do diagrama e produzirá a especificação de caso de uso, contando com apoio de Samuel e Davi para garantir que fluxos principais e alternativos estejam contemplados.

---

## Próximos Passos (se forem elencados na reunião)

1. Conectar os filtros do dashboard à planilha real (linhas e sublinhas) e incluir o primeiro gráfico na área de gráficos – responsável: Gabriel.  
2. Incorporar a tela de importação de planilha ao layout atual do dashboard, abaixo da área de gráficos – responsáveis: Amanda e Gabriel.  
3. Finalizar a lógica do requisito 7 e commitar código e evidências (prints) para o repositório – responsável: Samuel.  
4. Ajustar o diagrama de casos de uso e produzir a especificação de pelo menos um caso de uso com fluxos principais e alternativos – responsáveis: Amanda (especificação), com apoio de Samuel e Davi.  
5. Após estabilizar filtros e requisito 7, preparar o executável a ser enviado ao Arthur para testes de validação.

---

## Encaminhamentos Finais

- Reforçada a prioridade de concluir a integração filtros–planilha para permitir o teste real do dashboard.  
- Alinhado que a tela de importação existente será aproveitada no layout final, evitando retrabalho.  
- Destacada a importância de concluir o requisito 7 e as especificações de casos de uso dentro do prazo da próxima aula, com colaboração entre backend, frontend e documentação.

---

**Encerramento da reunião:** 22:16  
**Duração:** Aproximadamente 43 minutos  
