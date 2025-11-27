# Importações necessárias para criação da interface gráfica
import tkinter as tk
from tkinter import ttk

# Importação dos componentes personalizados da aplicação
from app.views.components.navbar import Header
from app.views.components.estoque_filters import EstoqueFilterFrame, setup_styles

class DashboardView(ttk.Frame):
    """
    Classe principal da view do Dashboard de Estoque.
    Herda de ttk.Frame e organiza a interface em header, sidebar com filtros e área de conteúdo.
    """
    def __init__(self, parent, controller):
        """
        Inicializa a view do Dashboard.
        
        Args:
            parent: Widget pai onde esta view será inserida
            controller: Controlador principal da aplicação (gerencia dados e navegação)
        """
        super().__init__(parent)
        self.controller = controller

        # Configura os estilos visuais (cores, fontes, etc.) para toda a aplicação
        setup_styles(self.controller)

        # Cria e posiciona o cabeçalho (header) no topo da tela
        self.header = Header(self, controller)
        self.header.pack(side="top", fill="x")

        # Cria o frame principal do corpo da aplicação (abaixo do header)
        self.body_frame = ttk.Frame(self)
        self.body_frame.pack(side="top", fill="both", expand=True)

        # Configura o layout em grid do body_frame:
        # - Coluna 0: sidebar fixa com largura mínima de 335px (weight=0 significa que não expande)
        # - Coluna 1: área de conteúdo que expande para preencher espaço restante (weight=1)
        # - Linha 0: ocupa toda a altura disponível (weight=1)
        self.body_frame.columnconfigure(0, weight=0, minsize=335)
        self.body_frame.columnconfigure(1, weight=1)
        self.body_frame.rowconfigure(0, weight=1)

        # Cria o container da sidebar (barra lateral esquerda) com estilo personalizado
        self.sidebar_container = ttk.Frame(self.body_frame, style="Sidebar.TFrame")
        self.sidebar_container.grid(row=0, column=0, sticky="nsew")
        
        # Cria o frame de filtros de estoque dentro da sidebar
        self.filters = EstoqueFilterFrame(self.sidebar_container)
        
        # Posiciona os filtros dentro da sidebar com padding (espaçamento interno)
        # pady=(85, 10) = 85px no topo, 10px embaixo
        self.filters.pack(fill="both", expand=True, padx=10, pady=(85, 10))

        # Cria a área de conteúdo principal (lado direito) onde ficará o gráfico
        self.content_area = ttk.Frame(self.body_frame)
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Cria e posiciona o título do dashboard
        self.title_label = ttk.Label(
            self.content_area,
            text="Dashboard de Estoque",
            font=("Segoe UI", 24, "bold"),
            foreground="white",
            background="#1e1e1e"
        )
        self.title_label.pack(anchor="w", pady=(0, 20))

        # Cria um placeholder (espaço reservado) para onde o gráfico será exibido
        self.graph_placeholder = ttk.Frame(self.content_area, style="Card.TFrame")
        self.graph_placeholder.pack(fill="both", expand=True)
        
        # Adiciona um texto temporário indicando onde o gráfico aparecerá
        ttk.Label(
            self.graph_placeholder,
            text="[Graph Area]",
            foreground="#343A40",
            background="#F4F9F4"
        ).pack(expand=True)

    def tkraise(self, aboveThis=None):
        """
        Sobrescreve o método tkraise para verificar atualizações de dados
        quando a view do dashboard é exibida (trazida para frente).
        
        Args:
            aboveThis: Widget opcional acima do qual esta view deve aparecer
        """
        # Chama o método original da classe pai para trazer a view para frente
        super().tkraise(aboveThis)
        
        # Verifica se há dados carregados no DataFrame mestre do controlador
        # e imprime informação de debug no console
        if not self.controller.df_master.empty:
            print(f"Dashboard Update: {len(self.controller.df_master)} rows available.")
            