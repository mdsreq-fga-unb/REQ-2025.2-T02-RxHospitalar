#RF08 - Consultar principais clientes de cada produto
import pandas as pd
from app.models.carregar_dados import file

def consulta_principais_clientes(codproduto: str, limite: int = 5) -> pd.DataFrame:
    
    #carrega vendas
    df_vendas = pd.read_excel(file, sheet_name="Vendas_Pendencia", dtype=str)

    #filtra produto
    df_prod = df_vendas[df_vendas["CODPRODUTO"].astype(str).str.strip() == str(codproduto).strip()].copy()
    if df_prod.empty:
        return pd.DataFrame(columns=["RAZAOSOCIAL", "FREQUENCIA", "MEDIA_MENSAL"])

    #normaliza DATASTATUS para mês/ano. Se ausente/inválida, média usará 1 mês
    if "DATASTATUS" in df_prod.columns:
        datas = pd.to_datetime(df_prod["DATASTATUS"], errors="coerce", dayfirst=False)
        df_prod["_MES_ANO"] = datas.dt.to_period("M").astype(str)
    else:
        df_prod["_MES_ANO"] = None

    #frequência de compras por cliente (contagem de registros)
    freq = (
        df_prod.groupby("RAZAOSOCIAL", as_index=False)
        .size()
        .rename(columns={"size": "FREQUENCIA"})
    )

    #meses distintos por cliente (mínimo 1) - só vai calcular os meses em que houver compra
    meses = (
        df_prod.groupby("RAZAOSOCIAL")["_MES_ANO"]
        .apply(lambda s: s.dropna().nunique() if s.notna().any() else 1)
        .rename("MESES")
        .reset_index()
    )

    #junta e calcula média mensal
    res = freq.merge(meses, on="RAZAOSOCIAL", how="left")
    res["MESES"] = res["MESES"].replace(0, 1)
    res["MEDIA_MENSAL"] = (res["FREQUENCIA"] / res["MESES"]).round(2)

    #ordena por frequência desc e limita
    res = res.sort_values(by="FREQUENCIA", ascending=False).head(limite).reset_index(drop=True)
    return res[["RAZAOSOCIAL", "FREQUENCIA", "MEDIA_MENSAL"]]