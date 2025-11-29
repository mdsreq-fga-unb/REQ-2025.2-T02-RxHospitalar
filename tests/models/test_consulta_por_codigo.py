#teste de RF03 - Consulta por código do produto
import pandas as pd
import pytest
from app.models.consulta_por_codigo import consulta_por_codigo
from app.models.carregar_dados import file

#teste para escolha da coluna na qual haverá a busca
def _escolher_coluna_codigo(cols):
  cand = ["Cód Original", "CODORIGINAL", "Código Original"]
  for c in cand:
    if c in cols:
      return c
  #fallback: primeira coluna que comece com "Cód" ou "COD"
  for c in cols:
    if str(c).lower().startswith(("cód", "cod", "códi", "código")):
      return c
  return None

#teste de um caso de sucesso para a aba estoque da planilha
def test_consulta_com_sucesso_aba_estoque():
    codigo_produto = "JG223R"
    resultado = consulta_por_codigo(codigo_produto)
    assert isinstance(resultado, dict)
    assert "df" in resultado and "card" in resultado
    df = resultado["df"]
    col = _escolher_coluna_codigo(df)
    assert col is not None
    assert df.iloc[0][col] == codigo_produto
    assert codigo_produto in resultado["card"]

def test_consulta_com_sucesso_aba_vendas_pendencia():
    codigo_produto = "MS005BRPT0619"
    resultado = consulta_por_codigo(codigo_produto)
    assert isinstance(resultado, dict)
    df = resultado["df"]
    col = _escolher_coluna_codigo(df)
    assert col is not None
    assert df.iloc[0][col] == codigo_produto

def test_consulta_por_codigo_retorno_padrao(monkeypatch, df_exemplo, tmp_path):
    # cria arquivo excel temporário com a aba simulada
    path = tmp_path / "fake.xlsx"
    with pd.ExcelWriter(path) as w:
        df_exemplo.to_excel(w, sheet_name="Estoque", index=False)
    # patch do caminho file usado pela função
    monkeypatch.setattr("app.models.consulta_por_codigo.file", str(path))
    resultado = consulta_por_codigo("JK489")
    assert isinstance(resultado, dict)
    df = resultado["df"]
    col = _escolher_coluna_codigo(df)
    assert col is not None
    assert df.iloc[0][col] == "JK489"
    assert "JK489" in resultado["card"]

@pytest.fixture
def df_exemplo():
    data = {
        "CODORIGINAL": ["JK489", "B456"],
        "DESCRICAO": ["1/1-TAMPA INFERIOR BÁSICO PRATEADA", "Produto 2"],
        "GRUPO": ["Eletrônicos", "Papelaria"],
        "ESTOQUE": [10, 5]
    }
    return pd.DataFrame(data)

def test_consulta_por_codigo_override(monkeypatch, df_exemplo, tmp_path):
    path = tmp_path / "fake.xlsx"
    with pd.ExcelWriter(path) as w:
        df_exemplo.to_excel(w, sheet_name="Estoque", index=False)

    #patch variável file usada pela função
    monkeypatch.setattr("app.models.consulta_por_codigo.file", str(path))

    #mock ExcelFile e read_excel para usar apenas nossa aba
    class FakeExcel:
        def __init__(self): self.sheet_names = ["Estoque"]
    monkeypatch.setattr("pandas.ExcelFile", lambda f: FakeExcel())
    monkeypatch.setattr("pandas.read_excel", lambda f, sheet_name, header=0, dtype=str: df_exemplo)

    resultado = consulta_por_codigo("JK489")
    assert isinstance(resultado, dict)
    assert "df" in resultado and "card" in resultado
    df = resultado["df"]
    col = _escolher_coluna_codigo(df.columns)
    assert col is not None
    assert "JK489" in df[col].values
    assert "JK489" in resultado["card"]
