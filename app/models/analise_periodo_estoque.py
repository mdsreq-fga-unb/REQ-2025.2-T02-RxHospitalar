from __future__ import annotations

from datetime import datetime
from typing import Dict, Iterable, Optional

import numpy as np
import pandas as pd
from pandas.tseries.offsets import DateOffset

from app.models import carregar_dados

#usa o pandas fornecido por carregar_dados (se houver) para permitir mocks nos testes
_PD = getattr(carregar_dados, "pd", pd)

#nomes de abas esperadas na planilha
SHEET_ESTOQUE = "Estoque"
SHEET_CONSIGNADOS = "Consignado"
SHEET_PENDENTES = "Pedido Fora"
SHEET_VENDAS = "Vendas_Pendencia"

#possíveis nomes de colunas que o sistema aceita (tenta detectar automaticamente)
#ajustados para bater com a planilha real fornecida
COL_DEFAULTS: Dict[str, Iterable[str]] = {
    #Estoque: "Cód Produto"
    #Consignado: "CODIGO" ou similar
    #Pedido Fora: "Código Original"
    #Vendas_Pendencia: "CODPRODUTO" (maiúsculo)
    "codigo": ("CODPRODUTO", "Cód Produto", "Código Original", "CODIGO", "COD_PRODUTO", "PRODUTO"),
    
    #Estoque: não tem coluna explícita de quantidade, assume 1 por linha ou usa "Preço Aquisição" como proxy
    "estoque": ("ESTOQUE_ATUAL", "ESTOQUE", "QTD_ESTOQUE", "Quantidade"),
    
    #Consignado: coluna "Quantidade" (assumindo)
    "consignado": ("QUANTIDADE", "QTDE_CONSIGNADA", "CONSIGNADO", "QTD_CONSIGNADA"),
    
    #Pedido Fora: "Quantidade"
    "pendente": ("QUANTIDADE", "QTDE_PENDENTE", "PENDENTE", "QTD_PENDENTE"),
    
    #Vendas_Pendencia: "QUANTIDADE" (maiúsculo)
    "quantidade": ("QUANTIDADE", "QTD", "QTD_VENDA"),
    
    #Vendas_Pendencia: coluna de data (você mencionou que tem maiúsculas)
    "data": ("DATASTATUS", "DATA", "DTEMISSAO", "DATA_EMISSAO"),
}


def _first_col(df: pd.DataFrame, candidates: Iterable[str]) -> Optional[str]:
    """Retorna o primeiro nome de coluna que existir no dataframe dentre os candidatos."""
    for col in candidates:
        if col in df.columns:
            return col
    return None


def _read_sheet(sheet_name: str) -> pd.DataFrame:
    """
    Lê a aba `sheet_name` do arquivo configurado em carregar_dados.file.
    Em caso de arquivo inexistente ou aba ausente, retorna DataFrame vazio.
    """
    try:
        return _PD.read_excel(carregar_dados.file, sheet_name=sheet_name, dtype=str)
    except FileNotFoundError:
        return pd.DataFrame()
    except ValueError:
        #aba inexistente
        return pd.DataFrame()


