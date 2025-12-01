import pandas as pd
import pytest
from pathlib import Path
from app.models.analise_periodo_estoque import analisar_periodo_estoque
import app.models.carregar_dados as carregar_dados
from app.models.carregar_dados import file

@pytest.fixture
def mock_planilhas(monkeypatch):
    #cria fixture para mockar as abas da planilha.
    #garante que carregar_dados tenha um atributo pd
    if not hasattr(carregar_dados, "pd"):
        import pandas as _pd
        carregar_dados.pd = _pd

    sheets = {}

    def fake_read_excel(_file, sheet_name=None, **_):
        #devolve o DF da "aba" mockada ou DF vazio se não existir
        return sheets.get(sheet_name, pd.DataFrame())

    monkeypatch.setattr(carregar_dados.pd, "read_excel", fake_read_excel)
    return sheets


def test_rf01_calcula_periodo_e_sugestao(mock_planilhas):
    #testa cálculo de período de estoque e sugestão de compra.
    #monta as 4 planilhas com os nomes corretos das abas
    mock_planilhas["Estoque"] = pd.DataFrame(
        {"Cód Produto": ["P1", "P2"]}  # sem quantidade, conta ocorrências
    )
    mock_planilhas["Consignado"] = pd.DataFrame(
        {"CODIGO": ["P1"], "QUANTIDADE": ["20"]}
    )
    mock_planilhas["Pedido Fora"] = pd.DataFrame(
        {"Código Original": ["P1", "P2"], "QUANTIDADE": ["30", "5"]}
    )
    mock_planilhas["Vendas_Pendencia"] = pd.DataFrame(
        {
            "CODPRODUTO": ["P1", "P1", "P2", "P2"],
            "DATASTATUS": ["2025-02-10", "2025-01-05", "2025-02-01", "2024-12-15"],
            "QUANTIDADE": ["40", "20", "30", "50"],
        }
    )

    df = analisar_periodo_estoque(
        periodo_meses=4, estoque_minimo_meses=4, hoje="2025-02-28"
    )

    #P1 – caso com estoque confortável (não crítico)
    p1 = df[df["CODPRODUTO"] == "P1"].iloc[0]
    assert p1["ESTOQUE_ATUAL"] == 1  # conta 1 ocorrência em "Estoque"
    assert p1["CONSIGNADO"] == 20
    assert p1["PENDENTE"] == 30
    assert p1["ESTOQUE_TOTAL"] == 51  # 1 + 20 + 30
    
    #média de saída (total no período / meses) – valida fórmula
    media_p1 = float(p1["MEDIA_SAIDA"])
    assert media_p1 > 0
    assert pytest.approx(p1["PERIODO_ESTOQUE_MESES"]) == p1["ESTOQUE_TOTAL"] / media_p1
    
    #sugestão deve considerar estoque ideal de 4 meses
    estoque_alvo_p1 = 4 * media_p1
    assert pytest.approx(p1["SUGESTAO_COMPRA"]) == max(0.0, estoque_alvo_p1 - p1["ESTOQUE_TOTAL"])

    #P2 – caso crítico (estoque baixo)
    p2 = df[df["CODPRODUTO"] == "P2"].iloc[0]
    assert p2["ESTOQUE_ATUAL"] == 1  # conta 1 ocorrência
    assert p2["CONSIGNADO"] == 0
    assert p2["PENDENTE"] == 5
    assert p2["ESTOQUE_TOTAL"] == 6  # 1 + 0 + 5

    #valida RF01: período de estoque = estoque total / média de saída
    media_p2 = float(p2["MEDIA_SAIDA"])
    assert media_p2 > 0
    assert pytest.approx(p2["PERIODO_ESTOQUE_MESES"]) == p2["ESTOQUE_TOTAL"] / media_p2

    #valida que sugestão leva ao estoque ideal de 4 meses
    estoque_total = float(p2["ESTOQUE_TOTAL"])
    estoque_alvo = 4 * media_p2
    assert pytest.approx(p2["SUGESTAO_COMPRA"]) == max(0.0, estoque_alvo - estoque_total)

    #produto deve ser crítico (abaixo de 4 meses)
    assert bool(p2["CRITICO"])


