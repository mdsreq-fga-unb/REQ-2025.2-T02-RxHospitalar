import tkinter as tk
from tkinter import ttk
from pandastable import Table, TableModel
import pandas as pd
import unicodedata
import re
import threading

# Importação dos componentes
from app.views.components.navbar import Header
from app.views.components.estoque_filters import EstoqueFilterFrame, setup_styles
from app.models.carregar_dados import carregar_dados_unificados 
from app.views.components.analytical_summary import AnalyticalSummary 
from app.views.components.purchase_suggestions import PurchaseSuggestions
from app.views.components.graphs_frame import GraphsFrame 
from app.controllers.chamadas import sugestao_compra 
from app.models.consulta_por_status import consulta_por_status
from app.views.components.loading_import_modal import LoadingImportModal

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

        # Estado atual dos filtros
        self.current_filters = {}

        setup_styles(self.controller)

        self.header = Header(self, controller)
        self.header.pack(side="top", fill="x")

        self.body_frame = ttk.Frame(self)
        self.body_frame.pack(side="top", fill="both", expand=True)

        self.body_frame.columnconfigure(0, weight=0, minsize=335)
        self.body_frame.columnconfigure(1, weight=1)
        self.body_frame.rowconfigure(0, weight=1)

        # --- SIDEBAR (FILTROS) ---
        self.sidebar_container = ttk.Frame(self.body_frame, style="Sidebar.TFrame")
        self.sidebar_container.grid(row=0, column=0, sticky="nsew")
        
        self.filters = EstoqueFilterFrame(self.sidebar_container, on_filter_callback=self.apply_filters)
        self.filters.pack(fill="both", expand=True, padx=10, pady=(85, 10))

        # --- ÁREA DE CONTEÚDO (DIREITA) ---
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

        self.content_area = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_area, anchor="nw")

        # Binds de redimensionamento e scroll
        self.content_area.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind_all("<Button-4>", self._on_mousewheel)
        self.bind_all("<Button-5>", self._on_mousewheel)

        # --- WIDGETS INTERNOS ---
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

        # 1. Gráficos
        self.graphs_section = GraphsFrame(self.inner_content)
        self.graphs_section.pack(fill="x", pady=(0, 20))

        # 2. Sugestões
        self.purchase_suggestions = PurchaseSuggestions(self.inner_content)
        self.purchase_suggestions.pack(fill="x", pady=(0, 20))

        # 3. Resumo Analítico
        self.analytical_summary = AnalyticalSummary(self.inner_content)
        self.analytical_summary.pack(fill="x", pady=(0, 20))

        # 4. Tabela
        self.frame_tabela_container = ttk.Frame(self.inner_content, style="Card.TFrame", height=600)
        self.frame_tabela_container.pack(fill="both", expand=True)
        self.frame_tabela_container.pack_propagate(False)

        # Carga Inicial
        if not hasattr(self.controller, 'df_master') or \
           (isinstance(self.controller.df_master, pd.DataFrame) and self.controller.df_master.empty):
            
            print("Carregando e unificando dados...")
            self.controller.df_master = carregar_dados_unificados()

        # Renderização inicial (Contexto = Específico = df_master)
        self.render_dataframe_table(
            df_specific=self.controller.df_master,
            df_context=self.controller.df_master
        )

        # Carrega sugestões iniciais
        try:
            df_sugestoes = sugestao_compra(linha=None, periodo=4)
            self.purchase_suggestions.update_cards(df_sugestoes)
        except Exception as e:
            print(f"Erro ao carregar sugestões de compra: {e}")

    def render_dataframe_table(self, df_specific, df_context=None):
        """
        Renderiza a UI com lógica de Contexto (Integra) vs Específico.
        """
        # Se não vier contexto, assume que é igual ao específico
        if df_context is None:
            df_context = df_specific

        # 1. Cards de Resumo -> Usa os dados FILTRADOS (o que o usuário vê na tabela)
        if hasattr(self, 'analytical_summary'):
            self.analytical_summary.update_metrics(df_specific)
            
        # 2. Gráficos -> Usa o CONTEXTO (para comparar Linha X com o Total)
        if hasattr(self, 'graphs_section'):
            self.graphs_section.update_graphs(df_context, self.current_filters)

        # 3. Tabela -> Usa os dados FILTRADOS
        # Limpa tabela anterior
        if hasattr(self, 'pt_widget') and self.pt_widget is not None:
             # Tenta limpar widget antigo se existir
            try:
                for widget in self.frame_tabela_container.winfo_children():
                    widget.destroy()
            except: pass

        if df_specific is None or df_specific.empty:
            ttk.Label(self.frame_tabela_container, 
                      text="Nenhum dado encontrado para os filtros selecionados.", 
                      font=("Segoe UI", 12),
                      background="#F4F9F4").pack(pady=50)
            self.pt_widget = None
            return

        # Recria tabela
        try:
            self.pt_widget = Table(self.frame_tabela_container, dataframe=df_specific,
                                   showtoolbar=True, showstatusbar=True)
            self.pt_widget.show()
            self.pt_widget.redraw()
        except Exception as e:
            print(f"Erro ao desenhar tabela: {e}")

    def apply_filters(self, filter_data):
        """Inicia a filtragem em Thread (Plot Cliente Vendedor)."""
        self.current_filters = filter_data
        
        # 1. Exibe Modal
        self.loading_modal = LoadingImportModal(self.controller)
        self.controller.update_idletasks()

        # 2. Inicia Thread
        filter_thread = threading.Thread(
            target=self._perform_filtering,
            args=(filter_data,)
        )
        filter_thread.start()

    def _perform_filtering(self, filter_data):
        """Lógica de filtragem unificada."""
        try:
            # A. SELEÇÃO DA BASE (Contexto Global)
            # Se 'Produto Parado' estiver ativo, a base muda completamente.
            df_base = self.controller.df_master
            
            if filter_data.get("condicoes", {}).get("Produto parado"):
                try:
                    print("Filtrando por Produtos Parados (Base Trocada)...")
                    resultado_status = consulta_por_status()
                    df_parados = resultado_status.get("df")
                    if df_parados is not None and not df_parados.empty:
                        df_base = df_parados
                    else:
                        df_base = pd.DataFrame(columns=df_base.columns if df_base is not None else None)
                except Exception as e:
                    print(f"Erro ao carregar produtos parados: {e}")
                    df_base = pd.DataFrame()

            # df_base é o nosso CONTEXTO para os gráficos (contém todas as linhas, mas respeita a condição global)
            df_context = df_base.copy() if df_base is not None else pd.DataFrame()

            if df_base is None or df_base.empty:
                self.after(0, self._on_filtering_complete, pd.DataFrame(), pd.DataFrame(), None)
                return

            print("Aplicando filtros específicos:", filter_data)
            df_filtered = df_base.copy()

            # B. FILTROS ESPECÍFICOS (Linha, Sublinha, Código)
            # Mapeamento de colunas
            cols_map = {_norm(c): c for c in df_filtered.columns}
            
            aliases_linha = {"grupo", "linha", "categoria"}
            aliases_sub = {"subgrupo", "sublinha", "subgruponivel1", "familia"}
            aliases_cod = {"codven", "codproduto", "referencia", "codigooriginal", "cod"}
            
            col_linha = next((cols_map[k] for k in cols_map if k in aliases_linha), None)
            col_sub = next((cols_map[k] for k in cols_map if k in aliases_sub), None)
            col_cod = next((cols_map[k] for k in cols_map if k in aliases_cod or "cod" in k), None)

            # Filtro Linha
            if val_linha := filter_data.get("linha"):
                if col_linha:
                    df_filtered = df_filtered[df_filtered[col_linha].astype(str).str.strip() == val_linha.strip()]

            # Filtro SubLinha
            if val_sub := filter_data.get("sub_linha"):
                if col_sub:
                    df_filtered = df_filtered[df_filtered[col_sub].astype(str).str.strip() == val_sub.strip()]

            # Filtro Código
            if val_cod := filter_data.get("codigo"):
                if col_cod:
                    df_filtered = df_filtered[df_filtered[col_cod].astype(str).str.contains(val_cod, case=False, na=False)]

            # C. ATUALIZAÇÃO DE SUGESTÕES
            df_sugestoes = None
            try:
                periodo_str = filter_data.get("periodo", "4 Meses")
                match = re.search(r'\d+', str(periodo_str))
                periodo_val = int(match.group()) if match else 4
                
                linha_para_sugestao = val_linha if val_linha else None
                df_sugestoes = sugestao_compra(linha=linha_para_sugestao, periodo=periodo_val)
            except Exception as e:
                print(f"Erro filtro sugestão: {e}")

            # D. RETORNO PARA UI
            # Passamos df_filtered (para tabela) e df_context (para gráficos)
            self.after(0, self._on_filtering_complete, df_filtered, df_context, df_sugestoes)

        except Exception as e:
            print(f"Erro crítico na thread de filtro: {e}")
            self.after(0, self._on_filtering_complete, None, None, None)

    def _on_filtering_complete(self, df_filtered, df_context, df_sugestoes):
        """Finaliza o carregamento e atualiza a UI com os dois contextos."""
        # 1. Fecha Modal
        if hasattr(self, 'loading_modal') and self.loading_modal:
            self.loading_modal.destroy_modal()
            self.loading_modal = None

        # 2. Renderiza UI Principal
        if df_filtered is not None:
            self.render_dataframe_table(df_specific=df_filtered, df_context=df_context)
        
        # 3. Atualiza Sugestões
        if df_sugestoes is not None:
             self.purchase_suggestions.update_cards(df_sugestoes)

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