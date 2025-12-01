# app/views/components/estoque_filters.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw

# Importação da lógica de dados
from app.models.carregar_dados import obter_dados_cascata

# --- CONSTANTES DE ESTILO ---
COLOR_BACKGROUND = "#FFFFFF"
COLOR_CARD_BG = "#F4F9F4"
COLOR_BORDER = "#5D8569"
COLOR_TEXT = "#343A40"
COLOR_INPUT_BG = "#E8F0E8"
COLOR_BUTTON_BG = "#B8D4C0"
COLOR_BUTTON_ACTIVE_BG = "#A0C0A8"
COLOR_CHECKED_SOLID = "#52805D"
COLOR_TEXT_HOVER = "#52805D"
COLOR_DASHBOARD_BG = "#1e1e1e" 

PLACEHOLDER_LINHA = "Selecione uma Linha"
PLACEHOLDER_SUB_LINHA = "Selecione uma Sub Linha"
PLACEHOLDER_CODIGO = "Insira um código"
PLACEHOLDER_PERIOD = "Opções"

_img_unchecked = None
_img_checked = None

def create_checkbox_assets():
    global _img_unchecked, _img_checked
    size = 16 
    
    img1 = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw1 = ImageDraw.Draw(img1)
    draw1.rectangle([0, 0, size-1, size-1], fill=COLOR_CARD_BG, outline=COLOR_BORDER, width=1)
    _img_unchecked = ImageTk.PhotoImage(img1)

    img2 = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw2 = ImageDraw.Draw(img2)
    draw2.rectangle([0, 0, size-1, size-1], fill=COLOR_CHECKED_SOLID, outline=COLOR_CHECKED_SOLID, width=1)
    draw2.line([(3, 8), (7, 12), (12, 4)], fill="white", width=2)
    _img_checked = ImageTk.PhotoImage(img2)

    return _img_unchecked, _img_checked

