import pandas as pd
from app.models.carregar_dados import file

def consulta_principais_clientes(codproduto: str, limite: int = 5) -> pd.DataFrame:
    df_vendas = pd.read_excel(file, sheet_name="Vendas", dtype=str)

    # Garante coluna quantitativa
    df_vendas["QUANTIDADE"] = df_vendas["QUANTIDADE"].astype(float)

    # Filtra produto
    df_prod = df_vendas[df_vendas["CODPRODUTO"].astype(str).str.strip() == str(codproduto).strip()]
    if df_prod.empty:
        return pd.DataFrame(columns=["Cliente", "Quantidade"])

    # Agrupa por cliente e soma
    grouped = (
        df_prod.groupby("CLIENTE")["QUANTIDADE"]
        .sum()
        .sort_values(ascending=False)
        .head(limite)
        .reset_index()
    )

    grouped.columns = ["Cliente", "Quantidade"]
    return grouped