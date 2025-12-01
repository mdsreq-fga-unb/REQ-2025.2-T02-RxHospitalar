# RF10 - Consultar performance por vendedor
import pandas as pd
from datetime import datetime
from app.models.carregar_dados import file

#isso normaliza os valores numéricos de string pra float
def _to_number(series: pd.Series) -> pd.Series:
    s = series.astype(str).str.strip()
    s = s.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    return pd.to_numeric(s, errors="coerce").fillna(0.0)

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
        return pd.DataFrame(columns=["CODVENDEDOR", "VALOR"])

    #usa apenas TOTALPAGO2 
    if "TOTALPAGO2" not in df_periodo.columns:
        return pd.DataFrame(columns=["CODVENDEDOR", "VALOR"])

    df_periodo["VALOR"] = _to_number(df_periodo["TOTALPAGO2"])

    #agrupa e ordena por valor
    grouped = (
        df_periodo.groupby("CODVENDEDOR")["VALOR"]
        .sum()
        .sort_values(ascending=False)
        .head(limite)
        .reset_index()
    )

    grouped.columns = ["CODVENDEDOR", "VALOR"]
    return grouped