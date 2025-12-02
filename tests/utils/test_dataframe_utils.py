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
def test_calculo_quantidade_compra_simples():
    """Testa a lógica matemática de sugestão de compra."""
    # Arrange
    # Prod A: Estoque 10, Vende 10/mês. Em 3 meses precisa de 30. Faltam 20.
    # Prod B: Estoque 100, Vende 10/mês. Em 3 meses precisa de 30. Sobram 70.
    df_entrada = pd.DataFrame({
        "CODORIGINAL": ["PROD_A", "PROD_B"],
        "GRUPO": ["TESTE", "TESTE"],
        "Estoque": [10, 100],
        "Qtd Caixa": [1, 1],
        "MEDIA_MENSAL": [10, 10],
        "10/2025": [0, 0] # Coluna dummy
    })
    periodo = 3 
    
    # Act
    resultado = quantidade_para_comprar(df_entrada, periodo=periodo)

    # Assert
    # 1. Verifica se filtrou quem não precisa comprar (Prod B sai)
    assert len(resultado) == 1
    
    # 2. Verifica se quem ficou foi o Prod A
    row = resultado.iloc[0]
    assert row["CODORIGINAL"] == "PROD_A"

    # 3. Valida a conta: (10 * 3) - 10 = 20
    assert row["SUGESTAO_COMPRA"] == 20