---
sidebar_label: "Priorização do Backlog Geral"
sidebar_position: 1
---
# Priorização do Backlog Geral

A priorização do backlog foi realizada utilizando o modelo Must Have, Should Have e Could Have, ajudando a identificar quais são as funcionalidades essenciais, desejáveis e opcionais, de modo a orientar o desenvolvimento de acordo com os objetivos do projeto. A priorização das funcionalidades também foi feita utilizando uma análise em relação aos objetivos específicos os quais eles representam e também critérios técnicos para avaliar a complexidade do requisito.

Abaixo estão detalhadas as evidências e os critérios utilizados nesse processo.

## Critérios de Valor de Negócio (MoSCoW) e Complexidade
Para avaliar cada requisito do backlog, a equipe utilizou uma análise multidimensional com base em três pilares centrais: Técnico, Experiência do Usuário (UX) e Negócio.

Esses critérios foram usados para definir as pontuações que alimentaram a matriz de priorização (detalhada no tópico 9.2.2). A avaliação de cada funcionalidade foi feita da seguinte forma:
- **Esforço (Técnico):** Mede a complexidade de implementação. A escala utilizada foi **E** (Baixo Esforço), **EE** (Médio Esforço) e **EEE** (Alto Esforço). Este critério informou o eixo de **Complexidade (C)** da matriz de priorização.
- **Valor de Negócio (Business):** Mede o impacto e o retorno financeiro ou estratégico para o projeto. A escala foi **$** (Baixo Valor), **$$** (Médio Valor) e **$$$** (Alto Valor).
- **Valor de Experiência (UX):** Mede a importância da funcionalidade para a jornada e satisfação do usuário. A escala foi ♥ (Baixo Valor), ♥♥ (Médio Valor) e ♥♥♥ (Alto Valor).

Os valores de **Business ($)** e **UX (♥)** foram então combinados para determinar a posição final do requisito no eixo de **Valor de Negócio (V.N)** da matriz, permitindo uma decisão balanceada entre os três pilares.

<a id="figura-2"></a>
*Figura 2: Critérios de valor de negócio.*
![Tabela de critérios de valor de negócio](../../static/img/prioridade.png)
*Fonte: De autoria própria.*

## Matriz de Valor vs. Complexidade

Utilizando os "pesos" de Valor de Negócio (eixo V.N) e a pontuação de Complexidade/Esforço (eixo C) definidos na etapa anterior, todas as funcionalidades foram plotadas na Matriz de Valor vs. Complexidade. Esta análise visual foi fundamental para a tomada de decisão estratégica, permitindo à equipe identificar o quadrante de "Alta Complexidade, Alto Valor de Negócio" e o de "Baixa Complexidade, Alto Valor de Negócio". O agrupamento desses dois quadrantes serviu como base principal para a definição do escopo do MVP.

<a id="figura-3"></a>
*Figura 3: Definição do MVP.*
![Matriz de valor x complexidade](../../static/img/mvp.png)
*Fonte: De autoria própria.*

## Escopo do MVP e Sequenciamento de Entregas

Para definir o escopo do MVP de forma estratégica, a equipe utilizou o sequenciador da metodologia Lean Inception. Essa parte do framework foi escolhida por permitir um alinhamento rápido entre a visão de negócio, as necessidades do usuário e a viabilidade técnica. O objetivo foi focar na construção do conjunto mínimo de funcionalidades que permite validar as principais hipóteses de valor do produto com o menor esforço possível, evitando o desperdício de recursos no desenvolvimento de itens não essenciais para a primeira versão.

<a id="figura-4"></a>
*Figura 4: Sequenciador.*
![Sequenciador](../../static/img/sequenciador.png)
*Fonte: De autoria própria.*