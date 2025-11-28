import tkinter as tk
from tkinter import ttk

class ListaVendedores:
    def __init__(self, master, vendedores, quantidade, faturamento):
        self.master = master
        self.vendedores = vendedores
        self.quantidade = quantidade
        self.faturamento = faturamento
        
        self._construir_lista()
    
    def _construir_lista(self):
        # Ordenar dados de forma decrescente por quantidade
        dados = list(zip(self.vendedores, self.quantidade, self.faturamento))
        dados_ordenados = sorted(dados, key=lambda x: x[1], reverse=True)
        self.vendedores, self.quantidade, self.faturamento = zip(*dados_ordenados)
        
        # Título
        titulo = tk.Label(
            self.master, 
            text="Top 5 Vendedores", 
            font=("Arial", 16, "bold"),
            bg="#FFFFFF",
            fg="#01252A"
        )
        titulo.pack(pady=(0, 5))  

        # Frame da tabela
        lista_frame = tk.Frame(self.master, bg="#FFFFFF")
        lista_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        # Larguras menores e iguais (colunas mais estreitas)
        col0_w, col1_w, col2_w = 14, 10, 14

        # Cabeçalho (tudo centralizado)
        header_bg = "#0BC0AF"
        header_font = ("Arial", 11, "bold")

        tk.Label(
            lista_frame, text="Vendedor", font=header_font,
            bg=header_bg, fg="#FFFFFF", width=col0_w, anchor="center"
        ).grid(row=0, column=0, padx=(5, 3), pady=5, sticky="nsew")

        tk.Label(
            lista_frame, text="Quantidade", font=header_font,
            bg=header_bg, fg="#FFFFFF", width=col1_w, anchor="center"
        ).grid(row=0, column=1, padx=3, pady=5, sticky="nsew")

        tk.Label(
            lista_frame, text="Faturamento (R$)", font=header_font,
            bg=header_bg, fg="#FFFFFF", width=col2_w, anchor="center"
        ).grid(row=0, column=2, padx=(3, 5), pady=5, sticky="nsew")

        # Linhas da tabela
        texto_font = ("Arial", 10)

        for i, (vend, qtd, fat) in enumerate(
            zip(self.vendedores, self.quantidade, self.faturamento),
            start=1
        ):
            bg_color = "#ACADAD" if (i % 2 == 0) else "#FFFFFF"
            fat_formatado = f"{fat:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            tk.Label(
                lista_frame, text=vend, font=texto_font,
                bg=bg_color, fg="#3A3939", width=col0_w, anchor="center"
            ).grid(row=i, column=0, padx=(5, 3), pady=3, sticky="nsew")

            tk.Label(
                lista_frame, text=str(qtd), font=texto_font,
                bg=bg_color, fg="#3A3939", width=col1_w, anchor="center"
            ).grid(row=i, column=1, padx=3, pady=3, sticky="nsew")

            tk.Label(
                lista_frame, text=fat_formatado, font=texto_font,
                bg=bg_color, fg="#3A3939", width=col2_w, anchor="center"
            ).grid(row=i, column=2, padx=(3, 5), pady=3, sticky="nsew")

        # Deixar colunas “flexíveis” dentro do frame
        lista_frame.grid_columnconfigure(0, weight=1)
        lista_frame.grid_columnconfigure(1, weight=1)
        lista_frame.grid_columnconfigure(2, weight=1)


# main dados exemplo
if __name__ == "__main__":
    vendedores = ['V1', 'V2', 'V3', 'V4', 'V5']
    quantidade = [12, 9, 7, 15, 10]
    faturamento = [1200.50, 890.00, 760.75, 1500.00, 980.30]
    
    root = tk.Tk()
    root.title("rx")
    root.geometry("900x600")
    root.configure(bg="#FFFFFF")
    
    # Container centralizado
    container = tk.Frame(root, bg="#FFFFFF", width=500, height=300)
    container.place(relx=1.0, rely=0.0, anchor="ne")  #posicionado no topo à direita
    container.pack_propagate(False)

    app = ListaVendedores(container, vendedores, quantidade, faturamento)
    
    root.mainloop()