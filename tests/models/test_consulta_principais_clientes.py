#teste da RF08 - consultar principais clientes por produto
import pandas as pd
from datetime import datetime
import pytest
from app.models.consulta_principais_clientes import consulta_principais_clientes
import app.models.carregar_dados as carregar_dados 
from app.models.carregar_dados import file

#teste para garantir até 5 resultados para o produto com código 28815
def test_consulta_5_clientes():
    df_result = consulta_principais_clientes("28815")

    assert isinstance(df_result, pd.DataFrame)
    assert set(df_result.columns) == {"RAZAOSOCIAL", "QUANTIDADE"}
    assert len(df_result) <= 5

def test_consulta_principais_clientes_real():
    df_result = consulta_principais_clientes("28815")

    # Carrega a aba real para comparação
    df_vendas = pd.read_excel(carregar_dados.file, sheet_name="Vendas_Pendencia", dtype=str)

    # Filtra todas as vendas do P1 na base real
    df_p1 = df_vendas[df_vendas["CODPRODUTO"].astype(str).str.strip() == "28815"]

    clientes_reais_p1 = set(df_p1["RAZAOSOCIAL"].astype(str).str.strip())

    # Garante que TODO cliente retornado realmente comprou P1
    clientes_retorno = set(df_result["RAZAOSOCIAL"].astype(str).str.strip())

    assert clientes_retorno.issubset(clientes_reais_p1)
    assert len(df_result) <= 5

def _mock_book_clientes(monkeypatch, df_vendas):
    # mesma ideia do _mock_book: monkeypatch em pd.read_excel ou no dataloader
    def fake_read_excel(file, sheet_name=None, *args, **kwargs):
        if sheet_name == "Vendas_Pendencia":
            return df_vendas
        raise ValueError("Sheet não mockada")

    monkeypatch.setattr(carregar_dados.pd, "read_excel", fake_read_excel)

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

#mais um teste para o mock segundo os critérios de aceitação do requisito
def test_rf08_top5_clientes_por_produto(workbook_clientes_produto):
    df_result = consulta_principais_clientes("P1")

    #deve trazer no máximo 5 linhas
    assert len(df_result) <= 5

    #verifica colunas esperadas
    assert set(df_result.columns) == {"RAZAOSOCIAL", "QUANTIDADE"}

    #clientes de P1 são C1 (5+2=7) e C2 (3)
    assert list(df_result["RAZAOSOCIAL"]) == ["C1", "C2"]
    assert list(df_result["QUANTIDADE"]) == [7, 3]
