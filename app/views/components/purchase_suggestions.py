import tkinter as tk
from tkinter import ttk

class PurchaseSuggestions(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame")
        
        # Title
        self.title_label = ttk.Label(
            self, 
            text="Sugestões de Compra", 
            font=("Segoe UI", 16, "bold"),
            foreground="#343A40",
            background="#F4F9F4"
        )
        self.title_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Separator
        separator = ttk.Separator(self, orient="horizontal")
        separator.pack(fill="x", padx=20, pady=(0, 20))

        self.title_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Scrollable Container
        self.scroll_container = ttk.Frame(self, style="Card.TFrame")
        self.scroll_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Canvas for horizontal scrolling
        self.canvas = tk.Canvas(
            self.scroll_container, 
            height=160, 
            background="#F4F9F4", 
            highlightthickness=0
        )

        self.title_label.pack(anchor="w", padx=20, pady=(20, 10))
        self.scrollbar = ttk.Scrollbar(
            self.scroll_container, 
            orient="horizontal", 
            command=self.canvas.xview
        )
        
        self.canvas.pack(side="top", fill="x", expand=True)
        self.scrollbar.pack(side="bottom", fill="x")
        
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        
        # Inner frame for cards
        self.cards_frame = ttk.Frame(self.canvas, style="Card.TFrame")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")
        
        self.cards_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Mousewheel scrolling (Horizontal)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.cards_frame.bind("<MouseWheel>", self._on_mousewheel)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        # Ensure height matches to avoid vertical scrolling issues if content is smaller
        self.canvas.itemconfig(self.canvas_window, height=event.height)

    def _on_mousewheel(self, event):
        # Shift + Scroll for horizontal on some systems, or just scroll
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")

    def update_cards(self, df_suggestions):
        # Clear existing cards
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
            
        if df_suggestions is None or df_suggestions.empty:
            ttk.Label(
                self.cards_frame, 
                text="Nenhuma sugestão de compra encontrada.",
                background="#F4F9F4",
                foreground="#5D8569",
                font=("Segoe UI", 12)
            ).pack(padx=20, pady=20)
            return
import tkinter as tk
from tkinter import ttk

class PurchaseSuggestions(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame")
        
        # Title
        self.title_label = ttk.Label(
            self, 
            text="Sugestões de Compra", 
            font=("Segoe UI", 16, "bold"),
            foreground="#343A40",
            background="#F4F9F4"
        )
        self.title_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Separator
        separator = ttk.Separator(self, orient="horizontal")
        separator.pack(fill="x", padx=20, pady=(0, 20))

        self.title_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Scrollable Container
        self.scroll_container = ttk.Frame(self, style="Card.TFrame")
        self.scroll_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Canvas for horizontal scrolling
        self.canvas = tk.Canvas(
            self.scroll_container, 
            height=160, 
            background="#F4F9F4", 
            highlightthickness=0
        )

        self.title_label.pack(anchor="w", padx=20, pady=(20, 10))
        self.scrollbar = ttk.Scrollbar(
            self.scroll_container, 
            orient="horizontal", 
            command=self.canvas.xview
        )
        
        self.canvas.pack(side="top", fill="x", expand=True)
        self.scrollbar.pack(side="bottom", fill="x")
        
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        
        # Inner frame for cards
        self.cards_frame = ttk.Frame(self.canvas, style="Card.TFrame")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")
        
        self.cards_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Mousewheel scrolling (Horizontal)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.cards_frame.bind("<MouseWheel>", self._on_mousewheel)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        # Ensure height matches to avoid vertical scrolling issues if content is smaller
        self.canvas.itemconfig(self.canvas_window, height=event.height)

    def _on_mousewheel(self, event):
        # Shift + Scroll for horizontal on some systems, or just scroll
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")

    def _create_card(self, row):
        # Card Container
        card = tk.Frame(
            self.cards_frame, 
            bg="#E8F5E9", 
            relief="solid",
            bd=1, 
            width=280,
            height=120
        )
        card.pack(side="left", padx=10, pady=5)
        card.pack_propagate(False) # Fixed size
        
        # Icon
        icon_label = tk.Label(
            card, 
            text="📦", 
            font=("Segoe UI", 24), 
            bg="#E8F5E9", 
            fg="#2E7D32"
        )
        icon_label.place(relx=0.15, rely=0.5, anchor="center")
        
        # Info Container (using place for precise positioning)
        
        # Product Name
        # Prioritize Description, fallback to CODORIGINAL
        product_name = row.get("Descrição", "")
        if not product_name or str(product_name).lower() == "nan":
            product_name = row.get("CODORIGINAL", "Produto")
        
        tk.Label(
            card, 
            text=str(product_name), 
            font=("Segoe UI", 10, "bold"), 
            bg="#E8F5E9", 
            fg="#1B5E20",
            wraplength=190,
            justify="left"
        ).place(x=70, y=10)
        
        # Product Code
        cod_original = row.get("CODORIGINAL", "")
        tk.Label(
            card, 
            text=f"Cód: {cod_original}", 
            font=("Segoe UI", 9), 
            bg="#E8F5E9", 
            fg="#5D8569"
        ).place(x=70, y=40)

        # Suggestion Value
        sugestao = row.get("SUGESTAO_COMPRA", 0)
        tk.Label(
            card, 
            text=f"Comprar: {int(sugestao)} un", 
            font=("Segoe UI", 12, "bold"), 
            bg="#E8F5E9", 
            fg="#388E3C"
        ).place(x=70, y=80)

    def update_cards(self, df_suggestions):
        # Clear existing cards
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
            
        if df_suggestions is None or df_suggestions.empty:
            ttk.Label(
                self.cards_frame, 
                text="Nenhuma sugestão de compra encontrada.",
                background="#F4F9F4",
                foreground="#5D8569",
                font=("Segoe UI", 12)
            ).pack(padx=20, pady=20)
            return

        # Filter only rows with SUGESTAO_COMPRA > 0
        # if "SUGESTAO_COMPRA" in df_suggestions.columns:
        #     df_suggestions = df_suggestions[df_suggestions["SUGESTAO_COMPRA"] > 0]

        # Create a card for each suggestion
        for _, row in df_suggestions.iterrows():
            self._create_card(row)