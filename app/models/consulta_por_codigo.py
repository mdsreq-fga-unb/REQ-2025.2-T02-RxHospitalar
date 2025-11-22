# RF03 - Consultar Produto por código original do produto
import re
import unicodedata
import pandas as pd
from app.models.carregar_dados import file

#esta função serve para normalizar os nomes de coluna, dado que há inconsistências entre as abas
def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s))
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w]+", " ", s).lower().strip()
    return s.replace(" ", "")

#alguns dos nomes que podem surgir para o código original e descrição do produto dentre as colunas da planilha
CODE_ALIASES = {"CODORIGINAL", "Cód Original", "Código Original"}
DESC_ALIASES = {"descricao", "descr", "Descricao", "nome"}

#a função core da RF03
def consulta_por_codigo(codigo_produto: str):
    if not codigo_produto or str(codigo_produto).strip() == "":
        raise ValueError("O código não foi encontrado")
    #o alvo no caso é a string a ser buscada nas colunas candidatas
    alvo = str(codigo_produto).strip()
    xls = pd.ExcelFile(file)

    for sheet in xls.sheet_names:
        try:
            df = pd.read_excel(file, sheet_name=sheet, header=0, dtype=str)
        #há um loop de continuidade porque às vezes a coluna pode estar em outra aba da planilha
        except Exception as e:
            print(f"[{sheet}] erro leitura: {e}")
            continue
        if df.empty:
            print(f"[{sheet}] dataframe vazio")
            continue
        
        #
        print(f"[{sheet}] colunas: {list(df.columns)}")
        #isso normaliza os nomes das colunas para achar caso ela esteja com case diferente a depender da aba
        norm_map = { _norm(c): c for c in df.columns }
        norm_aliases = {_norm(a) for a in CODE_ALIASES}
        
        #escolhe a coluna por alias normalizado
        code_col = next((orig for norm, orig in norm_map.items() if norm in norm_aliases), None)
        if not code_col:
            #tenta especificamente 'codoriginal'
            code_col = norm_map.get("codoriginal")
        if not code_col:
            #último fallback: qualquer coluna começando com 'cod'
            code_col = next((orig for norm, orig in norm_map.items() if norm.startswith("cod")), None)
        #
        print(f"[{sheet}] code_col escolhido: {code_col}")
        if not code_col:
            continue

        #busca agora pela coluna da descrição, que está na mesma aba da coluna do código original
        desc_col = next((orig for norm, orig in norm_map.items() if norm in {_norm(a) for a in DESC_ALIASES}), None)

        #pega a coluna escolhida e garante que os valores são strings para comparação
        series = df[code_col].astype(str).str.strip()
        #
        sample = series.dropna().head(10).tolist()
        print(f"[{sheet}] amostra valores em '{code_col}': {sample}")
        #compara elemento a elemento com a "string-alvo"
        mask = series == alvo
        print(f"[{sheet}] total_matches={mask.sum()}")

        if mask.any():
            row = df.loc[mask].iloc[0]
            #mantém o nome real da coluna encontrada (bate com os testes)
            result = {code_col: str(row[code_col]).strip()}
            if desc_col and desc_col in row:
                result["Descrição"] = row[desc_col]
            print(f"[{sheet}] ENCONTRADO -> {result}")
            return pd.Series(result)

    print(f"[consulta_por_codigo] NÃO ENCONTRADO alvo={alvo}")
    raise ValueError("O código não foi encontrado")