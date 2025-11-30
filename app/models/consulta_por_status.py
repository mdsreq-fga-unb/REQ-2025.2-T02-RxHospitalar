# RF05 - Consultar produtos "em estoque sem saída nos últimos 6 meses"
import os
from datetime import datetime
import unicodedata
import re
import pandas as pd
from app.models.carregar_dados import file

#esta função serve para normalizar os nomes de coluna, dado que há inconsistências entre as abas
def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s))
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w]+", " ", s).lower().strip()
    return s.replace(" ", "")

#aliases para identificar colunas chave
CODE_ALIASES = {"Cód Original", "CODORIGINAL", "Código Original", "CODPRODUTO", "Cód Produto"}
DESC_ALIASES = {"Descrição", "DESCRICAO", "Descricao"}
DATE_ALIASES = {"DATA", "DATASTATUS", "EMISSAO", "DTVENDA"}

def _achar_coluna(df: pd.DataFrame, aliases: set[str], prefix: str | None = None) -> str | None:
    norm_aliases = {_norm(a) for a in aliases}
    for c in df.columns:
        nc = _norm(c)
        if nc in norm_aliases:
            return c
    if prefix:
        for c in df.columns:
            if _norm(c).startswith(prefix):
                return c
    return None

def _carregar_planilha(sheet: str) -> pd.DataFrame:
    try:
        return pd.read_excel(file, sheet_name=sheet, header=0, dtype=str)
    except Exception:
        return pd.DataFrame()

#tenta converter várias representações sem quebrar
def _converter_tempo(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce", dayfirst=False)

#carrega dados de Estoque e Vendas
def consulta_por_status():
    df_estoque = _carregar_planilha("Estoque")
    df_vendas = _carregar_planilha("Vendas_Pendencia")
    if df_estoque.empty:
        return {"df": pd.DataFrame(), "card": "Nenhum produto encontrado (Estoque vazio)."}

    #detecta colunas relevantes
    est_code = _achar_coluna(df_estoque, CODE_ALIASES, prefix="cod")
    est_desc = _achar_coluna(df_estoque, DESC_ALIASES)
    if not est_code:
        #não há coluna de código em Estoque; sem ela, não há como cruzar
        return {"df": pd.DataFrame(), "card": "Coluna de código não encontrada na aba Estoque."}

    ven_code = _achar_coluna(df_vendas, CODE_ALIASES, prefix="cod")
    ven_date = _achar_coluna(df_vendas, DATE_ALIASES, prefix="data")
    #se Vendas estiver vazia ou sem colunas essenciais, todo estoque é “sem saída”
    if df_vendas.empty or not ven_code or not ven_date:
        resultado = df_estoque[[col for col in [est_code, est_desc] if col in df_estoque.columns]].copy()
        card = f"{len(resultado)} produtos em estoque sem registro de vendas."
        return {"df": resultado, "card": card}

    #normaliza colunas para comparação
    estoque_codes = df_estoque[est_code].astype(str).str.strip()
    vendas_codes = df_vendas[ven_code].astype(str).str.strip()
    vendas_dates = _converter_tempo(df_vendas[ven_date])

    #janela de 6 meses
    hoje = datetime.today()
    seis_meses_atras = hoje.replace(day=1)  # início do mês atual
    #subtrai 6 meses efetivos
    #usar pandas DateOffset para robustez
    seis_meses_atras = (pd.Timestamp(seis_meses_atras) - pd.DateOffset(months=6)).to_pydatetime()

    #filtra vendas recentes (últimos 6 meses)
    mask_recent = vendas_dates.notna() & (vendas_dates >= pd.Timestamp(seis_meses_atras))
    vendas_recent_codes = set(vendas_codes[mask_recent].tolist())

    #seleciona estoque cujos códigos NÃO aparecem em vendas recentes
    mask_sem_saida = ~estoque_codes.isin(vendas_recent_codes)
    resultado = df_estoque.loc[mask_sem_saida, [col for col in [est_code, est_desc] if col in df_estoque.columns]].copy()

    #saída no mesmo formato usado nos testes por linha (df + card)
    card = f"{len(resultado)} produto(s) em estoque sem saída nos últimos 6 meses."
    return {"df": resultado, "card": card}