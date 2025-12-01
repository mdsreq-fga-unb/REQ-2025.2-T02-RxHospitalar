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
            
        # Caso 1: DataFrame vazio ou None
        if df is None or df.empty:
            # Limpa tudo para mostrar a mensagem
            for widget in self.frame_tabela_container.winfo_children():
                widget.destroy()
            self.pt_widget = None # Remove referência
            
            ttk.Label(self.frame_tabela_container, 
                      text="Nenhum dado encontrado ou erro ao cruzar tabelas.", 
                      font=("Segoe UI", 12),
                      background="#F4F9F4").pack(pady=50)
            return

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

    def _perform_filtering(self, filter_data):
        """
        Lógica pesada de filtragem (executada em background).
        """
        try:
            # 1. Determina o DataFrame base
        # Se "Produto parado" estiver marcado, usamos o resultado de consulta_por_status
        # Caso contrário, usamos o df_master unificado
        
            df_base = self.controller.df_master
            
            if filter_data.get("condicoes", {}).get("Produto parado"):
                try:
                    print("Filtrando por Produtos Parados (Base Trocada)...")
                    resultado_status = consulta_por_status()
                    df_parados = resultado_status.get("df")
                    
                    if df_parados is not None and not df_parados.empty:
                        df_base = df_parados
                    else:
                    # Se não há produtos parados, começamos com vazio
                        df_base = pd.DataFrame(columns=df_base.columns if df_base is not None else None)
                except Exception as e:
                    print(f"Erro ao carregar produtos parados: {e}")
                    df_base = pd.DataFrame()

            if df_base is None or df_base.empty:
                self.after(0, self._on_filtering_complete, pd.DataFrame(), None)
                return

            print("Aplicando filtros adicionais:", filter_data)
            df_filtered = df_base.copy()

            cols_map = {_norm(c): c for c in df_filtered.columns}
            
            # Apelidos
            aliases_linha = {"grupo", "linha", "categoria"}
            aliases_sub = {"subgrupo", "sublinha", "subgruponivel1", "familia"}
            aliases_cod = {"codven", "codproduto", "referencia", "codigooriginal"}
            
            col_linha = next((cols_map[k] for k in cols_map if k in aliases_linha), None)
            col_sub = next((cols_map[k] for k in cols_map if k in aliases_sub), None)
            col_cod = next((cols_map[k] for k in cols_map if k in aliases_cod), None)
            if not col_cod:
                col_cod = next((cols_map[k] for k in cols_map if "cod" in k), None)

            if val_linha := filter_data.get("linha"):
                if col_linha:
                    df_filtered = df_filtered[df_filtered[col_linha].astype(str).str.strip() == val_linha.strip()]

            if val_sub := filter_data.get("sub_linha"):
                if col_sub:
                    df_filtered = df_filtered[df_filtered[col_sub].astype(str).str.strip() == val_sub.strip()]

            if val_cod := filter_data.get("codigo"):
                if col_cod:
                    df_filtered = df_filtered[df_filtered[col_cod].astype(str).str.contains(val_cod, case=False, na=False)]

            # --- ATUALIZA SUGESTÕES DE COMPRA ---
            df_sugestoes = None
            try:
            # Tenta pegar o período do filtro ou usa 4 como padrão
                periodo_str = filter_data.get("periodo", "4 Meses")
                match = re.search(r'\d+', str(periodo_str))
                periodo_val = int(match.group()) if match else 4
                
                linha_para_sugestao = val_linha if val_linha else None
                
                df_sugestoes = sugestao_compra(linha=linha_para_sugestao, periodo=periodo_val)
            except Exception as e:
                print(f"Erro ao atualizar sugestões de compra com filtro: {e}")

            # Agenda a atualização da UI na thread principal
            self.after(0, self._on_filtering_complete, df_filtered, df_sugestoes)

        except Exception as e:
            print(f"Erro crítico na thread de filtro: {e}")
            # Garante que o modal feche mesmo com erro
            self.after(0, self._on_filtering_complete, None, None)

    def _on_filtering_complete(self, df_filtered, df_sugestoes):
        """
        Atualiza a UI com os resultados e fecha o modal.
        """
        # 1. Fecha o Modal
        if hasattr(self, 'loading_modal') and self.loading_modal:
            self.loading_modal.destroy_modal()
            self.loading_modal = None

        # 2. Atualiza a Tabela
        if df_filtered is not None:
            self.render_dataframe_table(df_filtered)
        
        # 3. Atualiza Sugestões de Compra
        if df_sugestoes is not None:
             self.purchase_suggestions.update_cards(df_sugestoes)

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