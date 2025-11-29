#RF09 - Consultar histórico de compras por cliente
import pandas as pd
from app.models.carregar_dados import file
import warnings
warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)

def consulta_historico_compras(cliente: str, limite: int = 10) -> pd.DataFrame:
    df_vendas = pd.read_excel(file, sheet_name="Vendas_Pendencia", dtype=str)

    df_cliente = df_vendas[df_vendas["RAZAOSOCIAL"].astype(str).str.strip() == str(cliente).strip()]
    if df_cliente.empty:
        return pd.DataFrame(columns=df_vendas.columns)

    #converte data e ordena
    df_cliente.loc[:, "DATASTATUS"] = pd.to_datetime(df_cliente["DATASTATUS"], errors="coerce")
    df_cliente = df_cliente.sort_values("DATASTATUS", ascending=False)

    #pega as últimas 10 compras por cliente
    df_cliente = df_cliente.head(limite)

    return df_cliente.reset_index(drop=True)
