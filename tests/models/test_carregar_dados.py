import pandas as pd
from app.models.carregar_dados import carregar_dados_por_colunas

def test_load_selected_columns():
    # Definindo a planilha e as colunas a serem carregadas
    sheet = "BD - 14"
    cols = ["OPERADOR", "CODPRODUTO"]
    
    # Carregando os dados usando a função do data_loader
    df = carregar_dados_por_colunas(sheet, cols)
    
    # Verificações simples 
    assert isinstance(df, pd.DataFrame), "A função deve retornar um DataFrame"
    
    # Verificando se as colunas carregadas são as esperadas
    assert not df.empty, "O DataFrame não deveria estar vazio para essa planilha"
   
    assert list(df.columns) == cols, "As colunas retornadas devem ser as mesmas solicitadas"
    