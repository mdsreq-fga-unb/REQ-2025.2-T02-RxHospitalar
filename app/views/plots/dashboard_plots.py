import matplotlib.pyplot as plt
import pandas as pd
import unicodedata
import re
from app.models.consulta_sazonalidade import consulta_sazonalidade_dataframe
# --- Funções Auxiliares ---
def _norm(s):
    if not isinstance(s, str): return str(s)
    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w]+", " ", s).lower().strip()
    return s.replace(" ", "")

def find_col(df, aliases):
    cols_map = {_norm(c): c for c in df.columns}
    for alias in aliases:
        norm_alias = _norm(alias)
        if norm_alias in cols_map:
            return cols_map[norm_alias]
    return None

def _preparar_dados_estoque(df):
    """Função auxiliar para limpar e converter dados"""
    if df is None or df.empty: return None, None, None
    
    col_estoque = find_col(df, ["Estoque", "Qtd Estoque", "Saldo", "Quant"])
    col_grupo = find_col(df, ["Grupo", "Linha", "Categoria"])
    col_cod = find_col(df, ["Cód Produto", "Cod Produto", "Codigo", "Cod", "CODVEN"])

    if not col_estoque or not col_grupo: return None, None, None

    df_proc = df.copy()
    df_proc[col_estoque] = df_proc[col_estoque].astype(str).str.strip().str.replace(',', '.', regex=False)
    df_proc[col_estoque] = pd.to_numeric(df_proc[col_estoque], errors='coerce').fillna(0)

    if col_cod:
        df_proc = df_proc.drop_duplicates(subset=[col_cod])
        
    return df_proc, col_grupo, col_estoque

# --- 1. Gráfico Geral ---
def plot_geral_distribuicao_linhas(df):
    fig, ax = plt.subplots(figsize=(5, 3)) 
    fig.patch.set_facecolor('#F4F9F4')
    ax.set_facecolor('#F4F9F4')
    
    df_proc, col_grupo, col_estoque = _preparar_dados_estoque(df)
    
    if df_proc is None or df_proc.empty:
        ax.text(0.5, 0.5, "Sem dados", ha='center')
        ax.axis('off')
        return fig

    df_grouped = df_proc.groupby(col_grupo)[col_estoque].sum().sort_values(ascending=False)
    df_grouped = df_grouped[df_grouped > 0]

    if df_grouped.empty:
        ax.text(0.5, 0.5, "Estoque Zerado", ha='center')
        ax.axis('off')
        return fig

    top_n = 3
    if len(df_grouped) > top_n:
        main = df_grouped.iloc[:top_n]
        others_sum = df_grouped.iloc[top_n:].sum()
        others_series = pd.Series({'Outros': others_sum})
        df_final = pd.concat([main, others_series])
    else:
        df_final = df_grouped

    wedges, texts, autotexts = ax.pie(
        df_final, labels=None, autopct='%1.1f%%',
        startangle=90, pctdistance=0.82, explode=[0.02]*len(df_final)
    )
    plt.setp(autotexts, size=8, weight="bold", color="white")
    
    for i, autotext in enumerate(autotexts):
        if df_final.index[i] == 'Outros':
            x, y = autotext.get_position()
            autotext.set_position((x, y - 0.12))

    centre_circle = plt.Circle((0,0), 0.65, fc='#F4F9F4')
    fig.gca().add_artist(centre_circle)
    
    total_val = int(df_grouped.sum())
    total_str = f"Total\n{total_val}"
    center_text = ax.text(0, 0, total_str, ha='center', va='center', fontsize=9, color='#555')

    ax.set_title("Distribuição por Linha", fontsize=10, fontweight='bold', color='#333', pad=4)
    ax.legend(wedges, df_final.index, title="Linhas", loc="center left", bbox_to_anchor=(0.85, 0, 0.5, 1), fontsize=8, frameon=False)

    fig.my_wedges = wedges
    fig.my_names = df_final.index
    fig.my_values = df_final.values
    fig.my_center_text = center_text
    fig.my_total_str = total_str

    ax.axis('equal')
    plt.tight_layout()
    return fig

# --- 2. Gráfico Específico (Linha vs Total) ---

