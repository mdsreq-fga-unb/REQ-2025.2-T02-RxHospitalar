import os
import pandas as pd
from pathlib import Path

#caminho do arquivo excel
# Caminho da pasta /Projeto/REQ.../app/models/carregar_dados.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Sobe 2 níveis: models -> app -> REQ-... -> Projeto/
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR)))

# endereço planilha excel 
file = os.path.join(PROJECT_ROOT, "data", "planilha_de_dados.xlsx")

#Usada em RF07
#funcao para carregar dados das linhas com filtro de colunas
def carregar_dados_por_colunas(sheet_name: str, columns, linha=None, coluna=None):
    """
    Carrega colunas específicas de uma planilha e,
    opcionalmente, filtra pela igualdade entre coluna == linha.
    """
    try:
        # Carrega apenas as colunas pedidas
        df = pd.read_excel(file, sheet_name=sheet_name, usecols=columns)

        # Se coluna e linha foram fornecidos, aplica filtro
        if linha is not None and coluna is not None:

            # Segurança: garantir que coluna existe
            if coluna not in df.columns:
                raise KeyError(f"A coluna '{coluna}' não existe na planilha.")

            # Filtrar apenas onde coluna == linha
            df = df[df[coluna] == linha]

        return df

    except KeyError as e:
        print(f"[ERRO] Coluna não encontrada: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"[ERRO] Ocorreu um problema ao carregar a planilha: {e}")
        return pd.DataFrame()



#exemplo de uso

#sheet_test = "Vendas_Pendencia"
#cols_test = ["OPERADOR", "CODPRODUTO", "NOTAFISCAL"]

#df_test = carregar_dados_por_colunas(sheet_test, cols_test)


#funcao para encontrar a pasta de dados no Projeto
def find_data_dir(max_levels=6) -> Path:
    """
    Sobe a hierarquia a partir do arquivo atual e procura pela pasta 'data'.
    Retorna o Path da pasta 'data' quando encontrada ou None se não achar.
    max_levels limita quantos níveis subir (evita loop infinito).
    """
    current = Path(__file__).resolve()
    for i, parent in enumerate(current.parents):
        if i >= max_levels:
            break
        candidate = parent / "data"
        if candidate.exists() and candidate.is_dir():
            return candidate
    return None


def salvar_tabela_txt(tabela, nome_arquivo="resultado.txt", out_dir: str = None):
    """
    Salva um DataFrame em um arquivo .txt dentro da pasta 'data' do projeto.
    - tabela: pandas.DataFrame
    - nome_arquivo: nome do arquivo (ex: 'resultado.txt' ou 'saida/tabela.txt')
    - out_dir: opcional, caminho absoluto ou relativo para sobrescrever a pasta destino
    """
    # Se foi passado um out_dir, usa ele (pode ser relativo ao cwd)
    if out_dir:
        destino_dir = Path(out_dir).expanduser().resolve()
    else:
        # tenta localizar a pasta data subindo a hierarquia
        destino_dir = find_data_dir()
        if destino_dir is None:
            # fallback: assume que o projeto está 3 níveis acima (ajuste se necessário)
            destino_dir = Path(__file__).resolve().parents[3] / "data"

    # Se o nome_arquivo contém subpastas, respeita-as
    destino_path = destino_dir / nome_arquivo

    # Garante que a pasta destino existe
    destino_path.parent.mkdir(parents=True, exist_ok=True)

    # Salva em formato tabulado (ou troque por outro formato)
    try:
        tabela.to_csv(destino_path, sep="\t", index=False, encoding="utf-8")
        print(f"[OK] Arquivo salvo em: {destino_path}")
    except Exception as e:
        print(f"[ERRO] Não foi possível salvar o arquivo: {e}")