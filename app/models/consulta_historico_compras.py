#RF09 - Consultar histórico de compras por cliente
import pandas as pd
from app.models.carregar_dados import file
import warnings
warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)

def listar_clientes() -> pd.DataFrame:
    #Retorna DataFrame com a lista única de clientes em ordem alfabpetica para uso em dropdown
    df_vendas = pd.read_excel(file, sheet_name="Vendas_Pendencia", dtype=str)

    if "RAZAOSOCIAL" not in df_vendas.columns:
        return pd.DataFrame(columns=["RAZAOSOCIAL"])

    #não converter None para string; strip apenas em strings
    serie = df_vendas["RAZAOSOCIAL"].map(lambda x: x.strip() if isinstance(x, str) else x)
    #substituir vazios por NA e remover NA
    serie = serie.replace("", pd.NA).dropna()
    #deduplicar e ordenar
    clientes = serie.drop_duplicates().sort_values().reset_index(drop=True)

    return pd.DataFrame({"RAZAOSOCIAL": clientes})

def consulta_historico_compras(cliente: str, limite: int = 10) -> pd.DataFrame:
    #carrega vendas
    df_vendas = pd.read_excel(file, sheet_name="Vendas_Pendencia", dtype=str)

    #filtra cliente alvo
    df_cliente = df_vendas[df_vendas["RAZAOSOCIAL"].astype(str).str.strip() == str(cliente).strip()]
    if df_cliente.empty:
        return pd.DataFrame(columns=df_vendas.columns)

    #converte data e ordena
    df_cliente.loc[:, "DATASTATUS"] = pd.to_datetime(df_cliente["DATASTATUS"], errors="coerce")
    
    #ordena por data decrescente
    df_cliente = df_cliente.sort_values("DATASTATUS", ascending=False)

    #pega as últimas 10 compras por cliente
    df_cliente = df_cliente.head(limite)

    return df_cliente.reset_index(drop=True)