def plot_linha_especifica(df, linha_selecionada):
    fig, ax = plt.subplots(figsize=(5, 3)) 
    fig.patch.set_facecolor('#F4F9F4')
    ax.set_facecolor('#F4F9F4')

    df_proc, col_grupo, col_estoque = _preparar_dados_estoque(df)
    
    if df_proc is None:
        ax.text(0.5, 0.5, "Erro dados", ha='center')
        ax.axis('off')
        return fig

    # 1. Total de TUDO (do DataFrame passado)
    # Se você passou o DF com todas as linhas, isso será o total do estoque
    total_geral = df_proc[col_estoque].sum()
    
    # 2. Total da Linha Selecionada
    mask = df_proc[col_grupo].astype(str).apply(_norm) == _norm(linha_selecionada)
    total_linha = df_proc[mask][col_estoque].sum()
    
    # 3. Cálculo do Resto
    # Se você corrigiu o Passo 1, o total_resto agora será > 0
    total_resto = total_geral - total_linha
    
    if total_geral == 0:
        ax.text(0.5, 0.5, "Estoque Zerado", ha='center')
        ax.axis('off')
        return fig

    # Dados para plotagem
    labels_legend = [linha_selecionada, "Outras Linhas"]
    valores = [total_linha, total_resto]
    colors = ['#ff7f0e', '#e0e0e0'] # Laranja e Cinza Claro

    # Plotagem
    wedges, texts, autotexts = ax.pie(
        valores, 
        labels=None, 
        autopct='%1.1f%%',
        startangle=90, 
        pctdistance=0.82, 
        colors=colors,
        explode=[0.02, 0] 
    )

    # Estilo dos textos (Se for 0% o resto, esconde o texto cinza para ficar bonito)
    if len(autotexts) > 0:
        plt.setp(autotexts[0], size=9, weight="bold", color="white")
    if len(autotexts) > 1:
        if total_resto == 0:
            plt.setp(autotexts[1], visible=False)
        else:
            plt.setp(autotexts[1], size=8, color="#555")

    # Rosca
    centre_circle = plt.Circle((0,0), 0.65, fc='#F4F9F4')
    fig.gca().add_artist(centre_circle)

    # Texto Central (Share)
    percentual = (total_linha / total_geral * 100) if total_geral > 0 else 0
    total_str = f"{linha_selecionada}\n{percentual:.1f}%"
    
    center_text = ax.text(0, 0, total_str, ha='center', va='center', fontsize=9, color='#555', fontweight='bold')

    ax.set_title(f"Linha: {linha_selecionada} vs Resto do Estoque", fontsize=10, fontweight='bold', color='#333', pad=4)

    # Legenda Dinâmica
    legend_labels = [f"{l}: {int(v)}" for l, v in zip(labels_legend, valores)]
    
    ax.legend(
        wedges, 
        legend_labels, 
        title="Qtd Real", 
        loc="center left", 
        bbox_to_anchor=(0.85, 0, 0.5, 1), 
        fontsize=8, 
        frameon=False
    )

    # Interatividade
    fig.my_wedges = wedges
    fig.my_names = labels_legend
    fig.my_values = valores
    fig.my_center_text = center_text
    fig.my_total_str = total_str 

    ax.axis('equal')
    plt.tight_layout()

    return fig

def plot_sazonalidade(df_vendas, linha_selecionada=None):
    """
    Gera gráfico de linha para Sazonalidade (Evolução Mensal).
    """
    # 1. Processa os dados
    df_sazonal = consulta_sazonalidade_dataframe(df_vendas, linha_selecionada)
    
    # Configuração da Figura
    fig, ax = plt.subplots(figsize=(6, 3)) # Um pouco mais largo que a pizza
    fig.patch.set_facecolor('#F4F9F4')
    ax.set_facecolor('#F4F9F4')

    # Dados
    meses_nome = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    x = df_sazonal['MES']
    y = df_sazonal['TOTAL']

    # 2. Plotagem da Linha
    # Se tiver linha selecionada, usa laranja (destaque), senão azul (geral)
    cor_linha = '#ff7f0e' if linha_selecionada else '#1f77b4'
    
    ax.plot(x, y, marker='o', linestyle='-', linewidth=2, color=cor_linha, markersize=5)
    
    # Preenchimento (Area Chart style) suave abaixo da linha
    ax.fill_between(x, y, color=cor_linha, alpha=0.1)

    # 3. Estilização
    ax.set_title(f"Sazonalidade: {linha_selecionada if linha_selecionada else 'Global'}", 
                 fontsize=10, fontweight='bold', color='#333', pad=10)
    
    # Eixos
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(meses_nome, fontsize=8, color='#555')
    ax.tick_params(axis='y', labelsize=8, colors='#555')
    
    # Remove bordas desnecessárias (topo e direita)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#ddd')
    ax.spines['bottom'].set_color('#ddd')

    # Grid pontilhado apenas horizontal
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    # --- Interatividade (Dados ocultos na figura) ---
    # --- NOVO: CRIAR O TOOLTIP (BALÃO) INVISÍVEL ---
    annot = ax.annotate("", xy=(0,0), xytext=(-20,20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="white", ec="#aaa", alpha=0.9),
                        arrowprops=dict(arrowstyle="->", color="#aaa"))
    annot.set_visible(False)

    # --- DADOS PARA INTERATIVIDADE ---
    fig.my_x = x.values       # Lista de meses (1..12)
    fig.my_y = y.values       # Lista de valores
    fig.my_labels = meses_nome # Jan, Fev...
    fig.my_annot = annot      # O objeto de anotação que controlaremos

    plt.tight_layout()
    return fig

# --- Placeholders ---
def plot_sublinha_especifica(df, sub_linha):
    fig = plt.figure(figsize=(5, 3))
    fig.patch.set_facecolor('#F4F9F4')
    plt.text(0.5, 0.5, f"Sub-Linha: {sub_linha}", ha='center')
    plt.axis('off')
    return fig

def plot_produto_especifico(df, codigo):
    fig = plt.figure(figsize=(5, 3))
    fig.patch.set_facecolor('#F4F9F4')
    plt.text(0.5, 0.5, f"Produto: {codigo}", ha='center')
    plt.axis('off')
    return fig