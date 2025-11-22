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
  df0 = pd.read_excel(file, sheet_name=0, header=0, dtype=str)
  col = _escolher_coluna_codigo(df0.columns)
  assert col is not None, "Nenhuma coluna de código encontrada"
  codigo_produto = "JG223R"
  result = consulta_por_codigo(codigo_produto)
  assert result is not None
  assert result["Cód Original"] == codigo_produto

#teste de um caso de sucesso para a aba vendas da planilha
def test_consulta_com_sucesso_aba_vendas_pendencia():
  df0 = pd.read_excel(file, sheet_name=0, header=0, dtype=str)
  col = _escolher_coluna_codigo(df0.columns)
  assert col is not None, "Nenhuma coluna de código encontrada"
  codigo_produto = "MS005BRPT0619"
  result = consulta_por_codigo(codigo_produto)
  assert result is not None
  assert result["CODORIGINAL"] == codigo_produto

#teste para código original não encontrado/cadastrado
def test_consulta_codigo_nao_achado():
  with pytest.raises(ValueError, match="O código não foi encontrado"):
    consulta_por_codigo("X987654321")

#teste para consulta vazia de código original
def test_consulta_codigo_vazio():
  with pytest.raises(ValueError, match="O código não foi encontrado"):
    consulta_por_codigo("")

class MockExcelFile:
    sheet_names = ["Estoque", "Vendas_Pendencia", "Consignado"]

def _mock_df(sheet, *args, **kwargs):
    if sheet == "Estoque":
        return pd.DataFrame({
            "Cód Original": ["JG223R", "ABC"],
            "CODORIGINAL": ["JN0123", "99999"]
        })
    elif sheet == "Vendas_Pendencia":
        return pd.DataFrame({
            "Cód Original": ["XYZ", "MS005BRPT0619"],
            "CODORIGINAL": ["MS005BRPT0619", "JG223R"]
        })
    elif sheet == "Consignado":
        return pd.DataFrame({
            "Cód Original": [],
            "CODORIGINAL": []
        })
    else:
        return pd.DataFrame({
            "Cód Original": [],
            "CODORIGINAL": []
        })

@pytest.fixture
def monkeypatched_consulta(monkeypatch):
    # Mock para file (deve ser string ou path fictícia se demandado, mas só importa para interceptação)
    monkeypatch.setattr("app.models.consulta_por_codigo.file", "mock_path.xlsx")
    monkeypatch.setattr("pandas.ExcelFile", lambda f: MockExcelFile())
    monkeypatch.setattr("pandas.read_excel", lambda file, sheet_name, header, dtype: _mock_df(sheet_name))

def test_consulta_por_codigo_com_sucesso_aba_estoque(monkeypatched_consulta):
    codigo_produto = "JG223R"
    result = consulta_por_codigo(codigo_produto)
    assert result is not None
    # O resultado pode estar em qualquer coluna de código, pois depende de onde foi encontrado
    assert codigo_produto in result.values

def test_consulta_por_codigo_com_sucesso_aba_vendas_pendencia(monkeypatched_consulta):
    codigo_produto = "MS005BRPT0619"
    result = consulta_por_codigo(codigo_produto)
    assert result is not None
    assert result["CODORIGINAL"] == codigo_produto

def test_consulta_por_codigo_nao_achada(monkeypatched_consulta):
    with pytest.raises(ValueError, match="O código não foi encontrado"):
        consulta_por_codigo("X987654321")

def test_consulta_por_codigo_vazio(monkeypatched_consulta):
    with pytest.raises(ValueError, match="O código não foi encontrado"):
        consulta_por_codigo("")
