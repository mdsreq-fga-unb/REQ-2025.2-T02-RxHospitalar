import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class TopClientesGrafico:
    def __init__(self, master, clientes, quantidade, faturamento, frequencias):
        self.master = master
        self.clientes = clientes
        self.quantidade = quantidade
        self.faturamento = faturamento
        self.frequencias = frequencias

        # Se não tiver dados, não tenta montar gráfico
        if not self.clientes or not self.quantidade:
            return
        
        self.faturamento_total = sum(self.faturamento)

        # Ordenar dados de forma decrescente
        dados = list(zip(self.clientes, self.quantidade, self.faturamento, self.frequencias))
        dados_ordenados = sorted(dados, key=lambda x: x[1], reverse=True)

        # NOVO: checa se ainda tem dados após o sort
        if not dados_ordenados:
            return

        self.clientes, self.quantidade, self.faturamento, self.frequencias = zip(*dados_ordenados)

         # Guarda nomes completos e cria labels truncados
        self.clientes_full = list(self.clientes)
        self.clientes_labels = [self._truncate_label(nome) for nome in self.clientes_full]

        # Bind para redimensionamento
        self.master.bind("<Configure>", self._on_resize)
        
        self._construir_grafico()

    def _construir_grafico(self):
        # Calcular tamanho baseado no container
        largura_px = self.master.winfo_width() or 500
        altura_px = self.master.winfo_height() or 300
        largura_inches = largura_px / 100
        altura_inches = altura_px / 100
        
        # Cria gráfico
        self.fig = Figure(figsize=(largura_inches, altura_inches), dpi=100, facecolor="#FFFFFF")
        self.ax = self.fig.add_subplot(111, facecolor="#E2E2E2")

        # Barras
        cores = ["#06373D", "#08262C", "#2D595C", "#114640", "#7B8B7C"]
        self.barras = self.ax.bar(
            range(len(self.clientes_labels)), 
            self.quantidade,
            color=cores,
            edgecolor="#01252A",
            linewidth=0.8,
            alpha=0.9,
            width=0.5
        )
        # Define os ticks do eixo X com labels truncados
        self.ax.set_xticks(range(len(self.clientes_labels)))
        self.ax.set_xticklabels(self.clientes_labels, rotation=0, fontsize=7)

        # Eixos
        self.ax.set_ylabel("Quantidade", fontsize=9, color="#3A3939", fontweight="bold")
        self.ax.set_title("Top 5 Clientes por Produto", fontsize=11, color="#01252A", fontweight="bold", pad=10)
        self.ax.set_ylim(0, max(self.quantidade) * 1.2)

        # Cores dos eixos e textos
        self.ax.spines['bottom'].set_color("#000000")
        self.ax.spines['bottom'].set_linewidth(0.5)
        self.ax.spines['left'].set_color("#000000")
        self.ax.spines['left'].set_linewidth(0.5)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.tick_params(colors="#3A3939", labelsize=7, width=0.5)
        
        # Grid
        self.ax.grid(True, axis='y', linestyle='--', alpha=0.3, color="#000000", linewidth=0.5)
        self.ax.set_axisbelow(True)

        # Faturamento total
        texto_total = f"Total faturado: R$ {self.faturamento_total:,.2f}"
        texto_total = texto_total.replace(",", "X").replace(".", ",").replace("X", ".")

        self.ax.text(
            0.95, 0.92, texto_total,
            transform=self.ax.transAxes,
            ha="right",
            va="top",
            fontsize=8,
            fontweight="bold",
            color="#01252A",
            bbox=dict(boxstyle="round,pad=0.5", fc="#FFFFFF", ec="#0BC0AF", linewidth=1.5, alpha=0.95)
        )

        # Tooltip - detalhes ao passar o mouse
        self.annot = self.ax.annotate(
            "",
            xy=(0, 0),
            xytext=(0, 0),
            textcoords="data",
            bbox=dict(boxstyle="round,pad=0.5", fc="#FFFFFF", ec="#01252A", linewidth=1, alpha=0.95),
            fontsize=7,
            color="#01252A",
            fontweight="normal",
            ha="center",
            va="bottom",
            clip_on=False
        )
        self.annot.set_visible(False)

        def update_annot(idx,rect, quantidade, faturamento, freq):
            x = rect.get_x() + rect.get_width() / 2
            y = rect.get_height()

            self.annot.xy = (x, y)
            
            
            nome_completo = self.clientes_full[idx]

            texto = (
                f"{nome_completo}\n"
                f"Quantidade: {quantidade}\n"
                f"Faturamento: R$ {faturamento:,.2f}\n"
                f"Frequência: {freq}"
            )
            texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")

            self.annot.set_text(texto)
            # --- Ajuste para não sair do gráfico ---
            # posição "ideal" acima da barra
            x_disp = x
            y_disp = y + max(self.quantidade) * 0.05
            self.annot.set_position((x_disp, y_disp))
            # ------ Cálculo do bbox e correções nas bordas ------
            self.fig.canvas.draw_idle()
            renderer = self.fig.canvas.get_renderer()

            bbox = self.annot.get_window_extent(renderer=renderer)   # bbox do tooltip em pixels
            ax_bbox = self.ax.get_window_extent(renderer=renderer)   # bbox do eixo em pixels

            # transformação: data -> pixels e inversa pixels -> data
            data_to_px = self.ax.transData
            px_to_data = data_to_px.inverted()

            # Ajusta esquerda
            if bbox.x0 < ax_bbox.x0:
                dx_px = ax_bbox.x0 - bbox.x0          # quanto precisa andar pra direita em pixels
                # converte esse deslocamento horizontal em coordenadas de dados
                x0_data, _ = px_to_data.transform((0, 0))
                x1_data, _ = px_to_data.transform((dx_px, 0))
                x_disp += (x1_data - x0_data)

            # Atualiza posição e recalcula bbox
            self.annot.set_position((x_disp, y_disp))
            bbox = self.annot.get_window_extent(renderer=renderer)

            # Ajusta direita
            if bbox.x1 > ax_bbox.x1:
                dx_px = bbox.x1 - ax_bbox.x1          # quanto passou pra direita
                x0_data, _ = px_to_data.transform((0, 0))
                x1_data, _ = px_to_data.transform((dx_px, 0))
                x_disp -= (x1_data - x0_data)

            # Atualiza posição com correção horizontal final
            self.annot.set_position((x_disp, y_disp))
            bbox = self.annot.get_window_extent(renderer=renderer)

            # Ajusta topo: se estourar em cima, joga pra baixo da barra
            if bbox.y1 > ax_bbox.y1:
                y_disp = y - max(self.quantidade) * 0.05
                self.annot.set_position((x_disp, y_disp))

            self.annot.set_position((x_disp, y_disp))

        def hover(event):
            visivel = self.annot.get_visible()
            if event.inaxes == self.ax:
                for idx, (rect, quantidade, faturamento, freq) in enumerate(
                    zip(self.barras, self.quantidade, self.faturamento, self.frequencias)
                ):
                    if rect.contains(event)[0]:
                        update_annot(idx,rect, quantidade, faturamento, freq)
                        self.annot.set_visible(True)
                        self.fig.canvas.draw_idle()
                        return

            if visivel:
                self.annot.set_visible(False)
                self.fig.canvas.draw_idle()

        self.fig.canvas.mpl_connect("motion_notify_event", hover)
        #controle das margens
        self.fig.subplots_adjust(left=0.12, right=0.95, top=0.90, bottom=0.12)

        # Criar canvas
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()
            
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _on_resize(self, event):
        """Callback para redimensionar o gráfico quando o container muda de tamanho"""
        if event.widget == self.master and event.width > 100 and event.height > 100:
            self._construir_grafico()

    def get_widget(self):
        """Retorna o widget do canvas"""
        return self.canvas.get_tk_widget()

    def _truncate_label(self, text, max_len=12):
        """
        Corta o texto se for maior que max_len e adiciona '...'.
        Ex: 'Cliente Muito Grande' -> 'Cliente Mui...'
        """
        text = str(text)
        if len(text) <= max_len:
            return text
        return text[:max_len - 3] + "..."

# main - cria tela e container, grafico é criado dentro do container

if __name__ == "__main__":
    root = tk.Tk()
    root.title("rx - Gráfico à Direita")
    root.geometry("1200x800")
    root.configure(bg="#FFFFFF")

    # Dados exemplo
    clientes = ["cliente 3aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "cliente 1aaaaaaaaaaaaaa", "cliente 2", "cliente 4", "cliente aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa5"]
    quantidade = [1100, 1020, 950, 890, 789]
    faturamento = [9000, 7000, 5000, 3000, 2500]
    frequencias = [10, 8, 7, 5, 3]

    # Container principal
    container = tk.Frame(root, bg="#F5F5F5", width=532, height=300) #tamanho do container
    container.place(relx=0.5, rely=0.5, anchor="center") #aqui muda a posição do container
    container.pack_propagate(False) #tamanho fixo

    # Criar gráfico no frame interno
    grafico = TopClientesGrafico(container, clientes, quantidade, faturamento, frequencias)

    root.mainloop()