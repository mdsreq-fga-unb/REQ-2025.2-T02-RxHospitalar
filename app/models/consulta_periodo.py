import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.models.carregar_dados import file

def consulta_periodo(codproduto: str | None = None, n_meses: int = 3) -> pd.DataFrame:
    df = pd.read_excel(file, sheet_name="Vendas_Pendencia", dtype=str).copy()

    #normaliza quantidade
    df["QUANTIDADE"] = pd.to_numeric(df.get("QUANTIDADE", 0), errors="coerce").fillna(0)

    #normaliza datas como Series e aplica fallback
    if "INDICADOR_3" in df.columns:
        datas = pd.to_datetime(df["INDICADOR_3"], errors="coerce", dayfirst=True)
    else:
        datas = pd.Series([pd.NaT] * len(df), index=df.index)

    mask_invalid = datas.isna()
    if "DATASTATUS" in df.columns:
        datas_fallback = pd.to_datetime(df["DATASTATUS"], errors="coerce", dayfirst=True)
        datas = datas.where(~mask_invalid, datas_fallback)

    df["DATA_NORMALIZADA"] = datas
    df = df.dropna(subset=["DATA_NORMALIZADA"]).copy()

    #coluna de mês/ano
    df["MES_ANO"] = df["DATA_NORMALIZADA"].dt.strftime("%m/%Y")

    #últimos n meses
    hoje = datetime.today()
    meses = [(hoje - relativedelta(months=i)).strftime("%m/%Y") for i in range(1, n_meses + 1)]
    df = df[df["MES_ANO"].isin(meses)]
    df = df[df["QUANTIDADE"] > 0]

    #chave de agrupamento (usa CODPRODUTO se existir; senão, CODORIGINAL)
    chave = "CODPRODUTO" if "CODPRODUTO" in df.columns else "CODORIGINAL"

    #filtro opcional por produto
    if codproduto is not None:
        df = df[df[chave].astype(str).str.strip() == str(codproduto).strip()]
        if df.empty:
            cols = [chave] + meses + ["MEDIA_MENSAL"]
            return pd.DataFrame(columns=cols)

    #pivot por mês
    tabela = df.pivot_table(
        index=chave,
        columns="MES_ANO",
        values="QUANTIDADE",
        aggfunc="sum",
        fill_value=0
    )

    #garante todas as colunas dos meses
    for mes in meses:
        if mes not in tabela.columns:
            tabela[mes] = 0
    tabela = tabela[meses]

    #média mensal
    tabela["MEDIA_MENSAL"] = tabela.mean(axis=1)

    return tabela.reset_index()