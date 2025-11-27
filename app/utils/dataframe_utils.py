
import pandas as pd
from app.models.carregar_dados import carregar_dados_por_colunas
from app.utils.separar_por_data import separar_quantidade_por_data
import numpy as np
from math import ceil


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
    




def juntar_por_codigo(df_vendas, df_estoque):
    """
    Junta df_vendas e df_estoque apenas onde os códigos forem iguais.
    CODORIGINAL (df_vendas)
    Cód Original (df_estoque)
    """

    # Renomeia para padronizar
    df_estoque_ren = df_estoque.rename(columns={"Cód Original": "CODORIGINAL"})

    # Faz o join apenas dos produtos iguais
    df_merged = pd.merge(
        df_vendas,
        df_estoque_ren,
        on="CODORIGINAL",
        how="inner"       # mantém só os que existem nos dois
    )

    return df_merged



def quantidade_para_comprar(df, periodo):
    """
    Calcula a necessidade de compra baseada no estoque total vs média mensal.
    
    Lógica:
    1. Calcula ESTOQUE_TOTAL_UNIDADES (Estoque * Qtd Caixa)
    2. Calcula QUANTIDADE_NECESSARIA (Média * Periodo)
    3. Calcula SALDO (Estoque - Necessaria)
    4. Filtra apenas onde SALDO < 0 (Déficit)
    5. Gera SUGESTAO_COMPRA (Valor absoluto do déficit arredondado para cima)
    """
    
    # 1. Evita alterar o original
    df = df.copy()

    # ==============================================================================
    # PREPARAÇÃO (Garantir que colunas sejam números)
    # ==============================================================================
    cols_numericas = ['Estoque', 'Qtd Caixa', 'MEDIA_MENSAL']
    for col in cols_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # ==============================================================================
    # ETAPA 1: Calcular Estoque Total em Unidades
    # ==============================================================================
    # Nome sugerido: ESTOQUE_TOTAL_UNIDADES
    df["ESTOQUE_TOTAL_UNIDADES"] = df["Estoque"] * df["Qtd Caixa"]

    # ==============================================================================
    # ETAPA 2: Calcular Quantidade Necessária para o Período
    # ==============================================================================
    # Nome sugerido: QUANTIDADE_NECESSARIA
    df["QUANTIDADE_NECESSARIA"] = df["MEDIA_MENSAL"] * periodo

    # ==============================================================================
    # ETAPA 3: Calcular Diferença (Estoque - Necessidade)
    # ==============================================================================
    # Se o resultado for negativo, significa que FALTA produto.
    # Se for positivo, SOBRA produto.
    df["SALDO_ESTOQUE"] = df["ESTOQUE_TOTAL_UNIDADES"] - df["QUANTIDADE_NECESSARIA"]

    # ==============================================================================
    # ETAPA 4: Filtrar apenas os negativos (Onde precisa comprar)
    # ==============================================================================
    # Mantemos apenas onde o saldo é menor que 0
    df_compra = df[df["SALDO_ESTOQUE"] < 0].copy()

    # ==============================================================================
    # ETAPA 5: Coluna final de Sugestão (Positivando o valor)
    # ==============================================================================
    # Se o saldo é -100, a sugestão de compra deve ser 100.
    # Usamos np.ceil para arredondar pra cima (não compramos meia unidade) e abs() para tirar o sinal negativo.
    df_compra["SUGESTAO_COMPRA"] = np.ceil(df_compra["SALDO_ESTOQUE"].abs()).astype(int)

    # ==============================================================================
    # ETAPA 6: Organização Final das Colunas
    # ==============================================================================
    # Pega as colunas de meses dinamicamente (ex: 10/2025, 09/2025...)
    cols_meses = [c for c in df_compra.columns if '/' in c]
    
    colunas_finais = [
        "CODORIGINAL", 
        "GRUPO", 
        "MEDIA_MENSAL",
        "Estoque", 
        "Qtd Caixa", 
        "ESTOQUE_TOTAL_UNIDADES", 
        "QUANTIDADE_NECESSARIA", 
        "SALDO_ESTOQUE",    # Valor negativo mostrando o déficit
        "SUGESTAO_COMPRA"   # Valor positivo sugerindo quanto comprar
    ]
    
    # Adiciona os meses no meio para visualização, se existirem
    colunas_ordenadas = ["CODORIGINAL", "GRUPO"] + cols_meses + [
        "MEDIA_MENSAL", "ESTOQUE_TOTAL_UNIDADES", 
        "QUANTIDADE_NECESSARIA", "SALDO_ESTOQUE", "SUGESTAO_COMPRA"
    ]
    
    # Filtra colunas existentes para evitar erro se faltar alguma
    colunas_validas = [c for c in colunas_ordenadas if c in df_compra.columns]
    
    return df_compra[colunas_validas]