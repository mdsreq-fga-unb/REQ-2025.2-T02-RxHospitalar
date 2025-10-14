---
sidebar_label: "Solução proposta"
sidebar_position: 2
---
# Solução proposta

### 2.1 Objetivos do Produto

Com este produto visamos otimizar o processo de análise de planilhas de compras, estoque e vendas que são gerenciadas pelo cliente, focando em reduzir o tempo dedicado neste processo de análise. Adicionado a este objetivo, também buscaremos garantir que a centralização dos dados seja disposta de forma mais intuitiva para que outras áreas também possam compreender e utilizar insights de forma estratégica, o que também diminui a carga de trabalho delegada ao setor de compras.
Este produto também visa transformar a gestão de compras, estoque e vendas da RX Hospitalar, tornando-a mais ágil, intuitiva e estratégica. Os objetivos gerais abaixo orientam o desenvolvimento da solução, e cada um deles está diretamente associado a um ou mais **Objetivos Específicos (OE)** do Projeto detalhados na [Tabela 1](#tabela-1), assegurando rastreabilidade e foco nos resultados mensuráveis.
<a id="OG1"></a> <br/>
**Objetivos Gerais (OG) do Projeto:** 
<a id="OG2"></a>
- **OG1 Reduzir drasticamente o tempo de análise de compras e estoque**  
Relacionado ao [OE1](#OE1) – Diminuir o tempo de análise em pelo menos 50%, substituindo horas de trabalho manual por minutos com o uso da ferramenta.
<a id="OG3"></a>
- **OG2 Centralizar e unificar as fontes de dados**  
Relacionado ao [OE3](#OE3) – Integrar em uma única visão as planilhas de faturado, pendências, estoque e validades, eliminando a consulta fragmentada.
<a id="OG4"></a>
- **OG3 Automatizar a gestão de estoque com base em regras parametrizáveis**  
Relacionado ao [OE5](#OE5) e [OE06](#OE6) – Implementar cálculos automáticos de estoque ideal, sugerir reposições com alta precisão e reduzir riscos de ruptura ou perdas por validade.
<a id="OG5"></a>
- **OG4 Oferecer uma interface intuitiva e acessível**  
Relacionado ao [OE2](#OE2) e [OE04](#OE4) – Disponibilizar filtros dinâmicos e visões personalizadas que permitam ao usuário acessar e analisar dados em menos de 5 minutos.
<a id="OG6"></a>
- **OG5 Garantir segurança e controle de acesso**  
Relacionado ao [OE7](#OE7) – Assegurar que apenas usuários autorizados tenham acesso a dados sensíveis, com zero vazamentos.
<a id="OG7"></a>
- **OG6 Prover insights estratégicos por cliente e vendedor**  
Relacionado ao [OE9](#OE9) – Oferecer visão analítica do histórico de compras por cliente, facilitando a identificação de padrões e oportunidades de venda.
- **OG7 Notificar proativamente sobre situações críticas**  
Relacionado ao [OE8](#OE8) – Alertar sobre produtos parados, com giro baixo ou próximos do vencimento.

### 2.2 Características da Solução

Para materializar os objetivos definidos, a solução será construída sobre um conjunto de funcionalidades interconectadas. Cada componente foi pensado para resolver um desafio específico, desde a consolidação segura dos dados até a apresentação de insights acionáveis para as equipes de gestão e vendas. 

A seguir, detalhamos os pilares que compõem as características do produto:

- **Data Hub:** importação assistida de arquivos gerados pelo ERP, Planejamento de Recursos Empresariais (faturado, estoque, pendências) + cadastro de produtos/linhas/indústrias/regiões. 
- **Regras de estoque:** parametrização de estoque-alvo, curva ABC por linha, exceções por indústria (ex: 90 dias mínimos), estratégias de vendas de acordo com o estoque. 
- **Dashboards Operacionais:** Reposição por linha/indústria (priorização por criticidade ABC, cobertura , giro, validade); Produtos parados (dias sem saída) e a vencer (janelas de 30, 60 ou 90 dias). 
- **Catálogo e busca:** (produto, linha, indústria, região) com cobertura atual e histórico por meses. 
- **Segurança e sigilo:** (Compras, Vendas, Representante, Gestor). 
- **Interface amigável para os Representantes:** visão por hospital/médico, últimas compras, sugestões.

#### Objetivos Específicos (OE) do Projeto:

<a id="tabela-1"></a> <a id="OE1"></a>
*Tabela 1: Objetivos Específicos do Projeto*
| Código | Objetivo Específico   | Indicador de Sucesso                                |
|--------|-----------------------|-----------------------------------------------------|
| OE1 <a id="OE2"></a>| Reduzir o tempo de análise de compras e estoque | Diminuir o tempo gasto nas análises em no mínimo 50% |
| OE2 <a id="OE3"></a> | Disponibilizar interface intuitiva para análise e consulta de dados | Diminuir em 50% a quantidade de assistências dada à equipe de vendas (representantes) |
| OE3 <a id="OE4"></a> | Centralizar dados das planilhas de itens faturado, pendente, estoque, consignado e pedidos em uma visão única. | Eliminar completamente a necessidade de consulta parcelada das 5 planilhas distintas usadas. |
| OE4 <a id="OE5"></a> | Implementar filtros dinâmicos por linha, produto, cliente e período (ex: últimos 4 meses). | O usuário consegue filtrar e visualizar dados pesquisados em menos de 5 minutos. |
| OE5 <a id="OE6"></a> | Automatizar o cálculo de estoque ideal <br/> com base na média de vendas dos últimos <br/> 4 meses, gerando sugestões automáticas de reposição e pedidos fracionados por caixas. | O sistema sugere uma reposição com 100% de precisão em relação à análise manual atual, com isso se espera obter uma redução de até 80% na necessidade de cálculos manuais de compra. |
| OE6 <a id="OE7"></a> | Permitir a visualização rápida de produtos abaixo do estoque mínimo (4 meses) e produtos parados. | Redução em 80% do risco de ruptura de estoque ou perda por validade. |
| OE7 <a id="OE8"></a> | Garantir sigilo e controle de acesso aos dados sensíveis (preços, clientes). | Apenas usuários autorizados acessam informações críticas; zero vazamentos.     |
| OE8 <a id="OE9"></a> | Notificar automaticamente os produtos que estão com giro baixo dentro do estoque comparado a sua média. | Dispor as informações dos produtos parados pelo menos nos últimos 3 meses. |
| OE9 | Oferecer uma visão analítica sobre o histórico de compras de cada cliente por período específico e produto específico. | Diminuir em 80% a carga de pesquisa e análise sobre produtos que saem mais para um determinado cliente. |

*Fonte: De autoria própria.*

### 2.3 Pesquisa de Mercado e Análise Competitiva

No mercado de softwares aplicados ao setor hospitalar e de saúde, destacam-se empresas que oferecem sistemas de gestão (ERPs) consolidados, como Totvs, SAP e Omie. Essas plataformas já disponibilizam soluções robustas, com módulos abrangentes e boa integração de funcionalidades administrativas. No entanto, quando analisadas sob a perspectiva de empresas de pequeno e médio porte do setor de venda de materiais hospitalares, especialmente em Brasília-DF e em torno, algumas fragilidades se tornam evidentes: 

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
A implementação desta solução vai além da simples automação de tarefas, gerando valor tangível em múltiplas frentes da operação. Os impactos esperados, detalhados abaixo, estão diretamente ligados à consecução dos **Objetivos Específicos (OE)** do Projeto [Tabela 1](#tabela-1) e abrangem desde a melhoria do ambiente de trabalho para os colaboradores até ganhos expressivos em eficiência e governança. A seguir, detalhamos os principais benefícios que o projeto trará para a organização.

- **Aumento da Produtividade e Eficiência Operacional**  
**Impacto:** Redução drástica do tempo dedicado à análise de dados e conexão entre as planilhas, permitindo que a equipe foque em atividades estratégicas.  
**Viabilizado por:** [OE1](#OE1) (Reduzir tempo de análise), [OE3](#OE3) (Centralizar dados) e [OE5](#OE5) (Automatizar cálculos de reposição).

- **Melhoria na Confiabilidade e Redução de Riscos**  
**Impacto:** Diminuição significativa do risco de ruptura de estoque, produtos parados e erros manuais, assegurando a continuidade do negócio e o cumprimento de SLAs.  
**Viabilizado por:** [OE6](#OE6) (Visualizar produtos abaixo do mínimo e parados) e [OE8](#OE8) (Notificação sobre  produtos em estado crítico).

- **Tomada de Decisão Estratégica e Baseada em Dados**  
**Impacto:** Acesso rápido a insights acionáveis sobre o histórico de compras dos clientes, performance de vendedores e sazonalidade, habilitando ações de cross-sell e recuperação de clientes.  
**Viabilizado por:** [OE4](#OE4) (Filtros dinâmicos) e [OE9](#OE9) (Visão analítica do histórico por cliente).

- **Fortalecimento da Governança e Segurança da Informação**  
**Impacto:** Controle rigoroso sobre o acesso a dados sensíveis (preços e clientes), garantindo conformidade e proteção do patrimônio informacional da empresa.  
**Viabilizado por:** [OE7](#OE7) (Garantir sigilo e controle de acesso).

- **Padronização e Qualidade de Vida no Trabalho**  
**Impacto:** Unificação de processos e linguagem, redução da carga mental operacional e provisionamento de uma ferramenta intuitiva, resultando em um ambiente de trabalho mais organizado e com menor estresse.  
**Viabilizado por:** [OE2](#OE2) (Interface intuitiva) e a sinergia de todos os OEs que eliminam tarefas manuais repetitivas do escopo.