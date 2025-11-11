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

CODE_ALIASES = {"CODORIGINAL", "Cód Original", "Código Original"}
DESC_ALIASES = {"descricao", "descr", "Descricao", "nome"}

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
        norm_aliases = {_norm(a) for a in CODE_ALIASES}
        
        # escolhe a coluna por alias normalizado
        code_col = next((orig for norm, orig in norm_map.items() if norm in norm_aliases), None)
        if not code_col:
            # tenta especificamente 'codoriginal'
            code_col = norm_map.get("codoriginal")
        if not code_col:
            # último fallback: qualquer coluna começando com 'cod'
            code_col = next((orig for norm, orig in norm_map.items() if norm.startswith("cod")), None)
        if not code_col:
            continue

        desc_col = next((orig for norm, orig in norm_map.items() if norm in {_norm(a) for a in DESC_ALIASES}), None)

        series = df[code_col].astype(str).str.strip()
        mask = series == alvo
        if mask.any():
            row = df.loc[mask].iloc[0]
            # mantém o nome real da coluna encontrada (bate com os testes)
            result = {code_col: str(row[code_col]).strip()}
            if desc_col and desc_col in row:
                result["Descrição"] = row[desc_col]
            return pd.Series(result)

    raise ValueError("O código não foi encontrado")