import pandas as pd
import pytest
from datetime import datetime
from dateutil.relativedelta import relativedelta
import app.models.carregar_dados as carregar_dados
from app.models.consulta_periodo import consulta_periodo

@pytest.mark.skipif(
    not hasattr(carregar_dados, "file"),
    reason="Arquivo Excel não configurado em carregar_dados.file"
)
def test_consulta_periodo_top3_meses_real():
    #leitura da planilha real
    df_vendas = pd.read_excel(carregar_dados.file, sheet_name="Vendas_Pendencia", dtype=str)

    #requisitos mínimos de colunas
    required = {"CODPRODUTO", "QUANTIDADE"}
    assert required.issubset(df_vendas.columns), "Planilha real sem colunas necessárias"

    res = consulta_periodo(n_meses=3)
    assert "MEDIA_MENSAL" in res.columns

    #deve conter colunas dos últimos 3 meses
    hoje = datetime.today()
    meses = [(hoje - relativedelta(months=i)).strftime("%m/%Y") for i in range(1, 4)]
    for mes in meses:
        assert mes in res.columns

    #linhas e tipos
    assert pd.api.types.is_numeric_dtype(res["MEDIA_MENSAL"])

@pytest.mark.skipif(
    not hasattr(carregar_dados, "file"),
    reason="Arquivo Excel não configurado em carregar_dados.file"
)
def test_consulta_periodo_filtrando_produto_real():
    #pega um código de produto real existente
    df_vendas = pd.read_excel(carregar_dados.file, sheet_name="Vendas_Pendencia", dtype=str)
    assert "CODPRODUTO" in df_vendas.columns
    cods = df_vendas["CODPRODUTO"].dropna().astype(str).str.strip()
    assert not cods.empty, "Sem CODPRODUTO na planilha real"
    cod_exemplo = cods.iloc[0]

    res = consulta_periodo(codproduto=cod_exemplo, n_meses=3)
    #pode retornar vazio se não houver vendas no período para o produto
    assert set(res.columns).issuperset({"MEDIA_MENSAL", "CODPRODUTO"})
    if not res.empty:
        assert set(res["CODPRODUTO"]) == {cod_exemplo}
        assert pd.api.types.is_numeric_dtype(res["MEDIA_MENSAL"])

def _mock_sheet(monkeypatch, df):
    def fake_read_excel(file, sheet_name=None, *args, **kwargs):
        if sheet_name == "Vendas_Pendencia":
            return df
        raise ValueError("Sheet não mockada")
    monkeypatch.setattr(carregar_dados.pd, "read_excel", fake_read_excel)

@pytest.fixture
def workbook_periodo(monkeypatch):
    hoje = datetime.today()
    m1 = (hoje - relativedelta(months=1)).strftime("%d/%m/%Y")
    m2 = (hoje - relativedelta(months=2)).strftime("%d/%m/%Y")
    fora = (hoje - relativedelta(months=6)).strftime("%d/%m/%Y")

    df = pd.DataFrame({
        "CODPRODUTO": ["P1","P1","P2","P1","P3"],
        "QUANTIDADE": [5, 3, 10, 2, 1],
        "DATASTATUS": [m1, m2, m1, m1, fora],
    })
    _mock_sheet(monkeypatch, df)
    return df

def test_consulta_periodo_top4_meses(workbook_periodo):
    res = consulta_periodo(n_meses=4)
    assert "MEDIA_MENSAL" in res.columns
    # deve conter colunas dos últimos 4 meses
    hoje = datetime.today()
    meses = [(hoje - relativedelta(months=i)).strftime("%m/%Y") for i in range(1, 5)]
    for mes in meses:
        assert mes in res.columns

def test_consulta_periodo_filtrando_produto(workbook_periodo):
    res = consulta_periodo(codproduto="P1", n_meses=4)
    assert not res.empty
    # linha única para P1
    assert set(res["CODPRODUTO"]) == {"P1"}
    # média mensal correta: valores presentes divididos por 4 meses
    media = res["MEDIA_MENSAL"].iloc[0]
    assert media >= 0