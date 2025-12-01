import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# --- IMPORTS DA BRANCH PLOT_CLIENTE_VENDEDOR ---
from app.views.plots.clientes_principais import TopClientesGrafico
from app.views.plots.vendedor_performance import ListaVendedores
from app.models.consulta_principais_clientes import consulta_principais_clientes
from app.models.consulta_performance import consulta_performance

# --- IMPORTS DA BRANCH INTEGRA/SAZONALIDADE ---
from app.views.plots.dashboard_plots import (
    plot_geral_distribuicao_linhas,
    plot_linha_especifica,
    plot_sublinha_especifica,
    plot_produto_especifico,
    plot_sazonalidade 
)

class GraphsFrame(ttk.Frame):
    def __init__(self, parent):
        # Frame PRINCIPAL: Esse continua com Card.TFrame (para ter a borda externa bonita)
        super().__init__(parent, style="Card.TFrame")
        
        # Cria um estilo "interno" que só tem a cor de fundo, sem borda
        style = ttk.Style()
        style.configure("CardInner.TFrame", background="#F4F9F4", borderwidth=0, relief="flat")

        # --- Cabeçalho (Título + Linha) ---
        self.header_frame = ttk.Frame(self, style="CardInner.TFrame")
        self.header_frame.pack(fill="x", padx=15, pady=(15, 0))

        self.lbl_title = ttk.Label(
            self.header_frame, 
            text="Análise Gráfica",
            font=("Segoe UI", 16, "bold"), 
            foreground="#333333",
            background="#F4F9F4" 
        )
        self.lbl_title.pack(anchor="w")

        self.separator = ttk.Separator(self.header_frame, orient="horizontal")
        self.separator.pack(fill="x", pady=(5, 0))

        # --- Área de Conteúdo dos Gráficos ---
        # Container principal que segura tudo
        self.charts_container = ttk.Frame(self, style="CardInner.TFrame")
        self.charts_container.pack(fill="both", expand=True, padx=15, pady=15)

        # Placeholder inicial
        self.lbl_placeholder = ttk.Label(
            self.charts_container, 
            text="[ Selecione filtros para gerar gráficos ]",
            font=("Segoe UI", 12),
            foreground="#666666",
            background="#F4F9F4"
        )
        self.lbl_placeholder.pack(pady=50)

    def update_graphs(self, df_full, filter_data=None):
        """
        Método Mestre: Decide qual conjunto de gráficos mostrar baseado no filtro.
        Une funcionalidades de ambas as branches.
        """
        if filter_data is None:
            filter_data = {}

        # 1. Limpeza
        for widget in self.charts_container.winfo_children():
            widget.destroy()

        # Se não houver dados no DF e não for um filtro especial de vendedor (que busca do banco), sai.
        if (df_full is None or df_full.empty) and not filter_data.get("vendedores"):
            ttk.Label(self.charts_container, 
                      text="Sem dados para os filtros selecionados.", 
                      background="#F4F9F4").pack(pady=20)
            return

        # Prepara Frames Esquerda e Direita (Layout Padrão)
        left_frame = ttk.Frame(self.charts_container, style="CardInner.TFrame")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_frame = ttk.Frame(self.charts_container, style="CardInner.TFrame")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # === CENÁRIO 1: PERFORMANCE DE VENDEDORES (Prioridade Alta) ===
        if filter_data.get("vendedores"):
            self.lbl_title.configure(text="Performance de Vendedores")
            # Usa o left_frame para mostrar a lista
            self.mostrar_top_vendedores(container=left_frame)
            # O lado direito pode ficar vazio ou mostrar algo genérico
            return

        # === CENÁRIO 2: FILTRO POR CÓDIGO (Produto Específico) ===
        # Aqui fazemos o MERGE: Esquerda = Top Clientes (Plot), Direita = Sazonalidade (Integra)
        codigo_produto = filter_data.get("codigo")
        if codigo_produto:
            self.lbl_title.configure(text=f"Análise do Produto: {codigo_produto}")
            
            # Lado Esquerdo: Top Clientes (Lógica da branch plot_cliente_vendedor)
            self.mostrar_top_clientes(filter_data, container=left_frame)
            
            # Lado Direito: Sazonalidade/Vendas no tempo (Lógica da branch integra)
            # Nota: plot_produto_especifico retorna Pizza, mas plot_sazonalidade é melhor para produto único no tempo
            fig_right = plot_sazonalidade(df_full, None) # None pois o DF já está filtrado ou passamos contexto
            self._draw_figure(fig_right, right_frame)
            return

        # === CENÁRIO 3: VISÃO GERAL / LINHA / SUBLINHA (Padrão Integra) ===
        linha_selecionada = filter_data.get("linha")
        sub_linha_selecionada = filter_data.get("sub_linha")
        
        # Define Título e Gráfico da Esquerda (Pizza)
        fig_left = None
        if sub_linha_selecionada:
            self.lbl_title.configure(text=f"Análise: {sub_linha_selecionada}")
            fig_left = plot_sublinha_especifica(df_full, sub_linha_selecionada)
        elif linha_selecionada:
            self.lbl_title.configure(text=f"Análise: {linha_selecionada}")
            fig_left = plot_linha_especifica(df_full, linha_selecionada)
        else:
            self.lbl_title.configure(text="Visão Geral por Linhas")
            fig_left = plot_geral_distribuicao_linhas(df_full)

        # Gráfico da Direita (Sazonalidade)
        fig_right = plot_sazonalidade(df_full, linha_selecionada)

        # Renderiza Matplotlib
        self._draw_figure(fig_left, left_frame)
        self._draw_figure(fig_right, right_frame)

    # -------------------------------------------------------------------------
    # MÉTODOS AUXILIARES DA BRANCH PLOT_CLIENTE_VENDEDOR
    # -------------------------------------------------------------------------
    def mostrar_top_clientes(self, filter_data, container):
        """Renderiza o componente TopClientesGrafico dentro do container informado"""
        codproduto = filter_data.get("codigo")
        if not codproduto:
            return

        try:
            df_clientes = consulta_principais_clientes(codproduto=codproduto, limite=5)
        except Exception as e:
            print(f"[GraphsFrame] Erro ao carregar principais clientes: {e}")
            return

        if df_clientes.empty:
            ttk.Label(container, text="Sem clientes registrados.", background="#F4F9F4").pack()
            return

        clientes = df_clientes["RAZAOSOCIAL"].tolist()
        frequencia = df_clientes["FREQUENCIA"].tolist()
        faturamento = df_clientes["TOTAL_QUANTIDADE"].tolist()
        media_mensal = df_clientes["MEDIA_MENSAL"].tolist()

        # Instancia o componente visual no container
        TopClientesGrafico(container, clientes, faturamento, frequencia, media_mensal)

    def mostrar_top_vendedores(self, container):
        """Renderiza o componente ListaVendedores dentro do container informado"""
        try:
            df_perf = consulta_performance(limite=5)
        except Exception as e:
            print(f"[GraphsFrame] Erro ao carregar performance vendedores: {e}")
            return

        if df_perf.empty:
            ttk.Label(container, text="Sem dados de vendedores.", background="#F4F9F4").pack()
            return

        vendedores = df_perf["CODVENDEDOR"].tolist()
        faturamento = df_perf["VALOR"].tolist()

        ListaVendedores(container, vendedores, faturamento)

    # -------------------------------------------------------------------------
    # MÉTODOS AUXILIARES DA BRANCH INTEGRA (Matplotlib Helpers)
    # -------------------------------------------------------------------------
    def _draw_figure(self, fig, parent_frame):
        if fig:
            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            self._setup_hover(canvas, fig)

    def _setup_hover(self, canvas, fig):
        """Gerencia os eventos de hover para Pizza e Linha"""
        
        # === CASO 1: GRÁFICO DE PIZZA ===
        if hasattr(fig, 'my_wedges') and hasattr(fig, 'my_center_text'):
            def on_pie_hover(event):
                if event.inaxes == fig.axes[0]:
                    found = False
                    for i, w in enumerate(fig.my_wedges):
                        if w.contains_point([event.x, event.y]):
                            name = fig.my_names[i]
                            val = int(fig.my_values[i])
                            fig.my_center_text.set_text(f"{name}\n{val}")
                            fig.my_center_text.set_fontweight('bold')
                            fig.my_center_text.set_color('#333')
                            found = True
                            break
                    
                    if not found:
                        fig.my_center_text.set_text(fig.my_total_str)
                        fig.my_center_text.set_color('#555')
                        fig.my_center_text.set_fontweight('bold')
                    
                    canvas.draw_idle()

            canvas.mpl_connect("motion_notify_event", on_pie_hover)

        # === CASO 2: GRÁFICO DE LINHA ===
        elif hasattr(fig, 'my_x') and hasattr(fig, 'my_annot'):
            def on_line_hover(event):
                ax = fig.get_axes()[0]
                if event.inaxes == ax:
                    x_coord = event.xdata
                    if x_coord is not None:
                        idx = int(round(x_coord)) - 1
                        if 0 <= idx < len(fig.my_x):
                            if abs(x_coord - (idx + 1)) < 0.5:
                                x_val = fig.my_x[idx]
                                y_val = fig.my_y[idx]
                                label_mes = fig.my_labels[idx]
                                
                                annot = fig.my_annot
                                annot.xy = (x_val, y_val)
                                annot.set_text(f"{label_mes}: {int(y_val)}")
                                annot.set_visible(True)
                                canvas.draw_idle()
                                return

                if fig.my_annot.get_visible():
                    fig.my_annot.set_visible(False)
                    canvas.draw_idle()

            canvas.mpl_connect("motion_notify_event", on_line_hover)