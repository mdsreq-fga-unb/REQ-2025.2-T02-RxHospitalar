from app.models.consulta_performance import consulta_performance
import pandas as pd
import pytest
from tests.models.test_consulta_principais_clientes import _mock_book_clientes

@pytest.fixture
def workbook_performance_vendedor(monkeypatch):
    hoje = pd.Timestamp.today().normalize()
    mes_atras = hoje - pd.DateOffset(days=30)
    dois_meses_atras = hoje - pd.DateOffset(days=60)

    df_vendas = pd.DataFrame(
        {
            "VENDEDOR": ["V1", "V2", "V3", "V1", "V4", "V5"],
            "CODPRODUTO": ["P1", "P1", "P2", "P3", "P4", "P5"],
            "DATA": [
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

    # Máx. 5 vendedores
    assert len(df_perf) <= 5

    # Colunas esperadas
    assert set(df_perf.columns) == {"Vendedor", "Quantidade"}

    # V3 vendeu só fora da janela, então não deve aparecer
    assert "V3" not in df_perf["Vendedor"].tolist()

    # V1, V2, V4, V5 aparecem com as somas corretas dentro do período
