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

#tal qual consta na RNF03, a importação do arquivo só funcionará com .xlsx ou .csv
SUPPORTED_EXT = {".xlsx", ".csv"}

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

def importar_arquivo(caminho: str, required_sheets: dict[str, list[str]] | None = None, check_integrity: bool = False) -> dict:
    """
    Importa .xlsx ou .csv validando:
      - extensão suportada (.xlsx ou .csv)
      - presença de abas (XLSX) e colunas obrigatórias
      - integridade (opcional): compara contagem de linhas e soma de colunas numéricas definidas no template
    Parâmetros:
      caminho: str -> caminho do arquivo
      required_sheets: dict -> {"Estoque": ["Cód Original","Estoque"], "__csv__": ["Cód Original", ...]}
      check_integrity: bool -> se True, adiciona 'integrity' com métricas
    Retorno:
      {
        ok: bool,
        erro: str | None,
        data: {nome_aba: DataFrame},
        integrity: {aba: {"rows": int, "sums": {col: valor}}} (se check_integrity=True)
      }
    """
    p = Path(caminho).expanduser().resolve()
    if not p.exists():
        return {"ok": False, "erro": f"Importação: arquivo não encontrado: {p}", "data": {}}
    ext = p.suffix.lower()
    if ext not in SUPPORTED_EXT:
        return {"ok": False, "erro": f"Importação: formato inválido '{ext}'. Aceitos: {', '.join(SUPPORTED_EXT)}", "data": {}}
    integrity = {}
    try:
        if ext == ".csv":
            df = pd.read_csv(p)
            if required_sheets and "__csv__" in required_sheets:
                faltando = [c for c in required_sheets["__csv__"] if c not in df.columns]
                if faltando:
                    return {"ok": False, "erro": f"Importação: colunas faltando no CSV: {faltando}", "data": {}}
            if check_integrity and "__csv__" in (required_sheets or {}):
                sums = {}
                for col in required_sheets["__csv__"]:
                    if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                        sums[col] = pd.to_numeric(df[col], errors="coerce").sum()
                integrity["__csv__"] = {"rows": len(df), "sums": sums}
            return {"ok": True, "erro": None, "data": {"__csv__": df}, "integrity": integrity if check_integrity else None}

        xls = pd.ExcelFile(p)
        data = {}
        if required_sheets:
            faltam_abas = [s for s in required_sheets if s not in xls.sheet_names and s != "__csv__"]
            if faltam_abas:
                return {"ok": False, "erro": f"Importação: abas faltando: {faltam_abas}", "data": {}}

        for sheet in xls.sheet_names:
            df_sheet = pd.read_excel(p, sheet_name=sheet, dtype=str)
            if required_sheets and sheet in required_sheets:
                faltando_cols = [c for c in required_sheets[sheet] if c not in df_sheet.columns]
                if faltando_cols:
                    return {"ok": False, "erro": f"Importação: aba '{sheet}' com colunas faltando: {faltando_cols}", "data": {}}
            data[sheet] = df_sheet

            if check_integrity and required_sheets and sheet in required_sheets:
                sums = {}
                for col in required_sheets[sheet]:
                    if col in df_sheet.columns:
                        # converte para numérico se possível e soma; se não for numérico, ignora (NaN vira 0)
                        serie_num = pd.to_numeric(df_sheet[col], errors="coerce")
                        if serie_num.notna().any():
                            sums[col] = float(serie_num.sum())
                integrity[sheet] = {"rows": int(len(df_sheet)), "sums": sums}

        return {"ok": True, "erro": None, "data": data, "integrity": integrity if check_integrity else None}
    except Exception as e:
        return {"ok": False, "erro": f"Importação: falha ao importar: {e}", "data": {}}

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