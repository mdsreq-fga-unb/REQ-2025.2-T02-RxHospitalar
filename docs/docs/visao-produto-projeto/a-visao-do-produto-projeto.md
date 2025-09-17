---
sidebar_label: "Cenário atual do cliente e do negócio"
sidebar_position: 1
---

# Visão do produto e projeto 

## Cenário atual do cliente e do negócio

### 1. Introdução ao Negócio e Contexto  
A RX Hospitalar é uma empresa distribuidora de produtos médicos e oftalmológicos que atua em dois segmentos principais: o ramo de visão, com foco na comercialização de lentes de contato para óticas, e o ramo hospitalar, que envolve a distribuição de insumos e materiais cirúrgicos para hospitais, clínicas e, eventualmente, pacientes físicos. A empresa representa marcas de grande porte no setor de saúde, como Hollister, Abarth, Smith, B. Braun e Alcon, e possui abrangência em cinco estados brasileiros: Distrito Federal, Goiás, Mato Grosso, Mato Grosso do Sul e Tocantins. Com um portfólio que ultrapassa 14 mil itens apenas na área de cuidados da visão, a RX Hospitalar lida com um volume significativo de dados e transações, atendendo a mais de mil clientes entre empresas e pessoas físicas.  
Atualmente, a empresa enfrenta desafios significativos em sua operação devido à dependência de planilhas Excel para gestão de compras, estoque e vendas. Essas planilhas são atualizadas manualmente, exigindo análises demoradas e propensas a erros, especialmente considerando a grande variedade de produtos e a necessidade de acompanhar prazos de validade, sazonalidade e demandas específicas de cada cliente. Além disso, a falta de integração entre os setores e a dificuldade de visualização clara dos dados impedem tomadas de decisão ágeis e estratégicas, impactando tanto a eficiência operacional quanto a satisfação dos clientes.

### 1.2 Identificação da Oportunidade ou Problema
O processo de análise de estoque, compras e vendas dos produtos são processos cruciais para a continuidade e bom desempenho da empresa. Sua operacionalização influencia estrategicamente o seu setor e outras frentes do negócio. Os insights coletados a partir das várias planilhas diferentes guiam de forma tática, como por exemplo, os representante de vendas dos produtos, que fazem a ponte entre esta empresa, da qual é a fornecedora, e os seus clientes B2B ou B2C, que são as empresas/pessoas que adquirem os produtos oferecidos. Com isso, é possível de se perceber o quão importante é ter uma análise rápida das informações gerando insights válidos, tanto para o setor de compras, quanto para os representantes que estão na linha de frente da venda de produtos.  
Assim, a partir desta análise cenário atual, foi observado que as principais dores enfrentadas pela **RX Hospitalar** não se limitam a apenas um único fator, mas resultam de um conjunto de causas interligadas. Para organizar e compreender melhor essas origens, foi elaborado um **Diagrama de Ishikawa**, ferramenta que auxilia na visualização das principais fontes dos problemas, como a sobrecarga no uso de planilhas, falhas de integração de sistemas e dificuldades no acesso a informações críticas. A [Figura 1](#figura-1), a seguir, apresenta essa representação de forma estruturada.

<a id="figura-1"></a>
*Figura 1: Diagrama de Ishikawa.*
![Diagrama de Ishikawa do projeto.](../../static/img/Diagrama-ishikawa.png)
*Fonte: De autoria própria.*

**Principais dores:**
- Tempo elevado para compilar/atualizar bases (faturado + pendências) e analisar produto a produto.
- Risco operacional (erros de filtro/linhas ocultas, travamentos do Excel) e falta de visão unificada por linha/indústria/curva.
- Dificuldade em antecipar quebras de estoque e perdas por validade (produtos parados desde janeiro).
- Representantes sem acesso rápido a histórico por hospital/médico no campo (mobile), dependendo de repasses manuais.
- Integração limitada com ERP (sem APIs claras), exigindo importações/exportações manuais dos dados alocados sobre as vendas. 

### 1.3 Desafios do Projeto

Diante do cenário atual em que o negócio se encontra são observados alguns desafios que seriam enfrentados pela nossa equipe. Logo abaixo categorizamos e explicamos de forma mais detalhada sobre estes desafios.

#### Técnicos:

A construção de uma solução robusta e escalável exige a superação de desafios técnicos significativos, especialmente no que tange à integração de sistemas, ao tratamento de um grande volume de dados e a uma modelagem de dados que suporte análises complexas.

- Conectividade com Soft System/VIMAM 
    - Integração batch via arquivos / Explorar API (se possível) 
- Volume e variedade dos dados 
    - (14k SKUs no óptico; múltiplas linhas hospitalares com regras e SLA distintos).
- Modelagem de dados para histórico longo (vendas desde 2020), curva ABC por linha, políticas de estoque por indústria, controle de validade/lotes.

#### Operacionais:

No nível operacional, os desafios se concentram em assegurar que a solução seja segura, de fácil adoção pelos usuários e que os processos do dia a dia ocorram sem atritos, garantindo a integridade dos dados e a eficiência das equipes.

- Manter sigilo (dados sensíveis de preços/condições) e governança de acesso.
- Garantir usabilidade para representantes com diferentes níveis de alfabetização digital (uso em mobile dentro do hospital).

#### Negócio:

Do ponto de vista estratégico, o projeto deve estar estritamente alinhado às regras e exigências do negócio para garantir a sustentabilidade comercial e o cumprimento de acordos com parceiros.

- Respeitar exigências de estoque mínimo por indústria (ex: 90 dias) sob pena de perder condições comerciais.

### 1.4 Segmentação de Clientes

A estratégia comercial da RX Hospitalar é orientada por uma segmentação de clientes bastante clara, que direciona de forma eficiente seus esforços de mercado. O foco principal está no modelo **B2B (Business to Business)**, no qual a empresa atua de maneira consistente junto a diferentes frentes do setor de saúde. Entre os principais clientes estão **hospitais, clínicas, óticas** e instituições pertencentes tanto ao **setor público quanto ao privado**. Essa abordagem fortalece o posicionamento da organização como parceira estratégica para empresas que necessitam de soluções confiáveis e ágeis.  
Apesar da predominância do B2B, a RX também atende **nichos específicos no mercado B2C (Business to Consumer)**. Nesses casos, o relacionamento é direto com o consumidor final, geralmente em demandas mais personalizadas, como por exemplo a aquisição de **próteses mamárias** e outros produtos voltados para necessidades individuais.  
Outro ponto relevante da estratégia é a concentração da receita. A RX segue o princípio de **Pareto**, em que aproximadamente **20% dos clientes representam cerca de 80% do faturamento total**. Isso evidencia a importância de manter relacionamentos sólidos com clientes estratégicos, que não apenas garantem maior estabilidade financeira, mas também consolidam a posição da empresa em um mercado altamente competitivo.  
No contexto da solução de software proposta, os **usuários diretos** serão os **membros do setor administrativo responsáveis pela gestão de compras e estoque da RX Hospitalar**. Esse público, ao utilizar a ferramenta, terá sua rotina de análise otimizada, com ganhos de produtividade, precisão e eficiência na tomada de decisões.  
Assim, ao alinhar uma segmentação bem definida, uma atuação diversificada no B2B, nichos seletivos no B2C, aplicação de tecnologia para atender às necessidades internas, o que contribui para uma melhor sustentabilidade e crescimento contínuo da organização.

