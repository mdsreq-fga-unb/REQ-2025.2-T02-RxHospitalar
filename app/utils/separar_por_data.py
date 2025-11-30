import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta



#Usada em RF07
def separar_quantidade_por_data(df, n_meses):
    """
    Processa as datas, filtra últimos n meses, agrupa por CODORIGINAL e retorna
    uma tabela contendo as colunas mensais, média e também a coluna GRUPO.
    """

    # Garante uma cópia para evitar SettingWithCopyWarning
    df = df.copy()

    # ==============================
    # 1. Normalização de datas
    # ==============================
    df["DATA_NORMALIZADA"] = pd.to_datetime(
        df["INDICADOR"], 
        format="%d/%m/%Y",
        dayfirst=True, 
        errors="coerce"
    )

    mask_falha = df["DATA_NORMALIZADA"].isna()
    df.loc[mask_falha, "DATA_NORMALIZADA"] = pd.to_datetime(
        df.loc[mask_falha, "DATASTATUS"],
        format="%Y-%m-%d",
        dayfirst=True,
        errors="coerce"
    )

    df = df.dropna(subset=["DATA_NORMALIZADA"]).copy()

    # Coluna MES_ANO
    df["MES_ANO"] = df["DATA_NORMALIZADA"].dt.strftime("%m/%Y")

    # ==============================
    # 2. Últimos n meses
    # ==============================
    hoje = datetime.today()
    meses = [(hoje - relativedelta(months=i)).strftime("%m/%Y") for i in range(1, n_meses + 1)]

    df = df[df["MES_ANO"].isin(meses)]
    df = df[df["QUANTIDADE"] > 0]

    # ==============================
    # 3. Guardar coluna GRUPO por código
    # ==============================
    grupos = df[["CODORIGINAL", "GRUPO"]].drop_duplicates()

    # ==============================
    # 4. Pivot por mês
    # ==============================
    tabela = df.pivot_table(
        index="CODORIGINAL",
        columns="MES_ANO",
        values="QUANTIDADE",
        aggfunc="sum",
        fill_value=0
    )

    # Garantir todas as colunas (meses)
    for mes in meses:
        if mes not in tabela.columns:
            tabela[mes] = 0

    tabela = tabela[meses]  # Ordena colunas

    # Média mensal
    tabela["MEDIA_MENSAL"] = tabela.mean(axis=1)

    tabela = tabela.reset_index()

    # ==============================
    # 5. Recolocar GRUPO no resultado final
    # ==============================
    tabela = tabela.merge(grupos, on="CODORIGINAL", how="left")

    # Deixar GRUPO como segunda coluna (ficar organizado)
    cols = ["CODORIGINAL", "GRUPO"] + [c for c in tabela.columns if c not in ["CODORIGINAL", "GRUPO"]]
    tabela = tabela[cols]

    return tabela