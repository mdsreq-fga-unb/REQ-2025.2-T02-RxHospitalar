#teste de RF05 - Consulta por status do produto
import pandas as pd
import pytest
from datetime import datetime
from app.models.consulta_por_status import consulta_por_status

#este mock serve pra deixar o teste mais rápido!
def _mock_book(monkeypatch, df_estoque: pd.DataFrame, df_vendas: pd.DataFrame | None):
    #expõe as abas que a função espera
    class FakeExcel:
        def __init__(self):
            self.sheet_names = ["Estoque", "Vendas_Pendencia"]

    monkeypatch.setattr("pandas.ExcelFile", lambda f: FakeExcel(), raising=True)
    monkeypatch.setattr("app.models.consulta_por_status.file", "fake.xlsx", raising=False)

    def fake_read_excel(path, sheet_name=0, header=0, dtype=str, **kwargs):
        name = sheet_name if isinstance(sheet_name, str) else FakeExcel().sheet_names[sheet_name]
        if name == "Estoque":
            return df_estoque.copy()
        if name == "Vendas_Pendencia":
            return (df_vendas.copy() if df_vendas is not None else pd.DataFrame())
        return pd.DataFrame()

    monkeypatch.setattr("pandas.read_excel", fake_read_excel, raising=True)

@pytest.fixture
#preparação para cenários de teste
def workbook_sem_saida(monkeypatch):
    hoje = pd.Timestamp(datetime.today().date())
    recente = hoje - pd.DateOffset(months=2)
    antiga = hoje - pd.DateOffset(months=8)

    df_estoque = pd.DataFrame({
        "Cód Original": ["A001", "B002", "C003"],
        "Descrição": ["Item A", "Item B", "Item C"],
        "Estoque": [10, 5, 7],
    })
    df_vendas = pd.DataFrame({
        "CODORIGINAL": ["B002", "C003"],
        "DATASTATUS": [recente.strftime("%Y-%m-%d"), antiga.strftime("%Y-%m-%d")],
        "QUANTIDADE": [1, 2],
    })
    _mock_book(monkeypatch, df_estoque, df_vendas)

#testar um estoque sem saída
def test_status_em_estoque_sem_saida(workbook_sem_saida):
    resultado = consulta_por_status()
    assert isinstance(resultado, dict)
    assert "df" in resultado and "card" in resultado
    df = resultado["df"]
    codes = set(df["Cód Original"].astype(str) if "Cód Original" in df.columns else df["CODORIGINAL"].astype(str))
    assert codes == {"A001", "C003"}
    assert "sem saída nos últimos 6 meses" in resultado["card"]

#testar o status vazio para as vendas
def test_status_vendas_vazia(monkeypatch):
    df_estoque = pd.DataFrame({
        "CODORIGINAL": ["X1", "X2"],
        "DESCRICAO": ["Item X1", "Item X2"],
    })
    df_vendas = pd.DataFrame()  # vazia
    _mock_book(monkeypatch, df_estoque, df_vendas)

    resultado = consulta_por_status()
    df = resultado["df"]
    assert set(df["CODORIGINAL"]) == {"X1", "X2"}
    assert "sem registro de vendas" in resultado["card"] or "sem saída" in resultado["card"]

#teste sem a coluna de data em vendas
def test_status_sem_coluna_data_em_vendas(monkeypatch):
    df_estoque = pd.DataFrame({"Cód Original": ["Y1"], "Descrição": ["Item Y1"]})
    df_vendas = pd.DataFrame({"CODORIGINAL": ["Y1"], "OBS": ["qualquer"]})  # sem DATASTATUS/EMISSAO/etc.
    _mock_book(monkeypatch, df_estoque, df_vendas)

    resultado = consulta_por_status()
    df = resultado["df"]
    assert not df.empty
    assert df.iloc[0].tolist()[0] in ("Y1",)

#teste sem a coluna código em estoque
def test_status_sem_coluna_codigo_em_estoque(monkeypatch):
    df_estoque = pd.DataFrame({"Produto": ["Z1"], "Descrição": ["Item Z1"]})  # sem código
    df_vendas = pd.DataFrame({"CODORIGINAL": ["Z1"], "DATASTATUS": ["2024-01-01"]})
    _mock_book(monkeypatch, df_estoque, df_vendas)

    resultado = consulta_por_status()
    assert resultado["df"].empty
    assert "não encontrada" in resultado["card"].lower()