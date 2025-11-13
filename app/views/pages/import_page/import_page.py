import tkinter as tk
from tkinter import ttk

from app.views.components.loading_import_modal import LoadingModal

class ImportView(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(1, weight=1) # Faz o conteúdo expandir
        self.grid_columnconfigure(0, weight=1)
        
        # 1. Cabeçalho (Header Frame) - Linha 0
        self.create_header() 

        # 2. Conteúdo Principal (Main Content Frame) - Linha 1
        main_content_frame = ttk.Frame(self, style='TFrame') # Fundo escuro total
        main_content_frame.grid(row=1, column=0, sticky="nsew")
        
        # 3. Construção do Modal de Importação (Centralizado no Conteúdo)
        self.create_import_modal(main_content_frame)

    def create_header(self):
        # Frame do Cabeçalho: Fundo verde escuro (crie um estilo 'Header.TFrame')
        header_frame = ttk.Frame(self, style='Header.TFrame', height=50)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Label do Título (BASE RX HOSPITALAR)
        ttk.Label(header_frame, text="RX HOSPITALAR", 
                  style='HeaderTitle.TLabel').grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Ícones à direita (Notificações, Perfil, etc.)
        # Nota: Ícones em Tkinter são geralmente implementados com imagens (PNG/GIF)
        # ou fontes customizadas, mas aqui usamos placeholders de texto.
        icon_group = ttk.Frame(header_frame, style='Header.TFrame')
        icon_group.grid(row=0, column=0, sticky="e", padx=10)
        ttk.Label(icon_group, text="🔔").pack(side=tk.LEFT, padx=10)
        ttk.Label(icon_group, text="🔄").pack(side=tk.LEFT, padx=10)
        ttk.Label(icon_group, text="👤").pack(side=tk.LEFT, padx=10)
        
    def create_import_modal(self, parent_frame):
        # Cria o modal de confirmação no centro do parent_frame
        modal_frame = ttk.Frame(parent_frame, padding=20)
        modal_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Caixa de Lista (Lista de Arquivos)
        file_list_frame = ttk.Frame(modal_frame, relief="solid", borderwidth=1)
        file_list_frame.pack(pady=10, padx=10, fill='both', expand=True)


        # Botão Importar (Alinhado à direita)
        ttk.Button(modal_frame, text="Importar", style='Accent.TButton',
                   # O command chamará a lógica de leitura do Pandas (Controller/Model)
                   command=self.controller.start_data_loadings
                   ).pack(side=tk.RIGHT, padx=10, pady=10)