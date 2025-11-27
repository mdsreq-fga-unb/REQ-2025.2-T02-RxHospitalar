import pandas as pd
import pytest
from app.utils.dataframe_utils import filtrar_por_codigo 

@pytest.fixture
def sample_dataframe():
    """Cria um DataFrame de exemplo com casos de teste enviesados."""
    data = {
        'ID': [1, 2, 3, 4, 5, 6, 7],
        'CodigoProduto': [
            'ABC-101',
            'abc-101',      # Case-insensitive
            ' ABC-101 ',    # Ignorar espaços em branco
            'abc - 101',    # Caso ruim: espaços internos que DEVEM falhar
            'XYZ-999',
            'aBC-101',
            '  XYZ-999',
        ],
        'Descricao': ['Produto A', 'Produto A', 'Produto A', 'Produto B', 'Produto C', 'Produto A', 'Produto C']
    }
    return pd.DataFrame(data)

def test_filtrar_por_codigo_sucesso(sample_dataframe):
    """
    Testa se a função filtra corretamente, lidando com case-insensitivity e espaços.
    """
    # 1. Caso de Teste Normal e de Borda (Maiúsculas/Minúsculas, Espaços)
    
    # Valor de busca normalizado: 'ABC-101'
    code_value = " aBC-101 " 
    column_name = 'CodigoProduto'
    
    # Executa a função
    result_df = filtrar_por_codigo(sample_dataframe, column_name, code_value)
    
    # Verifica o resultado
    # Esperamos as linhas com ID 1, 2, 3, 6 (que se normalizam para 'ABC-101')
    expected_ids = [1, 2, 3, 6]
    assert len(result_df) == 4, f"Esperava 4 linhas, mas obteve {len(result_df)}"
    assert sorted(result_df['ID'].tolist()) == expected_ids, "Os IDs retornados não são os esperados."
    
    # 2. Caso de Teste para um Código Diferente
    code_value_2 = "xyz-999" 
    result_df_2 = filtrar_por_codigo(sample_dataframe, column_name, code_value_2)
    
    # Esperamos as linhas com ID 5 e 7
    expected_ids_2 = [5, 7]
    assert len(result_df_2) == 2, f"Esperava 2 linhas, mas obteve {len(result_df_2)}"
    assert sorted(result_df_2['ID'].tolist()) == expected_ids_2, "Os IDs retornados para XYZ-999 não são os esperados."
    
    # 3. Caso de Teste Vazio (Nenhum Resultado)
    code_value_3 = "NAO_EXISTE"
    result_df_3 = filtrar_por_codigo(sample_dataframe, column_name, code_value_3)
    
    assert result_df_3.empty, "Esperava um DataFrame vazio, mas obteve resultados."


def test_filtrar_por_codigo_coluna_nao_existe(sample_dataframe, capsys):
    """
    Testa se a função trata corretamente o erro quando a coluna não existe.
    """
    # Caso de Teste de Erro (Coluna Inexistente)
    column_name = 'ColunaInexistente'
    code_value = 'ABC-101'
    
    # Executa a função
    result_df = filtrar_por_codigo(sample_dataframe, column_name, code_value)
    
    # Verifica o resultado
    assert result_df.empty, "Esperava um DataFrame vazio no erro, mas obteve resultados."
    
    # Verifica se a mensagem de erro foi impressa
    captured = capsys.readouterr()
    expected_error_msg = f"Erro ao filtrar DataFrame: A coluna '{column_name}' não existe no DataFrame."
    assert expected_error_msg in captured.out, "A mensagem de erro esperada não foi impressa."


def test_filtrar_por_codigo_coluna_com_na(sample_dataframe):
    """
    Testa se a função lida corretamente com valores NaN/None na coluna, 
    garantindo que sejam tratados como strings.
    """
    df_with_nan = sample_dataframe.copy()
    # Adiciona um NaN (que o .astype(str) deve converter para 'nan')
    df_with_nan.loc[len(df_with_nan)] = {'ID': 8, 'CodigoProduto': float('nan'), 'Descricao': 'Produto D'}
    # Adiciona um 'NaN' literal que deve ser tratado como um valor
    df_with_nan.loc[len(df_with_nan)] = {'ID': 9, 'CodigoProduto': 'NaN', 'Descricao': 'Produto E'}
    
    column_name = 'CodigoProduto'
    
    # 1. Busca por 'nan' (resultado de float('nan').astype(str))
    code_value_nan = " nan " 
    result_df_nan = filtrar_por_codigo(df_with_nan, column_name, code_value_nan)
    # Espera a linha com ID 8
    assert len(result_df_nan) == 1, "Esperava 1 linha para 'nan'."
    assert result_df_nan['ID'].iloc[0] == 8, "O ID para 'nan' não é o esperado."
    
    # 2. Busca por 'NaN' (literal)
    code_value_NaN = "NaN" 
    result_df_NaN = filtrar_por_codigo(df_with_nan, column_name, code_value_NaN)
    # Espera a linha com ID 9
    assert len(result_df_NaN) == 1, "Esperava 1 linha para 'NaN'."
    assert result_df_NaN['ID'].iloc[0] == 9, "O ID para 'NaN' não é o esperado."