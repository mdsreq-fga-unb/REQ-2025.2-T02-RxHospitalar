import os
import pandas as pd
import pytest
from app.models.consulta_sazonalidade import consulta_sazonalidade_por_linha
from app.models.carregar_dados import file

def _file_exists() -> bool:
    #suporta tanto Path quanto str
    try:
        from pathlib import Path
        if isinstance(file, Path):
            return file.exists()
    except Exception:
        pass
    return os.path.exists(str(file))

@pytest.mark.skipif(
    not _file_exists(),  
    reason="Arquivo Excel não encontrado em app.models.carregar_dados.file",
)
def test_rf11_sazonalidade_formato_real():
    #carrega planilha real
    df = pd.read_excel(file, sheet_name="Vendas_Pendencia", dtype=str)

    if "GRUPO" not in df.columns:
        pytest.skip("Planilha real não possui coluna 'GRUPO'")

    #pega uma linha real existente
    linha_exemplo = (
        df["GRUPO"]
        .dropna()
        .astype(str)
        .str.strip()
        .iloc[0]
    )

    out = consulta_sazonalidade_por_linha(
        linha=linha_exemplo,
        coluna_linha="GRUPO",
        n_top=5,
        usar_valor=False,
    )

    #estrutura básica
    assert set(out.keys()) == {"linha", "mensal", "top_clientes", "recorrentes"}
    assert out["linha"] == linha_exemplo

    mensal = out["mensal"]
    assert list(mensal.columns) == ["MES", "TOTAL"]
    assert len(mensal) == 12
    assert set(mensal["MES"]) == set(range(1, 13))
    assert pd.api.types.is_numeric_dtype(mensal["TOTAL"])

    top = out["top_clientes"]
    #pode estar vazio se não houver vendas para a linha, mas as colunas devem existir
    assert {"RAZAOSOCIAL", "FREQUENCIA", "TOTAL_QUANTIDADE"}.issubset(top.columns)
    if not top.empty:
        assert pd.api.types.is_numeric_dtype(top["FREQUENCIA"])
        assert pd.api.types.is_numeric_dtype(top["TOTAL_QUANTIDADE"])

@pytest.mark.skipif(
    not _file_exists(),  
    reason="Arquivo Excel não encontrado em app.models.carregar_dados.file",
)
def test_rf11_sazonalidade_valor_e_recorrentes_real():
    df = pd.read_excel(file, sheet_name="Vendas_Pendencia", dtype=str)

    if "GRUPO" not in df.columns:
        pytest.skip("Planilha real não possui coluna 'GRUPO' para RF11")

    #escolhe uma linha com pelo menos um cliente repetido, se possível
    #(fallback: pega qualquer linha)
    grupo_cliente = df.dropna(subset=["GRUPO", "RAZAOSOCIAL"])
    if grupo_cliente.empty:
        pytest.skip("Planilha real não possui GRUPO/RAZAOSOCIAL preenchidos")

    linha_exemplo = grupo_cliente["GRUPO"].astype(str).str.strip().iloc[0]

    out = consulta_sazonalidade_por_linha(
        linha=linha_exemplo,
        coluna_linha="GRUPO",
        n_top=10,
        usar_valor=True,  #agora considera TOTALPAGO2 se existir
    )

    mensal = out["mensal"]
    assert list(mensal.columns) == ["MES", "TOTAL"]
    assert len(mensal) == 12
    assert pd.api.types.is_numeric_dtype(mensal["TOTAL"])

    top = out["top_clientes"]
    assert {"RAZAOSOCIAL", "FREQUENCIA", "TOTAL_QUANTIDADE"}.issubset(top.columns)
    #se TOTALPAGO2 existir e tiver sido usado, a coluna TOTAL_VALOR deve estar presente
    if "TOTAL_VALOR" in top.columns:
        assert pd.api.types.is_numeric_dtype(top["TOTAL_VALOR"])

    #recorrentes é coerente com FREQUENCIA >= 2
    recorrentes = out["recorrentes"]
    if recorrentes:
        freq_map = dict(zip(top["RAZAOSOCIAL"], top["FREQUENCIA"]))
        for cli in recorrentes:
            assert freq_map.get(cli, 0) >= 2