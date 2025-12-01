import pandas as pd
from app.models.carregar_dados import carregar_dados_por_colunas, salvar_tabela_txt
from app.utils.separar_por_data import separar_quantidade_por_data
from app.utils.dataframe_utils import juntar_por_codigo, quantidade_para_comprar


# Função usada no RF07
# Sugere quantidade de compra com base na média dos últimos “periodo” meses
def sugestao_compra(linha: str, periodo):
    """
    Executa o fluxo principal:
    1. Carrega vendas filtradas pelo grupo (linha).
    2. Processa vendas por mês e calcula média.
    3. Carrega estoque.
    4. Junta vendas + estoque por código.
    5. Calcula quantidade sugerida para compra.
    """

    # ============================
    # 1. Carregar vendas pendentes
    # ============================
    sheet = "Vendas_Pendencia"
    cols = ["GRUPO", "CODORIGINAL", "DATASTATUS", "QUANTIDADE", "INDICADOR"]
    linha_aux = linha
    coluna = "GRUPO"

    # Carrega somente as linhas da GRUPO selecionado
    df_vendas = carregar_dados_por_colunas(sheet, cols, linha=linha_aux, coluna=coluna)
    #print("== VENDAS CARREGADAS ==")
    #print(df_vendas.head())

    # ====================================
    # 2. Processa datas e gera colunas por mês
    # ====================================
    df_vendas = separar_quantidade_por_data(df_vendas, periodo)
    #print("\n== VENDAS AGRUPADAS POR MÊS ==")
    #print(df_vendas.head())

    # ======================
    # 3. Carregar estoque
    # ======================
    df_estoque = carregar_dados_por_colunas(
        sheet_name="Estoque",
        columns=["Grupo", "Cód Original", "Qtd Caixa", "Estoque", "Preço Aquisição"],
        linha=linha_aux,
        coluna="Grupo"
    )

    # ======================
    # 4. Juntar vendas + estoque por código
    # ======================
    df_compras = juntar_por_codigo(df_vendas, df_estoque)

    # ======================
    # 5. Calcular sugestão de compra
    # ======================
    df_compras = quantidade_para_comprar(df_compras, periodo)

    return df_compras



# ======================
# TESTE LOCAL
# ======================
if __name__ == "__main__":
    linha_teste = "BBRAUN"
    periodo_teste = 5

    print(sugestao_compra(linha_teste, periodo_teste))