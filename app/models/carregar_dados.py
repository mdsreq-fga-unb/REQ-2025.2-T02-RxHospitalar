import os
import pandas as pd
from pathlib import Path
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
    """Normaliza strings para comparação (remove acentos, espaços e lower case)."""
    if not isinstance(s, str): s = str(s)
    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w]+", " ", s).lower().strip()
    return s.replace(" ", "")

def _encontrar_coluna_cod_original(colunas_existentes):
    """Procura especificamente por colunas de Código ORIGINAL."""
    norm_map = { _norm(c): c for c in colunas_existentes }
    aliases = ["CODORIGINAL", "Cód Original", "Código Original", "Ref Original", "Referência Original"]
    for alias in aliases:
        if _norm(alias) in norm_map:
            return norm_map[_norm(alias)]
    return None

def _encontrar_coluna_cod_interno(colunas_existentes):
    """Procura especificamente por colunas de Código INTERNO (para cruzamento)."""
    norm_map = { _norm(c): c for c in colunas_existentes }
    # Evita aliases que pareçam com 'Original'
    aliases = ["Cód Produto", "Codigo", "Cod", "Referencia", "CODVEN", "Produto"]
    
    # 1. Tenta match exato nos aliases comuns
    for alias in aliases:
        if _norm(alias) in norm_map:
            return norm_map[_norm(alias)]
            
    # 2. Fallback: Procura algo que comece com 'cod' e NÃO tenha 'original'
    for norm_name, real_name in norm_map.items():
        if norm_name.startswith("cod") and "original" not in norm_name:
            return real_name
    return None

def _encontrar_melhor_coluna_filtro(colunas_existentes):
    """
    Decide qual coluna usar para o FILTRO DO USUÁRIO.
    Prioridade: Original -> Interno.
    """
    col_orig = _encontrar_coluna_cod_original(colunas_existentes)
    if col_orig: return col_orig
    return _encontrar_coluna_cod_interno(colunas_existentes)

# --- FUNÇÕES PRINCIPAIS ---

def carregar_dados_por_colunas(sheet_name: str, columns, linha=None, coluna=None):
    try:
        df = pd.read_excel(file, sheet_name=sheet_name, usecols=columns)
        if linha is not None and coluna is not None:
            if coluna not in df.columns:
                return pd.DataFrame() # Falha silenciosa segura
            df = df[df[coluna] == linha]
        return df
    except Exception as e:
        print(f"[ERRO] carregar_dados_por_colunas: {e}")
        return pd.DataFrame()

def obter_dados_cascata():
    """
    Gera as listas para os filtros (Linha, Sublinha, Códigos).
    Usa a coluna 'Original' se existir, para que o filtro mostre os códigos que o usuário conhece.
    """
    try:
        xls = pd.ExcelFile(file)
    except Exception:
        return [], [], {}, []

    todas_linhas = set()
    todas_sublinhas = set()
    todos_codigos = set()
    mapa_relacao = {} 

    ALIASES_LINHA = {_norm(x) for x in ["Grupo", "Linha", "Categoria"]}
    ALIASES_SUB_LINHA = {_norm(x) for x in ["Sub Grupo", "Sub Linha", "Sub Grupo Nível 1"]}
    
    TARGET_SHEET = "Estoque"

    if TARGET_SHEET not in xls.sheet_names:
        return [], [], {}, []

    try:
        df_head = pd.read_excel(file, sheet_name=TARGET_SHEET, nrows=0)
        cols_norm = { _norm(c): c for c in df_head.columns }
        
        col_linha = next((cols_norm[k] for k in cols_norm if k in ALIASES_LINHA), None)
        col_sub = next((cols_norm[k] for k in cols_norm if k in ALIASES_SUB_LINHA), None)
        
        # AQUI: Usa a lógica de prioridade (Original > Interno) para o FILTRO
        col_cod = _encontrar_melhor_coluna_filtro(df_head.columns)

        if col_linha:
            cols_to_load = [col_linha]
            if col_sub: cols_to_load.append(col_sub)
            if col_cod: cols_to_load.append(col_cod)
            
            df = pd.read_excel(file, sheet_name=TARGET_SHEET, usecols=cols_to_load, dtype=str)
            
            df = df.dropna(subset=[col_linha])
            df[col_linha] = df[col_linha].str.strip()
            todas_linhas.update(df[col_linha].unique())

            if col_sub:
                df[col_sub] = df[col_sub].str.strip()
                subs_validas = df[col_sub].dropna().unique()
                todas_sublinhas.update(subs_validas)
                for linha, grupo in df.groupby(col_linha):
                    sublinhas_do_grupo = set(grupo[col_sub].dropna().unique())
                    if linha not in mapa_relacao: mapa_relacao[linha] = sublinhas_do_grupo
                    else: mapa_relacao[linha].update(sublinhas_do_grupo)
            
            if col_cod:
                codigos_limpos = df[col_cod].dropna().astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
                todos_codigos.update(codigos_limpos.unique())

    except Exception as e:
        print(f"Erro cascata: {e}")

    return sorted(list(todas_linhas)), sorted(list(todas_sublinhas)), {k: sorted(list(v)) for k,v in mapa_relacao.items()}, sorted(list(todos_codigos))


