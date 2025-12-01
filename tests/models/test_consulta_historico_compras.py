from app.models.consulta_historico_compras import consulta_historico_compras
import pandas as pd
import pytest
from tests.models.test_consulta_principais_clientes import _mock_book_clientes
import app.models.carregar_dados as carregar_dados 
from app.models.carregar_dados import file

#teste geral para o requisito
def test_historico_compras_real_cliente():
    cliente = "UNIMED GOIANIA COOPERATIVA DE TRABALHO MEDICO"  

    df_result = consulta_historico_compras(cliente)

    #carrega a aba real para comparação
    df_vendas = pd.read_excel(
        carregar_dados.file,
        sheet_name="Vendas_Pendencia",
        dtype=str
    )

    #filtra todas as vendas desse cliente na base real
    df_cli_real = df_vendas[
        df_vendas["RAZAOSOCIAL"].astype(str).str.strip() == str(cliente).strip()
    ]

    #qualquer registro retornado precisa ser desse cliente
    clientes_ret = set(df_result["RAZAOSOCIAL"].astype(str).str.strip())
    clientes_reais = set(df_cli_real["RAZAOSOCIAL"].astype(str).str.strip())
    assert clientes_ret.issubset(clientes_reais)

    #no máximo 10 registros
    assert len(df_result) <= 10

    #datas em ordem decrescente
    datas = pd.to_datetime(df_result["DATASTATUS"])
    assert datas.is_monotonic_decreasing

@pytest.fixture
def workbook_historico_cliente(monkeypatch):
    df_vendas = pd.DataFrame(
        {
            "RAZAOSOCIAL": ["C1"] * 12 + ["C2"],
            "CODPRODUTO": [f"P{i}" for i in range(12)] + ["P99"],
            "DATASTATUS": pd.date_range("2024-01-01", periods=13, freq="D").strftime("%Y-%m-%d"),
            "QUANTIDADE": [1] * 13,
        }
    )
    _mock_book_clientes(monkeypatch, df_vendas)
    return df_vendas

#teste do mock para verificar os critérios de aceitação do requisito
def test_ultimas_10_compras(workbook_historico_cliente):
    df_hist = consulta_historico_compras("C1")

    #deve retornar no máximo 10
    assert len(df_hist) == 10

    #verifica ordenação (da mais recente para a mais antiga)
    datas = pd.to_datetime(df_hist["DATASTATUS"])
    assert datas.is_monotonic_decreasing
