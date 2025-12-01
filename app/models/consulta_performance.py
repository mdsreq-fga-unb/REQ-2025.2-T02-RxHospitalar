# RF10 - Consultar performance por vendedor
import pandas as pd
from datetime import datetime
from app.models.carregar_dados import file

def consulta_performance(limite: int = 5) -> pd.DataFrame:
    df_vendas = pd.read_excel(file, sheet_name="Vendas_Pendencia", dtype=str)

    #converte data
    df_vendas["DATASTATUS"] = pd.to_datetime(df_vendas["DATASTATUS"], errors="coerce", dayfirst=False)

    #define a janela como o último mês
    hoje = pd.Timestamp(datetime.today().date())
    um_mes_atras = hoje - pd.DateOffset(months=1)

    #filtra período
    mask_periodo = (df_vendas["DATASTATUS"] >= um_mes_atras) & (df_vendas["DATASTATUS"] <= hoje)
    df_periodo = df_vendas[mask_periodo].copy()

    #caso não haja registros
    if df_periodo.empty:
        return pd.DataFrame(columns=["CODVENDEDOR", "QUANTIDADE"])

    #garante tipo numérico para agregar
    df_periodo["QUANTIDADE"] = df_periodo["QUANTIDADE"].astype(float)

    #agrupa e ordena
    grouped = (
        df_periodo.groupby("CODVENDEDOR")["QUANTIDADE"]
        .sum()
        .sort_values(ascending=False)
        .head(limite)
        .reset_index()
    )

    #ajusta nomes finais das colunas
    grouped.columns = ["CODVENDEDOR", "QUANTIDADE"]
    return grouped