def setup_styles(root):
    """Configura os estilos TTK."""
    style = ttk.Style(root)
    style.theme_use("clam")

    img_u, img_c = create_checkbox_assets()

    try:
        style.element_create("Custom.Indicator", "image", img_u,
                            ("selected", img_c),
                            width=20, sticky="w")
    except tk.TclError:
        pass

    style.layout("Filter.TCheckbutton", [
        ('Checkbutton.padding', {'sticky': 'nswe', 'children': [
            ('Custom.Indicator', {'side': 'right', 'sticky': ''}), 
            ('Checkbutton.focus', {'side': 'left', 'sticky': 'w', 'children': [
                ('Checkbutton.label', {'sticky': 'nswe'})
            ]})
        ]})
    ])

    style.configure("Filter.TCheckbutton",
                    background=COLOR_CARD_BG,
                    foreground=COLOR_TEXT,
                    focuscolor=COLOR_CARD_BG)
    
    style.map("Filter.TCheckbutton",
              background=[('active', COLOR_CARD_BG)],
              foreground=[('active', COLOR_TEXT_HOVER)])

    style.configure("Sidebar.TFrame", background=COLOR_DASHBOARD_BG, borderwidth=0, relief="flat")

    style.configure("Filter.TLabel", font=("Segoe UI", 10), foreground=COLOR_TEXT, background=COLOR_CARD_BG)
    style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), foreground=COLOR_TEXT, background=COLOR_CARD_BG)
    style.configure("Subtitle.TLabel", font=("Segoe UI", 11), foreground=COLOR_TEXT, background=COLOR_CARD_BG)
    style.configure("Header.TLabel", font=("Segoe UI", 10, "bold"), foreground=COLOR_TEXT, background=COLOR_CARD_BG)

    style.configure("Card.TFrame", background=COLOR_CARD_BG, borderwidth=1, relief="solid", bordercolor=COLOR_BORDER)
    style.map("Card.TFrame", bordercolor=[('focus', COLOR_BORDER)])

    style.configure("TCombobox", fieldbackground=COLOR_INPUT_BG, background=COLOR_INPUT_BG, bordercolor=COLOR_BORDER, borderwidth=1, relief="solid", padding=[5, 2])
    style.map("TCombobox", 
              fieldbackground=[('readonly', COLOR_INPUT_BG)], 
              selectbackground=[('readonly', COLOR_INPUT_BG)], 
              selectforeground=[('readonly', COLOR_TEXT)],
              bordercolor=[('focus', COLOR_BORDER), ('!focus', COLOR_BORDER)],
              lightcolor=[('focus', COLOR_BORDER), ('!focus', COLOR_BORDER)],
              darkcolor=[('focus', COLOR_BORDER), ('!focus', COLOR_BORDER)])
    
    style.configure("TEntry", fieldbackground=COLOR_INPUT_BG, bordercolor=COLOR_BORDER, borderwidth=1, relief="solid", padding=[5, 2])
    style.map("TEntry", 
              fieldbackground=[('!disabled', COLOR_INPUT_BG), ('disabled', COLOR_INPUT_BG)],
              bordercolor=[('focus', COLOR_BORDER), ('!focus', COLOR_BORDER)],
              lightcolor=[('focus', COLOR_BORDER), ('!focus', COLOR_BORDER)],
              darkcolor=[('focus', COLOR_BORDER), ('!focus', COLOR_BORDER)])

    style.configure("Period.TRadiobutton", background=COLOR_CARD_BG, foreground=COLOR_TEXT, relief="flat", padding=[2, 2])
    style.map("Period.TRadiobutton", background=[('selected', COLOR_BUTTON_BG), ('active', COLOR_BUTTON_ACTIVE_BG), ('!selected', COLOR_CARD_BG)], foreground=[('selected', COLOR_TEXT)])
    style.configure("PeriodButton.TFrame", background=COLOR_CARD_BG)

    style.configure("Period.TCombobox", fieldbackground=COLOR_CARD_BG, background=COLOR_CARD_BG, bordercolor=COLOR_BUTTON_BG, borderwidth=1, relief="solid", padding=[2, 2])
    style.map("Period.TCombobox", fieldbackground=[('readonly', COLOR_CARD_BG)], bordercolor=[('readonly', COLOR_BUTTON_BG)], selectbackground=[('readonly', COLOR_CARD_BG)], selectforeground=[('readonly', COLOR_TEXT)])     
    style.configure("Active.Period.TCombobox", fieldbackground=COLOR_BUTTON_BG, background=COLOR_BUTTON_BG, bordercolor=COLOR_BUTTON_BG, borderwidth=1, relief="solid", padding=[2, 2])
    style.map("Active.Period.TCombobox", fieldbackground=[('readonly', COLOR_BUTTON_BG)], bordercolor=[('readonly', COLOR_BUTTON_BG)], selectbackground=[('readonly', COLOR_BUTTON_BG)], selectforeground=[('readonly', COLOR_TEXT)])     

    style.configure("Filter.TButton", background=COLOR_BUTTON_BG, foreground=COLOR_TEXT, font=("Segoe UI", 11, "bold"), borderwidth=0, relief="flat", padding=[10, 5])
    style.map("Filter.TButton", background=[('active', COLOR_BUTTON_ACTIVE_BG), ('!active', COLOR_BUTTON_BG)])


