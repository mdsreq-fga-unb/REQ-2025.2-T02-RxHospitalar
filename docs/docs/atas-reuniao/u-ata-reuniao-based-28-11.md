---
sidebar_label: "Ata N.º21 | 28/11"
sidebar_position: 21
---

# ATA N.º21 | 28/11

**Disciplina:** Requisitos de Software  
**Data:** 28/11/2025  
**Horário:** 21:34  
**Local:** Microsoft Teams

---

## Participantes

**Integrantes do Grupo:**

- Beatriz Figueiredo dos Santos  
- Davi Marques do Egito Coelho  
- Eduardo Oliveira Valadares  
- Gabriel Augusto Vilarinho Viana Rocha  
- Samuel Rodrigues Viana Lobo  

**Cliente (se participou):**
- Arthur (cliente), de forma indireta, por meio de contato presencial com Samuel no mesmo dia.

**Ausentes:**  
- Amanda de Moura (falta justificada)

---

## Objetivos da Reunião

- Atualizar o status dos gráficos, lista de requisitos e evidências de MVP.  
- Discutir problemas identificados no executável (troca de senha) e possíveis soluções.  
- Planejar a finalização dos requisitos pendentes (especialmente 9 e 11) e organizar reunião de feedback com o cliente Arthur.

---

## Principais Pontos Abordados

### 1. Gráficos, lista de requisitos e evidências de MVP

**Discussão:** Beatriz apresentou a implementação do gráfico e da lista de requisitos referentes a dados de clientes e vendedores, explicando o código e a estrutura em um “container” pensado para facilitar o posicionamento do gráfico na página. Também relatou ter iniciado a página de evidências de MVP, preenchendo com itens dos requisitos 2, 3, 4, 5 e 7.  

**Justificativa (se houver):** Organizar gráficos em containers desacoplados do layout facilita futuras mudanças de estilo e disposição, enquanto as evidências de MVP são necessárias para comprovar o que foi de fato entregue em relação aos requisitos priorizados.  

**Decisão:** Manter o padrão de encapsular gráficos em containers para posterior integração no dashboard e continuar o preenchimento da página de evidências de MVP, refinando a seleção e descrição das evidências ao longo do fim de semana.

---

### 2. Problema no executável ao mudar senha

**Discussão:** Beatriz relatou que, ao testar o executável, a alteração de senha funciona apenas durante a execução, mas, ao fechar e abrir novamente, a senha volta ao valor padrão, apesar da lógica aparentar salvar a alteração em arquivo (JSON). O grupo discutiu que o executável provavelmente está reexecutando o script e carregando o valor padrão em vez de utilizar a senha persistida.  

**Justificativa (se houver):** A persistência correta da senha é necessária para cumprir requisitos de segurança e usabilidade, evitando inconsistência entre o que é exibido ao usuário e o que é realmente salvo.  

**Decisão:** Davi abriu uma issue específica para o problema da senha e o grupo acordou que, após Beatriz avançar nas correções do diagrama de casos de uso, ela poderá investigar a causa e propor uma correção na lógica de leitura/gravação da senha, com apoio de quem se dispuser a ajudar.

---

### 3. Requisitos pendentes e reunião com o cliente

**Discussão:** Em diálogo entre Gabriel, Davi e Samuel, foi apontado que o requisito 9 (consulta de histórico de compras) ainda não teve avanços concretos. Davi reforçou a necessidade de concluir todos os requisitos até domingo, pois a segunda-feira será dedicada à gravação de vídeo, atualização do GitHub Pages e finalização de documentação. Samuel relatou ter iniciado o requisito 11 (padrões de compra e sazonalidade), mas com pouco progresso devido a outras atividades acadêmicas no dia. Ele informou ter encontrado o Arthur na academia, combinando com ele uma reunião de feedback e demonstração do produto na segunda-feira, em horário a definir conforme a disponibilidade do grupo.  

**Justificativa (se houver):** Concluir os requisitos funcionais principais antes da reunião com o cliente é essencial para apresentar um produto coerente e obter feedback útil, além de evitar sobrecarga no último dia de entrega.  

**Decisão:** Samuel dedicará o período de sexta a domingo exclusivamente ao projeto, focando nos requisitos que ainda lhe cabem (especialmente 6 e 11, além de outros que eventualmente permaneçam pendentes). O grupo manterá o plano de finalizar requisitos até domingo e, em seguida, concentrar esforços na documentação, evidências e preparação da reunião de segunda-feira com o Arthur.

---

## Próximos Passos (se forem elencados na reunião)

1. Refinar o gráfico e a lista de requisitos, garantindo que a estrutura em containers funcione bem para integração no dashboard – responsável: Beatriz.  
2. Continuar o preenchimento da página de evidências de MVP com requisitos já implementados – responsável: Beatriz.  
3. Investigar e corrigir o problema de persistência da senha no executável – responsáveis: Beatriz e Davi (issue já criada).  
4. Avançar na implementação do requisito 9 (histórico de compras) – responsável: Gabriel.  
5. Avançar na implementação do requisito 11 e demais requisitos pendentes atribuídos – responsável: Samuel.  
6. Confirmar horário da reunião de feedback com Arthur na segunda-feira e preparar o sistema para demonstração – responsável: Samuel, com apoio do grupo.

---

## Encaminhamentos Finais

- Registrada a necessidade de fechar requisitos até domingo para liberar a segunda-feira para vídeo, documentação e ajustes finais.  
- Reforçada a importância de resolver o bug de senha no executável antes da entrega final ao cliente.  
- Confirmada a intenção de realizar reunião de feedback com Arthur na segunda-feira, aproveitando o contato presencial já estabelecido por Samuel.

---

**Encerramento da reunião:** 21:58  
**Duração:** Aproximadamente 24 minutos  
