---
sidebar_label: "Ata N.º15 | 20/11"
sidebar_position: 15
---

# ATA N.º15 | 20/11

**Disciplina:** Requisitos de Software  
**Data:** 20/11/2025  
**Horário:** 21:29
**Local:** Microsoft Teams   
[Evidencia](https://teams.microsoft.com/v2/)
---

## Participantes

**Integrantes do Grupo:**
- Amanda de Moura
- Beatriz Figueiredo dos Santos
- Davi Marques do Egito Coelho
- Samuel Rodrigues Viana Lobo

**Ausentes:**
- Eduardo Oliveira Valadares
- Gabriel Augusto Vilarinho Viana Rocha (participação assíncrona)

---

## Objetivos da Reunião
- Acompanhar o andamento das tasks do backend e frontend.
- Planejar as próximas ações para viabilizar o teste de usuário e a entrega da versão estável do sistema.

---

## Principais Pontos Abordados

### 1. Padronização de nomenclaturas e requisito de “Compras Inteligentes” (Samuel)
**Discussão:**
- Samuel trabalhou no requisito de “compras inteligentes”, que analisa a saída mensal de produtos, calcula média, verifica estoque disponível e gera sugestão de compra.
- Durante o desenvolvimento, identificou inconsistências de nomenclatura (funções em português/inglês, nomes de variáveis e arquivos, planilha chamada “testes” etc.).
- Realizou a padronização para português em nomes de funções, documentos e arquivos, visando evitar retrabalho e facilitar o entendimento do grupo.
- Houve problemas com testes que não estavam passando 100% e com o nome do diretório/planilha, que acabou voltando ao nome anterior em algum momento. O padrão correto foi enviado no Discord para o grupo adotar.

**Justificativa**:  
- Padronizar agora evita conflitos futuros, principalmente na integração entre planilhas, diretórios e funções que dependem de nomes consistentes.

**Decisão:**  
- Samuel seguirá no requisito de compras inteligentes e na tarefa de atualização de datas de reuniões do backend.

### 2. Estrutura do requisito de “Compras Inteligentes” para o front (Amanda & Samuel)

**Discussão:**

- Amanda perguntou como o requisito funcionará para poder desenvolver o front.
- Samuel explicou que será retornado um *dataframe* com, aproximadamente, as colunas:
    - Código do produto
    - Nome do produto
    - Saída por mês (para os meses definidos)
    - Média de saída
    - Estoque atual
    - Sugestão de compra
- “Sugestivo” corresponde à sugestão de compra.

**Justificativa:**

- O front necessita de clareza sobre o formato dos dados para exibir corretamente as informações da sugestão de compra inteligente.

**Decisão:**

- Backend retornará um *dataframe* com os campos descritos.
- Front será desenhado considerando essa estrutura de dados.

---

### 3. Atividades de testes, branches e configuração do Pytest (Davi)

**Discussão:**

- Davi fez alterações na documentação e configurou o arquivo `pytest.ini` (arquivo de configuração de testes), abrindo PR para inclusão na branch `experiments` e posterior integração.
- Revisou PRs de Beatriz e Gabriel e comentou em documentos.
- Criou branch para RF8 e RF9; ia começar o desenvolvimento, mas os testes quebraram devido à mudança do nome da planilha feita por Samuel (precisou ajustar localmente).
- Explicou a diferença entre branch de integração e developer: integração funciona como salvaguarda adicional antes da `main`, evitando que quebras de testes cheguem diretamente à branch principal.

**Justificativa:**

- A branch de integração adiciona uma camada de segurança para o fluxo de desenvolvimento.
- Arquivo de configuração do Pytest permite definir cobertura mínima de testes, alinhando-se ao que foi especificado como requisito de qualidade.

**Decisão:**

- Manter a branch de integração como etapa intermediária antes da `main`.
- Prosseguir com a configuração do Pytest levando em conta uma cobertura mínima a ser alinhada com o grupo.

---

### 4. Débito de RF5 e RF6 e replanejamento (Amanda & Davi)

**Discussão:**

- Amanda ressaltou que há um débito de RF5 e RF6, atrasado em cerca de 9 dias.
- Esses requisitos são importantes para a primeira versão estável a ser avaliada pelo cliente (Arthur) e para o teste de usuário.
- Davi sugeriu que, caso Eduardo não consiga entregar, ele e Samuel podem assumir: Davi ficaria com RF5 e Samuel com RF6, para garantir pelo menos até o RF6 pronto.

**Justificativa:**

- É necessário concluir essas funcionalidades para viabilizar o teste de usuário e ter material concreto para a apresentação da unidade 10 e para cumprir o processo RUP/RAD (testes com usuário).

**Decisão:**

- Amanda conversará com Eduardo sobre os atrasos.
- Caso não haja evolução, será feito remanejamento: Davi e Samuel assumirão RF5 e RF6, respectivamente.

---

### 5. Histórias de usuário, requisitos funcionais e roadmap (Amanda)

**Discussão:**

- Amanda conectou histórias de usuário aos requisitos funcionais, mas encontrou dificuldade porque antes estavam ligadas apenas a objetivos específicos.
- Cada história de usuário, no roadmap, possui (ou deve possuir) uma sub-issue correspondente a um requisito funcional.
- Nem todas as histórias de usuário ficaram claramente conectadas a um requisito funcional; Amanda pediu revisão de Samuel como PO.

**Justificativa:**

- É importante que histórias de usuário, objetivos específicos e requisitos funcionais estejam coerentes entre si, tanto para o entendimento interno quanto para apresentação ao professor.

**Decisão:**

- Samuel revisará a ligação entre histórias de usuário, objetivos específicos e requisitos funcionais.
- Ajustes serão feitos para tornar a visualização mais clara no roadmap.

---

### 6. Dashboard e sugestão de compra inteligente no front (Amanda)

**Discussão:**

- Amanda iniciou a página de dashboard em Python, responsável por exibir gráficos e a sugestão de compra inteligente.
- Dúvida principal: como apresentar a sugestão de compra ao Arthur de forma clara e intuitiva. Considerou:
    - Uso de gráficos;
    - Uso de cards com síntese da análise, exibindo diretamente os produtos com estoque baixo/zerado e a sugestão de compra.
- Beatriz entendeu a proposta como “trazer nos cards a análise que ele faria a partir dos gráficos”, ou seja, já apresentar a interpretação dos dados.
- Concluiu-se que se trata de uma sugestão, uma análise pronta, mas que o cliente continua livre para analisar por conta própria.

**Justificativa:**

- O requisito de sugestão de compra inteligente tem alto valor de negócio. É fundamental que a interface facilite o entendimento do cliente.

**Decisão:**

- Seguir com a ideia de apresentar, além de gráficos, componentes (como cards) que evidenciem as principais sugestões de compra.
- Amanda continuará explorando o layout da página de dashboard com foco na clareza para o cliente.

---

### 7. Gráfico de clientes e parte de vendedores (Beatriz)

**Discussão:**

- Beatriz reestruturou o protótipo do gráfico de clientes por produto, simplificando a visualização e destacando as informações mais importantes logo de início, a partir do feedback do grupo e do PO.
- Intenção de dar continuidade ao estilo do gráfico atual e desenvolver gráficos relacionados a vendedores.

**Justificativa:**

- Melhorar a clareza visual dos gráficos aumenta a utilidade da ferramenta para o cliente.

**Decisão:**

- Beatriz seguirá aprimorando o gráfico de clientes e, posteriormente, a parte de vendedores, conforme disponibilidade e prioridades do projeto.

---

### 8. Cobertura de testes (90% vs. 80%) e “módulos de regra de negócio”

**Discussão:**

- Davi sugeriu reduzir o valor prometido para 80%, por ser mais realista e alinhar melhor expectativas do documento com a prática.

**Justificativa:**

- É preferível prometer uma cobertura de testes alcançável e eventualmente superar a meta, em vez de não cumprir o que foi especificado, o que pode impactar negativamente na avaliação do professor.

**Decisão:**

- Grupo tende a ajustar a cobertura mínima para 80% no documento (a ser confirmado e atualizado).
- Davi utilizará o Discord para formalizar essa decisão e ajustar o arquivo de configuração do Pytest conforme o valor acordado.

---

### 9. Uso de TDD e coerência com o processo descrito no DoD

**Discussão:**

- No documento (DoD), está indicado que o código deve ser desenvolvido com TDD.
- Na prática, o TDD vem sendo aplicado apenas no backend, o que gerou preocupação no Davi quanto à coerência com o que será avaliado pelo professor (alinhamento entre processo descrito e processo de fato).
- Beatriz inicialmente argumentou que front e back seguem processos diferentes (RAD e XP), mas Amanda pontuou que o projeto é um só e que a segmentação pode não fazer sentido na perspectiva da avaliação.
- Discutiu-se a possibilidade de não deixar explicitamente prometido que todos os módulos (incluindo front) seriam implementados com TDD, para evitar questionamentos.

**Justificativa:**

- Evitar inconsistências entre o processo “no papel” e o processo realmente utilizado no desenvolvimento, o que pode resultar em perda de pontos na avaliação.

**Decisão:**

- Ajustar o documento para não prometer TDD de forma ampla para todo o projeto; deixar claro que TDD está sendo aplicado principalmente no backend.
- Rever o texto do DoD para garantir coerência com a prática atual.

---

### 10. Teste de usuário e necessidade de mostrar dados importados ao cliente (RAD)

**Discussão:**

- Amanda reforçou que, dentro do processo RAD, após o *design*, há a fase de teste com usuário e que isso precisa acontecer antes da apresentação da unidade 3.
- Para viabilizar esse teste, é necessário que a importação de dados já esteja aparecendo minimamente no dashboard (mesmo que sem todos os gráficos prontos).
- Beatriz sugeriu que, como já existe importação de dados, poderia ser mostrado algo simples como uma tabela com os dados importados no dashboard, apenas para que o Arthur veja que a funcionalidade está operando.
- Amanda concordou que não precisa estar tudo perfeito, mas deve haver “algo” visível para o cliente interagir.
- Também foi levantado que, se possível, seria interessante fazer funcionar minimamente o componente de filtros (filtro por linha, código original e status do produto), pois foi algo prometido para a primeira fase de teste de usuário.

**Justificativa:**

- O teste de usuário é fundamental para o processo definido (RAD) e para colher feedback do Arthur, devendo ocorrer com alguma interface funcional.

**Decisão:**

- Amanda ficará responsável por tentar:
    - Fazer aparecer no dashboard ao menos uma visualização simples (tabela) com os dados importados.
- Caso a implementação se mostre muito complexa no prazo, será priorizada a parte mais crítica e viável para o teste de usuário.

---

## Próximos Passos (se forem elencados na reunião)
1. **Samuel**
    - Dar continuidade ao requisito de compras inteligentes, garantindo o *dataframe* com as colunas acordadas.
    - Manter a padronização dos nomes de arquivos, planilhas e funções e orientar o grupo quanto ao padrão.
    - Possível divisão de tarefas de RF5/RF6 caso Eduardo não consiga entregar.
2. **Davi**
    - Ajustar e manter o arquivo de configuração do Pytest, considerando a cobertura mínima acordada (provável 80%).
    - Prosseguir com planejamento e implementação dos RF8 e RF9, bem como testes associados.
    - Ajudar no replanejamento caso RF5/RF6 sejam redistribuídos.
    - Atualizar documento para refletir corretamente o uso de TDD.
3. **Amanda**
    - Revisar, junto com Samuel, a ligação entre histórias de usuário, requisitos funcionais e objetivos específicos no roadmap.
    - Continuar o desenvolvimento da página de dashboard, priorizando:
        - Exibição mínima dos dados importados (tabela ou equivalente).
        - Estudo da melhor forma de apresentar a sugestão de compra inteligente (cards, gráficos, etc.).
4. **Beatriz**
    - Continuar refinando o gráfico de clientes (melhorias de clareza e estilo).
    - Planejar gráfico/visualização para vendedores, mantendo consistência visual.
5. **Grupo em geral**
    - Ajustar documentos (DoD) para refletir adequadamente uso de TDD .

---

## Encaminhamentos Finais
Foi reforçada a importância de:
- Manter consistência entre o processo descrito na documentação e o aplicado na prática (TDD, cobertura de testes, RAD).
- Priorizar requisitos de maior valor de negócio (especialmente sugestão de compra inteligente, consultas diretas e importação de dados).
- Garantir, no curto prazo, uma versão minimamente utilizável do dashboard para que o cliente possa realizar testes de usuário e fornecer feedback.

---

**Encerramento da reunião:** 22:10  
**Duração:** Aproximadamente 0h40 
**Responsável pela redação da ata:** Beatriz Figueiredo dos Santos
