import tkinter as tk
from tkinter import ttk
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.views.components.estoque_filters import EstoqueFilterFrame

from app.views.components.navbar import Header

from pandastable import Table

class DashboardView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # ===== Header =====
        self.header = Header(self, controller)
        self.header.pack(side="top", fill="x")
        ttk.Label(self, text="Dashboard", foreground="white").pack(padx=20, pady=20)

        self.frame_tabela_container = ttk.Frame(self)
        self.frame_tabela_container.pack(fill='both', expand=True, padx=20, pady=10)

        ttk.Label(self.frame_tabela_container, text="Aguardando importação de dados...").pack(pady=50)

    def render_dataframe_table(self, df):
        """Renderiza o DataFrame na área da tabela."""
        # Limpa container
        for widget in self.frame_tabela_container.winfo_children():
            widget.destroy()

        print("Carregamento concluído. Exibindo DataFrame...")

        if df is None or df.empty:
            ttk.Label(
                self.frame_tabela_container,
                text="Dados não disponíveis ou importação falhou.",
                foreground='red'
            ).pack(pady=50)
            return

        # Cria a tabela uma única vez
        pt = Table(
            self.frame_tabela_container,
            dataframe=df,
            showtoolbar=True,
            showstatusbar=True
        )

        # Apenas mostra (não use pack/grid depois de show se show já usou grid)
        pt.show()


        print("Tabela pandastable renderizada na DashboardView.")
        
        