---
sidebar_label: "MVP"
sidebar_position: 1
---

# MVP

O **MVP (Minimum Viable Product)** refere-se ao conjunto mínimo de funcionalidades que permite que o produto seja lançado e utilizado pelos clientes. Ele foca nos recursos essenciais necessários para testar o mercado e validar as principais hipóteses de valor de negócio.  
A tabela a seguir consolida todos os **[Requisitos Funcionais (RF)](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/requisitos-de-software/a-requisitos-funcionais)** e **[Requisitos Não Funcionais (RNF)](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/requisitos-de-software/b-requisitos-nao-funcionais)**, reunindo-os em um único quadro para facilitar a análise integrada entre as dimensões técnicas e de valor do produto.  
Cada requisito está diretamente relacionado aos **[Objetivos Gerais (OG)](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#21-objetivos-do-produto)** e **[Objetivos Específicos (OE)](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta/#22-caracter%C3%ADsticas-da-solu%C3%A7%C3%A3o)** definidos para o projeto, evidenciando como cada funcionalidade ou característica técnica contribui para o alcance dos resultados esperados.

<table className="requirements-table">
  <thead>
    <tr>
      <th>OG</th>
      <th>OE</th>
      <th>Descrição</th>
      <th>Requisito</th>
      <th>Priorização</th>
      <th>MVP</th>
    </tr>
  </thead>
  <tbody>

    <!-- === FUNCIONAIS === -->
    <tr className="functional"><td>OG1, OG3</td><td>OE01, OE05</td><td>Análise Base do Sistema</td><td>RF01</td><td>Must</td><td>✅</td></tr>
    <tr className="functional alt"><td>OG4, OG6</td><td>OE04, OE09</td><td>Filtros avançados</td><td>RF02</td><td>Must</td><td>✅</td></tr>
    <tr className="functional alt"><td>OG4, OG6</td><td>OE04, OE09</td><td>Filtros avançados</td><td>RF03</td><td>Must</td><td>✅</td></tr>
    <tr className="functional alt"><td>OG4, OG6</td><td>OE04, OE09</td><td>Filtros avançados</td><td>RF04</td><td>Must</td><td>✅</td></tr>
    <tr className="functional alt"><td>OG4, OG6</td><td>OE04, OE09</td><td>Filtros avançados</td><td>RF05</td><td>Must</td><td>✅</td></tr>
    <tr className="functional alt"><td>OG4, OG6</td><td>OE04, OE09</td><td>Filtros avançados</td><td>RF06</td><td>Must</td><td>✅</td></tr>

    <tr className="functional"><td>OG6</td><td>OE05, OE09</td><td>Análises Avançadas</td><td>RF07</td><td>Could</td><td>❌</td></tr>
    <tr className="functional"><td>OG6</td><td>OE05, OE09</td><td>Análises Avançadas</td><td>RF08</td><td>Could</td><td>❌</td></tr>
    <tr className="functional"><td>OG6</td><td>OE05, OE09</td><td>Análises Avançadas</td><td>RF09</td><td>Could</td><td>❌</td></tr>
    <tr className="functional"><td>OG6</td><td>OE05, OE09</td><td>Análises Avançadas</td><td>RF10</td><td>Could</td><td>❌</td></tr>
    <tr className="functional"><td>OG6</td><td>OE05, OE09</td><td>Análises Avançadas</td><td>RF11</td><td>Could</td><td>❌</td></tr>

    <tr className="functional alt"><td>OG7</td><td>OE06, OE08</td><td>Notificação sobre produtos em estado crítico</td><td>RF12</td><td>Should</td><td>✅</td></tr>
    <tr className="functional alt"><td>OG7</td><td>OE06, OE08</td><td>Notificação sobre produtos em estado crítico</td><td>RF13</td><td>Should</td><td>✅</td></tr>
    <tr className="functional alt"><td>OG7</td><td>OE06, OE08</td><td>Notificação sobre produtos em estado crítico</td><td>RF14</td><td>Should</td><td>✅</td></tr>

    <tr className="functional"><td>OG5</td><td>OE07</td><td>Autorização de Acesso</td><td>RF15</td><td>Should</td><td>❌</td></tr>
    <tr className="functional"><td>OG5</td><td>OE07</td><td>Autorização de Acesso</td><td>RF16</td><td>Should</td><td>❌</td></tr>

    <!-- === NÃO FUNCIONAIS === -->
    <tr className="nonfunctional"><td>OG1</td><td>OE01</td><td>Performance</td><td>RFN01</td><td>Must</td><td>✅</td></tr>
    <tr className="nonfunctional"><td>OG4</td><td>OE02, OE04</td><td>Usabilidade</td><td>RFN02</td><td>Must</td><td>✅</td></tr>
    <tr className="nonfunctional"><td>OG2</td><td>OE03</td><td>Compatibilidade</td><td>RFN03</td><td>Must</td><td>✅</td></tr>
    <tr className="nonfunctional alt"><td>OG5</td><td>OE07</td><td>Segurança</td><td>RFN04</td><td>Should</td><td>❌</td></tr>
    <tr className="nonfunctional"><td>OG3, OG7</td><td>OE06, OE08</td><td>Confiabilidade</td><td>RFN05</td><td>Must</td><td>✅</td></tr>
    <tr className="nonfunctional alt"><td>OG2, OG3</td><td>OE03</td><td>Escalabilidade</td><td>RFN06</td><td>Should</td><td>❌</td></tr>
    <tr className="nonfunctional alt"><td>OG2, OG3, OG5</td><td>OE05, OE07</td><td>Manutenibilidade</td><td>RFN07</td><td>Should</td><td>❌</td></tr>
    <tr className="nonfunctional alt"><td>OG6, OG7</td><td>OE08</td><td>Manter Histórico de Notificações</td><td>RFN08</td><td>Could</td><td>❌</td></tr>

  </tbody>
</table>

#### 🔎 Legenda da Tabela

- **OG:** [Objetivos Gerais do Projeto](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta#21-objetivos-do-produto)  
- **OE:** [Objetivos Específicos do Projeto](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/b-solucao-proposta/#22-caracter%C3%ADsticas-da-solu%C3%A7%C3%A3o)  
- **RF:** [Requisitos Funcionais (RF)](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/requisitos-de-software/a-requisitos-funcionais) 
- **RNF:** [Requisitos Não Funcionais (RNF)](https://mdsreq-fga-unb.github.io/REQ-2025.2-T02-RxHospitalar/docs/visao-produto-projeto/requisitos-de-software/b-requisitos-nao-funcionais)  
- **Priorização:** nível de importância do requisito conforme o método **MoSCoW** (*Must*, *Should*, *Could*).  
- **MVP:** indica se o requisito faz parte do **escopo mínimo do produto** (`✅` = incluído | `❌` = fora do MVP).