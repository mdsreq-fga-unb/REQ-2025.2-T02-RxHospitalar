from app.models.consulta_performance import consulta_performance
import pandas as pd
import pytest
from tests.models.test_consulta_principais_clientes import _mock_book_clientes
from datetime import datetime
from app.models.consulta_performance import consulta_performance
import app.models.carregar_dados as carregar_dados

def test_performance_vendedor_real():
    df_perf = consulta_performance()

    #carrega vendas reais
    df_vendas = pd.read_excel(
        carregar_dados.file,
        sheet_name="Vendas_Pendencia",
        dtype=str
    )

    #reproduz a mesma lógica da função
    df_vendas["DATASTATUS"] = pd.to_datetime(
        df_vendas["DATASTATUS"],
        errors="coerce",
        dayfirst=False,
    )
    hoje = pd.Timestamp(datetime.today().date())
    um_mes_atras = hoje - pd.DateOffset(months=1)

    mask = (df_vendas["DATASTATUS"] >= um_mes_atras) & (df_vendas["DATASTATUS"] <= hoje)
    df_periodo = df_vendas[mask].copy()

    if df_periodo.empty:
        #se não tem vendas no período, o resultado deve ser DF vazio com as mesmas colunas
        assert df_perf.empty
        assert set(df_perf.columns) == {"CODVENDEDOR", "QUANTIDADE"}
        return

    df_periodo["QUANTIDADE"] = df_periodo["QUANTIDADE"].astype(float)

    df_expected = (
        df_periodo.groupby("CODVENDEDOR")["QUANTIDADE"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    df_expected.columns = ["CODVENDEDOR", "QUANTIDADE"]

    #colunas e limite
    assert set(df_perf.columns) == {"CODVENDEDOR", "QUANTIDADE"}
    assert len(df_perf) <= 5

    #vendedores retornados têm vendas no período
    vends_ret = set(df_perf["CODVENDEDOR"].astype(str).str.strip())
    vends_exp = set(df_expected["CODVENDEDOR"].astype(str).str.strip())
    assert vends_ret.issubset(vends_exp)

    #confere as somas para os vendedores em comum
    merged = df_perf.merge(df_expected, on="CODVENDEDOR", suffixes=("_resp", "_exp"))
    assert all(abs(merged["QUANTIDADE_resp"] - merged["QUANTIDADE_exp"]) < 1e-6)

@pytest.fixture
def workbook_performance_vendedor(monkeypatch):
    hoje = pd.Timestamp.today().normalize()
    mes_atras = hoje - pd.DateOffset(days=30)
    dois_meses_atras = hoje - pd.DateOffset(days=60)

    df_vendas = pd.DataFrame(
        {
            "CODVENDEDOR": ["V1", "V2", "V3", "V1", "V4", "V5"],
            "CODPRODUTO": ["P1", "P1", "P2", "P3", "P4", "P5"],
            "DATASTATUS": [
                mes_atras.strftime("%Y-%m-%d"),   # dentro da janela
                hoje.strftime("%Y-%m-%d"),        # dentro da janela
                dois_meses_atras.strftime("%Y-%m-%d"),  # fora da janela
                hoje.strftime("%Y-%m-%d"),
                hoje.strftime("%Y-%m-%d"),
                mes_atras.strftime("%Y-%m-%d"),
            ],
            "QUANTIDADE": [5, 3, 100, 2, 4, 1],
        }
    )
    _mock_book_clientes(monkeypatch, df_vendas)
    return df_vendas

def test_rf10_top5_vendedores_ultimo_mes(workbook_performance_vendedor):
    df_perf = consulta_performance()

    # 5 vendedores no máximo
    assert len(df_perf) <= 5

    #colunas esperadas
    assert set(df_perf.columns) == {"CODVENDEDOR", "QUANTIDADE"}

    #V3 vendeu só fora da janela, então não deve aparecer
    assert "V3" not in df_perf["CODVENDEDOR"].tolist()

    #V1, V2, V4, V5 aparecem com as somas corretas dentro do período
