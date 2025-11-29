# RF08 - Consultar principais clientes de cada produto
import pandas as pd
from app.models.carregar_dados import file

def consulta_principais_clientes(codproduto: str, limite: int = 5) -> pd.DataFrame:
    df_vendas = pd.read_excel(file, sheet_name="Vendas_Pendencia", dtype=str)

    #garante coluna quantitativa
    df_vendas["QUANTIDADE"] = df_vendas["QUANTIDADE"].astype(float)

    #filtra produto
    df_prod = df_vendas[df_vendas["CODPRODUTO"].astype(str).str.strip() == str(codproduto).strip()]
    if df_prod.empty:
        return pd.DataFrame(columns=["RAZAOSOCIAL", "QUANTIDADE"])

    #agrupa por cliente e soma
    grouped = (
        df_prod.groupby("RAZAOSOCIAL")["QUANTIDADE"]
        .sum()
        .sort_values(ascending=False)
        .head(limite)
        .reset_index()
    )

    grouped.columns = ["RAZAOSOCIAL", "QUANTIDADE"]
    return grouped