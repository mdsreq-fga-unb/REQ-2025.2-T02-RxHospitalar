import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta



#Usada em RF07
def separar_quantidade_por_data(df, n_meses):
    """
    Processa datas usando INDICADOR_3 como prioridade.
    Se INDICADOR_3 não puder ser interpretado como data,
    tenta usar DATASTATUS.
    """

    # 1. Tentativa 1: converter INDICADOR_3
    df["DATA_NORMALIZADA"] = pd.to_datetime(
        df["INDICADOR_3"], 
        dayfirst=True, 
        errors="coerce"
    )

    # 2. Tentativa 2: onde INDICADOR_3 falhou, usar DATASTATUS
    mask_falha = df["DATA_NORMALIZADA"].isna()

    df.loc[mask_falha, "DATA_NORMALIZADA"] = pd.to_datetime(
        df.loc[mask_falha, "DATASTATUS"],
        dayfirst=True,
        errors="coerce"
    )

    # 3. Agora remove qualquer linha onde as duas opções falharam
    df = df.dropna(subset=["DATA_NORMALIZADA"])

    # 4. Criar coluna MES_ANO
    df["MES_ANO"] = df["DATA_NORMALIZADA"].dt.strftime("%m/%Y")

    # 5. Gerar lista dos últimos n meses
    hoje = datetime.today()
    meses = []
    for i in range(1, n_meses + 1):
        m = hoje - relativedelta(months=i)
        meses.append(m.strftime("%m/%Y"))

    # 6. Filtrar só meses desejados
    df = df[df["MES_ANO"].isin(meses)]

    # 7. Ignorar quantidades negativas
    df = df[df["QUANTIDADE"] > 0]

    # 8. Pivotar
    tabela = df.pivot_table(
        index="CODORIGINAL",
        columns="MES_ANO",
        values="QUANTIDADE",
        aggfunc="sum",
        fill_value=0
    )

    # 9. Garantir todas as colunas
    for mes in meses:
        if mes not in tabela.columns:
            tabela[mes] = 0

    tabela = tabela[meses]  # ordena as colunas

    # 10. Média mensal
    tabela["MEDIA_MENSAL"] = tabela.mean(axis=1)

    return tabela.reset_index()
