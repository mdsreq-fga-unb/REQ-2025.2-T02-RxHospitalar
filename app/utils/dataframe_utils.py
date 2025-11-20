

import pandas as pd
from app.models.carregar_dados import carregar_dados_por_colunas
from app.utils.separar_por_data import separar_quantidade_por_data



#Usada em RF07
def filtrar_por_codigo(df, column_name: str, code_value: str):
    """
    Filtra um DataFrame selecionando todas as linhas onde a coluna especificada
    contém o valor desejado (comparação case-insensitive e ignorando espaços).
    """
    try:
        if column_name not in df.columns:
            raise ValueError(f"A coluna '{column_name}' não existe no DataFrame.")

        # Normaliza valores antes de comparar
        filtered_df = df[
            df[column_name]
            .astype(str)
            .str.strip()
            .str.upper()
            == code_value.strip().upper()
        ]

        return filtered_df

    except Exception as e:
        print(f"Erro ao filtrar DataFrame: {e}")
        return pd.DataFrame()
    