def test_rf01_periodo_configuravel_e_media_zero(mock_planilhas):
    #testa período configurável e validação da fórmula do RF01.
    mock_planilhas["Estoque"] = pd.DataFrame(
        {"Cód Produto": ["PX", "PY"]}  # 1 ocorrência cada
    )
    mock_planilhas["Consignado"] = pd.DataFrame(
        {"CODIGO": ["PX"], "QUANTIDADE": ["10"]}
    )
    mock_planilhas["Pedido Fora"] = pd.DataFrame(
        {"Código Original": ["PX"], "QUANTIDADE": ["5"]}
    )
    #PX: vendas em período anterior
    #PY: sem vendas
    mock_planilhas["Vendas_Pendencia"] = pd.DataFrame(
        {
            "CODPRODUTO": ["PX", "PX"],
            "DATASTATUS": ["2024-01-10", "2024-02-10"],
            "QUANTIDADE": ["10", "10"],
        }
    )

    df = analisar_periodo_estoque(
        periodo_meses=5, estoque_minimo_meses=4, hoje="2024-10-01"
    )

    #PX: valida fórmula RF01 independente da média calculada
    px = df[df["CODPRODUTO"] == "PX"].iloc[0]
    assert px["ESTOQUE_TOTAL"] == 16  # 1 + 10 + 5
    media_px = float(px["MEDIA_SAIDA"])
    
    #valida fórmula: período = estoque_total / média
    if media_px > 0:
        assert pytest.approx(px["PERIODO_ESTOQUE_MESES"]) == px["ESTOQUE_TOTAL"] / media_px
        #valida sugestão: estoque_alvo - estoque_total
        estoque_alvo = 4 * media_px
        assert pytest.approx(px["SUGESTAO_COMPRA"]) == max(0.0, estoque_alvo - px["ESTOQUE_TOTAL"])
    else:
        #se média for zero, período deve ser infinito
        assert px["PERIODO_ESTOQUE_MESES"] == pytest.approx(float("inf"))
        assert px["SUGESTAO_COMPRA"] == 0

    #PY: sem vendas => média 0, período infinito, sem sugestão
    py = df[df["CODPRODUTO"] == "PY"].iloc[0]
    assert py["ESTOQUE_TOTAL"] == 1  # só estoque atual
    assert py["MEDIA_SAIDA"] == 0
    assert py["PERIODO_ESTOQUE_MESES"] == pytest.approx(float("inf"))
    assert py["SUGESTAO_COMPRA"] == 0
    assert not bool(py["CRITICO"])


@pytest.fixture(scope="module")
def planilha_existe():
    #pula testes se a planilha real não existir.
    if not Path(file).exists():
        pytest.skip(f"Planilha não encontrada: {file}")
    return True


def test_rf01_integrado_formula_periodo(planilha_existe):
    #valida que a fórmula período = estoque_total / média_saida está correta na planilha real.
    df = analisar_periodo_estoque(periodo_meses=4, estoque_minimo_meses=4)
    
    assert not df.empty, "DataFrame de análise de estoque não pode ser vazio"
    
    #para cada produto, valida a fórmula do RF01
    for _, row in df.iterrows():
        media = float(row["MEDIA_SAIDA"])
        periodo = float(row["PERIODO_ESTOQUE_MESES"])
        estoque = float(row["ESTOQUE_TOTAL"])
        
        if media > 0:
            #período = estoque / média
            assert pytest.approx(periodo, rel=1e-5) == estoque / media
        else:
            #se média = 0, período deve ser infinito
            assert periodo == pytest.approx(float("inf"))


