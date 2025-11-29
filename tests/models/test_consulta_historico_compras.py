from app.models.consulta_historico_compras import consulta_historico_compras
import pandas as pd
import pytest
from tests.models.test_consulta_principais_clientes import _mock_book_clientes

@pytest.fixture
def workbook_historico_cliente(monkeypatch):
    df_vendas = pd.DataFrame(
        {
            "CLIENTE": ["C1"] * 12 + ["C2"],
            "CODPRODUTO": [f"P{i}" for i in range(12)] + ["P99"],
            "DATASTATUS": pd.date_range("2024-01-01", periods=13, freq="D").strftime("%Y-%m-%d"),
            "QUANTIDADE": [1] * 13,
        }
    )
    _mock_book_clientes(monkeypatch, df_vendas)
    return df_vendas

def test_rf09_ultimas_10_compras(workbook_historico_cliente):
    df_hist = consulta_historico_compras("C1")

    # Deve retornar no máximo 10
    assert len(df_hist) == 10

    # Verifica ordenação (da mais recente para a mais antiga)
    datas = pd.to_datetime(df_hist["DATA"])
    assert datas.is_monotonic_decreasing
