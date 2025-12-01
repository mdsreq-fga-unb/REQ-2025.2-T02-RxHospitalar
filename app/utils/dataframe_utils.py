
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
    Calcula a necessidade de compra em CAIXAS e o valor financeiro.
    
    Lógica:
    1. Calcula estoque total em unidades.
    2. Calcula necessidade baseada na média mensal.
    3. Filtra produtos com déficit (Saldo Negativo).
    4. Converte o déficit de unidades para QUANTIDADE DE CAIXAS (arredondando para cima).
    5. Calcula o custo total (Caixas * Preço Aquisição).
    """
    
    # 1. Evita alterar o original
    df = df.copy()

    # ==============================================================================
    # PREPARAÇÃO (Garantir que colunas sejam números)
    # ==============================================================================
    # Importante: Incluir 'Preço Aquisição' na conversão
    cols_numericas = ['Estoque', 'Qtd Caixa', 'MEDIA_MENSAL', 'Preço Aquisição']
    for col in cols_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # ==============================================================================
    # ETAPA 1: Calcular Estoque Total em Unidades
    # ==============================================================================
    df["ESTOQUE_TOTAL_UNIDADES"] = df["Estoque"] * df["Qtd Caixa"]

    # ==============================================================================
    # ETAPA 2: Calcular Quantidade Necessária para o Período (em Unidades)
    # ==============================================================================
    df["QUANTIDADE_NECESSARIA"] = df["MEDIA_MENSAL"] * periodo

    # ==============================================================================
    # ETAPA 3: Calcular Saldo em Unidades
    # ==============================================================================
    # Negativo = Falta | Positivo = Sobra
    df["SALDO_ESTOQUE_UNIDADES"] = df["ESTOQUE_TOTAL_UNIDADES"] - df["QUANTIDADE_NECESSARIA"]

    # ==============================================================================
    # ETAPA 4: Filtrar apenas os negativos (Onde precisa comprar)
    # ==============================================================================
    df_compra = df[df["SALDO_ESTOQUE_UNIDADES"] < 0].copy()

    if df_compra.empty:
        return pd.DataFrame() # Retorna vazio se não tiver nada para comprar

    # ==============================================================================
    # ETAPA 5: Converter Déficit de Unidades para CAIXAS (NOVO!)
    # ==============================================================================
    # Pega o valor absoluto do déficit (ex: faltam -50 unidades -> 50)
    deficit_unidades = df_compra["SALDO_ESTOQUE_UNIDADES"].abs()
    
    # Proteção contra divisão por zero (se Qtd Caixa for 0, considera 1)
    qtd_caixa_segura = df_compra["Qtd Caixa"].replace(0, 1)
    
    # Divide pela caixa e arredonda pra CIMA (np.ceil)
    # Ex: Faltam 13 un, caixa de 12 -> 1.08 -> Comprar 2 caixas
    df_compra["SUGESTAO_QTD_CAIXAS"] = np.ceil(deficit_unidades / qtd_caixa_segura).astype(int)

    # ==============================================================================
    # ETAPA 6: Calcular Valor Financeiro (NOVO!)
    # ==============================================================================
    # Multiplica número de caixas pelo preço unitário da caixa
    if "Preço Aquisição" in df_compra.columns:
        df_compra["VALOR_TOTAL_COMPRA"] = df_compra["SUGESTAO_QTD_CAIXAS"] * df_compra["Preço Aquisição"]
    else:
        df_compra["VALOR_TOTAL_COMPRA"] = 0.0

    # ==============================================================================
    # ETAPA 7: Organização Final das Colunas
    # ==============================================================================
    # Pega as colunas de meses dinamicamente para mostrar no relatório
    cols_meses = [c for c in df_compra.columns if '/' in c]
    
    colunas_ordenadas = [
        "CODORIGINAL", 
        "GRUPO", 
        cols_meses,              # Lista de meses
        "MEDIA_MENSAL", 
        "Estoque",               # Estoque físico atual
        "Qtd Caixa",             # Unidades por caixa
        "Preço Aquisição",       # Preço da caixa
        "ESTOQUE_TOTAL_UNIDADES",
        "QUANTIDADE_NECESSARIA", 
        "SALDO_ESTOQUE_UNIDADES",
        "SUGESTAO_QTD_CAIXAS",   # <--- RESULTADO EM CAIXAS
        "VALOR_TOTAL_COMPRA"     # <--- CUSTO ESTIMADO
    ]
    
    # "Achata" a lista (para tirar a lista de meses de dentro da lista principal)
    colunas_finais_flat = []
    for item in colunas_ordenadas:
        if isinstance(item, list):
            colunas_finais_flat.extend(item)
        else:
            colunas_finais_flat.append(item)

    # Filtra apenas as colunas que realmente existem
    colunas_validas = [c for c in colunas_finais_flat if c in df_compra.columns]
    
    return df_compra[colunas_validas]