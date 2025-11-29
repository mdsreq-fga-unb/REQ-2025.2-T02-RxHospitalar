import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import pandas as pd
from datetime import datetime

# 1. IMPORTS DO MODEL (app/models)
from app.models.data_loader import load_selected_columns 

# 2. IMPORTS DAS VIEWS (app/views/pages)
from app.views.pages.auth_page.login import LoginPage, ForgotPasswordPage
from app.views.components.loading_import_modal import LoadingImportModal
from app.views.pages.dashboard_page.dashboard_page import DashboardView 

from app.utils.login_utils import *
# ----------------------------------------------------

class AppController(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        try:
            self.state("zoomed") 
        except tk.TclError:
            self.attributes('-zoomed', True)
        
        self.title("Sistema de Estoque - RX Hospitalar")
        
        # Atributos de estado do Controller
        self.df_master = pd.DataFrame() 
        self.loading_import_modal = None
        self.last_update_time = None

        # 1. Configuração do Contêiner Principal
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # 2. Inicialização do Tema
        self.style = ttk.Style()
        self.style.theme_use('clam') 
        self.configure(bg='#1e1e1e')
        self.style.configure('TFrame', background='#1e1e1e') 
        self.style.configure('TLabel', background='#1e1e1e', foreground='white') 
        
        self.frames = {}
        
        # 3. Criação e Empilhamento dos Frames (Views)
        for F in (LoginPage, ForgotPasswordPage, DashboardView): 
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew") 

        self.show_frame("LoginPage")
        
    def show_frame(self, page_name):
        """Traz o frame para o topo (front) e o exibe."""
        frame = self.frames[page_name]
        frame.tkraise()
    
    # 1. Lógica de Validação da Autenticação

    def attempt_login(self, username, password, feedback_label):
        """
        Recebe as credenciais da LoginView, verifica e, em caso de sucesso, 
        inicia automaticamente o carregamento dos dados.
        """

        is_authenticated = validate_login(username, password, self.frames["LoginPage"].feedback_label);  
        print(is_authenticated)
        
        if is_authenticated:
            print("Login bem-sucedido. Iniciando carregamento de dados...")
            self.loading_import_modal = LoadingImportModal(self)

            self.update_idletasks() # força o desenho do modal na tela antes de iniciar o loading dos dados

            """Inicia o fluxo de carregamento de dados do caminho fixo definido no Model."""
        
            sheet_name = None
            columns_to_load = None 
            
            # Inicia o loading assíncrono
            self.start_data_loading(sheet_name, columns_to_load)

        else:
            print("[ERRO] Credenciais inválidas, não é possível fazer a importação dos dados.")
            messagebox.showerror("Erro de Login", "Usuário ou senha inválidos. Não é possível fazer a importação dos dados.")
            self.show_frame("LoginPage")
        
    # 2. INÍCIO DO CARREGAMENTO: Exibe modal e inicia thread
    def start_data_loading(self, sheet_name, columns_to_load):
        """Exibe o modal de carregamento e inicia o processamento assíncrono."""

        # Inicia a thread para carregar os dados
        loader_thread = threading.Thread(
            target=self._run_pandas_in_thread,
            args=(sheet_name, columns_to_load) 
        )
        loader_thread.start()

    # 3. THREAD SECUNDÁRIA: Executa o Model 
    def _run_pandas_in_thread(self, sheet_name, columns_to_load):
        """Executa a função do Model que lê o arquivo fixo."""
        
        # O MODEL É CHAMADO
        df_master = load_selected_columns(sheet_name, columns_to_load)
        
        # Retorna para a thread principal (UI)
        self.after(0, self.finish_data_loading, df_master)

    # 4. FINALIZAÇÃO NA THREAD PRINCIPAL: Fecha modal e troca tela
    def finish_data_loading(self, df_master):
        """Roda na thread principal: destrói o modal e troca a tela."""

        success = (df_master is not None and not df_master.empty)

        if success:
            self.df_master = df_master
            self.last_update_time = datetime.now()
            print("Dados carregados com sucesso. Próxima tela: Dashboard.")
            
            # 2. Define o TIMER para transicionar após 1500ms (1.5 segundos)
            self.after(1500, self.handle_final_transition, "DashboardView")
        else:
            print(" Erro na importação.")
            # 2. Define o TIMER para transicionar após 2500ms (dá mais tempo para ler o erro)
            self.after(2500, self.handle_final_transition, "LoginPage")

    def handle_final_transition(self, next_page):
        """Fecha o modal de carregamento e navega para a próxima página."""
        
        # 1. Fecha o Modal de forma segura
        if self.loading_import_modal:
            self.loading_import_modal.destroy_modal()
            self.loading_import_modal = None

        # 2. Transiciona para a página de destino
        self.show_frame(next_page)
