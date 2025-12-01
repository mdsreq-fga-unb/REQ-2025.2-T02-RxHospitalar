#teste da RF08 - consultar principais clientes por produto (frequência e média mensal)
import pandas as pd
import pytest
import os, warnings
from app.models.consulta_principais_clientes import consulta_principais_clientes
from app.models.carregar_dados import file
import app.models.carregar_dados as carregar_dados 
warnings.filterwarnings(
    "ignore",
    message="Could not infer format, so each element will be parsed individually",
    category=UserWarning,
)

def test_consulta_5_clientes():
    df_result = consulta_principais_clientes("28815")
    assert isinstance(df_result, pd.DataFrame)
    # agora inclui quantidade total
    assert set(df_result.columns) == {"RAZAOSOCIAL", "FREQUENCIA", "TOTAL_QUANTIDADE", "MEDIA_MENSAL"}
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
    assert "FREQUENCIA" in df_result.columns and "MEDIA_MENSAL" in df_result.columns and "TOTAL_QUANTIDADE" in df_result.columns
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
    assert set(df_result.columns) == {"RAZAOSOCIAL", "FREQUENCIA", "TOTAL_QUANTIDADE", "MEDIA_MENSAL"}

    #C1 tem 2 compras em 2 meses => QUANTIDADE default 1 -> TOTAL_QUANTIDADE=2 -> média 1.0; C2 tem 1 compra em 1 mês => média 1.0
    assert list(df_result["RAZAOSOCIAL"]) == ["C1", "C2"]
    assert list(df_result["FREQUENCIA"]) == [2, 1]
    assert list(df_result["MEDIA_MENSAL"]) == [1.0, 1.0]

def test_top5_e_media_mensal(monkeypatch):
    """Testa frequência, quantidade total e média mensal com quantidades reais"""
    df = pd.DataFrame({
        "CODPRODUTO": ["P1","P1","P1","P1","P2"],
        "RAZAOSOCIAL": ["C1","C1","C2","C3","C1"],
        "DATASTATUS": ["2025-01-10","2025-02-10","2025-01-15","2025-01-20","2025-01-01"],
        "QUANTIDADE": ["5", "5", "3", "2", "1"],  # strings como vêm do Excel
    })
    monkeypatch.setattr(carregar_dados.pd, "read_excel", lambda *a, **k: df)
    
    res = consulta_principais_clientes("P1", limite=5)
    
    #C1: 2 compras em 2 meses distintos (jan e fev), total 10, média 5.0
    c1 = res[res["RAZAOSOCIAL"] == "C1"].iloc[0]
    assert c1["FREQUENCIA"] == 2
    assert c1["TOTAL_QUANTIDADE"] == 10
    assert c1["MEDIA_MENSAL"] == 5.0
    
    #C2: 1 compra em jan, total 3, média 3.0
    c2 = res[res["RAZAOSOCIAL"] == "C2"].iloc[0]
    assert c2["FREQUENCIA"] == 1
    assert c2["TOTAL_QUANTIDADE"] == 3
    assert c2["MEDIA_MENSAL"] == 3.0
    
    #C3: 1 compra em jan, total 2, média 2.0
    c3 = res[res["RAZAOSOCIAL"] == "C3"].iloc[0]
    assert c3["FREQUENCIA"] == 1
    assert c3["TOTAL_QUANTIDADE"] == 2
    assert c3["MEDIA_MENSAL"] == 2.0

def test_datas_fallback_e_meses_minimo(monkeypatch):
    #testa que a função não quebra com datas inválidas e garante MESES >= 1
    df = pd.DataFrame({
        "CODPRODUTO": ["P1","P1","P1","P1"],
        "RAZAOSOCIAL": ["C1","C1","C2","C3"],
        "DATASTATUS": ["invalid","invalid","2025-02-05",None],  
        "QUANTIDADE": ["2", "3", "7", "1"],
    })
    monkeypatch.setattr(carregar_dados.pd, "read_excel", lambda *a, **k: df)
    
    res = consulta_principais_clientes("P1", limite=5)
    
    #C1: 2 compras, 0 datas válidas -> fallback MESES=1 -> média = 5/1 = 5.0
    c1 = res[res["RAZAOSOCIAL"] == "C1"].iloc[0]
    assert c1["FREQUENCIA"] == 2
    assert c1["TOTAL_QUANTIDADE"] == 5
    assert c1["MEDIA_MENSAL"] == 5.0  #não dividiu por zero, usou MESES=1
    
    #C2: 1 compra válida -> média = 7/1 = 7.0
    c2 = res[res["RAZAOSOCIAL"] == "C2"].iloc[0]
    assert c2["MEDIA_MENSAL"] == 7.0
    
    #C3: sem data -> MESES=1 -> média = 1/1 = 1.0
    c3 = res[res["RAZAOSOCIAL"] == "C3"].iloc[0]
    assert c3["MEDIA_MENSAL"] == 1.0

@pytest.mark.skipif(not os.path.exists(str(file)), reason="planilha não encontrada")
def test_real_structure():
    """Smoke test com planilha real: valida estrutura de saída"""
    df = pd.read_excel(file, sheet_name="Vendas_Pendencia", dtype=str)
    assert "CODPRODUTO" in df.columns, "Planilha real deve ter coluna CODPRODUTO"
    
    #escolhe um produto real para smoke test
    cod = df["CODPRODUTO"].dropna().astype(str).str.strip().iloc[0]
    res = consulta_principais_clientes(cod)
    
    #valida estrutura (não valores específicos, pois são dados reais)
    assert isinstance(res, pd.DataFrame)
    assert set(res.columns) == {"RAZAOSOCIAL", "FREQUENCIA", "TOTAL_QUANTIDADE", "MEDIA_MENSAL"}
    assert len(res) <= 5
    
    #valida tipos
    if not res.empty:
        assert pd.api.types.is_numeric_dtype(res["FREQUENCIA"])
        assert pd.api.types.is_numeric_dtype(res["TOTAL_QUANTIDADE"])
        assert pd.api.types.is_numeric_dtype(res["MEDIA_MENSAL"])
        #valida que média mensal é >= 0 (não há divisão por zero)
        assert (res["MEDIA_MENSAL"] >= 0).all()
