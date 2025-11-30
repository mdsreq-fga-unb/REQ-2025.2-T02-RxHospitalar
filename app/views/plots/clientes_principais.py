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

        self.faturamento_total = sum(self.faturamento)

        # Ordenar dados de forma decrescente
        dados = list(zip(self.clientes, self.quantidade, self.faturamento, self.frequencias))
        dados_ordenados = sorted(dados, key=lambda x: x[1], reverse=True)
        self.clientes, self.quantidade, self.faturamento, self.frequencias = zip(*dados_ordenados)

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
            self.clientes, 
            self.quantidade,
            color=cores,
            edgecolor="#01252A",
            linewidth=0.8,
            alpha=0.9,
            width=0.5
        )

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

        def update_annot(rect, quantidade, faturamento, freq):
            x = rect.get_x() + rect.get_width() / 2
            y = rect.get_height()

            self.annot.xy = (x, y)
            y_offset = max(self.quantidade) * 0.08
            self.annot.xyann = (x, y + y_offset)

            texto = (
                f"Quantidade: {quantidade}\n"
                f"Faturamento: R$ {faturamento:,.2f}\n"
                f"Frequência: {freq}"
            )
            texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")

            self.annot.set_text(texto)
            self.annot.set_position((x, y + max(self.quantidade) * 0.05))

        def hover(event):
            visivel = self.annot.get_visible()
            if event.inaxes == self.ax:
                for rect, quantidade, faturamento, freq in zip(
                    self.barras, self.quantidade, self.faturamento, self.frequencias
                ):
                    if rect.contains(event)[0]:
                        update_annot(rect, quantidade, faturamento, freq)
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



# main - cria tela e container, grafico é criado dentro do container

if __name__ == "__main__":
    root = tk.Tk()
    root.title("rx - Gráfico à Direita")
    root.geometry("1200x800")
    root.configure(bg="#FFFFFF")

    # Dados exemplo
    clientes = ["cliente 3", "cliente 1", "cliente 2", "cliente 4", "cliente 5"]
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