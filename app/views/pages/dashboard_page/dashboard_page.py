import tkinter as tk
from tkinter import ttk
from pandastable import Table
import pandas as pd
import unicodedata
import re

# Importações dos componentes
from app.views.components.estoque_filters import EstoqueFilterFrame, setup_styles
from app.views.components.navbar import Header
from app.models.carregar_dados import carregar_dados_unificados 
from app.views.components.analytical_summary import AnalyticalSummary 
from app.views.components.purchase_suggestions import PurchaseSuggestions
from app.views.components.graphs_frame import GraphsFrame 
from app.controllers.chamadas import sugestao_compra 

def _norm(s):
    if not isinstance(s, str): return str(s)
    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w]+", " ", s).lower().strip()
    return s.replace(" ", "")

class DashboardView(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Variável para guardar o contexto atual dos filtros
        self.current_filters = {} 

        setup_styles(self.controller)

        # --- HEADER ---
        self.header = Header(self, controller)
        self.header.pack(side="top", fill="x")

        # --- CORPO PRINCIPAL ---
        self.body_frame = ttk.Frame(self)
        self.body_frame.pack(side="top", fill="both", expand=True)

        self.body_frame.columnconfigure(0, weight=0, minsize=335)
        self.body_frame.columnconfigure(1, weight=1)
        self.body_frame.rowconfigure(0, weight=1)

        # --- BARRA LATERAL (FILTROS) ---
        self.sidebar_container = ttk.Frame(self.body_frame, style="Sidebar.TFrame")
        self.sidebar_container.grid(row=0, column=0, sticky="nsew")
        
        # Passamos self.apply_filters como callback
        self.filters = EstoqueFilterFrame(self.sidebar_container, on_filter_callback=self.apply_filters)
        self.filters.pack(fill="both", expand=True, padx=10, pady=(85, 10))

        # --- ÁREA DE CONTEÚDO (DIREITA) ---
        self.right_container = ttk.Frame(self.body_frame)
        self.right_container.grid(row=0, column=1, sticky="nsew")
        self.right_container.rowconfigure(0, weight=1)
        self.right_container.columnconfigure(0, weight=1)

        # Canvas com Scrollbar
        self.canvas = tk.Canvas(self.right_container, background="#1e1e1e", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.right_container, orient="vertical", command=self.canvas.yview)
        
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.content_area = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_area, anchor="nw")

        # Eventos de redimensionamento
        self.content_area.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Scroll do Mouse
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind_all("<Button-4>", self._on_mousewheel)
        self.bind_all("<Button-5>", self._on_mousewheel)

        # --- CONTEÚDO INTERNO ---
        self.inner_content = ttk.Frame(self.content_area)
        self.inner_content.pack(fill="both", expand=True, padx=20, pady=20)

        self.title_label = ttk.Label(
            self.inner_content,
            text="Dashboard",
            font=("Segoe UI", 24, "bold"),
            foreground="white",
            background="#1e1e1e"
        )
        self.title_label.pack(anchor="w", pady=(0, 20))

        # 1. GRÁFICOS (Aqui aparecerá o gráfico de pizza)
        self.graphs_section = GraphsFrame(self.inner_content)
        self.graphs_section.pack(fill="x", pady=(0, 20))

        # 2. SUGESTÕES DE COMPRA
        self.purchase_suggestions = PurchaseSuggestions(self.inner_content)
        self.purchase_suggestions.pack(fill="x", pady=(0, 20))

        # 3. RESUMO ANALÍTICO (Cards)
        self.analytical_summary = AnalyticalSummary(self.inner_content)
        self.analytical_summary.pack(fill="x", pady=(0, 20))

        # 4. TABELA DE DADOS
        self.frame_tabela_container = ttk.Frame(self.inner_content, style="Card.TFrame", height=600)
        self.frame_tabela_container.pack(fill="both", expand=True)
        self.frame_tabela_container.pack_propagate(False)

        # --- CARREGAMENTO INICIAL DE DADOS ---
        # Verifica se os dados já existem no controller, senão carrega
        if not hasattr(self.controller, 'df_master') or \
           (isinstance(self.controller.df_master, pd.DataFrame) and self.controller.df_master.empty):
            print("Carregando dados iniciais...")
            try:
                self.controller.df_master = carregar_dados_unificados()
            except Exception as e:
                print(f"Erro ao carregar dados: {e}")
                self.controller.df_master = pd.DataFrame() 

        # Carrega sugestões iniciais
        try:
            df_sugestoes = sugestao_compra(linha=None, periodo=4)
            self.purchase_suggestions.update_cards(df_sugestoes)
        except Exception as e:
            print(f"Erro ao carregar sugestões: {e}")

        # --- RENDERIZAÇÃO INICIAL ---
        self.current_filters = {} 
        
        # Na inicialização, o dado do gráfico é igual ao da tabela (Tudo cheio)
        self.after(100, lambda: self.render_dataframe_table(
            df_specific=self.controller.df_master, 
            df_context=self.controller.df_master
        ))

    def render_dataframe_table(self, df_specific, df_context=None):
        """
        Atualiza Tabela, Gráficos e Cards.
        
        Args:
            df_specific: DataFrame filtrado (Linha/Sublinha) -> Para Tabela e Cards.
            df_context: DataFrame global (Só Data/Condição) -> Para Gráficos comparativos.
        """
        
        # Se não vier o contexto (ex: chamada antiga), usa o específico como fallback
        if df_context is None:
            df_context = df_specific

        self.update_idletasks()

        # 1. Atualiza Métricas (Cards) -> Usa o específico (o que o usuário vê)
        if hasattr(self, 'analytical_summary'):
            self.analytical_summary.update_metrics(df_specific)
            
        # 2. Atualiza Gráficos -> AQUI É O PULO DO GATO
        # Mandamos o df_context (que tem todas as linhas) e o self.current_filters
        # O GraphsFrame vai ler o filtro 'linha': 'MDS' e destacar 'MDS' no total.
        if hasattr(self, 'graphs_section'):
            self.graphs_section.update_graphs(df_context, self.current_filters)

        # 3. Renderiza Tabela -> Usa o específico
        for widget in self.frame_tabela_container.winfo_children():
            widget.destroy()

        if df_specific is None or df_specific.empty:
            ttk.Label(self.frame_tabela_container, text="Nenhum dado encontrado.", background="#F4F9F4").pack(pady=50)
            return

        self.pt_widget = Table(self.frame_tabela_container, dataframe=df_specific, showtoolbar=True, showstatusbar=True)
        self.pt_widget.show()
        self.pt_widget.redraw()

    def apply_filters(self, filter_data):
        df = self.controller.df_master
        if df is None or df.empty:
            return

        print("Aplicando filtros:", filter_data)
        self.current_filters = filter_data 
        
        # --- ETAPA 1: FILTROS GLOBAIS (Data, Condição) ---
        # Esses filtros devem ser aplicados TANTO para o gráfico QUANTO para a tabela.
        # (OBS: Se você tiver lógica de filtrar data/período, insira aqui em df_base)
        df_base = df.copy() 
        
        # [Seu código de filtro de Data/Condição entraria aqui se existisse]
        # Ex: df_base = filtrar_por_data(df_base, filter_data['periodo'])
        
        # Este é o DataFrame que vai pro Gráfico (contém todas as Linhas, mas respeita a Data)
        df_contexto_grafico = df_base.copy()

        # --- ETAPA 2: FILTROS ESPECÍFICOS (Linha, Sublinha, Código) ---
        # Este DataFrame será cortado e irá apenas para a Tabela e Cards
        df_filtrado_tabela = df_base.copy()
        
        cols_map = {_norm(c): c for c in df_filtrado_tabela.columns}
        
        aliases_linha = {"grupo", "linha", "categoria"}
        aliases_sub = {"subgrupo", "sublinha", "subgruponivel1", "familia"}
        aliases_cod = {
            "codven", "codproduto", "referencia", "cod", "produto",
            "codoriginal", "reforiginal", "codigooriginal", "codigofabricante",
            "codoriginalvendas"
        }

        col_linha = next((cols_map[k] for k in cols_map if k in aliases_linha), None)
        col_sub = next((cols_map[k] for k in cols_map if k in aliases_sub), None)
        cols_codigo_encontradas = [cols_map[k] for k in cols_map if k in aliases_cod or "cod" in k]

        # 1. Filtra Linha (APENAS na tabela)
        if val_linha := filter_data.get("linha"):
            if col_linha:
                df_filtrado_tabela = df_filtrado_tabela[df_filtrado_tabela[col_linha].astype(str).str.strip() == val_linha.strip()]

        # 2. Filtra SubLinha (APENAS na tabela)
        if val_sub := filter_data.get("sub_linha"):
            if col_sub:
                df_filtrado_tabela = df_filtrado_tabela[df_filtrado_tabela[col_sub].astype(str).str.strip() == val_sub.strip()]

        # 3. Filtra Código (APENAS na tabela)
        if val_cod := filter_data.get("codigo"):
            val_cod = str(val_cod).strip()
            if cols_codigo_encontradas:
                mask = pd.Series(False, index=df_filtrado_tabela.index)
                for col_name in cols_codigo_encontradas:
                    match_nesta_coluna = df_filtrado_tabela[col_name].astype(str).str.contains(val_cod, case=False, na=False)
                    mask |= match_nesta_coluna
                df_filtrado_tabela = df_filtrado_tabela[mask]

        # --- CHAMADA FINAL ---
        # Passamos os DOIS dataframes:
        # 1. df_filtrado_tabela -> Para a tabela ver só a linha escolhida.
        # 2. df_contexto_grafico -> Para o gráfico ver TUDO e calcular a diferença.
        self.render_dataframe_table(df_specific=df_filtrado_tabela, df_context=df_contexto_grafico)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        if self.winfo_viewable():
            if event.delta:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            elif event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")