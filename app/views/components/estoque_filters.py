import tkinter as tk
from tkinter import ttk

class EstoqueFilterFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.configure(style="Card.TFrame")

        # Título
        ttk.Label(self, text="Estoque", style="Title.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 4))
        ttk.Label(self, text="Filtros", style="Subtitle.TLabel").grid(row=1, column=0, sticky="w")

        ttk.Separator(self, orient="horizontal").grid(row=2, column=0, sticky="ew", pady=6)

        # Seleção de produtos
        ttk.Label(self, text="Produto:").grid(row=3, column=0, sticky="w")
        ttk.Label(self, text="Linha:").grid(row=4, column=0, sticky="w")
        self.linha_var = tk.StringVar()
        ttk.Combobox(self, textvariable=self.linha_var, values=["Linha A", "Linha B"], state="readonly").grid(row=5, column=0, sticky="ew")

        ttk.Label(self, text="Sub Linha:").grid(row=6, column=0, sticky="w")
        self.sub_linha_var = tk.StringVar()
        ttk.Combobox(self, textvariable=self.sub_linha_var, values=["Sub 1", "Sub 2"], state="readonly").grid(row=7, column=0, sticky="ew")

        ttk.Label(self, text="Código:").grid(row=8, column=0, sticky="w")
        self.codigo_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.codigo_var).grid(row=9, column=0, sticky="ew")

        # Período
        ttk.Label(self, text="Período:").grid(row=10, column=0, sticky="w", pady=(10, 0))
        period_frame = ttk.Frame(self)
        period_frame.grid(row=11, column=0, sticky="w")
        self.period_var = tk.StringVar(value="4 Meses")
        for p in ["4 Meses", "8 Meses", "Todo Período"]:
            ttk.Radiobutton(period_frame, text=p, variable=self.period_var, value=p).pack(side="left", padx=2)

        ttk.Separator(self, orient="horizontal").grid(row=12, column=0, sticky="ew", pady=6)

        # Condição
        ttk.Label(self, text="Condição:").grid(row=13, column=0, sticky="w")
        self.condicoes = {
            "Estoque crítico": tk.BooleanVar(),
            "Baixo estoque": tk.BooleanVar(),
            "Produto parado": tk.BooleanVar()
        }
        for i, (label, var) in enumerate(self.condicoes.items(), start=14):
            ttk.Checkbutton(self, text=label, variable=var).grid(row=i, column=0, sticky="w")

        ttk.Separator(self, orient="horizontal").grid(row=17, column=0, sticky="ew", pady=6)

        # Recomendações
        ttk.Label(self, text="Recomendações:").grid(row=18, column=0, sticky="w")
        self.sugestao_var = tk.BooleanVar()
        ttk.Checkbutton(self, text="Sugestão de compra", variable=self.sugestao_var).grid(row=19, column=0, sticky="w")

        # Botão de filtro
        ttk.Button(self, text="Filtrar", command=self.filtrar).grid(row=20, column=0, sticky="ew", pady=(10, 0))

    def filtrar(self):
        # Exemplo de ação: imprimir todos os filtros
        print({
            "linha": self.linha_var.get(),
            "sub_linha": self.sub_linha_var.get(),
            "codigo": self.codigo_var.get(),
            "periodo": self.period_var.get(),
            "condicoes": {k: v.get() for k, v in self.condicoes.items()},
            "sugestao_compra": self.sugestao_var.get(),
        })


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Estoque Filtros")
    root.geometry("300x600")

    # Estilização básica
    style = ttk.Style()
    style.configure("Card.TFrame", background="#f4f9f4")
    style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))
    style.configure("Subtitle.TLabel", font=("Segoe UI", 11))

    frame = EstoqueFilterFrame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    root.mainloop()