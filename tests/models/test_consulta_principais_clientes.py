#teste da RF08 - consultar principais clientes por produto (frequência e média mensal)
import pandas as pd
import pytest
from app.models.consulta_principais_clientes import consulta_principais_clientes
import app.models.carregar_dados as carregar_dados 

def test_consulta_5_clientes():
    df_result = consulta_principais_clientes("28815")
    assert isinstance(df_result, pd.DataFrame)
    assert set(df_result.columns) == {"RAZAOSOCIAL", "FREQUENCIA", "MEDIA_MENSAL"}
    assert len(df_result) <= 5

def test_consulta_principais_clientes_real():
    df_result = consulta_principais_clientes("28815")

    df_vendas = pd.read_excel(carregar_dados.file, sheet_name="Vendas_Pendencia", dtype=str)
    df_p = df_vendas[df_vendas["CODPRODUTO"].astype(str).str.strip() == "28815"]
    clientes_reais = set(df_p["RAZAOSOCIAL"].astype(str).str.strip())

    #garante que todo cliente retornado realmente comprou o produto
    clientes_retorno = set(df_result["RAZAOSOCIAL"].astype(str).str.strip())
    assert clientes_retorno.issubset(clientes_reais)
    assert len(df_result) <= 5

    #colunas e tipos esperados
    assert "FREQUENCIA" in df_result.columns and "MEDIA_MENSAL" in df_result.columns
    assert pd.api.types.is_numeric_dtype(df_result["FREQUENCIA"])
    assert pd.api.types.is_numeric_dtype(df_result["MEDIA_MENSAL"])

def _mock_book_clientes(monkeypatch, df_vendas):
    def fake_read_excel(file, sheet_name=None, *args, **kwargs):
        if sheet_name == "Vendas_Pendencia":
            return df_vendas
        raise ValueError("Sheet não mockada")
    monkeypatch.setattr(carregar_dados.pd, "read_excel", fake_read_excel)

@pytest.fixture
def workbook_clientes_produto(monkeypatch):
    #3 compras de C1 em 2 meses; 1 compra de C2 em 1 mês
    df_vendas = pd.DataFrame(
        {
            "CODPRODUTO": ["P1", "P1", "P1", "P2"],
            "RAZAOSOCIAL": ["C1", "C1", "C2", "C1"],
            "DATASTATUS": ["2025-10-01", "2025-11-02", "2025-10-15", "2025-10-05"],
        }
    )
    _mock_book_clientes(monkeypatch, df_vendas)
    return df_vendas

def test_rf08_top5_clientes_por_produto_frequencia(workbook_clientes_produto):
    df_result = consulta_principais_clientes("P1")

    assert len(df_result) <= 5
    assert set(df_result.columns) == {"RAZAOSOCIAL", "FREQUENCIA", "MEDIA_MENSAL"}

    #C1 tem 2 compras em 2 meses => média 1.0; C2 tem 1 compra em 1 mês => média 1.0
    assert list(df_result["RAZAOSOCIAL"]) == ["C1", "C2"]
    assert list(df_result["FREQUENCIA"]) == [2, 1]
    assert list(df_result["MEDIA_MENSAL"]) == [1.0, 1.0]