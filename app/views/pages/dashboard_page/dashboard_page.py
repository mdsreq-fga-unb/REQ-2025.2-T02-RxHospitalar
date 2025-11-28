import tkinter as tk
from tkinter import ttk
from pandastable import Table
import pandas as pd
import unicodedata
import re

from app.views.components.navbar import Header
from app.views.components.estoque_filters import EstoqueFilterFrame, setup_styles
# IMPORT ATUALIZADO:
from app.models.carregar_dados import carregar_dados_unificados 

def _norm(s):
    if not isinstance(s, str): return str(s)
    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w]+", " ", s).lower().strip()
    return s.replace(" ", "")

class DashboardView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
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

        self.content_area = ttk.Frame(self.body_frame)
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.title_label = ttk.Label(
            self.content_area,
            text="Planilha de dados",
            font=("Segoe UI", 24, "bold"),
            foreground="white",
            background="#1e1e1e"
        )
        self.title_label.pack(anchor="w", pady=(0, 20))

        # Container da Tabela
        self.frame_tabela_container = ttk.Frame(self.content_area, style="Card.TFrame")
        self.frame_tabela_container.pack(fill="both", expand=True)
        
        self.pt_widget = None

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        
        # LÓGICA ATUALIZADA:
        if not hasattr(self.controller, 'df_master') or \
           (isinstance(self.controller.df_master, pd.DataFrame) and self.controller.df_master.empty):
            
            print("Carregando e unificando dados...")
            # Chama a função que cruza as tabelas
            self.controller.df_master = carregar_dados_unificados()

        self.render_dataframe_table(self.controller.df_master)

    def render_dataframe_table(self, df):
        for widget in self.frame_tabela_container.winfo_children():
            widget.destroy()

        if df is None or df.empty:
            ttk.Label(self.frame_tabela_container, 
                      text="Nenhum dado encontrado ou erro ao cruzar tabelas.", 
                      font=("Segoe UI", 12),
                      background="#F4F9F4").pack(pady=50)
            return

        self.pt_widget = Table(self.frame_tabela_container, dataframe=df,
                               showtoolbar=True, showstatusbar=True)
        self.pt_widget.show()
        self.pt_widget.redraw()

    def apply_filters(self, filter_data):
        # A lógica de filtro permanece a mesma, pois o df_master agora contém todas as colunas
        df = self.controller.df_master
        if df is None or df.empty:
            return

        print("Aplicando filtros:", filter_data)
        df_filtered = df.copy()

        cols_map = {_norm(c): c for c in df_filtered.columns}
        
        # Apelidos para encontrar as colunas no DF unificado
        aliases_linha = {"grupo", "linha", "categoria"}
        aliases_sub = {"subgrupo", "sublinha", "subgruponivel1", "familia"}
        aliases_cod = {"codven", "codproduto", "referencia", "codigooriginal"}
        
        col_linha = next((cols_map[k] for k in cols_map if k in aliases_linha), None)
        col_sub = next((cols_map[k] for k in cols_map if k in aliases_sub), None)
        
        # Busca coluna de código (pode ter mudado com o merge)
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

        self.render_dataframe_table(df_filtered)