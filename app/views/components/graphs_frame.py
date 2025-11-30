import tkinter as tk
from tkinter import ttk
from app.views.plots.clientes_principais import TopClientesGrafico
from app.views.plots.vendedor_performance import ListaVendedores
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

    def update_graphs(self, df, filter_data=None):
        """
        Método que será chamado pelo DashboardView para desenhar/atualizar
        os gráficos com base nos dados (df).
        """
        if filter_data is None:
            filter_data = {}
        # Limpa gráficos anteriores (se houver)
        for widget in self.charts_container.winfo_children():
            widget.destroy()

        # Verifica se deve mostrar gráficos baseado nos checkboxes marcados
        tem_clientes = filter_data.get("clientes")
        tem_vendedores = filter_data.get("vendedores")

        # Decide se mostra os gráficos ou placeholder(tirar placeholder quando hover gráficos fixos)
        if tem_clientes or tem_vendedores:   
            if tem_clientes:
                self.mostrar_top_clientes()
            if tem_vendedores:
                self.mostrar_top_vendedores()
        else:
            # Nenhum filtro: mostra placeholder
            ttk.Label(self.charts_container, 
                    text=f"Gráficos gerados com {len(df)} registros\n(O tamanho deste card se ajustará ao gráfico)", 
                    font=("Segoe UI", 10),
                    background="#F4F9F4").pack(pady=20)
                    

    def mostrar_top_clientes(self,df=None):
        client_frame = ttk.Frame(self.charts_container,style="CardInner.TFrame", width=532, height=320)
        client_frame.pack(side="left", expand=True, padx=10)
        client_frame.pack_propagate(False)

        # Dados de exemplo
        clientes = ["cliente 3", "cliente 1", "cliente 2", "cliente 4", "cliente 5"]
        quantidade = [1100, 1020, 950, 890, 789]
        faturamento = [9000, 7000, 5000, 3000, 2500]
        frequencias = [10, 8, 7, 5, 3]

        TopClientesGrafico(client_frame, clientes, quantidade, faturamento, frequencias)

    def mostrar_top_vendedores(self,df=None):
        vendor_frame = ttk.Frame(self.charts_container,style="CardInner.TFrame", width=500, height=250)
        vendor_frame.pack(side="left", expand=True, padx=10)
        vendor_frame.pack_propagate(False)

        # Dados de exemplo
        vendedores = ['V1', 'V2', 'V3', 'V4', 'V5']
        quantidade = [12, 9, 7, 15, 10]
        faturamento = [1200.50, 890.00, 760.75, 1500.00, 980.30]

        ListaVendedores(vendor_frame, vendedores, quantidade, faturamento)
