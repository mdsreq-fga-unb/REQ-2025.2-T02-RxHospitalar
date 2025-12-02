from app.models.consulta_performance import consulta_performance
import pandas as pd
import pytest
from tests.models.test_consulta_principais_clientes import _mock_book_clientes
from datetime import datetime
import app.models.carregar_dados as carregar_dados

#isso normaliza os valores numéricos de string pra float
def _to_number(series: pd.Series) -> pd.Series:
    s = series.astype(str).str.strip()
    s = s.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    return pd.to_numeric(s, errors="coerce").fillna(0.0)

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

    if df_periodo.empty or "TOTALPAGO2" not in df_periodo.columns:
        #se não tem vendas no período ou não há TOTALPAGO2, o resultado deve ser DF vazio com as mesmas colunas
        assert df_perf.empty
        assert set(df_perf.columns) == {"CODVENDEDOR", "VALOR"}
        return

    #usa TOTALPAGO2 obrigatoriamente
    df_periodo["VALOR"] = _to_number(df_periodo["TOTALPAGO2"])

    df_expected = (
        df_periodo.groupby("CODVENDEDOR")["VALOR"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    df_expected.columns = ["CODVENDEDOR", "VALOR"]

    #colunas e limite
    assert set(df_perf.columns) == {"CODVENDEDOR", "VALOR"}
    assert len(df_perf) <= 5

    #vendedores retornados têm vendas no período
    vends_ret = set(df_perf["CODVENDEDOR"].astype(str).str.strip())
    vends_exp = set(df_expected["CODVENDEDOR"].astype(str).str.strip())
    assert vends_ret.issubset(vends_exp)

    #confere as somas para os vendedores em comum
    merged = df_perf.merge(df_expected, on="CODVENDEDOR", suffixes=("_resp", "_exp"))
    assert all(abs(merged["VALOR_resp"] - merged["VALOR_exp"]) < 1e-6)

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
            # adiciona TOTALPAGO2 
            "TOTALPAGO2": ["50,00", "30,00", "1000,00", "20,00", "40,00", "10,00"],
        }
    )
    _mock_book_clientes(monkeypatch, df_vendas)
    return df_vendas

#teste de RF10 agora baseado em VALOR total
def test_rf10_top5_vendedores_ultimo_mes(workbook_performance_vendedor):
    df_perf = consulta_performance()

    #5 vendedores no máximo
    assert len(df_perf) <= 5

    #colunas esperadas
    assert set(df_perf.columns) == {"CODVENDEDOR", "VALOR"}

    #V3 vendeu só fora da janela, então não deve aparecer
    assert "V3" not in df_perf["CODVENDEDOR"].tolist()

    #checagem básica de ordenação por valor decrescente
    vals = df_perf["VALOR"].tolist()
    assert vals == sorted(vals, reverse=True)
