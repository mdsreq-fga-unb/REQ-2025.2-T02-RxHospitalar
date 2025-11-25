import tkinter as tk
from tkinter import ttk

from matplotlib import style

# Configuração de Cores, Estilos e Constantes 
# Cores da imagem do Figma (aproximações)
COLOR_BACKGROUND = "#FFFFFF" 
COLOR_CARD_BG = "#F4F9F4" 
COLOR_BORDER = "#B8D4C0" 
COLOR_TEXT = "#343A40" 
COLOR_INPUT_BG = "#E8F0E8"
COLOR_BUTTON_BG = "#B8D4C0" 
COLOR_BUTTON_ACTIVE_BG = "#A0C0A8"
COLOR_CHECKED_SOLID = "#52805D" # Cor do checkbox
# Cor de destaque para o Hover (Condição e Recomendações)
COLOR_TEXT_HOVER = "#52805D" 

# Constantes de Placeholders
PLACEHOLDER_LINHA = "Selecione uma Linha"
PLACEHOLDER_SUB_LINHA = "Selecione uma Sub Linha"
PLACEHOLDER_CODIGO = "Insira um código"
PLACEHOLDER_PERIOD = "Opções"

def setup_styles(root):
    """Configura os estilos TTK para simular o visual do Figma."""
    style = ttk.Style(root)
    style.theme_use("clam") 

    # 2. Estilo da Fonte e Rótulos (Background definido para a cor do Card)
    style.configure(".", font=("Segoe UI", 10), foreground=COLOR_TEXT, background=COLOR_CARD_BG)
    style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), foreground=COLOR_TEXT, background=COLOR_CARD_BG)
    style.configure("Subtitle.TLabel", font=("Segoe UI", 11), foreground=COLOR_TEXT, background=COLOR_CARD_BG)
    style.configure("Header.TLabel", font=("Segoe UI", 10, "bold"), foreground=COLOR_TEXT, background=COLOR_CARD_BG)

    # 3. Estilo dos Cards 
    style.configure("Card.TFrame", background=COLOR_CARD_BG, borderwidth=1, relief="solid", bordercolor=COLOR_BORDER)
    style.map("Card.TFrame", bordercolor=[('focus', COLOR_BORDER)])

    # 4. Estilo dos Inputs 
    style.configure("TCombobox", fieldbackground=COLOR_INPUT_BG, background=COLOR_INPUT_BG, bordercolor=COLOR_BORDER, borderwidth=1, relief="solid", padding=[5, 2])
    style.map("TCombobox", 
              fieldbackground=[('readonly', COLOR_INPUT_BG), ('!disabled', COLOR_INPUT_BG)],
              # Define que a cor de fundo da seleção (selectbackground) será IGUAL ao fundo normal
              selectbackground=[('readonly', COLOR_INPUT_BG), ('focus', COLOR_INPUT_BG), ('!focus', COLOR_INPUT_BG)],
              # Define que a cor do texto selecionado (selectforeground) será a cor normal (e não branco)
              selectforeground=[('readonly', COLOR_TEXT), ('focus', COLOR_TEXT), ('!focus', COLOR_TEXT)])

    style.configure("TEntry", fieldbackground=COLOR_INPUT_BG, bordercolor=COLOR_BORDER, borderwidth=1, relief="solid", padding=[5, 2])

    # 5. Estilo dos Radiobuttons de Período
    style.configure("Period.TRadiobutton", background=COLOR_CARD_BG, foreground=COLOR_TEXT, relief="flat", padding=[2, 2])
    style.map("Period.TRadiobutton",
              background=[('selected', COLOR_BUTTON_BG), ('active', COLOR_BUTTON_ACTIVE_BG), ('!selected', COLOR_CARD_BG)],
              foreground=[('selected', COLOR_TEXT)])
    
    style.configure("PeriodButton.TFrame", background=COLOR_CARD_BG)

    # 6. Estilo do Combobox de Período
    # --- ESTILO NORMAL (Fundo Claro) ---
    style.configure("Period.TCombobox", fieldbackground=COLOR_CARD_BG, background=COLOR_CARD_BG, bordercolor=COLOR_BUTTON_BG, borderwidth=1, relief="solid", padding=[2, 2])
    style.map("Period.TCombobox", 
              fieldbackground=[('readonly', COLOR_CARD_BG), ('!disabled', COLOR_CARD_BG)],
              bordercolor=[('readonly', COLOR_BUTTON_BG), ('!disabled', COLOR_BUTTON_BG)],
              selectbackground=[('readonly', COLOR_CARD_BG)], 
              selectforeground=[('readonly', COLOR_TEXT)])     

    # --- ESTILO ATIVO (Fundo Verde) ---
    # Criamos um estilo novo que herda do Combobox, mas com fundo verde
    style.configure("Active.Period.TCombobox", 
                    fieldbackground=COLOR_BUTTON_BG, 
                    background=COLOR_BUTTON_BG,      
                    bordercolor=COLOR_BUTTON_BG, 
                    borderwidth=1, 
                    relief="solid", 
                    padding=[2, 2])
    
    # Mapeamento para garantir que fique verde mesmo quando focado/selecionado
    style.map("Active.Period.TCombobox", 
              fieldbackground=[('readonly', COLOR_BUTTON_BG), ('!disabled', COLOR_BUTTON_BG)],
              bordercolor=[('readonly', COLOR_BUTTON_BG), ('!disabled', COLOR_BUTTON_BG)],
              selectbackground=[('readonly', COLOR_BUTTON_BG)], 
              selectforeground=[('readonly', COLOR_TEXT)])     

    # 7. Estilo dos Checkbuttons (Visual Sólido)
    style.configure("TCheckbutton", 
                    background=COLOR_CARD_BG, 
                    foreground=COLOR_TEXT, 
                    indicatorrelief="solid", 
                    indicatorforeground=COLOR_BORDER,
                    indicatorsize=11) 
    
    style.map("TCheckbutton", 
             indicatorbackground=[('selected', COLOR_CHECKED_SOLID), ('!selected', COLOR_CARD_BG)],
             indicatorforeground=[('selected', COLOR_CHECKED_SOLID), ('!selected', COLOR_BORDER)],
             indicatorcolor=[('selected', COLOR_CHECKED_SOLID), ('!selected', COLOR_BORDER)])

    # 8. Estilo do Botão "Filtrar"
    style.configure("Filter.TButton", background=COLOR_BUTTON_BG, foreground=COLOR_TEXT, font=("Segoe UI", 11, "bold"), borderwidth=0, relief="flat", padding=[10, 5])
    style.map("Filter.TButton", background=[('active', COLOR_BUTTON_ACTIVE_BG), ('!active', COLOR_BUTTON_BG)])


class EstoqueFilterFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=0, style="PeriodButton.TFrame")
        self.columnconfigure(0, weight=1)

        # --- Card Principal de Filtros ---
        self.filter_card = ttk.Frame(self, padding=20, style="Card.TFrame")
        self.filter_card.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 10))
        self.filter_card.columnconfigure(0, weight=1)

        # Título
        ttk.Label(self.filter_card, text="Estoque", style="Title.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 0))
        ttk.Label(self.filter_card, text="Filtros", style="Subtitle.TLabel").grid(row=1, column=0, sticky="w", pady=(0, 10))
        
        # --- Seleção de Produtos ---
        # Linha
        ttk.Label(self.filter_card, text="Linha:", style="Header.TLabel").grid(row=2, column=0, sticky="w", pady=(5, 0))
        self.linha_var = tk.StringVar(value=PLACEHOLDER_LINHA) 
        self.linha_values = [PLACEHOLDER_LINHA, "Linha A", "Linha B", "Linha C"] 
        self.linha_combo = ttk.Combobox(self.filter_card, textvariable=self.linha_var, values=self.linha_values, state="readonly")
        self.linha_combo.grid(row=3, column=0, sticky="ew", pady=(0, 5))
        self.set_placeholder(self.linha_combo, PLACEHOLDER_LINHA)

        # Sub Linha
        ttk.Label(self.filter_card, text="Sub Linha:", style="Header.TLabel").grid(row=4, column=0, sticky="w", pady=(5, 0))
        self.sub_linha_var = tk.StringVar(value=PLACEHOLDER_SUB_LINHA) 
        self.sub_linha_values = [PLACEHOLDER_SUB_LINHA, "Sub 1", "Sub 2", "Sub 3"] 
        self.sub_linha_combo = ttk.Combobox(self.filter_card, textvariable=self.sub_linha_var, values=self.sub_linha_values, state="readonly")
        self.sub_linha_combo.grid(row=5, column=0, sticky="ew", pady=(0, 5))
        self.set_placeholder(self.sub_linha_combo, PLACEHOLDER_SUB_LINHA)

        # Código (Com Placeholder)
        ttk.Label(self.filter_card, text="Código:", style="Header.TLabel").grid(row=6, column=0, sticky="w", pady=(5, 0))
        self.codigo_var = tk.StringVar()
        self.codigo_entry = ttk.Entry(self.filter_card, textvariable=self.codigo_var, style="TEntry")
        self.codigo_entry.grid(row=7, column=0, sticky="ew", pady=(0, 10))
        self.add_placeholder(self.codigo_entry, PLACEHOLDER_CODIGO)

        # --- Período ---
        ttk.Label(self.filter_card, text="Período:", style="Header.TLabel").grid(row=8, column=0, sticky="w", pady=(10, 5))
        
        # Frame que usa GRID para controlar o layout e tamanho dos botões de período
        period_grid_frame = ttk.Frame(self.filter_card, style="PeriodButton.TFrame")
        period_grid_frame.grid(row=9, column=0, sticky="ew", pady=(0, 10))
        
        # Configuração de Tamanho (Weight 1:1:3)
        period_grid_frame.columnconfigure(0, weight=1) 
        period_grid_frame.columnconfigure(1, weight=1)
        period_grid_frame.columnconfigure(2, weight=2) # Combobox mais largo

        # Variáveis de Controle Separadas
        self.radio_period_var = tk.StringVar(value="4 Meses") # Para 4 Meses e 8 Meses
        self.combo_period_var = tk.StringVar(value=PLACEHOLDER_PERIOD) # Para o Combobox
        # Variável final que armazena o valor a ser filtrado (tratada nas funções auxiliares)
        self.final_period_var = tk.StringVar(value="4 Meses") 

        # Rádio Buttons (4 Meses e 8 Meses) - Usando colunas 0 e 1
        self.rb_4 = self.create_period_button(period_grid_frame, "4 Meses", self.radio_period_var, 0)
        self.rb_8 = self.create_period_button(period_grid_frame, "8 Meses", self.radio_period_var, 1)
        
        # ComboBox para o restante das opções, começando com o Placeholder
        self.period_options = [PLACEHOLDER_PERIOD, "Todo Período", "1 semana", "2 semanas", "3 semanas", 
                               "4 semanas", "5 semanas", "2 meses", "3 meses", "4 meses", 
                               "5 meses", "6 meses", "7 meses", "8 meses", "9 meses", 
                               "10 meses", "11 meses", "1 ano", "2 anos"]
        self.period_combo = ttk.Combobox(period_grid_frame, 
                                         textvariable=self.combo_period_var, 
                                         values=self.period_options, 
                                         state="readonly", 
                                         width=9, 
                                         style="Period.TCombobox")
        
        self.period_combo.set(PLACEHOLDER_PERIOD)
        self.period_combo.grid(row=0, column=2, sticky="ew", padx=(0, 0)) 
        
        self.set_placeholder(self.period_combo, PLACEHOLDER_PERIOD) 
        self.period_combo.bind("<<ComboboxSelected>>", self._handle_period_combo_select)
        
        # --- Card Secundário (Condição e Recomendações) ---
        self.sub_card = ttk.Frame(self, padding=20, style="Card.TFrame")
        self.sub_card.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 10))
        self.sub_card.columnconfigure(0, weight=1)
        self.sub_card.columnconfigure(1, weight=1)

        # Condição
        ttk.Label(self.sub_card, text="Condição:", style="Header.TLabel").grid(row=0, column=0, sticky="w", columnspan=2, pady=(0, 5))
        self.condicoes = {
            "Estoque crítico": tk.BooleanVar(),
            "Baixo estoque": tk.BooleanVar(),
            "Produto parado": tk.BooleanVar()
        }
        
        self._add_checkbuttons(self.sub_card, self.condicoes, start_row=1)

        # Recomendações
        ttk.Label(self.sub_card, text="Recomendações:", style="Header.TLabel").grid(row=5, column=0, sticky="w", columnspan=2, pady=(10, 5))
        self.sugestao_var = tk.BooleanVar()
        self._add_checkbuttons(self.sub_card, {"Sugestão de compra": self.sugestao_var}, start_row=6)
        
        # --- Botão de filtro ---
        ttk.Button(self, text="Filtrar", command=self.filtrar, style="Filter.TButton").grid(row=2, column=0, sticky="ew", padx=0, pady=(0, 0))

    def create_period_button(self, parent, text, var, column):
        """Cria um Radiobutton e o posiciona via grid."""
        frame = ttk.Frame(parent, style="PeriodButton.TFrame", padding=[0, 0, 0, 0]) 
        frame.grid(row=0, column=column, sticky="ew", padx=(0, 5)) 
        
        rb = ttk.Radiobutton(frame, text=text, variable=var, value=text, style="Period.TRadiobutton")
        rb.pack(fill="both", expand=True) 
        
        # Atualiza a variável final e reseta o Combobox ao clicar
        rb.bind("<Button-1>", lambda e, val=text: self._handle_radiobutton_select(val))
        
        return frame

    def _handle_radiobutton_select(self, value):
        """Lida com a seleção de RadioButton: reseta o Combobox para o estilo NORMAL."""
        # 1. Garante que o Combobox volte ao placeholder visual
        self.combo_period_var.set(PLACEHOLDER_PERIOD)
        self.set_placeholder(self.period_combo, PLACEHOLDER_PERIOD) 
        
        # --- MUDANÇA: VOLTAR PARA ESTILO NORMAL ---
        self.period_combo.configure(style="Period.TCombobox")

        # 2. Atualiza a variável final
        self.final_period_var.set(value)

    def _handle_period_combo_select(self, event):
        """Lida com a seleção do ComboBox: troca para o estilo VERDE se válido."""
        selected_value = self.combo_period_var.get()
        
        if selected_value != PLACEHOLDER_PERIOD:
            # 1. Se valor válido, desativa os Radiobuttons
            self.radio_period_var.set("") 
            # 2. Atualiza a variável final
            self.final_period_var.set(selected_value) 
            # 3. Fonte normal
            self.period_combo.configure(font=("Segoe UI", 10), foreground=COLOR_TEXT)
            
            # --- MUDANÇA: APLICAR ESTILO VERDE ---
            self.period_combo.configure(style="Active.Period.TCombobox")
            
        else:
            # 1. Se placeholder, reseta
            self.radio_period_var.set("")
            self.final_period_var.set("")
            self.set_placeholder(self.period_combo, PLACEHOLDER_PERIOD)
            
            # --- MUDANÇA: VOLTAR PARA ESTILO NORMAL ---
            self.period_combo.configure(style="Period.TCombobox")
            
    def _add_checkbuttons(self, parent, check_dict, start_row):
        """Adiciona Checkbuttons, torna o TEXTO clicável e adiciona HOVER com BOLD."""
        
        # Definição das fontes para alternar
        FONT_NORMAL = ("Segoe UI", 10)
        FONT_BOLD = ("Segoe UI", 10, "bold")
        
        for i, (label_text, var) in enumerate(check_dict.items(), start=start_row):
            # Frame container
            check_frame = ttk.Frame(parent, style="PeriodButton.TFrame")
            check_frame.grid(row=i, column=0, sticky="ew", columnspan=2, pady=(2, 2))
            check_frame.columnconfigure(0, weight=1) 
            
            # Label (Texto)
            lbl = ttk.Label(check_frame, text=label_text, style="TLabel", background=COLOR_CARD_BG)
            lbl.pack(side="left", fill="x", expand=True, padx=(0, 10))
            
            # Checkbutton (Caixinha)
            chk = ttk.Checkbutton(check_frame, variable=var, text="", style="TCheckbutton", cursor="hand2")
            chk.pack(side="right")
            
            # --- LÓGICA DE CLIQUE ---
            def toggle_selection(event, v=var):
                v.set(not v.get())

            # --- LÓGICA DE HOVER (Mudar para Bold) ---
            def on_enter(event):
                # Muda a fonte para Negrito e a cor para preto
                event.widget.configure(font=FONT_BOLD, foreground=COLOR_TEXT_HOVER)

            def on_leave(event):
                # Volta para a fonte Normal e a cor cinza original
                event.widget.configure(font=FONT_NORMAL, foreground=COLOR_TEXT)

            # Bindings (Conexões dos eventos)
            lbl.bind("<Button-1>", toggle_selection) # Clicar
            lbl.bind("<Enter>", on_enter)            # Mouse entrou
            lbl.bind("<Leave>", on_leave)            # Mouse saiu
            
            # Cursor de mãozinha
            lbl.configure(cursor="hand2")

    # --- Funções de Placeholder ---
    def add_placeholder(self, widget, text):
        """Adiciona um texto de placeholder a um Entry widget."""
        widget.insert(0, text)
        widget.configure(foreground='grey')

        def on_focus_in(event):
            if widget.get() == text:
                widget.delete(0, tk.END)
                widget.configure(foreground=COLOR_TEXT)

        def on_focus_out(event):
            if not widget.get():
                widget.insert(0, text)
                widget.configure(foreground='grey')

        widget.bind('<FocusIn>', on_focus_in)
        widget.bind('<FocusOut>', on_focus_out)

    def set_placeholder(self, combobox, text):
        """Define um placeholder visual para um Combobox."""
        combobox.set(text)
        combobox.configure(font=("Segoe UI", 10, "italic"), foreground='grey')
        
        def on_combo_select(event):
            # Ao selecionar, remover a cor cinza e o itálico
            combobox.configure(font=("Segoe UI", 10), foreground=COLOR_TEXT)
        
        combobox.bind("<<ComboboxSelected>>", on_combo_select, add="+")
        
    def filtrar(self):
        """Ação de filtro: trata os placeholders como string vazia."""
        
        def get_value_or_empty(var, placeholder):
            """Retorna string vazia se o valor for o placeholder, ou o valor real."""
            value = var.get()
            return "" if value == placeholder else value

        # Obtendo os valores, tratando os placeholders
        linha_filtrada = get_value_or_empty(self.linha_var, PLACEHOLDER_LINHA)
        sub_linha_filtrada = get_value_or_empty(self.sub_linha_var, PLACEHOLDER_SUB_LINHA)
        codigo_filtrado = get_value_or_empty(self.codigo_var, PLACEHOLDER_CODIGO)
        
        # O valor do período é obtido da variável final (que já foi tratada pelas funções _handle...)
        periodo_filtrado = get_value_or_empty(self.final_period_var, "") # Verifica se a final_var está vazia.

        # Exemplo de ação: imprimir todos os filtros
        print({
            "linha": linha_filtrada,
            "sub_linha": sub_linha_filtrada,
            "codigo": codigo_filtrado,
            "periodo": periodo_filtrado,
            "condicoes": {k: v.get() for k, v in self.condicoes.items()},
            "sugestao_compra": self.sugestao_var.get(),
        })


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Estoque Filtros - Figma Style")
    root.geometry("355x650")
    root.configure(background=COLOR_CARD_BG) 

    setup_styles(root)

    frame = EstoqueFilterFrame(root)
    frame.pack(fill="both", expand=True, padx=20, pady=20) 

    root.mainloop()