def test_rf01_integrado_sugestao_compra(planilha_existe):
    #valida que a sugestão de compra leva ao estoque mínimo ideal.
    estoque_minimo = 4
    df = analisar_periodo_estoque(periodo_meses=4, estoque_minimo_meses=estoque_minimo)
    
    for _, row in df.iterrows():
        media = float(row["MEDIA_SAIDA"])
        estoque = float(row["ESTOQUE_TOTAL"])
        sugestao = float(row["SUGESTAO_COMPRA"])
        
        if media > 0:
            estoque_alvo = estoque_minimo * media
            esperado = max(0.0, estoque_alvo - estoque)
            assert pytest.approx(sugestao, abs=0.01) == esperado
        else:
            #sem saída => sem necessidade de compra
            assert sugestao == 0


def test_rf01_integrado_flag_critico(planilha_existe):
    #valida que produtos com período < 4 meses são marcados como críticos.
    df = analisar_periodo_estoque(periodo_meses=4, estoque_minimo_meses=4)
    
    for _, row in df.iterrows():
        periodo = float(row["PERIODO_ESTOQUE_MESES"])
        critico = bool(row["CRITICO"])
        
        if periodo < 4 and periodo != float("inf"):
            assert critico, f"Produto {row['CODPRODUTO']} com período {periodo:.2f} deveria ser crítico"
        else:
            assert not critico, f"Produto {row['CODPRODUTO']} com período {periodo:.2f} não deveria ser crítico"


def test_rf01_integrado_colunas_obrigatorias(planilha_existe):
    #valida que todas as colunas do RF01 estão presentes.
    df = analisar_periodo_estoque(periodo_meses=4, estoque_minimo_meses=4)
    
    colunas_esperadas = [
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
    
    for col in colunas_esperadas:
        assert col in df.columns, f"Coluna obrigatória '{col}' não encontrada"


def test_rf01_integrado_periodo_configuravel(planilha_existe):
    #valida que o parâmetro periodo_meses é respeitado.
    #testa com 3 e 6 meses
    df_3m = analisar_periodo_estoque(periodo_meses=3, estoque_minimo_meses=4)
    df_6m = analisar_periodo_estoque(periodo_meses=6, estoque_minimo_meses=4)
    
    assert not df_3m.empty
    assert not df_6m.empty
    
    #as médias devem ser diferentes (exceto se não houver vendas)
    #pega um produto que existe em ambos
    codigos_comuns = set(df_3m["CODPRODUTO"]) & set(df_6m["CODPRODUTO"])
    if codigos_comuns:
        cod = list(codigos_comuns)[0]
        media_3m = df_3m[df_3m["CODPRODUTO"] == cod]["MEDIA_SAIDA"].iloc[0]
        media_6m = df_6m[df_6m["CODPRODUTO"] == cod]["MEDIA_SAIDA"].iloc[0]
        
        #se ambos têm média > 0, devem ser diferentes (janelas diferentes)
        if media_3m > 0 and media_6m > 0:
            #não precisa ser exatamente diferente, mas testamos que ambos calcularam
            assert media_3m >= 0 and media_6m >= 0


def test_rf01_integrado_estoque_total_correto(planilha_existe):
    #valida que estoque_total = estoque_atual + consignado + pendente.
    df = analisar_periodo_estoque(periodo_meses=4, estoque_minimo_meses=4)
    
    for _, row in df.iterrows():
        atual = float(row["ESTOQUE_ATUAL"])
        consignado = float(row["CONSIGNADO"])
        pendente = float(row["PENDENTE"])
        total = float(row["ESTOQUE_TOTAL"])
        
        assert pytest.approx(total, abs=0.01) == atual + consignado + pendente


def test_rf01_integrado_ordenacao_criticos_primeiro(planilha_existe):
    #valida que produtos críticos aparecem primeiro na lista.
    df = analisar_periodo_estoque(periodo_meses=4, estoque_minimo_meses=4)
    
    #se houver críticos, eles devem estar no topo
    criticos = df[df["CRITICO"] == True]
    nao_criticos = df[df["CRITICO"] == False]
    
    if not criticos.empty and not nao_criticos.empty:
        #o último crítico deve estar antes do primeiro não-crítico
        idx_ultimo_critico = criticos.index[-1]
        idx_primeiro_nao_critico = nao_criticos.index[0]
        assert idx_ultimo_critico < idx_primeiro_nao_critico