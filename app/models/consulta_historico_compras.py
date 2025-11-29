#RF09 - Consultar histórico de compras por cliente
import pandas as pd
from app.models.carregar_dados import file
import warnings
warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)

def consulta_historico_compras(cliente: str, limite: int = 10) -> pd.DataFrame:
    df_vendas = pd.read_excel(file, sheet_name="Vendas", dtype=str)

    df_cliente = df_vendas[df_vendas["CLIENTE"].astype(str).str.strip() == str(cliente).strip()]
    if df_cliente.empty:
        return pd.DataFrame(columns=df_vendas.columns)

    #converte data e ordena
    df_cliente.loc[:, "DATA"] = pd.to_datetime(df_cliente["DATA"], errors="coerce")
    df_cliente = df_cliente.sort_values("DATA", ascending=False)

    #pega as últimas 10 compras por cliente
    df_cliente = df_cliente.head(limite)

    return df_cliente.reset_index(drop=True)
