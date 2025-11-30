import pandas as pd
from app.models.carregar_dados import carregar_dados_por_colunas
from app.models.carregar_dados import importar_arquivo

def test_load_selected_columns_vendas():
    #definindo a planilha e as colunas a serem carregadas
    sheet = "Vendas_Pendencia"
    cols = ["RAZAOSOCIAL", "OBS"]
    
    # Carregando os dados usando a função do data_loader
    df = carregar_dados_por_colunas(sheet, cols)
    
    #verificações simples 
    assert isinstance(df, pd.DataFrame), "A função deve retornar um DataFrame"
    
    #verificando se as colunas carregadas são as esperadas
    assert not df.empty, "O DataFrame não deveria estar vazio para essa planilha"
   
    assert list(df.columns) == cols, "As colunas retornadas devem ser as mesmas solicitadas"
    
def test_load_selected_columns_estoque():
    #definindo a planilha e as colunas a serem carregadas
    sheet = "Estoque"
    cols = ["Preço Aquisição", "Sit. Fiscal"]
    
    #carregando os dados usando a função do data_loader
    df = carregar_dados_por_colunas(sheet, cols)
    
    #verificações simples 
    assert isinstance(df, pd.DataFrame), "A função deve retornar um DataFrame"
    
    #verificando se as colunas carregadas são as esperadas
    assert not df.empty, "O DataFrame não deveria estar vazio para essa planilha"
   
    assert list(df.columns) == cols, "As colunas retornadas devem ser as mesmas solicitadas"

def test_importar_xlsx_integridade(tmp_path):
    df = pd.DataFrame({
        "Cód Original": ["A1","A2","A3"],
        "Descrição": ["X","Y","Z"],
        "Estoque": [10, 5, 7]
    })
    p = tmp_path / "base.xlsx"
    with pd.ExcelWriter(p) as w:
        df.to_excel(w, sheet_name="Estoque", index=False)
    req = {"Estoque": ["Cód Original", "Descrição", "Estoque"]}
    res = importar_arquivo(str(p), req, check_integrity=True)
    assert res["ok"]
    assert res["integrity"]["Estoque"]["rows"] == 3
    assert res["integrity"]["Estoque"]["sums"]["Estoque"] == 22

def test_importar_csv_colunas_faltando(tmp_path):
    p = tmp_path / "dados.csv"
    pd.DataFrame({"Cód Original": ["X1"]}).to_csv(p, index=False)
    req = {"__csv__": ["Cód Original", "Descrição"]}
    res = importar_arquivo(str(p), req)
    assert not res["ok"]
    assert "colunas faltando" in res["erro"].lower()

def test_importar_xlsx_abas_faltando(tmp_path):
    p = tmp_path / "dados.xlsx"
    with pd.ExcelWriter(p) as w:
        pd.DataFrame({"Cód Original": ["A1"], "Descrição": ["Item A"]}).to_excel(w, sheet_name="Estoque", index=False)
    req = {"Estoque": ["Cód Original"], "Vendas_Pendencia": ["CODORIGINAL"]}
    res = importar_arquivo(str(p), req)
    assert not res["ok"]
    assert "abas faltando" in res["erro"].lower()

def test_importar_ext_maiuscula(tmp_path):
    p = tmp_path / "BASE.XLSX"
    with pd.ExcelWriter(p) as w:
        pd.DataFrame({"Cód Original": ["A1"]}).to_excel(w, sheet_name="Estoque", index=False)
    req = {"Estoque": ["Cód Original"]}
    res = importar_arquivo(str(p), req)
    assert res["ok"]

def test_importar_corrompido(tmp_path):
    p = tmp_path / "corrompido.xlsx"
    p.write_text("conteudo nao excel")
    req = {"Estoque": ["Cód Original"]}
    res = importar_arquivo(str(p), req)
    assert not res["ok"]
    assert "falha ao importar" in res["erro"].lower()

def test_windows_style_path(tmp_path):
    df = pd.DataFrame({"Cód Original": ["W1"], "Descrição": ["Win Item"]})
    p = tmp_path / "win.xlsx"
    with pd.ExcelWriter(p) as w:
        df.to_excel(w, sheet_name="Estoque", index=False)
    win_style = str(p).replace("/", "\\")
    req = {"Estoque": ["Cód Original", "Descrição"]}
    res = importar_arquivo(win_style, req)
    assert res["ok"]