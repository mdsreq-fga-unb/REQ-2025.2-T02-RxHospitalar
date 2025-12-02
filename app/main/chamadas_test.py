import pandas as pd
import os
from pathlib import Path
from app.models.carregar_dados import carregar_dados_por_colunas
from app.utils.separar_por_data import separar_quantidade_por_data
from app.utils.dataframe_utils import filtrar_por_codigo
from app.utils.salva_output import salvar_tabela_txt


if __name__ == "__main__":

    sheet_test = "Vendas_Pendencia"
    cols_test = ["INDICADOR", "CODORIGINAL", "DATASTATUS", "QUANTIDADE", "INDICADOR_3"]

    df_test = carregar_dados_por_colunas(sheet_test, cols_test)


    #df_test = filtrar_por_codigo(df_test, "INDICADOR", "ALESSANDRA")
    #print(df_test.head())

    sheet_test2 = "Estoque"
    cols_test2 = ["Grupo", "Cód Original", "Estoque", "Preço Aquisição"]
    df_test2 = carregar_dados_por_colunas(sheet_test2, cols_test2)

    df_test2 = filtrar_por_codigo(df_test2, "Grupo", "BBRAUN")
    

    print(separar_quantidade_por_data(df_test, 4)) #dataframe de venda/pendencias separado por mes
