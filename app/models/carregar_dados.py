import os
import pandas as pd
import unicodedata
import re
from app.utils.path import get_resource_path

#caminho do arquivo excel

# refatorado para  o executavel

# --- BLOCO DE DIAGNÓSTICO (Copie isto) ---
print("="*50)
print("DIAGNÓSTICO DE CAMINHOS:")
raiz = get_resource_path(".")
print(f"1. Raiz do App: {raiz}")

file = get_resource_path(os.path.join("data", "planilha_de_dados.xlsx"))
print(f"2. Onde o código procura a planilha: {file}")

existe = os.path.exists(file)
print(f"3. O arquivo existe lá? {'SIM' if existe else 'NÃO'}")

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
    Retorna (APENAS DA ABA ESTOQUE):
    1. Lista de todas as Linhas (para o filtro inicial)
    2. Lista de todas as Sub Linhas (caso nenhuma linha seja selecionada)
    3. Um Dicionário mapeando Linha -> [Lista de Sub Linhas permitidas]
    """
    
    # 1. Tenta abrir o arquivo Excel
    try:
        xls = pd.ExcelFile(file)
    except Exception as e:
        print(f"Erro ao abrir arquivo Excel: {e}")
        return [], [], {}

    todas_linhas = set()
    todas_sublinhas = set()
    mapa_relacao = {} 

    ALIASES_LINHA = {_norm(x) for x in ["Grupo", "Linha", "Categoria"]}
    ALIASES_SUB_LINHA = {_norm(x) for x in ["Sub Grupo", "Sub Linha", "Sub Grupo Nível 1"]}
    
    # NOME DA ABA QUE QUEREMOS FIXAR
    TARGET_SHEET = "Estoque"

    # Verifica se a aba existe antes de tentar ler
    if TARGET_SHEET not in xls.sheet_names:
        print(f"Aviso: Aba '{TARGET_SHEET}' não encontrada no arquivo. Filtros vazios.")
        return [], [], {}

    try:
        # Leitura otimizada do cabeçalho apenas da aba Estoque
        df_head = pd.read_excel(file, sheet_name=TARGET_SHEET, nrows=0)
        cols_norm = { _norm(c): c for c in df_head.columns }
        
        # Identifica as colunas dinamicamente
        col_linha = next((cols_norm[k] for k in cols_norm if k in ALIASES_LINHA), None)
        col_sub = next((cols_norm[k] for k in cols_norm if k in ALIASES_SUB_LINHA), None)

        if col_linha:
            cols_to_load = [col_linha]
            if col_sub:
                cols_to_load.append(col_sub)
            
            # Carrega os dados da aba Estoque
            df = pd.read_excel(file, sheet_name=TARGET_SHEET, usecols=cols_to_load, dtype=str)
            
            # Normaliza e limpa a coluna de Linha
            df = df.dropna(subset=[col_linha])
            df[col_linha] = df[col_linha].str.strip()
            
            # Adiciona ao conjunto geral de linhas
            todas_linhas.update(df[col_linha].unique())

            if col_sub:
                # Limpa a coluna de Sub Linha
                df[col_sub] = df[col_sub].str.strip()
                
                # Adiciona ao conjunto geral de sublinhas
                subs_validas = df[col_sub].dropna().unique()
                todas_sublinhas.update(subs_validas)

                # CONSTRUÇÃO DO MAPA (RELACIONAMENTO)
                for linha, grupo in df.groupby(col_linha):
                    sublinhas_do_grupo = set(grupo[col_sub].dropna().unique())
                    
                    if linha not in mapa_relacao:
                        mapa_relacao[linha] = sublinhas_do_grupo
                    else:
                        mapa_relacao[linha].update(sublinhas_do_grupo)

    except Exception as e:
        print(f"Erro ao processar aba {TARGET_SHEET}: {e}")

    # Converte os sets para listas ordenadas para o Frontend
    lista_linhas = sorted([l for l in todas_linhas if l]) 
    lista_sublinhas = sorted([s for s in todas_sublinhas if s])
    
    # Converte os sets do mapa para listas ordenadas também
    mapa_final = {k: sorted(list(v)) for k, v in mapa_relacao.items()}

    return lista_linhas, lista_sublinhas, mapa_final

# ... (mantenha os imports e variáveis anteriores)

def carregar_dados_unificados():
    """
    Lê a aba 'Vendas_Pendencia' e a aba 'Estoque'.
    Cruza as informações usando o Código do Produto para preencher 
    as colunas de Descrição, Grupo, etc. na tabela de vendas.
    """
    try:
        # 1. Carregar as duas abas
        df_vendas = pd.read_excel(file, sheet_name="Vendas_Pendencia")
        df_estoque = pd.read_excel(file, sheet_name="Estoque")

        # 2. Limpeza básica para garantir que o cruzamento funcione
        # Removemos espaços em branco dos nomes das colunas
        df_vendas.columns = [str(c).strip() for c in df_vendas.columns]
        df_estoque.columns = [str(c).strip() for c in df_estoque.columns]

        # 3. Identificar as colunas chaves (Baseado nas suas imagens)
        # Na aba Vendas, o código parece ser 'CODVEN' ou 'Cód Prod'
        # Na aba Estoque, o código é 'Cód Produto'
        
        col_chave_vendas = "CODVEN" # Verifique se na sua planilha Vendas é este o nome exato
        col_chave_estoque = "Cód Produto" # Nome na aba Estoque

        # Verifica se as colunas existem antes de tentar cruzar
        if col_chave_vendas not in df_vendas.columns:
            # Tenta achar um nome parecido se CODVEN não existir
            possiveis = [c for c in df_vendas.columns if "COD" in c.upper() or "PROD" in c.upper()]
            if possiveis:
                col_chave_vendas = possiveis[0]
            else:
                print(f"Aviso: Coluna chave não encontrada em Vendas. Colunas: {df_vendas.columns}")
                return df_vendas # Retorna só vendas se não der pra cruzar

        if col_chave_estoque not in df_estoque.columns:
             print(f"Aviso: Coluna '{col_chave_estoque}' não encontrada em Estoque.")
             return df_vendas

        # 4. Converter códigos para texto (para evitar erro de número vs texto)
        df_vendas[col_chave_vendas] = df_vendas[col_chave_vendas].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
        df_estoque[col_chave_estoque] = df_estoque[col_chave_estoque].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)

        # 5. Selecionar colunas do estoque que queremos trazer para preencher os vazios
        # Ajuste esta lista conforme o que você quer ver
        cols_estoque_desejadas = [col_chave_estoque, 'Descrição', 'Grupo', 'Sub Grupo Nível 1', 'Estoque', 'Preço Aquisição']
        
        # Filtra o dataframe de estoque para ter apenas o necessário (evita duplicidade desnecessária)
        # Usamos intersection para pegar apenas colunas que realmente existem no arquivo
        cols_existentes = [c for c in cols_estoque_desejadas if c in df_estoque.columns]
        df_estoque_limpo = df_estoque[cols_existentes]

        # 6. O MERGE (O "PROCV" do Python)
        # how='left' significa: Mantém todas as linhas de Vendas e traz info do Estoque onde der match
        df_final = pd.merge(
            df_vendas, 
            df_estoque_limpo, 
            left_on=col_chave_vendas, 
            right_on=col_chave_estoque, 
            how="left",
            suffixes=('_vendas', '') # Se houver colunas repetidas, a do estoque mantém o nome original
        )

        # Opcional: Se a aba vendas tinha uma coluna "Descrição" vazia, ela agora virou "Descrição_vendas".
        # A coluna preenchida vinda do estoque se chama "Descrição".
        
        df_final = df_final.fillna("")
        return df_final

    except Exception as e:
        print(f"Erro ao unificar dados: {e}")
        # Retorna um dataframe vazio ou o básico em caso de erro crítico
        return pd.DataFrame()
