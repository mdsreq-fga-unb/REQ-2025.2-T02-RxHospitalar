# RF03 - Consultar Produto por código original do produto
import re
import unicodedata
import pandas as pd
from app.models.data_loader import file

def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s))
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w]+", " ", s).lower().strip()
    return s.replace(" ", "")

CODE_ALIASES = {"codoriginal", "codproduto", "cod", "codigo"}
DESC_ALIASES = {"descricao", "descr", "produto", "nome"}

def consulta_por_codigo(codigo_produto: str):
    if not codigo_produto or str(codigo_produto).strip() == "":
        raise ValueError("O código não foi encontrado")

    alvo = str(codigo_produto).strip()
    xls = pd.ExcelFile(file)

    for sheet in xls.sheet_names:
        try:
            df = pd.read_excel(file, sheet_name=sheet, header=0, dtype=str)
        except Exception:
            continue
        if df.empty:
            continue

        norm_map = { _norm(c): c for c in df.columns }
        # tenta achar coluna de código por alias
        code_col = next((norm_map[n] for n in CODE_ALIASES if n in norm_map), None)
        if not code_col:
            # fallback: qualquer coluna que comece com "cod"
            code_col = next((orig for n, orig in norm_map.items() if n.startswith("cod")), None)
        if not code_col:
            continue

        desc_col = next((norm_map[n] for n in DESC_ALIASES if n in norm_map), None)

        series = df[code_col].astype(str).str.strip()
        mask = series == alvo
        if mask.any():
            row = df.loc[mask].iloc[0]
            result = {"Cód. Original": str(row[code_col]).strip()}
            if desc_col and desc_col in row:
                result["Descrição"] = row[desc_col]
            return pd.Series(result)

    raise ValueError("O código não foi encontrado")