def carregar_dados_unificados():
    """
    Cruza Vendas e Estoque.
    CORREÇÃO: 
    1. Usa CÓDIGO INTERNO para fazer o MERGE (garantir que os dados batam).
    2. Traz o CÓDIGO ORIGINAL (se existir) para que o filtro funcione na tela.
    """
    try:
        df_vendas = pd.read_excel(file, sheet_name="Vendas_Pendencia")
        df_estoque = pd.read_excel(file, sheet_name="Estoque")

        # Limpeza nomes colunas
        df_vendas.columns = [str(c).strip() for c in df_vendas.columns]
        df_estoque.columns = [str(c).strip() for c in df_estoque.columns]

        # 1. IDENTIFICAR CHAVES DE MERGE (CÓDIGO INTERNO)
        col_join_estoque = _encontrar_coluna_cod_interno(df_estoque.columns)
        
        col_join_vendas = "CODVEN"
        if col_join_vendas not in df_vendas.columns:
            col_join_vendas = _encontrar_coluna_cod_interno(df_vendas.columns)

        # Se não achou chave interna no estoque, tenta qualquer código como fallback
        if not col_join_estoque:
             col_join_estoque = _encontrar_melhor_coluna_filtro(df_estoque.columns)

        if not col_join_estoque or not col_join_vendas:
             print(f"Aviso: Chaves de merge não encontradas. Vendas:{col_join_vendas} Estoque:{col_join_estoque}")
             return df_vendas

        # 2. IDENTIFICAR COLUNA DE EXIBIÇÃO (ORIGINAL)
        # Queremos ter certeza que essa coluna estará no DataFrame final para o filtro funcionar
        col_display_estoque = _encontrar_coluna_cod_original(df_estoque.columns)

        # Padronizar chaves para string
        df_vendas[col_join_vendas] = df_vendas[col_join_vendas].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
        df_estoque[col_join_estoque] = df_estoque[col_join_estoque].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)

        # 3. SELECIONAR COLUNAS
        cols_base = ['Descrição', 'Grupo', 'Sub Grupo Nível 1', 'Estoque', 'Preço Aquisição']
        cols_estoque_desejadas = [col_join_estoque] + cols_base
        
        # Importante: Se existe coluna de código original, adiciona ela para ser carregada!
        if col_display_estoque and col_display_estoque not in cols_estoque_desejadas:
            cols_estoque_desejadas.append(col_display_estoque)

        # Filtra apenas colunas que realmente existem
        cols_existentes = [c for c in cols_estoque_desejadas if c in df_estoque.columns]
        df_estoque_limpo = df_estoque[cols_existentes]

        # 4. MERGE (USANDO CHAVES INTERNAS)
        df_final = pd.merge(
            df_vendas, 
            df_estoque_limpo, 
            left_on=col_join_vendas, 
            right_on=col_join_estoque, 
            how="left",
            suffixes=('_vendas', '')
        )
        
        df_final = df_final.fillna("")
        return df_final

    except Exception as e:
        print(f"Erro ao unificar dados: {e}")
        return pd.DataFrame()


def find_data_dir(max_levels=6) -> Path:
    current = Path(__file__).resolve()
    for i, parent in enumerate(current.parents):
        if i >= max_levels: break
        candidate = parent / "data"
        if candidate.exists() and candidate.is_dir(): return candidate
    return None

def salvar_tabela_txt(tabela, nome_arquivo="resultado.txt", out_dir: str = None):
    if out_dir: destino_dir = Path(out_dir).expanduser().resolve()
    else:
        destino_dir = find_data_dir()
        if destino_dir is None: destino_dir = Path(__file__).resolve().parents[3] / "data"
    destino_path = destino_dir / nome_arquivo
    destino_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        tabela.to_csv(destino_path, sep="\t", index=False, encoding="utf-8")
        print(f"[OK] Salvo em: {destino_path}")
    except Exception as e:
        print(f"[ERRO] Salvar TXT: {e}")