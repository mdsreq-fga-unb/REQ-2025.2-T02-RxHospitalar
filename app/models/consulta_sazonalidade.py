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
def consulta_sazonalidade_por_linha(
    linha: str,
    coluna_linha: str = "Grupo",
    n_top: int = 5,
    usar_valor: bool = False,
):
    #lê planilha (mockado em teste)
    df = pd.read_excel(file, sheet_name="Vendas_Pendencia", dtype=str)

    #coluna de linha precisa existir
    if coluna_linha not in df.columns:
        vazio_mensal = pd.DataFrame({"MES": list(range(1, 13)), "TOTAL": [0] * 12})
        vazio_top = pd.DataFrame(columns=["RAZAOSOCIAL", "FREQUENCIA", "TOTAL_QUANTIDADE"])
        return {"linha": linha, "mensal": vazio_mensal, "top_clientes": vazio_top, "recorrentes": []}

    #filtra linha
    df = df[df[coluna_linha].astype(str).str.strip() == str(linha).strip()].copy()
    if df.empty:
        vazio_mensal = pd.DataFrame({"MES": list(range(1, 13)), "TOTAL": [0] * 12})
        vazio_top = pd.DataFrame(columns=["RAZAOSOCIAL", "FREQUENCIA", "TOTAL_QUANTIDADE"])
        return {"linha": linha, "mensal": vazio_mensal, "top_clientes": vazio_top, "recorrentes": []}

    #converte DATASTATUS para datetime e extrai mês
    datas = pd.to_datetime(df["DATASTATUS"], errors="coerce", dayfirst=True)
    df = df.assign(_DATA=datas).dropna(subset=["_DATA"]).copy()
    df["_MES"] = df["_DATA"].dt.month.astype(int)

    #métricas base
    df["QUANTIDADE"] = pd.to_numeric(df.get("QUANTIDADE", 1), errors="coerce").fillna(1)
    if usar_valor:
        df["VALOR"] = _to_number(df.get("TOTALPAGO2", pd.Series(index=df.index, dtype=str)))

    #agrega mensal: sempre 12 meses (1..12)
    col_metric = "VALOR" if usar_valor and "VALOR" in df.columns else "QUANTIDADE"
    grp = (
        df.groupby("_MES", as_index=False)
        .agg(TOTAL=(col_metric, "sum"))
        .rename(columns={"_MES": "MES"})
    )
    full = pd.DataFrame({"MES": list(range(1, 13))})
    mensal = full.merge(grp, on="MES", how="left").fillna({"TOTAL": 0})
    mensal["TOTAL"] = pd.to_numeric(mensal["TOTAL"], errors="coerce").fillna(0)

    #top clientes por frequência
    freq = (
        df.groupby("RAZAOSOCIAL")
        .size()
        .reset_index(name="FREQUENCIA")
        .sort_values("FREQUENCIA", ascending=False)
    )
    tot_qtd = (
        df.groupby("RAZAOSOCIAL")["QUANTIDADE"]
        .sum()
        .reset_index(name="TOTAL_QUANTIDADE")
    )
    top = freq.merge(tot_qtd, on="RAZAOSOCIAL", how="left")

    if usar_valor and "VALOR" in df.columns:
        tot_val = (
            df.groupby("RAZAOSOCIAL")["VALOR"]
            .sum()
            .reset_index(name="TOTAL_VALOR")
        )
        top = top.merge(tot_val, on="RAZAOSOCIAL", how="left")

    top = (
        top.sort_values(["FREQUENCIA", "TOTAL_QUANTIDADE"], ascending=[False, False])
        .head(n_top)
        .reset_index(drop=True)
    )

    recorrentes = top.loc[top["FREQUENCIA"] >= 2, "RAZAOSOCIAL"].tolist()

    return {
        "linha": linha,
        "mensal": mensal,
        "top_clientes": top,
        "recorrentes": recorrentes,
    }
