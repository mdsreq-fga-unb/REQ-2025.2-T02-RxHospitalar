import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# --- IMPORTS DA BRANCH PLOT_CLIENTE_VENDEDOR ---
from app.views.plots.clientes_principais import TopClientesGrafico
from app.views.plots.vendedor_performance import ListaVendedores
from app.models.consulta_principais_clientes import consulta_principais_clientes
from app.models.consulta_performance import consulta_performance

# --- IMPORTS NOVOS PARA RESOLVER O PROBLEMA DO CÓDIGO ---
from app.models.consulta_por_codigo import consulta_por_codigo
from app.models.carregar_dados import _encontrar_coluna_cod_interno

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
        super().__init__(parent, style="Card.TFrame")
        
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
        self.charts_container = ttk.Frame(self, style="CardInner.TFrame")
        self.charts_container.pack(fill="both", expand=True, padx=15, pady=15)

        self.lbl_placeholder = ttk.Label(
            self.charts_container, 
            text="[ Selecione filtros para gerar gráficos ]",
            font=("Segoe UI", 12),
            foreground="#666666",
            background="#F4F9F4"
        )
        self.lbl_placeholder.pack(pady=50)

    def update_graphs(self, df_full, filter_data=None):
        if filter_data is None:
            filter_data = {}

        # 1. Limpeza
        for widget in self.charts_container.winfo_children():
            widget.destroy()

        if (df_full is None or df_full.empty) and not filter_data.get("vendedores"):
            ttk.Label(self.charts_container, 
                      text="Sem dados para os filtros selecionados.", 
                      background="#F4F9F4").pack(pady=20)
            return

        left_frame = ttk.Frame(self.charts_container, style="CardInner.TFrame")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_frame = ttk.Frame(self.charts_container, style="CardInner.TFrame")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # === CENÁRIO 1: PERFORMANCE DE VENDEDORES ===
        if filter_data.get("vendedores"):
            self.lbl_title.configure(text="Performance de Vendedores")
            self.mostrar_top_vendedores(container=left_frame)
            return

        # === CENÁRIO 2: FILTRO POR CÓDIGO (Produto Específico) ===
        codigo_produto = filter_data.get("codigo")
        if codigo_produto:
            self.lbl_title.configure(text=f"Análise do Produto: {codigo_produto}")
            
            # AQUI ESTÁ A MÁGICA: Passamos o filter_data, e o método cuida da conversão
            self.mostrar_top_clientes(filter_data, container=left_frame)
            
            fig_right = plot_sazonalidade(df_full, None)
            self._draw_figure(fig_right, right_frame)
            return

        # === CENÁRIO 3: VISÃO GERAL / LINHA / SUBLINHA ===
        linha_selecionada = filter_data.get("linha")
        sub_linha_selecionada = filter_data.get("sub_linha")
        
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

        fig_right = plot_sazonalidade(df_full, linha_selecionada)

        self._draw_figure(fig_left, left_frame)
        self._draw_figure(fig_right, right_frame)

    # -------------------------------------------------------------------------
    # MÉTODOS AUXILIARES DA BRANCH PLOT_CLIENTE_VENDEDOR
    # -------------------------------------------------------------------------
    def mostrar_top_clientes(self, filter_data, container):
        """Renderiza o componente TopClientesGrafico convertendo Original -> Interno se necessário"""
        cod_filtro = filter_data.get("codigo") # Este é o Original (ex: REF-123)
        if not cod_filtro:
            return

        # --- LÓGICA DE TRADUÇÃO: ORIGINAL -> INTERNO ---
        cod_para_busca = cod_filtro
        
        try:
            # 1. Busca os dados completos do produto usando o código original
            dados_produto = consulta_por_codigo(cod_filtro)
            df_row = dados_produto['df']
            
            # 2. Descobre qual é a coluna do código interno (ex: CODVEN, Cód Produto)
            col_interno_name = _encontrar_coluna_cod_interno(df_row.columns)
            
            if col_interno_name:
                # 3. Pega o valor real do código interno (ex: 1050)
                valor_interno = df_row.iloc[0][col_interno_name]
                cod_para_busca = str(valor_interno).strip().replace(".0", "")
                print(f"[GraphsFrame] Convertido Original '{cod_filtro}' -> Interno '{cod_para_busca}'")
            else:
                print("[GraphsFrame] Coluna interna não encontrada, tentando com original...")
        
        except Exception as e:
            print(f"[GraphsFrame] Aviso: Não foi possível converter código original para interno: {e}")
            # Se der erro, segue com o código original mesmo (vai que já era o interno)
            cod_para_busca = cod_filtro

        # --- CONSULTA E GERAÇÃO DO GRÁFICO ---
        try:
            # Agora passamos o código "traduzido" para a busca de vendas
            df_clientes = consulta_principais_clientes(codproduto=cod_para_busca, limite=5)
        except Exception as e:
            print(f"[GraphsFrame] Erro ao carregar principais clientes: {e}")
            return

        if df_clientes.empty:
            ttk.Label(container, text="Sem clientes registrados para este produto.", background="#F4F9F4").pack()
            return

        clientes = df_clientes["RAZAOSOCIAL"].tolist()
        frequencia = df_clientes["FREQUENCIA"].tolist()
        faturamento = df_clientes["TOTAL_QUANTIDADE"].tolist()
        media_mensal = df_clientes["MEDIA_MENSAL"].tolist()

        TopClientesGrafico(container, clientes, faturamento, frequencia, media_mensal)

    def mostrar_top_vendedores(self, container):
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
    # MÉTODOS AUXILIARES (DRAW & HOVER)
    # -------------------------------------------------------------------------
    def _draw_figure(self, fig, parent_frame):
        if fig:
            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            self._setup_hover(canvas, fig)

    def _setup_hover(self, canvas, fig):
        # ... (MANTER O CÓDIGO DE HOVER ORIGINAL AQUI) ...
        # (Copiei apenas a estrutura para não ficar gigante, mantenha o conteúdo do seu arquivo original)
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