import pandas as pd
from app.models.carregar_dados import carregar_dados_por_colunas

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