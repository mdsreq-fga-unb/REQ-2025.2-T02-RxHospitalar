#teste da RF08 - consultar principais clientes por produto
import pandas as pd
from datetime import datetime
import pytest
from app.models.consulta_principais_clientes import consulta_principais_clientes
import app.models.carregar_dados as carregardados

def _mock_book_clientes(monkeypatch, df_vendas):
    # mesma ideia do _mock_book: monkeypatch em pd.read_excel ou no dataloader
    def fake_read_excel(file, sheet_name=None, *args, **kwargs):
        if sheet_name == "Vendas_Pendencia":
            return df_vendas
        raise ValueError("Sheet não mockada")

    monkeypatch.setattr(carregardados.pd, "read_excel", fake_read_excel)

@pytest.fixture
def workbook_clientes_produto(monkeypatch):
    df_vendas = pd.DataFrame(
        {
            "CODPRODUTO": ["P1", "P1", "P1", "P2", "P2"],
            "RAZAOSOCIAL": ["C1", "C2", "C1", "C3", "C1"],
            "QUANTIDADE": [5, 3, 2, 10, 1],
        }
    )
    _mock_book_clientes(monkeypatch, df_vendas)
    return df_vendas

def test_rf08_top5_clientes_por_produto(workbook_clientes_produto):
    df_result = consulta_principais_clientes("P1")

    # Deve trazer no máximo 5 linhas
    assert len(df_result) <= 5

    # Verifica colunas esperadas
    assert set(df_result.columns) == {"RAZAOSOCIAL", "QUANTIDADE"}

    # Clientes de P1 são C1 (5+2=7) e C2 (3)
    assert list(df_result["RAZAOSOCIAL"]) == ["C1", "C2"]
    assert list(df_result["QUANTIDADE"]) == [7, 3]
