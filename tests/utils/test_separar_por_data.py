import pandas as pd
import pytest
from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.utils.separar_por_data import separar_quantidade_por_data

def test_separar_quantidade_por_data_completo():
    """
    Testa o fluxo completo da função:
    1. Normalização de datas (INDICADOR_3 vs DATASTATUS).
    2. Filtragem dos últimos N meses (ignorando mês atual/futuro).
    3. Agrupamento (Pivot) e soma de quantidades.
    4. Cálculo da média.
    """
    
    # --- ARRANGE (Cenário) ---
    hoje = datetime.today()
    
    # Datas relativas para o teste ficar dinâmico
    mes_passado = hoje - relativedelta(months=1)
    dois_meses_atras = hoje - relativedelta(months=2)
    
    # Strings esperadas nas colunas
    str_mes_passado = mes_passado.strftime("%m/%Y")
    str_dois_meses = dois_meses_atras.strftime("%m/%Y")
    
    # Criando DataFrame simulado
    data = {
        "CODORIGINAL": ["PROD_A", "PROD_A", "PROD_A", "PROD_B", "PROD_C"],
        "GRUPO":       ["G1",     "G1",     "G1",     "G2",     "G3"],
        
        # PROD_A: Tem venda mês passado e 2 meses atrás
        # PROD_B: Venda HOJE (deve ser ignorada pois range começa em 1)
        # PROD_C: Data inválida (deve ser removido)
        "INDICADOR_3": [mes_passado, dois_meses_atras, mes_passado, hoje, None],
        
        # PROD_C tenta salvar com DATASTATUS ruim
        "DATASTATUS":  [None, None, None, None, "Data Invalida"],
        
        # Quantidades
        "QUANTIDADE":  [10, 20, 5, 100, 50]
    }
    
    df_entrada = pd.DataFrame(data)
    
    # --- ACT (Execução) ---
    # Pedimos análise dos últimos 2 meses
    # Esperado: PROD_A deve aparecer. PROD_B (hoje) e PROD_C (inválido) devem sumir.
    resultado = separar_quantidade_por_data(df_entrada, n_meses=2)
    
    # --- ASSERT (Verificação) ---
    
    # 1. Verificações de estrutura
    assert "CODORIGINAL" in resultado.columns
    assert "GRUPO" in resultado.columns
    assert "MEDIA_MENSAL" in resultado.columns
    assert str_mes_passado in resultado.columns
    assert str_dois_meses in resultado.columns
    
    # 2. Verifica filtros
    # PROD_B foi excluído (mês atual)? PROD_C foi excluído (data inválida)?
    # Deve restar apenas PROD_A
    assert len(resultado) == 1
    assert resultado.iloc[0]["CODORIGINAL"] == "PROD_A"
    
    # 3. Verifica soma (Pivot)
    # PROD_A teve duas vendas no mês passado: 10 + 5 = 15
    # PROD_A teve uma venda 2 meses atrás: 20
    row = resultado.iloc[0]
    assert row[str_mes_passado] == 15
    assert row[str_dois_meses] == 20
    
    # 4. Verifica média
    # (15 + 20) / 2 = 17.5
    assert row["MEDIA_MENSAL"] == 17.5