class EstoqueFilterFrame(ttk.Frame):
    def __init__(self, parent, on_filter_callback=None):
        """
        on_filter_callback: Função que será chamada quando o botão filtrar for clicado. 
                            Deve receber um dicionário com os filtros.
        """
        super().__init__(parent, padding=0, style="Sidebar.TFrame")
        self.columnconfigure(0, weight=1)
        self.on_filter_callback = on_filter_callback

        # 1. CARREGAMENTO DE DADOS (ATUALIZADO: Recebe 4 valores)
        try:
            # Importante: obter_dados_cascata agora deve retornar a lista de códigos também!
            self.dados_linhas, self.dados_sublinhas_totais, self.mapa_cascata, self.dados_codigos = obter_dados_cascata()
        except ValueError:
            # Caso a função ainda retorne 3 valores (fallback)
            try:
                self.dados_linhas, self.dados_sublinhas_totais, self.mapa_cascata = obter_dados_cascata()
                self.dados_codigos = []
            except Exception:
                self.dados_linhas, self.dados_sublinhas_totais, self.mapa_cascata, self.dados_codigos = [], [], {}, []
        except Exception as e:
            print(f"Erro ao carregar dados do Excel no filtro: {e}")
            self.dados_linhas, self.dados_sublinhas_totais, self.mapa_cascata, self.dados_codigos = [], [], {}, []

        # 2. CARD PRINCIPAL
        self.filter_card = ttk.Frame(self, padding=20, style="Card.TFrame")
        self.filter_card.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 10))
        self.filter_card.columnconfigure(0, weight=1)

        # Título
        ttk.Label(self.filter_card, text="Estoque", style="Title.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 0))
        ttk.Label(self.filter_card, text="Filtros", style="Subtitle.TLabel").grid(row=1, column=0, sticky="w", pady=(0, 10))
        
        # 3. SELEÇÃO DE PRODUTOS (LINHA)
        ttk.Label(self.filter_card, text="Linha:", style="Header.TLabel").grid(row=2, column=0, sticky="w", pady=(5, 0))
        self.linha_var = tk.StringVar(value=PLACEHOLDER_LINHA)
        self.linha_values = [PLACEHOLDER_LINHA] + self.dados_linhas
        
        self.linha_combo = ttk.Combobox(self.filter_card, textvariable=self.linha_var, values=self.linha_values, state="readonly")
        self.linha_combo.grid(row=3, column=0, sticky="ew", pady=(0, 5))
        self.set_placeholder(self.linha_combo, PLACEHOLDER_LINHA)
        self.linha_combo.bind("<<ComboboxSelected>>", self._on_linha_selected, add="+")

        # 4. SELEÇÃO DE PRODUTOS (SUB LINHA)
        ttk.Label(self.filter_card, text="Sub Linha:", style="Header.TLabel").grid(row=4, column=0, sticky="w", pady=(5, 0))
        self.sub_linha_var = tk.StringVar(value=PLACEHOLDER_SUB_LINHA)
        self.sub_linha_values = [PLACEHOLDER_SUB_LINHA] + self.dados_sublinhas_totais
        
        self.sub_linha_combo = ttk.Combobox(self.filter_card, textvariable=self.sub_linha_var, values=self.sub_linha_values, state="readonly")
        self.sub_linha_combo.grid(row=5, column=0, sticky="ew", pady=(0, 5))
        self.set_placeholder(self.sub_linha_combo, PLACEHOLDER_SUB_LINHA)

        # 5. INPUT CÓDIGO 
        ttk.Label(self.filter_card, text="Código:", style="Header.TLabel").grid(row=6, column=0, sticky="w", pady=(5, 0))
        self.codigo_var = tk.StringVar()
        self.codigo_entry = ttk.Entry(self.filter_card, textvariable=self.codigo_var, style="TEntry")
        self.codigo_entry.grid(row=7, column=0, sticky="ew", pady=(0, 2)) # Padding bottom reduzido
        
        # --- NOVO: Label para Mensagem de Erro ---
        self.lbl_erro_codigo = tk.Label(
            self.filter_card, 
            text="", 
            fg="#ff4444",   # Cor vermelha para erro
            bg=COLOR_CARD_BG, 
            font=("Segoe UI", 8, "bold"),
            anchor="w"
        )
        self.lbl_erro_codigo.grid(row=8, column=0, sticky="w", pady=(0, 5))
        
        # Placeholder e Bindings de validação
        self.add_placeholder(self.codigo_entry, PLACEHOLDER_CODIGO)
        self.codigo_entry.bind("<FocusOut>", self._validar_codigo, add="+")
        self.codigo_entry.bind("<Return>", self._validar_codigo, add="+")

        # 6. PERÍODO (Ajustado para Rows 9 e 10 por causa da Label de erro)
        ttk.Label(self.filter_card, text="Período:", style="Header.TLabel").grid(row=9, column=0, sticky="w", pady=(5, 5))
        
        period_grid_frame = ttk.Frame(self.filter_card, style="PeriodButton.TFrame")
        period_grid_frame.grid(row=10, column=0, sticky="ew", pady=(0, 10))
        period_grid_frame.columnconfigure(0, weight=1)
        period_grid_frame.columnconfigure(1, weight=1)
        period_grid_frame.columnconfigure(2, weight=2)

        self.radio_period_var = tk.StringVar(value="4 Meses")
        self.combo_period_var = tk.StringVar(value=PLACEHOLDER_PERIOD)
        self.final_period_var = tk.StringVar(value="4 Meses")

        self.rb_4 = self.create_period_button(period_grid_frame, "4 Meses", self.radio_period_var, 0)
        self.rb_8 = self.create_period_button(period_grid_frame, "8 Meses", self.radio_period_var, 1)
        
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
        
        # 7. CARD SECUNDÁRIO
        self.sub_card = ttk.Frame(self, padding=20, style="Card.TFrame")
        self.sub_card.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 10))
        self.sub_card.columnconfigure(0, weight=1)
        self.sub_card.columnconfigure(1, weight=1)

        ttk.Label(self.sub_card, text="Condição:", style="Header.TLabel").grid(row=0, column=0, sticky="w", columnspan=2, pady=(0, 5))
        self.condicoes = {
            "Estoque crítico": tk.BooleanVar(),
            "Baixo estoque": tk.BooleanVar(),
            "Produto parado": tk.BooleanVar()
        }
        self._add_checkbuttons(self.sub_card, self.condicoes, start_row=1)

        ttk.Label(self.sub_card, text="Recomendações:", style="Header.TLabel").grid(row=5, column=0, sticky="w", columnspan=2, pady=(10, 5))
        self.sugestao_var = tk.BooleanVar()
        self._add_checkbuttons(self.sub_card, {"Sugestão de compra": self.sugestao_var}, start_row=6)
        
        ttk.Label(self.sub_card, text="Outros:", style="Header.TLabel").grid(row=7, column=0, sticky="w", columnspan=2, pady=(0, 5))
        self.outros = {
            "Performance de Vendedores": tk.BooleanVar()
        }
        self._add_checkbuttons(self.sub_card, self.outros, start_row=8)
        # Botão de filtro 
        ttk.Button(self, text="Filtrar", command=self.filtrar, style="Filter.TButton").grid(row=2, column=0, sticky="ew", padx=0, pady=(0, 0))

    # --- LÓGICA DE VALIDAÇÃO DO CÓDIGO ---
    def _validar_codigo(self, event=None):
        """Verifica se o código digitado existe na lista de códigos carregados."""
        valor_digitado = self.codigo_var.get().strip()

        # Ignora se for vazio ou se for o placeholder
        if not valor_digitado or valor_digitado == PLACEHOLDER_CODIGO:
            self.lbl_erro_codigo.config(text="")
            return

        # Verifica se o código existe na lista (case insensitive, convertendo pra str)
        # Assumindo que self.dados_codigos é uma lista de strings
        if valor_digitado not in self.dados_codigos:
            # ERRO: Mostra mensagem e limpa
            self.lbl_erro_codigo.config(text="Código não encontrado!")
            
            # Limpa o campo e restaura o placeholder
            self.codigo_entry.delete(0, tk.END)
            self.add_placeholder(self.codigo_entry, PLACEHOLDER_CODIGO)
            
            # Opcional: Feedback sonoro
            self.bell()
        else:
            # SUCESSO: Limpa mensagem de erro
            self.lbl_erro_codigo.config(text="")

    def _on_linha_selected(self, event):
        linha_selecionada = self.linha_var.get()

        if linha_selecionada == PLACEHOLDER_LINHA:
            novas_opcoes = [PLACEHOLDER_SUB_LINHA] + self.dados_sublinhas_totais
        elif linha_selecionada in self.mapa_cascata:
            novas_opcoes = [PLACEHOLDER_SUB_LINHA] + self.mapa_cascata[linha_selecionada]
        else:
            novas_opcoes = [PLACEHOLDER_SUB_LINHA]

        self.sub_linha_combo['values'] = novas_opcoes
        self.sub_linha_var.set(PLACEHOLDER_SUB_LINHA)
        self.set_placeholder(self.sub_linha_combo, PLACEHOLDER_SUB_LINHA)
        self.linha_combo.configure(font=("Segoe UI", 10), foreground=COLOR_TEXT)

    def create_period_button(self, parent, text, var, column):
        frame = ttk.Frame(parent, style="PeriodButton.TFrame", padding=[0, 0, 0, 0])
        frame.grid(row=0, column=column, sticky="ew", padx=(0, 5))
        rb = ttk.Radiobutton(frame, text=text, variable=var, value=text, style="Period.TRadiobutton")
        rb.pack(fill="both", expand=True)
        rb.bind("<Button-1>", lambda e, val=text: self._handle_radiobutton_select(val))
        return frame

    def _handle_radiobutton_select(self, value):
        self.combo_period_var.set(PLACEHOLDER_PERIOD)
        self.set_placeholder(self.period_combo, PLACEHOLDER_PERIOD)
        self.period_combo.configure(style="Period.TCombobox")
        self.final_period_var.set(value)

    def _handle_period_combo_select(self, event):
        selected_value = self.combo_period_var.get()
        if selected_value != PLACEHOLDER_PERIOD:
            self.radio_period_var.set("")
            self.final_period_var.set(selected_value)
            self.period_combo.configure(font=("Segoe UI", 10), foreground=COLOR_TEXT)
            self.period_combo.configure(style="Active.Period.TCombobox")
        else:
            self.radio_period_var.set("")
            self.final_period_var.set("")
            self.set_placeholder(self.period_combo, PLACEHOLDER_PERIOD)
            self.period_combo.configure(style="Period.TCombobox")
            
    def _add_checkbuttons(self, parent, check_dict, start_row):
        FONT_NORMAL = ("Segoe UI", 10)
        FONT_BOLD = ("Segoe UI", 10, "bold")
        for i, (label_text, var) in enumerate(check_dict.items(), start=start_row):
            check_frame = ttk.Frame(parent, style="PeriodButton.TFrame")
            check_frame.grid(row=i, column=0, sticky="ew", columnspan=2, pady=(2, 2))
            check_frame.columnconfigure(0, weight=1)
            lbl = ttk.Label(check_frame, text=label_text, style="Filter.TLabel")
            lbl.pack(side="left", fill="x", expand=True, padx=(0, 10))
            chk = ttk.Checkbutton(check_frame, variable=var, text="", style="Filter.TCheckbutton", cursor="hand2")
            chk.pack(side="right")
            
            def toggle_selection(event, v=var):
                v.set(not v.get())
            def on_enter(event):
                event.widget.configure(font=FONT_BOLD, foreground=COLOR_TEXT_HOVER)
            def on_leave(event):
                event.widget.configure(font=FONT_NORMAL, foreground=COLOR_TEXT)
            lbl.bind("<Button-1>", toggle_selection)
            lbl.bind("<Enter>", on_enter)            
            lbl.bind("<Leave>", on_leave)            
            lbl.configure(cursor="hand2")

    def add_placeholder(self, widget, text):
        # Configuração inicial
        if not widget.get():
            widget.insert(0, text)
            widget.configure(foreground='grey')
            
        def on_focus_in(event):
            # Quando foca, limpa placeholder e erro
            if widget.get() == text:
                widget.delete(0, tk.END)
                widget.configure(foreground=COLOR_TEXT)
            # ATUALIZAÇÃO: Limpa mensagem de erro ao tentar digitar novamente
            if hasattr(self, 'lbl_erro_codigo'):
                self.lbl_erro_codigo.config(text="")

        def on_focus_out(event):
            # Quando sai, se estiver vazio, volta placeholder
            if not widget.get():
                widget.insert(0, text)
                widget.configure(foreground='grey')
                # Se saiu vazio, garante que não tem erro de "Não encontrado"
                if hasattr(self, 'lbl_erro_codigo'):
                    self.lbl_erro_codigo.config(text="")

        widget.bind('<FocusIn>', on_focus_in, add="+")
        widget.bind('<FocusOut>', on_focus_out, add="+")

    def set_placeholder(self, combobox, text):
        combobox.set(text)
        combobox.configure(font=("Segoe UI", 10, "italic"), foreground='grey')
        def on_combo_select(event):
            combobox.configure(font=("Segoe UI", 10), foreground=COLOR_TEXT)
        combobox.bind("<<ComboboxSelected>>", on_combo_select, add="+")
        
    def filtrar(self):
        def get_value_or_empty(var, placeholder):
            value = var.get()
            return "" if value == placeholder else value

        linha_filtrada = get_value_or_empty(self.linha_var, PLACEHOLDER_LINHA)
        sub_linha_filtrada = get_value_or_empty(self.sub_linha_var, PLACEHOLDER_SUB_LINHA)
        codigo_filtrado = get_value_or_empty(self.codigo_var, PLACEHOLDER_CODIGO)
        periodo_filtrado = get_value_or_empty(self.final_period_var, "")

        filter_data = {
            "linha": linha_filtrada,
            "sub_linha": sub_linha_filtrada,
            "codigo": codigo_filtrado,
            "periodo": periodo_filtrado,
            "condicoes": {k: v.get() for k, v in self.condicoes.items()},
            "sugestao_compra": self.sugestao_var.get(),
            "vendedores": self.outros["Performance de Vendedores"].get()
        }

        # CHAMA O CALLBACK DO DASHBOARD SE ELE EXISTIR
        if self.on_filter_callback:
            self.on_filter_callback(filter_data)
        else:
            print("Nenhum callback de filtro configurado:", filter_data)