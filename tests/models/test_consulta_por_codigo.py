#teste de RF03 - Consulta por código do produto
import pandas as pd
import pytest
from app.models.consulta_por_codigo import consulta_por_codigo
from app.models.data_loader import file

def _pick_code_column(cols):
  cand = ["Cód. Original", "Cód Produto", "Cód. Produto", "COD", "Código"]
  for c in cand:
    if c in cols:
      return c
  # fallback: primeira coluna que comece com "Cód" ou "COD"
  for c in cols:
    if str(c).lower().startswith(("cód", "cod", "códi", "código")):
      return c
  return None

def test_consulta_por_codigo_com_sucesso():
  df0 = pd.read_excel(file, sheet_name=0, header=0, dtype=str)
  col = _pick_code_column(df0.columns)
  assert col is not None, "Nenhuma coluna de código encontrada na primeira aba"
  codigo_produto = "SK020BRPT"
  result = consulta_por_codigo(codigo_produto)
  assert result is not None
  assert result["Cód. Original"] == codigo_produto

def test_consulta_por_codigo_nao_achada():
  with pytest.raises(ValueError, match="O código não foi encontrado"):
    consulta_por_codigo("X987654321")

def test_consulta_por_codigo_vazio():
  with pytest.raises(ValueError, match="O código não foi encontrado"):
    consulta_por_codigo("")