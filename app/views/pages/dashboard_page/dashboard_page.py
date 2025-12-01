import tkinter as tk
from tkinter import ttk
from pandastable import Table, TableModel
import pandas as pd
import unicodedata
import re
import threading
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.views.components.estoque_filters import EstoqueFilterFrame

from app.views.components.navbar import Header
from app.views.components.estoque_filters import EstoqueFilterFrame, setup_styles
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

        setup_styles(self.controller)

        self.header = Header(self, controller)
        self.header.pack(side="top", fill="x")

        self.body_frame = ttk.Frame(self)
        self.body_frame.pack(side="top", fill="both", expand=True)

        self.body_frame.columnconfigure(0, weight=0, minsize=335)
        self.body_frame.columnconfigure(1, weight=1)
        self.body_frame.rowconfigure(0, weight=1)

        self.sidebar_container = ttk.Frame(self.body_frame, style="Sidebar.TFrame")
        self.sidebar_container.grid(row=0, column=0, sticky="nsew")
        
        self.filters = EstoqueFilterFrame(self.sidebar_container, on_filter_callback=self.apply_filters)
        self.filters.pack(fill="both", expand=True, padx=10, pady=(85, 10))

        # --- ÁREA DE CONTEÚDO COM SCROLL ---
        # Container principal da direita (onde ficará o canvas)
        self.right_container = ttk.Frame(self.body_frame)
        self.right_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        
        self.right_container.rowconfigure(0, weight=1)
        self.right_container.columnconfigure(0, weight=1)

        # Canvas e Scrollbar
        self.canvas = tk.Canvas(self.right_container, background="#1e1e1e", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.right_container, orient="vertical", command=self.canvas.yview)
        
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame interno que vai dentro do Canvas (onde ficam os widgets reais)
        self.content_area = ttk.Frame(self.canvas)
        
        # Janela do canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_area, anchor="nw")

        # Configurações de redimensionamento do Canvas
        self.content_area.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # --- BIND DO MOUSEWHEEL (Atualizado para funcionar melhor) ---
        # Vincula o scroll para Windows e MacOS
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        # Vincula o scroll para Linux
        self.bind_all("<Button-4>", self._on_mousewheel)
        self.bind_all("<Button-5>", self._on_mousewheel)

        # --- CONTEÚDO DO DASHBOARD ---
        # Adicionando padding no frame interno
        self.inner_content = ttk.Frame(self.content_area)
        self.inner_content.pack(fill="both", expand=True, padx=20, pady=20)

        self.title_label = ttk.Label(
            self.inner_content,
            text="Dashboard Unificado (Vendas + Estoque)",
            font=("Segoe UI", 24, "bold"),
            foreground="white",
            background="#1e1e1e"
        )
        self.title_label.pack(anchor="w", pady=(0, 20))

        # --- ÁREA DOS GRÁFICOS ---
        self.graphs_section = GraphsFrame(self.inner_content)
        self.graphs_section.pack(fill="x", pady=(0, 20))

        # Sugestões de Compra
        self.purchase_suggestions = PurchaseSuggestions(self.inner_content)
        self.purchase_suggestions.pack(fill="x", pady=(0, 20))

        # Resumo Analítico
        self.analytical_summary = AnalyticalSummary(self.inner_content)
        self.analytical_summary.pack(fill="x", pady=(0, 20))

        # Container da Tabela (Com altura mínima garantida)
        self.frame_tabela_container = ttk.Frame(self.inner_content, style="Card.TFrame", height=600)
        self.frame_tabela_container.pack(fill="both", expand=True)
        self.frame_tabela_container.pack_propagate(False) # Garante que a altura seja respeitada

        if not hasattr(self.controller, 'df_master') or \
           (isinstance(self.controller.df_master, pd.DataFrame) and self.controller.df_master.empty):
            
            print("Carregando e unificando dados...")
            # Chama a função que cruza as tabelas
            self.controller.df_master = carregar_dados_unificados()

        # Carregar sugestões iniciais
        try:
            df_sugestoes = sugestao_compra(linha=None, periodo=4)
            self.purchase_suggestions.update_cards(df_sugestoes)
        except Exception as e:
            print(f"Erro ao carregar sugestões de compra: {e}")

        self.render_dataframe_table(self.controller.df_master)

    def render_dataframe_table(self, df):
        # Atualiza os cards de resumo
        if hasattr(self, 'analytical_summary'):
            self.analytical_summary.update_metrics(df)
            
        # 2. Atualiza Gráficos -> AQUI É O PULO DO GATO
        # Mandamos o df_context (que tem todas as linhas) e o self.current_filters
        # O GraphsFrame vai ler o filtro 'linha': 'MDS' e destacar 'MDS' no total.
        if hasattr(self, 'graphs_section'):
            self.graphs_section.update_graphs(df_context, self.current_filters)

        # Caso 2: Tabela já existe, apenas atualiza os dados
        if hasattr(self, 'pt_widget') and self.pt_widget is not None:
            try:
                # Verifica se o widget ainda existe no Tkinter
                if self.pt_widget.winfo_exists():
                    self.pt_widget.updateModel(TableModel(df))
                    self.pt_widget.redraw()
                    return
            except Exception as e:
                print(f"Erro ao atualizar tabela existente: {e}")
                # Se der erro, cai no fallback de recriar
        
        # Caso 3: Tabela não existe ou precisa ser recriada
        for widget in self.frame_tabela_container.winfo_children():
            widget.destroy()

        self.pt_widget = Table(self.frame_tabela_container, dataframe=df,
                               showtoolbar=True, showstatusbar=True)
        self.pt_widget.show()
        self.pt_widget.redraw()

    def apply_filters(self, filter_data):
        """
        Inicia o processo de filtragem em uma thread separada,
        exibindo o modal de carregamento.
        """
        # 1. Exibe o Modal de Carregamento
        self.loading_modal = LoadingImportModal(self.controller)
        self.controller.update_idletasks() # Força a renderização imediata do modal

        # 2. Inicia a Thread de Filtragem
        filter_thread = threading.Thread(
            target=self._perform_filtering,
            args=(filter_data,)
        )
        filter_thread.start()

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
        """Reseta a região de scroll para englobar o frame interno"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        """Redimensiona a janela interna para a largura do canvas"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        """
        Função unificada de scroll que funciona em Windows, Linux e MacOS
        """
        if self.winfo_viewable():
            # Verifica se é Windows/Mac (event.delta) ou Linux (event.num)
            
            # Windows / MacOS
            if event.delta:
                # O divisor 120 é padrão do Windows. Negativo para inverter a direção natural.
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            # Linux (Button-4 é pra CIMA, Button-5 é pra BAIXO)
            elif event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")