import os
import pandas as pd
import unicodedata
import re

#caminho do arquivo excel
# Caminho da pasta /Projeto/REQ.../app/models/carregar_dados.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Sobe 2 níveis: models -> app -> REQ-... -> Projeto/
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR)))

# endereço planilha excel 
file = os.path.join(PROJECT_ROOT, "data", "planilha_de_dados.xlsx")

#Usada em RF07
#funcao para carregar dados das linhas com filtro de colunas
def carregar_dados_por_colunas( sheet_name: str, columns):

    try:
        df = pd.read_excel(file, sheet_name=sheet_name, usecols=columns)
        return df
    
    except KeyError as e:
        print(f"Error: One or more columns not found in the sheet. {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()
    
# Função auxiliar para normalizar nomes de colunas (Reaproveitada de consulta_por_linha.py)
def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s))
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w]+", " ", s).lower().strip()
    return s.replace(" ", "")

def obter_dados_cascata():
    """
    Retorna:
    1. Lista de todas as Linhas (para o filtro inicial)
    2. Lista de todas as Sub Linhas (caso nenhuma linha seja selecionada)
    3. Um Dicionário mapeando Linha -> [Lista de Sub Linhas permitidas]
    """
    xls = pd.ExcelFile(file)
    
    todas_linhas = set()
    todas_sublinhas = set()
    mapa_relacao = {} # Ex: {'Linha A': {'Sub 1', 'Sub 2'}, 'Linha B': {'Sub 3'}}

    ALIASES_LINHA = {_norm(x) for x in ["Grupo", "Linha", "Categoria"]}
    ALIASES_SUB_LINHA = {_norm(x) for x in ["Sub Grupo", "Sub Linha", "Sub Grupo Nível 1"]}

    for sheet in xls.sheet_names:
        try:
            # Leitura otimizada do cabeçalho
            df_head = pd.read_excel(file, sheet_name=sheet, nrows=0)
            cols_norm = { _norm(c): c for c in df_head.columns }
            
            col_linha = next((cols_norm[k] for k in cols_norm if k in ALIASES_LINHA), None)
            col_sub = next((cols_norm[k] for k in cols_norm if k in ALIASES_SUB_LINHA), None)

            if col_linha:
                cols_to_load = [col_linha]
                if col_sub:
                    cols_to_load.append(col_sub)
                
                # Carrega os dados garantindo que sejam strings
                df = pd.read_excel(file, sheet_name=sheet, usecols=cols_to_load, dtype=str)
                
                # Normaliza e limpa a coluna de Linha
                df = df.dropna(subset=[col_linha])
                df[col_linha] = df[col_linha].str.strip()
                
                # Adiciona ao conjunto geral de linhas
                todas_linhas.update(df[col_linha].unique())

                if col_sub:
                    # Limpa a coluna de Sub Linha
                    df[col_sub] = df[col_sub].str.strip()
                    
                    # Adiciona ao conjunto geral de sublinhas (ignorando vazios/NaN)
                    subs_validas = df[col_sub].dropna().unique()
                    todas_sublinhas.update(subs_validas)

                    # CONSTRUÇÃO DO MAPA (RELACIONAMENTO)
                    # Agrupa por linha e pega as sublinhas únicas daquela linha
                    for linha, grupo in df.groupby(col_linha):
                        sublinhas_do_grupo = set(grupo[col_sub].dropna().unique())
                        
                        # Se a linha já existe no mapa, unimos os novos dados (caso haja múltiplas abas)
                        if linha not in mapa_relacao:
                            mapa_relacao[linha] = sublinhas_do_grupo
                        else:
                            mapa_relacao[linha].update(sublinhas_do_grupo)

        except Exception as e:
            print(f"Erro ao processar aba {sheet}: {e}")
            continue

    # Converte os sets para listas ordenadas para o Frontend
    lista_linhas = sorted([l for l in todas_linhas if l]) # Remove strings vazias se houver
    lista_sublinhas = sorted([s for s in todas_sublinhas if s])
    
    # Converte os sets do mapa para listas ordenadas também
    mapa_final = {k: sorted(list(v)) for k, v in mapa_relacao.items()}

    return lista_linhas, lista_sublinhas, mapa_final
