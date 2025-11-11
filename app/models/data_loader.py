import os
import pandas as pd

#caminho do arquivo excel
# Caminho da pasta /Projeto/REQ.../app/models/data_loader.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Sobe 2 níveis: models -> app -> REQ-... -> Projeto/
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR)))

# endereço planilha excel 
file = os.path.join(PROJECT_ROOT, "data", "RRX Análise Compras.xlsx")

#funcao para carregar dados das linhas com filtro de colunas
def load_selected_columns( sheet_name: str, columns):

    try:
        df = pd.read_excel(file, sheet_name=sheet_name, usecols=columns)
        return df
    
    except KeyError as e:
        print(f"Error: One or more columns not found in the sheet. {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()

