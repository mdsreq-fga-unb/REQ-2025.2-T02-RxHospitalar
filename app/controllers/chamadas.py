import pandas as pd
from app.models.carregar_dados import carregar_dados_por_colunas
from app.utils.separar_por_data import separar_quantidade_por_data


#funcao incompleta
#Usada em RF07
# Função para sugerir quantidade de compra com base na média de vendas dos últimos 'periodo' meses
def sugestao_compra(linha: str, periodo):
    """
    Funcao que sugere a quantidade de compra com base na media de vendas dos ultimos 'period' meses.
    """
    sheet = "Vendas_Pendencia"
    cols = ["INDICADOR", "CODORIGINAL", "DATASTATUS", "QUANTIDADE", "INDICADOR_3"]

    df_aux = carregar_dados_por_colunas(sheet, cols)
    periodo_aux = periodo
    df_aux = separar_quantidade_por_data(df_aux, periodo_aux)

    return df_aux


# Exemplo de uso parar teste 
if __name__ == "__main__":
    linha_teste = "BBRAUN"
    periodo_teste = 4

    
    print(sugestao_compra(linha_teste, periodo_teste))