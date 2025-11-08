#teste de RF04 - Consulta por linha do produto
import pandas as pd
from app import consulta_por_linha

#critério de aceitação: utilizar a linha escolhida do produto pelo usuário para listar
def test_consulta_por_linha_com_sucesso():
  df = pd.DataFrame([{}])

  result = consulta_por_linha(df, "X")

  assert result is not None
  assert result["linha"] == ""
  assert result["nome"] == ""
  assert result["código"] == ""

def test_consulta_por_linha_nao_achada():
  df = pd.DataFrame([{}])

  result = consulta_por_linha(df, "BLABLA")

  assert result is not None
  assert ValueError("Linha de produto não encontrada")

def test_consulta_por_linha_int():
  df = pd.DataFrame([
    {"codigo": "456", "nome": "Dexametasona", "linha": 123}
  ])

  result = consulta_por_linha(df, 123)

  assert result is not None
  raise TypeError("A linha não pode ser composta por números")

def test_consulta_por_linha_vazia():
  df = pd.DataFrame([
    {"codigo": "456", "nome": "Dexametasona", "linha": ""}
  ])

  result = consulta_por_linha(df, "")

  assert result is not None
  raise ValueError("A linha do produto não pode estar vazia")  


