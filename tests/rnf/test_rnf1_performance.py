import time
import pandas as pd
import pytest
from pathlib import Path
from app.models.carregar_dados import importar_arquivo
from app.utils.separar_por_data import separar_quantidade_por_data
from datetime import datetime
from dateutil.relativedelta import relativedelta

'''
#teste do tempo de resposta da análise período
@pytest.mark.performance
def test_rnf01_tempo_resposta_analise_periodo(monkeypatch, tmp_path):
    rows = 5000
    hoje = datetime.today()
    # distribui datas nos últimos 6 meses
    datas = [(hoje - relativedelta(months=i)).strftime("%Y-%m-%d") for i in range(6)]
    df_estoque = pd.DataFrame({
        "Cód Original": [f"C{i:05d}" for i in range(rows)],
        "Descrição": [f"Item {i}" for i in range(rows)],
        "DATASTATUS": [datas[i % 6] for i in range(rows)],
    })
    path = tmp_path / "estoque.xlsx"
    with pd.ExcelWriter(path) as w:
        df_estoque.to_excel(w, sheet_name="Estoque", index=False)
    monkeypatch.setattr("app.models.carregar_dados.file", str(path))
    t0 = time.perf_counter()
    resultado = separar_quantidade_por_data(df_estoque, n_meses=6)
    dt = time.perf_counter() - t0
    assert dt < 30.0, f"Análise excedeu o limite (dt={dt:.2f}s)"
    assert not resultado.empty
'''

#teste do tempo de importação inferior a 10 minutos
@pytest.mark.performance
def test_rnf01_tempo_importacao_xlsx_ate_10min(tmp_path):
    # Planilha com 1000 linhas (limite do RNF para integridade)
    rows = 1000
    df_estoque = pd.DataFrame({
        "Cód Original": [f"P{i:04d}" for i in range(rows)],
        "Descrição": [f"Produto {i}" for i in range(rows)],
        "Estoque": [i % 11 + 1 for i in range(rows)]
    })
    df_vendas = pd.DataFrame({
        "CODORIGINAL": [f"P{i:04d}" for i in range(rows)],
        "DATASTATUS": ["2024-10-01"] * rows,
        "QUANTIDADE": [1] * rows
    })
    path = tmp_path / "dados.xlsx"
    with pd.ExcelWriter(path) as w:
        df_estoque.to_excel(w, sheet_name="Estoque", index=False)
        df_vendas.to_excel(w, sheet_name="Vendas_Pendencia", index=False)
    requisitos = {
        "Estoque": ["Cód Original", "Descrição", "Estoque"],
        "Vendas_Pendencia": ["CODORIGINAL", "DATASTATUS", "QUANTIDADE"]
    }
    t0 = time.perf_counter()
    res = importar_arquivo(str(path), requisitos, check_integrity=True)
    dt = time.perf_counter() - t0
    assert res["ok"], f"Falha na importação: {res['erro']}"
    assert dt < 600.0, f"Importação excedeu 10 minutos (dt={dt:.2f}s)"
    # Integridade: número de linhas
    assert len(res["data"]["Estoque"]) == rows
    # Integridade: soma da coluna numérica
    soma_original = df_estoque["Estoque"].sum()
    soma_importada = res["integrity"]["Estoque"]["sums"]["Estoque"]
    assert soma_importada == soma_original

#teste de importação de csv sem quebras
@pytest.mark.performance
def test_rnf01_importacao_csv_integridade(tmp_path):
    rows = 1000
    df_csv = pd.DataFrame({
        "Cód Original": [f"C{i:04d}" for i in range(rows)],
        "Descrição": [f"Item {i}" for i in range(rows)],
        "Estoque": [2] * rows
    })
    path = tmp_path / "dados.csv"
    df_csv.to_csv(path, index=False)
    requisitos = {"__csv__": ["Cód Original", "Descrição", "Estoque"]}
    res = importar_arquivo(str(path), requisitos, check_integrity=True)
    assert res["ok"]
    assert len(res["data"]["__csv__"]) == rows
    soma_original = df_csv["Estoque"].sum()
    soma_importada = res["integrity"]["__csv__"]["sums"]["Estoque"]
    assert soma_importada == soma_original

#teste com importação de xlsx com coluna não numérica ignorada
@pytest.mark.performance
def test_rnf01_importacao_xlsx_coluna_nao_numerica_ignorada(tmp_path):
    df = pd.DataFrame({
        "Cód Original": ["A1", "A2"],
        "Descrição": ["X", "Y"],
        "TextoLivre": ["abc", "def"]
    })
    path = tmp_path / "base.xlsx"
    with pd.ExcelWriter(path) as w:
        df.to_excel(w, sheet_name="Estoque", index=False)
    req = {"Estoque": ["Cód Original", "Descrição", "TextoLivre"]}
    res = importar_arquivo(str(path), req, check_integrity=True)
    assert res["ok"]
    # Coluna não numérica não entra em sums
    assert "TextoLivre" not in res["integrity"]["Estoque"]["sums"]

#teste de importação com arquivo que não seja .csv ou .xlsx
@pytest.mark.performance
def test_rnf01_importacao_falha_extensao_invalida(tmp_path):
    p = tmp_path / "arquivo.txt"
    p.write_text("dummy")
    res = importar_arquivo(str(p), {"Estoque": ["Cód Original"]}, check_integrity=True)
    assert not res["ok"]
    assert "formato inválido" in res["erro"].lower()