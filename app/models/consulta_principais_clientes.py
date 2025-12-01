#RF08 - Consultar principais clientes de cada produto
import warnings
import pandas as pd
from app.models.carregar_dados import file
warnings.filterwarnings(
    "ignore",
    message="Could not infer format, so each element will be parsed individually",
    category=UserWarning,
)

def consulta_principais_clientes(codproduto: str, limite: int = 5) -> pd.DataFrame:
    
    #carrega vendas
    df_vendas = pd.read_excel(file, sheet_name="Vendas_Pendencia", dtype=str)

    #filtra produto
    df_prod = df_vendas[df_vendas["CODPRODUTO"].astype(str).str.strip() == str(codproduto).strip()].copy()
    if df_prod.empty:
        return pd.DataFrame(columns=["RAZAOSOCIAL", "FREQUENCIA", "TOTAL_QUANTIDADE", "MEDIA_MENSAL"])

    #normaliza quantidade (se não existir, assume 1 por registro)
    df_prod["QUANTIDADE"] = pd.to_numeric(df_prod.get("QUANTIDADE", pd.Series(index=df_prod.index, dtype="int")), errors="coerce").fillna(1)

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
        .reset_index(name="FREQUENCIA") if False else None
    )
    #usar .size() confiável pra evitar confusão
    freq = df_prod.groupby("RAZAOSOCIAL").size().reset_index(name="FREQUENCIA")

    #meses distintos por cliente (mínimo 1) - só vai calcular os meses em que houver compra
    meses = (
        df_prod.groupby("RAZAOSOCIAL")["_MES_ANO"]
        .apply(lambda s: s.dropna().nunique() if s.notna().any() else 1)
        .rename("MESES")
        .reset_index()
    )

    #total de quantidade por cliente
    tot_qtd = (
        df_prod.groupby("RAZAOSOCIAL")["QUANTIDADE"]
        .sum()
        .reset_index(name="TOTAL_QUANTIDADE")
    )

    #junta e calcula média mensal (TOTAL_QUANTIDADE / MESES)
    res = freq.merge(meses, on="RAZAOSOCIAL", how="left")
    res = res.merge(tot_qtd, on="RAZAOSOCIAL", how="left")
    res["MESES"] = res["MESES"].replace(0, 1)
    res["MEDIA_MENSAL"] = (res["TOTAL_QUANTIDADE"] / res["MESES"]).round(2)

    #ordena por frequência desc e limita
    res = res.sort_values(by="FREQUENCIA", ascending=False).head(limite).reset_index(drop=True)
    return res[["RAZAOSOCIAL", "FREQUENCIA", "TOTAL_QUANTIDADE", "MEDIA_MENSAL"]]
