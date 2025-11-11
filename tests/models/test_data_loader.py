import pandas as pd
from app.models.data_loader import load_selected_columns

def test_load_selected_columns():
    # definindo a planilha e as colunas a serem carregadas
    sheet = "Estoque"
    cols = ["Preço Aquisição", "Sit. Fiscal"]
    
    # carregando os dados usando a função do data_loader
    df = load_selected_columns(sheet, cols)
    
    # verificações simples 
    assert isinstance(df, pd.DataFrame), "A função deve retornar um DataFrame"
    
    # verificando se as colunas carregadas são as esperadas
    assert not df.empty, "O DataFrame não deveria estar vazio para essa planilha"
   
    assert list(df.columns) == cols, "As colunas retornadas devem ser as mesmas solicitadas"
    