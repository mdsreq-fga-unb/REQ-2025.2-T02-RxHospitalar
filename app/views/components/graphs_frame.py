import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Importa as funções de plotagem
from app.views.plots.dashboard_plots import (
    plot_geral_distribuicao_linhas,
    plot_linha_especifica,
    plot_sublinha_especifica,
    plot_produto_especifico,
    plot_sazonalidade 
)

class GraphsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame")
        
        style = ttk.Style()
        style.configure("CardInner.TFrame", background="#F4F9F4", borderwidth=0, relief="flat")

        # Cabeçalho
        self.header_frame = ttk.Frame(self, style="CardInner.TFrame")
        self.header_frame.pack(fill="x", padx=15, pady=(10, 0))

        self.lbl_title = ttk.Label(
            self.header_frame, 
            text="Análise Gráfica", 
            font=("Segoe UI", 12, "bold"),
            foreground="#333333",
            background="#F4F9F4" 
        )
        self.lbl_title.pack(anchor="w")
        
        ttk.Separator(self.header_frame, orient="horizontal").pack(fill="x", pady=(5, 0))

        # Container dos Gráficos
        self.charts_container = ttk.Frame(self, style="CardInner.TFrame")
        self.charts_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.left_chart_frame = ttk.Frame(self.charts_container, style="CardInner.TFrame")
        self.left_chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        self.right_chart_frame = ttk.Frame(self.charts_container, style="CardInner.TFrame")
        self.right_chart_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

    def update_graphs(self, df_full, filter_context=None):
        # Limpa gráficos anteriores
        for widget in self.left_chart_frame.winfo_children(): widget.destroy()
        for widget in self.right_chart_frame.winfo_children(): widget.destroy()

        if df_full is None or df_full.empty:
            return

        if filter_context is None: filter_context = {}

        # --- GRÁFICO 1: PIZZA (ESQUERDA) ---
        fig_left = None
        linha_selecionada = filter_context.get("linha")

        if filter_context.get("codigo"):
            fig_left = plot_produto_especifico(df_full, filter_context["codigo"])
            self.lbl_title.configure(text="Análise: Produto")
        elif filter_context.get("sub_linha"):
            fig_left = plot_sublinha_especifica(df_full, filter_context["sub_linha"])
            self.lbl_title.configure(text=f"Análise: {filter_context['sub_linha']}")
        elif linha_selecionada:
            fig_left = plot_linha_especifica(df_full, linha_selecionada)
            self.lbl_title.configure(text=f"Análise: {linha_selecionada}")
        else:
            fig_left = plot_geral_distribuicao_linhas(df_full)
            self.lbl_title.configure(text="Visão Geral")

        # --- GRÁFICO 2: SAZONALIDADE (DIREITA) ---
        fig_right = plot_sazonalidade(df_full, linha_selecionada)

        # Renderiza
        self._draw_figure(fig_left, self.left_chart_frame)
        self._draw_figure(fig_right, self.right_chart_frame)

    def _draw_figure(self, fig, parent_frame):
        if fig:
            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Ativa o hover
            self._setup_hover(canvas, fig)

    def _setup_hover(self, canvas, fig):
        """Gerencia os eventos de hover para Pizza e Linha"""
        
        # === CASO 1: GRÁFICO DE PIZZA (Interatividade no Texto Central) ===
        if hasattr(fig, 'my_wedges') and hasattr(fig, 'my_center_text'):
            def on_pie_hover(event):
                if event.inaxes == fig.axes[0]:
                    found = False
                    for i, w in enumerate(fig.my_wedges):
                        if w.contains_point([event.x, event.y]):
                            name = fig.my_names[i]
                            val = int(fig.my_values[i])
                            
                            # Atualiza texto central
                            fig.my_center_text.set_text(f"{name}\n{val}")
                            fig.my_center_text.set_fontweight('bold')
                            fig.my_center_text.set_color('#333')
                            found = True
                            break
                    
                    if not found:
                        # Restaura texto original
                        fig.my_center_text.set_text(fig.my_total_str)
                        fig.my_center_text.set_color('#555')
                        fig.my_center_text.set_fontweight('bold')
                    
                    canvas.draw_idle()

            canvas.mpl_connect("motion_notify_event", on_pie_hover)

        # === CASO 2: GRÁFICO DE LINHA (Interatividade com Tooltip) ===
        elif hasattr(fig, 'my_x') and hasattr(fig, 'my_annot'):
            def on_line_hover(event):
                ax = fig.get_axes()[0]
                # Verifica se o mouse está dentro da área do gráfico
                if event.inaxes == ax:
                    # Encontra o índice do mês mais próximo do mouse
                    # O eixo X é 1, 2, 3... O mouse retorna float (ex: 1.2). Arredondamos.
                    x_coord = event.xdata
                    if x_coord is not None:
                        idx = int(round(x_coord)) - 1 # Subtrai 1 pois lista começa em 0
                        
                        # Verifica se o índice é válido (0 a 11)
                        if 0 <= idx < len(fig.my_x):
                            # Se o mouse estiver muito longe do ponto X (ex: no meio entre jan e fev), não mostra
                            if abs(x_coord - (idx + 1)) < 0.5:
                                x_val = fig.my_x[idx]
                                y_val = fig.my_y[idx]
                                label_mes = fig.my_labels[idx]
                                
                                # Atualiza o balão
                                annot = fig.my_annot
                                annot.xy = (x_val, y_val) # Ponto onde a seta aponta
                                annot.set_text(f"{label_mes}: {int(y_val)}") # Texto
                                annot.set_visible(True)
                                canvas.draw_idle()
                                return

                # Se saiu do gráfico ou não achou ponto próximo, esconde o balão
                if fig.my_annot.get_visible():
                    fig.my_annot.set_visible(False)
                    canvas.draw_idle()

            canvas.mpl_connect("motion_notify_event", on_line_hover)