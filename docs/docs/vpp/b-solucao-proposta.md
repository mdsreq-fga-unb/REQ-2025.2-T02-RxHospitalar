---
sidebar_label: "Solução proposta"
sidebar_position: 2
---
# Solução proposta

### 2.1 Objetivos do Produto

Com este produto visamos otimizar o processo de análise de planilhas de compras, estoque e vendas que são gerenciados pelo cliente, focando em reduzir o tempo dedicado neste processo de análise. Adicionado à este objetivo, também buscaremos garantir que a centralização dos dados seja disposta de forma mais intuitiva para que outras áreas também possam compreender e utilizar insights de forma estratégica, o que também diminui a carga de trabalho delegada ao setor de compras.
Os objetivos a seguir detalham especificamente o que o produto busca alcançar, transformando a gestão de compras e estoque em um processo mais ágil, intuitivo, estratégico e centralizado.

- **Reduzir o tempo** de análise de compras por **linha** de “horas/manhãs” para **minutos**.
- **Consolidar** faturado + pendências + estoque + validade em **visão única** por **produto/linha/ indústria/região**.
- **Evitar ruptura** e **perdas por validação** via **alertas** (estoque alvo, itens parados, lote a vencer). 
- **Apoiar o cliente** com informações: histórico por hospital/médico, mix já vendido, sugestões de cross-sell/recuperação de recorrência
- **Padronizar regras** de **curva ABC** e **estoque alvo** por **linha/indústria**, configuráveis. 
- **Preservar sigilo** e rastreabilidade de acesso. 

### 2.2 Características da Solução

Para materializar os objetivos definidos, a solução será construída sobre um conjunto de funcionalidades interconectadas. Cada componente foi pensado para resolver um desafio específico, desde a consolidação segura dos dados até a apresentação de insights acionáveis para as equipes de gestão e vendas. 

A seguir, detalhamos os pilares que compõem as características do produto:

- **Data Hub:** importação assistida de arquivos gerados pelo ERP, Planejamento de Recursos Empresariais (faturado, estoque, pendências) + cadastro de produtos/linhas/indústrias/regiões. 
- **Regras de estoque:** parametrização de estoque-alvo, curva ABC por linha, exceções por indústria (ex: 90 dias mínimos), estratégias de vendas de acordo com o estoque. 
- **Dashboards Operacionais:** Reposição por linha/indústria (priorização por criticidade ABC, cobertura , giro, validade); Produtos parados (dias sem saída) e a vencer (janelas Dias-30/Dias-60/Dias-90). 
- **Catálogo e busca:** (produto, linha, indústria, região) com cobertura atual e histórico por meses. 
- **Segurança e sigilo:** (Compras, Vendas, Representante, Gestor). 
- **Interface amigável para os Representantes:** visão por hospital/médico, últimas compras, sugestões.

#### Objetivos Específicos do Projeto:

| Código | Objetivo Específico   | Indicador de Sucesso                                |
|--------|-----------------------|-----------------------------------------------------|
| OE1    | Otimização de tempo   | Diminuir o tempo gasto nas análises em no mínimo 50%               |
| OE2    | Interface amigável    | Diminuir em 50% a quantidade de assistências dada à equipe de vendas (representantes)    |

### 2.3 Pesquisa de Mercado e Análise Competitiva

No mercado de softwares aplicados ao setor hospitalar e de saúde, destacam-se empresas que oferecem sistemas de gestão (ERPs) consolidados, como Totvs, SAP e Omie. Essas plataformas já disponibilizam soluções robustas, com módulos abrangentes e boa integração de funcionalidades administrativas. No entanto, quando analisadas sob a perspectiva de empresas de pequeno e médio porte do setor de venda de materiais hospitalares, especialmente em Brasília-DF e em torno, algumas fragilidades se tornam evidentes: 

A seguir, detalhamos os pilares que compõem as características do produto:

- **Totvs:** Apresenta alto custo de implementação e manutenção, o que dificulta o acesso de empresas menores. Além disso, sua estrutura complexa pode demandar treinamentos extensos e maior tempo de adaptação.
- **SAP:**  É uma solução completa e de grande escala, mas justamente por isso carece de flexibilidade para personalizações específicas. Seu processo de implantação é demorado e oneroso, o que inviabiliza muitas vezes a adoção em realidades menores.
- **Omie:** Apesar de ser mais acessível financeiramente que os dois anteriores, ainda é uma plataforma generalista, sem foco direto nas necessidades específicas do setor hospitalar, como o controle rígido de prazos de validade e rastreabilidade de materiais.

