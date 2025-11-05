#teste de RF03 - Consulta por código do produto
import pandas as pd
from app import consulta_por_codigo

#critério de aceitação: utilizar o código original do produto para listar o produto
def test_consulta_por_codigo_com_sucesso():
  df = pd.DataFrame([
    {"codigo": "123", "nome": "Dipirona", "linha": "ABC"},
    {"codigo": "456", "nome": "Dexametasona", "linha": "DEF"}
  ])

  result = consulta_por_codigo(df, "123")

  assert result is not None 
  assert result["codigo"] == "123"
  assert result["nome"] == "Dipirona"
  assert result["linha"] == "ABC"

def test_consulta_por_codigo_nao_achada():
  df = pd.DataFrame([
    {"codigo": "456", "nome": "Dexametasona", "linha": "DEF"}
  ])

  result = consulta_por_codigo(df, "X987654321")

  assert result is not None 
  assert ValueError("Código não encontrado")  

def test_consulta_por_codigo_string():
  df = pd.DataFrame([
    {"codigo": "456", "nome": "Dexametasona", "linha": "DEF"}
  ])

  result = consulta_por_codigo(df, "AS12312")

  assert result is not None
  raise TypeError("O código é composto apenas por números inteiros")

def test_consulta_por_codigo_vazio():
  df = pd.DataFrame([
    {"codigo": "", "nome": "Dexametasona", "linha": "DEF"}
  ])

  result = consulta_por_codigo(df, "")

  assert result is not None
  raise ValueError("O código não pode estar vazio")  