def _parse_numeric(series: pd.Series) -> pd.Series:
    """
    Normaliza strings numéricas (remove pontos de milhar e converte vírgula decimal)
    e converte para float; valores inválidos viram 0.0.
    """
    if series is None:
        return pd.Series(dtype=float)
    s = (
        series.astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    return pd.to_numeric(s, errors="coerce").fillna(0.0)


def _group_sum(df: pd.DataFrame, value_candidates: Iterable[str]) -> pd.Series:
    """
    Soma valores por código de produto em `df`.
    - Detecta automaticamente a coluna de código e a coluna de valor (a partir de candidates)
    - Retorna uma Series indexada por código (string), com a soma por produto.
    """
    if df.empty:
        return pd.Series(dtype=float)
    codigo_col = _first_col(df, COL_DEFAULTS["codigo"])
    value_col = _first_col(df, value_candidates)
    
    if not codigo_col:
        return pd.Series(dtype=float)
    
    #para aba Estoque: se não houver coluna de quantidade, conta ocorrências (assume 1 por linha)
    if not value_col:
        df_count = df[[codigo_col]].copy()
        df_count[codigo_col] = df_count[codigo_col].astype(str).str.strip()
        grouped = df_count.groupby(codigo_col).size().astype(float)
        return grouped
    
    df = df[[codigo_col, value_col]].copy()
    df[value_col] = _parse_numeric(df[value_col])
    grouped = df.groupby(codigo_col)[value_col].sum()
    grouped.index = grouped.index.astype(str).str.strip()
    return grouped


def _media_saida(
    df_vendas: pd.DataFrame, periodo_meses: int, hoje: Optional[str | datetime]
) -> pd.Series:
    """
    Calcula a média mensal de saída por produto sobre os últimos `periodo_meses`.
    - Converte a coluna de data e filtra registros no intervalo [inicio_ref, hoje]
    - Soma quantidades por produto no período e divide por `periodo_meses`
    - Retorna Series (index: CODPRODUTO) com a média (float). Produtos sem vendas no período não aparecem.
    """
    if df_vendas.empty or periodo_meses <= 0:
        return pd.Series(dtype=float)

    codigo_col = _first_col(df_vendas, COL_DEFAULTS["codigo"])
    qtd_col = _first_col(df_vendas, COL_DEFAULTS["quantidade"])
    data_col = _first_col(df_vendas, COL_DEFAULTS["data"])

    if not all([codigo_col, qtd_col, data_col]):
        return pd.Series(dtype=float)

    df = df_vendas[[codigo_col, qtd_col, data_col]].copy()
    df[qtd_col] = _parse_numeric(df[qtd_col])

    #converte datas e remove linhas com datas inválidas
    df["_DATA"] = pd.to_datetime(df[data_col], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["_DATA"])
    if df.empty:
        return pd.Series(dtype=float)

    #define janela de análise: de (hoje - periodo_meses) até 'hoje'
    fim_ref = pd.Timestamp(hoje) if hoje is not None else df["_DATA"].max()
    inicio_ref = (fim_ref - DateOffset(months=periodo_meses)).normalize()

    #filtra registros dentro da janela
    df = df[df["_DATA"] >= inicio_ref]
    if df.empty:
        return pd.Series(dtype=float)

    #soma quantidades por produto e divide pelo número de meses configurado
    tot = df.groupby(codigo_col)[qtd_col].sum()
    media = tot / float(periodo_meses)

    media.index = media.index.astype(str).str.strip()
    return media


def analisar_periodo_estoque(
    periodo_meses: int = 4,
    estoque_minimo_meses: int = 4,
    hoje: Optional[str | datetime] = None,
) -> pd.DataFrame:
  
    if periodo_meses <= 0:
        raise ValueError("periodo_meses deve ser >= 1")
    if estoque_minimo_meses <= 0:
        raise ValueError("estoque_minimo_meses deve ser >= 1")

    #lê as planilhas necessárias (usa _read_sheet que retorna DF vazio se não existir)
    #Estoque: conta ocorrências de "Cód Produto" (cada linha = 1 unidade)
    estoque_atual = _group_sum(_read_sheet(SHEET_ESTOQUE), COL_DEFAULTS["estoque"])
    
    #Consignado: soma coluna "Quantidade" por código
    consignados = _group_sum(
        _read_sheet(SHEET_CONSIGNADOS), COL_DEFAULTS["consignado"]
    )
    
    #Pedido Fora: soma coluna "Quantidade" por "Código Original"
    pendentes = _group_sum(_read_sheet(SHEET_PENDENTES), COL_DEFAULTS["pendente"])
    
    #Vendas_Pendencia: calcula média de "QUANTIDADE" por "CODPRODUTO" no período
    media_saida = _media_saida(_read_sheet(SHEET_VENDAS), periodo_meses, hoje)

    #reúne todos os códigos presentes em qualquer fonte
    todos_codigos = (
        estoque_atual.index.union(consignados.index)
        .union(pendentes.index)
        .union(media_saida.index)
    )

    #constrói DataFrame de resultado indexado por código
    resultado = pd.DataFrame(index=todos_codigos)
    resultado["ESTOQUE_ATUAL"] = estoque_atual.reindex(resultado.index, fill_value=0)
    resultado["CONSIGNADO"] = consignados.reindex(resultado.index, fill_value=0)
    resultado["PENDENTE"] = pendentes.reindex(resultado.index, fill_value=0)

    #estoque total = estoque atual + consignado + pendente
    resultado["ESTOQUE_TOTAL"] = (
        resultado["ESTOQUE_ATUAL"]
        + resultado["CONSIGNADO"]
        + resultado["PENDENTE"]
    )

    #média de saída (pode ser zero se não houver vendas no período)
    resultado["MEDIA_SAIDA"] = media_saida.reindex(resultado.index, fill_value=0)

    #cálculo do período de estoque em meses:
    #se MEDIA_SAIDA > 0: estoque_total / media
    #se média == 0: período infinito (np.inf)
    resultado["PERIODO_ESTOQUE_MESES"] = np.where(
        resultado["MEDIA_SAIDA"] > 0,
        resultado["ESTOQUE_TOTAL"] / resultado["MEDIA_SAIDA"],
        np.inf,
    )

    #sugestão bruta = estoque ideal em unidades (estoque_minimo_meses * média) - estoque_total
    sugestao_bruta = (
        estoque_minimo_meses * resultado["MEDIA_SAIDA"] - resultado["ESTOQUE_TOTAL"]
    )
    #sugere apenas valores >= 0 e arredonda a 2 casas
    resultado["SUGESTAO_COMPRA"] = sugestao_bruta.clip(lower=0).round(2)

    #flag crítico: True quando período calculado está abaixo do estoque mínimo (em meses)
    resultado["CRITICO"] = resultado["PERIODO_ESTOQUE_MESES"] < estoque_minimo_meses

    #formata o resultado final, renomeando índice para CODPRODUTO e ordenando:
    #produtos críticos primeiro (CRITICO=True) e, dentro disso, por menor período
    resultado = (
        resultado.reset_index()
        .rename(columns={"index": "CODPRODUTO"})
        .sort_values(["CRITICO", "PERIODO_ESTOQUE_MESES"], ascending=[False, True])
        .reset_index(drop=True)
    )

    #retorna apenas as colunas públicas esperadas
    return resultado[
        [
            "CODPRODUTO",
            "ESTOQUE_ATUAL",
            "CONSIGNADO",
            "PENDENTE",
            "ESTOQUE_TOTAL",
            "MEDIA_SAIDA",
            "PERIODO_ESTOQUE_MESES",
            "SUGESTAO_COMPRA",
            "CRITICO",
        ]
    ]