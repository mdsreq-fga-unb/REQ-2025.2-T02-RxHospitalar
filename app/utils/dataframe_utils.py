
import pandas as pd
from app.models.carregar_dados import carregar_dados_por_colunas
from app.utils.separar_por_data import separar_quantidade_por_data

#Usada em RF07
def filtrar_por_codigo(df, column_name: str, code_value: str):
    """
    Filtra um DataFrame selecionando todas as linhas onde a coluna especificada
    contém o valor desejado (comparação case-insensitive e ignorando espaços).
    """
    if column_name not in df.columns:
        print(f"Erro ao filtrar DataFrame: A coluna '{column_name}' não existe no DataFrame.")
        return pd.DataFrame()

    if code_value is None:
        return pd.DataFrame()

    raw_target = code_value.strip()
    lower_target = raw_target.lower()

    col = df[column_name]

    #caso especial para distinguir NaN real (float) da string literal 'NaN'
    if lower_target == "nan":
        #se o usuário passou tudo em minúsculas (ex: ' nan ')
        if raw_target == lower_target:
            return df[col.isna()]
        else:
            #forma mista (ex: 'NaN') -> procurar exatamente a célula com string 'NaN'
            #garante que não pegue o float NaN convertido
            return df[(~col.isna()) & (col.astype(str) == "NaN")]

    #não converta NaN real em 'nan' antes de comparação
    series = col.where(~col.isna(), "__FLOAT_NAN__").astype(str).str.strip()
    mask = series.str.lower() == lower_target
    #remove o marcador especial que só servia para evitar colisão com 'nan'
    result = df[mask & (series != "__FLOAT_NAN__")]
    return result

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
    