A solução proposta neste trabalho se diferenciará por:

- **Simplicidade e Customização:** O sistema será desenvolvido sob medida para as necessidades da empresa, evitando a sobrecarga de funções desnecessárias e priorizando usabilidade. 
- **Gestão de Estoque Especializada:** Haverá um controle preciso de materiais, incluindo prazos de validade e rastreabilidade, aspecto essencial no setor hospitalar. 
- **Custo Reduzido e Acessibilidade:** Por ser pensado para uma realidade interna, o software terá menor custo de implantação e manutenção, quando comparado a grandes ERPs, tornando-se mais viável para pequenas e médias empresas.
- **Eficiência Operacional:** A proposta visa otimizar fluxos de trabalho como controle de pedidos e organização de informações, reduzindo erros e aumentando a segurança nos processos.

### 2.4 Análise de Viabilidade
  Com os desafios identificados para este projeto, a viabilidade técnica do projeto é média, dado que alguns membros da equipe possuem experiências prévias com Python e bibliotecas que geram gráficos e consomem tabelas, como o Panda. Mesmo com a não possibilidade de conseguirmos realizar a integração com o software de gestão já utilizado pela empresa, a Soft System, pois é um sistema privado, o cliente nos garantiu a possibilidade de compartilhar o modelo de planilha usado pelo setor, que já é retirado do sistema. A lógica e regras já utilizadas pelo cliente já existem, nosso desafio é como serão transparecidos esses dados de forma mais rápida e intuitiva para o usuário.						
  Além disso, com informações advindas da nossa pesquisa, já há soluções parecidas com o nosso produto no mercado e que podem ser usadas como referência no desenvolvimento, ao invés de precisar começar tudo do zero. Com a utilização de bibliotecas como Panda, para os gráficos dos dashboards, e frameworks, como o Django, o projeto tende a ser mais fácil de ser executado pela disponibilidade de informação nos meios de pesquisa. A disposição, interesse e compromisso do grupo, até o presente momento, por inteiro são fatores que também demonstram uma boa perspectiva da execução do projeto.
  O prazo estimado de acordo com o planejamento das sprints é 3 meses, no máximo, de sprints de no mínimo 1 semana, com 5 horas de trabalho cada uma, por integrante do grupo. Cada sprint terá entregas incrementais ao sistema, que o irá deixando mais robusto e completo para o uso do cliente, com foco em analisar rapidamente diferentes planilhas de forma intuitiva, o que permitirá validações constantes e ajustes rápidos. O cronograma é considerado viável, mas aidna sim apertado, dado a ambientação da equipe com as tecnologias a serem usadas e conhecimento sobre manipulação de tabelas e dados, já que a equipe não possui processos semelhantes a esse feito previamente. 
  Todavia, mesmo com a restrição de tempo, a viabilidade do projeto é possível, pois a equipe de desenvolvimento usará uma base de dados já existente, regras de negócio já definidas, já há soluções parecidas no mercado que servirão como referência, utilizando o PowerBI por exemplo. Deixando o nosso desafio tornar esses dados mais fáceis e rápidos de serem analisados dentro de um sistema interno e seguro para o cliente.

### 2.5 Impacto da Solução
- **Qualidade de vida:** A implementação desta solução vai além da simples automação de tarefas, gerando valor tangível em múltiplas frentes da operação. Os impactos esperados abrangem desde a melhoria do ambiente de trabalho para os colaboradores até ganhos expressivos em eficiência e governança. A seguir, detalhamos os principais benefícios que o projeto trará para a organização.

- **Produtividade:** É esperado uma maior capacidade de execução das atividades no setor, uma vez que as atividades poderão ser feitas em um período de tempo mais curto e com um volume maior.

- **Padronização:** A execução do projeto permite uma padronização de operar. Isso, diminuiu os riscos de erro humano e mantém um nível de qualidade mais consistente.

- **Controle e Rastreabilidade:**  Registros e estruturas digitais facilitam auditorias, relatórios e acompanhamento em tempo real do funcionamento do setor.
