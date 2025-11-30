import tkinter as tk
from tkinter import ttk

class GraphsFrame(ttk.Frame):
    def __init__(self, parent):
        # Frame PRINCIPAL: Esse continua com Card.TFrame (para ter a borda externa bonita)
        super().__init__(parent, style="Card.TFrame")
        
        # Cria um estilo "interno" que só tem a cor de fundo, sem borda
        style = ttk.Style()
        # Copia a cor de fundo que você usa (#F4F9F4), mas tira a borda
        style.configure("CardInner.TFrame", background="#F4F9F4", borderwidth=0, relief="flat")

        # --- Cabeçalho (Título + Linha) ---
        self.header_frame = ttk.Frame(self, style="CardInner.TFrame")
        self.header_frame.pack(fill="x", padx=15, pady=(15, 0))

        self.lbl_title = ttk.Label(
            self.header_frame, 
            text="Dashboard",
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


        # Placeholder temporário
        self.lbl_placeholder = ttk.Label(
            self.charts_container, 
            text="[ Área reservada para os Gráficos ]",
            font=("Segoe UI", 12),
            foreground="#666666",
            background="#F4F9F4"
        )
        # ALTERADO: De .place() para .pack().
        # O pack faz com que o container "sinta" o tamanho do texto e cresça para caber ele.
        # O pady=50 garante que ele comece com uma altura razoável antes de ter gráficos.
        self.lbl_placeholder.pack(pady=50)

    def update_graphs(self, df):
        """
        Método que será chamado pelo DashboardView para desenhar/atualizar
        os gráficos com base nos dados (df).
        """
        # Limpa gráficos anteriores (se houver)
        for widget in self.charts_container.winfo_children():
            widget.destroy()
            
        # Apenas um aviso temporário (Simulando um gráfico)
        # Quando você colocar o Matplotlib aqui, o frame vai expandir para o tamanho da figura.
        ttk.Label(self.charts_container, 
                  text=f"Gráficos gerados com {len(df)} registros\n(O tamanho deste card se ajustará ao gráfico)", 
                  font=("Segoe UI", 10),
                  background="#F4F9F4").pack(pady=20)