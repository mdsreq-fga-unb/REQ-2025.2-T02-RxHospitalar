import pandas as pd
import numpy as np

def _to_number(series: pd.Series) -> pd.Series:
    s = series.astype(str).str.strip()
    s = s.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    return pd.to_numeric(s, errors="coerce").fillna(0.0)

def consulta_sazonalidade_dataframe(df_completo: pd.DataFrame, linha_filtro: str = None):
    """
    Calcula a sazonalidade (vendas por mês) baseada no DataFrame de Vendas/Pendências.
    Se linha_filtro for None, calcula do total global.
    """
    if df_completo is None or df_completo.empty:
        return pd.DataFrame({"MES": list(range(1, 13)), "TOTAL": [0] * 12})

    df = df_completo.copy()

    # Tenta encontrar a coluna de data (DATASTATUS ou DATA)
    col_data = next((c for c in df.columns if "DATA" in c.upper() or "DT" in c.upper()), None)
    col_qtd = next((c for c in df.columns if "QUANT" in c.upper() or "QTD" in c.upper()), None)
    
    # Identifica colunas de linha/grupo
    col_linha = next((c for c in df.columns if c.lower() in ["grupo", "linha", "categoria"]), None)

    if not col_data or not col_qtd:
        return pd.DataFrame({"MES": list(range(1, 13)), "TOTAL": [0] * 12})

    # 1. Filtra Linha (se houver)
    if linha_filtro and col_linha:
        df = df[df[col_linha].astype(str).str.strip() == str(linha_filtro).strip()]

    # 2. Converte Data e Extrai Mês
    # Força formato dia/mês/ano (dayfirst=True é comum no BR)
    df["_DATA_PROC"] = pd.to_datetime(df[col_data], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["_DATA_PROC"])
    
    # Filtra últimos 12 meses (Opção Global) ou Ano Corrente
    # Aqui vamos simplificar e pegar apenas o mês (1..12) ignorando o ano para ver Sazonalidade Pura
    df["_MES"] = df["_DATA_PROC"].dt.month.astype(int)

    # 3. Trata Quantidade
    df["_QTD_PROC"] = _to_number(df[col_qtd])

    # 4. Agrupa
    grp = df.groupby("_MES")["_QTD_PROC"].sum().reset_index()
    grp.columns = ["MES", "TOTAL"]

    # 5. Merge com todos os meses (1 a 12) para não ficar buraco
    all_months = pd.DataFrame({"MES": list(range(1, 13))})
    final = all_months.merge(grp, on="MES", how="left").fillna(0)
    
    return final