# app/models/rf10_performance_vendedor.py
import pandas as pd
from datetime import datetime
from app.models.carregar_dados import file

def consulta_performance(limite: int = 5) -> pd.DataFrame:
    df_vendas = pd.read_excel(file, sheet_name="Vendas", dtype=str)

    # Converte data
    df_vendas["DATA"] = pd.to_datetime(df_vendas["DATA"], errors="coerce", dayfirst=False)

    hoje = pd.Timestamp(datetime.today().date())
    um_mes_atras = hoje - pd.DateOffset(months=1)

    mask_periodo = (df_vendas["DATA"] >= um_mes_atras) & (df_vendas["DATA"] <= hoje)
    df_periodo = df_vendas[mask_periodo].copy()

    if df_periodo.empty:
        return pd.DataFrame(columns=["Vendedor", "Quantidade"])

    df_periodo["QUANTIDADE"] = df_periodo["QUANTIDADE"].astype(float)

    grouped = (
        df_periodo.groupby("VENDEDOR")["QUANTIDADE"]
        .sum()
        .sort_values(ascending=False)
        .head(limite)
        .reset_index()
    )

    grouped.columns = ["Vendedor", "Quantidade"]
    return grouped
