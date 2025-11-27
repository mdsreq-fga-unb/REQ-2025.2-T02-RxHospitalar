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

# teste do caso de sucesso para a busca de um grupo
def test_consulta_por_linha_com_sucesso_grupo():
  df0 = pd.read_excel(file, sheet_name=0, header=0, dtype=str)
  col = _escolher_coluna_codigo(df0.columns)
  assert col is not None, "Nenhuma coluna da linha encontrada"
  linha_produto = "BBRAUN"
  result = consulta_por_linha(linha_produto)
  assert result is not None
  assert result["Grupo"] == linha_produto

# teste do caso de sucesso para a busca de um subgrupo
def test_consulta_por_linha_com_sucesso_sub_grupo():
  df0 = pd.read_excel(file, sheet_name=0, header=0, dtype=str)
  col = _escolher_coluna_codigo(df0.columns)
  assert col is not None, "Nenhuma coluna da linha encontrada"
  linha_produto = "IV ACESS"
  result = consulta_por_linha(linha_produto)
  assert result is not None
  assert result["Sub Grupo Nível 1"] == linha_produto

# teste para linha não encontrada/cadastrada
def test_consulta_por_linha_nao_achada():
  with pytest.raises(ValueError, match="A linha não foi encontrada"):
    consulta_por_linha("INEXISTENTE")

# teste para consulta vazia de linha
def test_consulta_por_linha_vazio():
  with pytest.raises(ValueError, match="A linha não foi encontrada"):
    consulta_por_linha("")