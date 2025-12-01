import pandas as pd
import pytest
from app.utils.dataframe_utils import filtrar_por_codigo, juntar_por_codigo, quantidade_para_comprar

# ==============================================================================
# 1. Testes para filtrar_por_codigo
# ==============================================================================
def test_filtrar_por_codigo_basico():
    """Testa se o filtro funciona para um código simples existente."""
    # Arrange
    df = pd.DataFrame({
        'CODIGO': ['A100', 'B200', 'C300'],
        'VALOR': [1, 2, 3]
    })
    
    # Act
    resultado = filtrar_por_codigo(df, 'CODIGO', 'B200')
    
    # Assert
    assert len(resultado) == 1
    assert resultado.iloc[0]['CODIGO'] == 'B200'

def test_filtrar_por_codigo_case_insensitive():
    """Testa se o filtro ignora maiúsculas/minúsculas e espaços."""
    # Arrange
    df = pd.DataFrame({
        'CODIGO': [' a100 ', 'B200'],
        'VALOR': [1, 2]
    })
    
    # Act - busca 'A100' num dataframe que tem ' a100 '
    resultado = filtrar_por_codigo(df, 'CODIGO', 'A100')
    
    # Assert
    assert len(resultado) == 1
    assert resultado.iloc[0]['VALOR'] == 1

# ==============================================================================
# 2. Testes para juntar_por_codigo
# ==============================================================================
def test_juntar_por_codigo_match():
    """Testa o Inner Join entre Vendas e Estoque."""
    # Arrange
    df_vendas = pd.DataFrame({
        'CODORIGINAL': ['PROD_A', 'PROD_B'], # PROD_B só tem aqui
        'MEDIA_MENSAL': [10, 20]
    })
    
    df_estoque = pd.DataFrame({
        'Cód Original': ['PROD_A', 'PROD_C'], # PROD_C só tem aqui
        'Estoque': [100, 50]
    })
    
    # Act
    resultado = juntar_por_codigo(df_vendas, df_estoque)
    
    # Assert
    # Deve sobrar apenas PROD_A (interseção)
    assert len(resultado) == 1
    assert resultado.iloc[0]['CODORIGINAL'] == 'PROD_A'
    # Verifica se trouxe colunas dos dois lados
    assert 'MEDIA_MENSAL' in resultado.columns
    assert 'Estoque' in resultado.columns

# ==============================================================================
# 3. Testes para quantidade_para_comprar
# ==============================================================================

def test_calculo_quantidade_compra_caixas_e_valor():
    """
    Testa a lógica de:
    1. Filtrar necessidade.
    2. Converter falta de unidades para caixas (arredondamento pra cima).
    3. Calcular valor total monetário.
    """
    # ARRANGE
    df_entrada = pd.DataFrame({
        "CODORIGINAL": ["PROD_A", "PROD_B"],
        "GRUPO": ["TESTE", "TESTE"],
        
        # PROD_A: Tem 2 caixas de 10 un (Total 20 un). 
        # Vende 20/mês. Em 3 meses precisa de 60 un.
        # Faltam 40 unidades.
        # Como a caixa tem 10, precisa comprar 4 CAIXAS.
        # Preço da caixa: R$ 50,00 -> Total: 4 * 50 = R$ 200,00
        
        # PROD_B: Estoque gigante, não precisa comprar.
        "Estoque": [2, 100],        
        "Qtd Caixa": [10, 10],      
        "Preço Aquisição": [50.0, 50.0],
        "MEDIA_MENSAL": [20, 10],   
        "10/2025": [0, 0]
    })
    periodo = 3 
    
    # ACT
    resultado = quantidade_para_comprar(df_entrada, periodo=periodo)

    # ASSERT
    # 1. Filtro (Prod B sai)
    assert len(resultado) == 1
    row = resultado.iloc[0]
    assert row["CODORIGINAL"] == "PROD_A"

    # 2. Valida conta de unidades
    # Estoque Total: 2 * 10 = 20
    # Necessidade: 20 * 3 = 60
    # Saldo: 20 - 60 = -40
    assert row["SALDO_ESTOQUE_UNIDADES"] == -40

    # 3. Valida conversão para CAIXAS
    # Faltam 40 un / 10 por caixa = 4 caixas
    assert row["SUGESTAO_QTD_CAIXAS"] == 4

    # 4. Valida Valor Financeiro
    # 4 caixas * 50 reais = 200 reais
    assert row["VALOR_TOTAL_COMPRA"] == 200.0