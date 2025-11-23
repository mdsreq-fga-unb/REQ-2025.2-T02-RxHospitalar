import tkinter as tk
from tkinter import ttk
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.views.components.estoque_filters import EstoqueFilterFrame

from app.views.components.navbar import Header

from pandastable import Table

class DashboardView(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        # --- Configuração do Layout GRID Principal ---
        # A DashboardView terá 3 linhas principais e 1 coluna
        self.grid_rowconfigure(0, weight=1) # Linha 0 (navbar) - Expande um pouco
        self.grid_rowconfigure(1, weight=0) # Linha 1 (cardsframe_cards) - Não expande verticalmente
        self.grid_rowconfigure(2, weight=1) # Linha 2 (Gráficos) - Expande um pouco
        self.grid_rowconfigure(3, weight=4) # Linha 3 (Tabela) - Expande mais
        self.grid_columnconfigure(0, weight=1) # Coluna 0 (Principal) - Expande horizontalmente
        # ---------------------------------------------

        # INSTANCIANDO E POSICIONANDO O HEADER NO GRID
        self.navbar = Header(self, controller=self.controller)
        self.navbar.grid(row=0, column=0, sticky="nsew") # sticky="ew" garante que preencha toda a largura
        
        # # LINHA 1: Cards ---
        # self.frame_cards = ttk.Frame(self, padding="10")
        # self.frame_cards.grid(row=1, column=0, sticky="ew") # sticky="ew" garante que preencha a largura
        # self.setup_kpi_cards()
        
        # # ---  LINHA 2: Gráfico Principal ---
        # self.frame_chart = ttk.Frame(self, padding="10", relief="groove", borderwidth=1)
        # self.frame_chart.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        # ttk.Label(self.frame_chart, text="[Placeholder: Gráfico de Movimentação/Estoque]").pack(expand=True)
        
        # --- LINHA 3: Tabela de Dados (Pandastable Container) ---
        self.frame_tabela_container = ttk.Frame(self, padding="10")
        self.frame_tabela_container.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        
        # Placeholder inicial
        self.tabela_placeholder = ttk.Label(self.frame_tabela_container, text="Aguardando importação de dados para exibir a planilha...")
        self.tabela_placeholder.grid(row=0, column=0, sticky='nsew', padx=50, pady=50)

    # def setup_kpi_cards(self):
    #     """Cria e organiza os mini-cards de cardsframe_cards (Exemplo)."""
        
    #     # Usamos o 'pack' dentro do frame_cards para organizá-los horizontalmente (lado a lado)
        
    #     kpi_data = [
    #         ("Estoque Total", "12.500 Unid."),
    #         ("Produtos Críticos", "25 Itens"),
    #         ("Última Atualização", "Carregando...")
    #     ]
        
    #     for titulo, valor in kpi_data:
    #         # Container para cada card
    #         card = ttk.Frame(self.frame_cards, relief="raised", padding="10")
    #         card.pack(side="left", padx=15, fill="x", expand=True) # side="left" coloca lado a lado

    #         ttk.Label(card, text=titulo, font=('Helvetica', 10)).pack(anchor='nw')
            
    #         # Adicionamos um ID para que possamos atualizar dinamicamente o valor (ex: o timestamp de atualização)
    #         lbl_valor = ttk.Label(card, text=valor, font=('Helvetica', 16, 'bold'))
    #         lbl_valor.pack(anchor='sw')
            
    #         if titulo == "Última Atualização":
    #             self.lbl_ultima_atualizacao = lbl_valor # Guarda a referência para atualizar depois

    def render_dataframe_table(self, df):
        """
        Método chamado pelo AppController para exibir o DataFrame (pandastable).
        """
        
        # 1. Limpa o container antes de renderizar a nova tabela
        for widget in self.frame_tabela_container.winfo_children():
            widget.destroy()

        if df.empty:
            ttk.Label(self.frame_tabela_container, 
                      text="Dados não disponíveis ou importação falhou.", 
                      foreground='red').pack(pady=50)
            return

        # 2. Cria e exibe o Widget Table (pandastable)
        pt = Table(self.frame_tabela_container, dataframe=df,
                   showtoolbar=True,
                   showstatusbar=True,
                   showscrolly=True,  # Mostra a rolagem vertical (Y)
                   showscrollx=True,
                   )
        
        # Força o re-cálculo das dimensões e dos parâmetros de visualização
        pt.redraw() 

        # O widget Table preenche todo o container
        pt.grid(row=0, column=0, sticky='nsew')
        pt.show()
        
        # # 3. Atualiza o KPI de última atualização (se o Controller definiu)
        # if hasattr(self.controller, 'last_update_time') and self.controller.last_update_time:
        #      time_str = self.controller.last_update_time.strftime("%d/%m/%Y %H:%M")
        #      self.lbl_ultima_atualizacao.config(text=time_str)