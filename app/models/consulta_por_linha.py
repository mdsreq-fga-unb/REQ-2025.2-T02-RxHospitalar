# RF04 - Consultar Produto por linha do produto
import re
import unicodedata
import pandas as pd
from app.models.data_loader import file

#esta função serve para normalizar os nomes de coluna, dado que há inconsistências entre as abas
def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s))
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w]+", " ", s).lower().strip()
    return s.replace(" ", "")

#alguns dos nomes que podem surgir para a linha do produto dentre as colunas da planilha
CODE_ALIASES = {"Grupo", "GRUPO", "Sub Grupo Nível 1", "Sub Grupo Nível 2"}
CANONICAL = {
    _norm("Grupo"): "Grupo",
    _norm("Sub Grupo Nível 1"): "Sub Grupo Nível 1",
    _norm("Sub Grupo Nível 2"): "Sub Grupo Nível 2",
}

#a função core da RF04
def consulta_por_linha(linha_produto: str):
    if not linha_produto or str(linha_produto).strip() == "":
        raise ValueError("A linha não foi encontrada")
    
    #o alvo no caso é a string a ser buscada nas colunas candidatas
    alvo = str(linha_produto).strip()
    xls = pd.ExcelFile(file)

    for sheet in xls.sheet_names:
        try:
            df = pd.read_excel(file, sheet_name=sheet, header=0, dtype=str)
        #há um loop de continuidade porque às vezes a coluna pode estar em outra aba da planilha
        except Exception:
            continue
        if df.empty:
            continue

        #isso normaliza os nomes das colunas para achar caso ela esteja com case diferente a depender da aba
        norm_map = { _norm(c): c for c in df.columns }
        norm_aliases = {_norm(a) for a in CODE_ALIASES}

        #busca a coluna candidata
        candidata_cols = [orig for norm, orig in norm_map.items() if norm in norm_aliases]
        if not candidata_cols:
            #tentar exatamente "Grupo"
            for c in df.columns:
                if _norm(c) == _norm("Grupo"):
                    candidata_cols.append(c)
                    break
        if not candidata_cols:
            #procurar qualquer coisa que minimamente lembre grupo
            candidata_cols.extend([orig for norm, orig in norm_map.items() if norm.startswith("gru")])

        #verificando e achando a "coluna-alvo"
        for col in candidata_cols:
            series = df[col].astype(str).str.strip()
            if series.eq(alvo).any():
                row = df.loc[series == alvo].iloc[0]
                canon_key = CANONICAL.get(_norm(col), col)
                return pd.Series({canon_key: str(row[col]).strip()})

    raise ValueError("A linha não foi encontrada")