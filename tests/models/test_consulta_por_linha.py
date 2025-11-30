#teste de RF04 - Consulta por linha do produto
import pandas as pd
import pytest
from app.models.consulta_por_linha import consulta_por_linha
from app.models.carregar_dados import file

# teste para escolha da coluna na qual haverá a busca
def _escolher_coluna_codigo(cols):
  cand = ["Grupo", "Sub Grupo Nível 1"]
  for c in cand:
    if c in cols:
      return c
  # para procurar colunas relacionadas
  for c in cols:
    if str(c).lower().startswith(("gru", "GRU", "Gru")):
      return c
  return None

#teste de um caso de sucesso para a aba estoque da planilha
def test_consulta_com_sucesso_aba_estoque():
    linha_produto = "BBRAUN"
    resultado = consulta_por_linha(linha_produto)
    assert isinstance(resultado, dict)
    assert "df" in resultado and "card" in resultado
    df = resultado["df"]
    col = _escolher_coluna_codigo(df)
    assert col is not None
    assert df.iloc[0][col] == linha_produto
    assert linha_produto in resultado["card"]

#teste de um caso de sucesso para a aba vendas_pendencia da planilha
def test_consulta_com_sucesso_aba_vendas_pendencia():
    linha_produto = "SMITH"
    resultado = consulta_por_linha(linha_produto)
    assert isinstance(resultado, dict)
    df = resultado["df"]
    col = _escolher_coluna_codigo(df)
    assert col is not None
    assert df.iloc[0][col] == linha_produto

#teste para o retorno sair conforme o esperado
def test_consulta_por_codigo_retorno_padrao(monkeypatch, df_exemplo, tmp_path):
    # cria arquivo excel temporário com a aba simulada
    path = tmp_path / "fake.xlsx"
    with pd.ExcelWriter(path) as w:
        df_exemplo.to_excel(w, sheet_name="Estoque", index=False)
    # patch do caminho file usado pela função
    monkeypatch.setattr("app.models.consulta_por_linha.file", str(path))
    resultado = consulta_por_linha("AAD")
    assert isinstance(resultado, dict)
    df = resultado["df"]
    col = _escolher_coluna_codigo(df)
    assert col is not None
    assert df.iloc[0][col] == "AAD"
    assert "AAD" in resultado["card"]

@pytest.fixture
def df_exemplo():
    data = {
        "CODORIGINAL": ["JK489", "B456"],
        "DESCRICAO": ["1/1-TAMPA INFERIOR BÁSICO PRATEADA", "Produto 2"],
        "GRUPO": ["AAD", "BBRAUN"],
        "ESTOQUE": [10, 5]
    }
    return pd.DataFrame(data)

#teste para consulta por codigo
def test_consulta_por_codigo_override(monkeypatch, df_exemplo, tmp_path):
    path = tmp_path / "fake.xlsx"
    with pd.ExcelWriter(path) as w:
        df_exemplo.to_excel(w, sheet_name="Estoque", index=False)

    #patch variável file usada pela função
    monkeypatch.setattr("app.models.consulta_por_linha.file", str(path))

    #mock ExcelFile e read_excel para usar apenas nossa aba
    class FakeExcel:
        def __init__(self): self.sheet_names = ["Estoque"]
    monkeypatch.setattr("pandas.ExcelFile", lambda f: FakeExcel())
    monkeypatch.setattr("pandas.read_excel", lambda f, sheet_name, header=0, dtype=str: df_exemplo)

    resultado = consulta_por_linha("BBRAUN")
    assert isinstance(resultado, dict)
    assert "df" in resultado and "card" in resultado
    df = resultado["df"]
    col = _escolher_coluna_codigo(df.columns)
    assert col is not None
    assert "BBRAUN" in df[col].values
    assert "BBRAUN" in resultado["card"]