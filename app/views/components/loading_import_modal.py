import tkinter as tk
from tkinter import ttk

class LoadingImportModal:
    def __init__(self, root_controller):
        self.root = root_controller
        
        # 1. Cria a janela secundária (Toplevel)
        self.modal = tk.Toplevel(self.root)
        self.modal.title("Carregando Dados...")
        self.modal.overrideredirect(True) 
        
        # 2. Configuração Visual
        self._center_modal(self.modal, width=350, height=180)
        self.modal.grab_set() 
        self.root.attributes('-alpha', 1) 
        
        # 3. Adiciona Componentes de Feedback (Estado Inicial: Carregando)
        content_frame = ttk.Frame(self.modal, padding=20)
        content_frame.pack(expand=True, fill='both')

        # Label de Status (Vamos usar este label para a mensagem final)
        self.status_label = ttk.Label(content_frame, 
                                      text="Carregando e Consolidando Dados...", 
                                      font=("Arial", 12))
        self.status_label.pack(pady=10)
        
        # Barra de Progresso Indeterminada
        self.progress_bar = ttk.Progressbar(content_frame, 
                                            mode='indeterminate', 
                                            length=300)
        self.progress_bar.pack(pady=15, padx=20)
        
        # Inicia a Animação da Barra
        self.progress_bar.start(10) 

    def _create_overlay(self):
        self.root.update_idletasks()
        self.overlay = tk.Toplevel(self.root)
        self.overlay.overrideredirect(True)
        self.overlay.transient(self.root)
        self.overlay.configure(bg='black')
        self.overlay.attributes('-alpha', 0.35)  # opacidade do fundo
        self._sync_overlay_position()
        # acompanha movimentos/redimensionamento da janela principal
        self._bind_id = self.root.bind('<Configure>', self._sync_overlay_position)

        # garante Z-order: root < overlay < modal
        self.overlay.lift(self.root)

    def _sync_overlay_position(self, event=None):
        self.root.update_idletasks()
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        # fallback se width/height vierem 1 no primeiro draw
        if w < 2 or h < 2:
            w = self.root.winfo_reqwidth()
            h = self.root.winfo_reqheight()
        self.overlay.geometry(f"{w}x{h}+{x}+{y}")
        
    def update_status(self, success: bool):
        """Para a barra de progresso e exibe a mensagem de sucesso ou erro."""
        
        self.progress_bar.stop() # Para a animação da barra
        self.progress_bar.pack_forget() # Remove a barra da tela

        if success:
            self.status_label.config(
                text="Dados Importados com sucesso!", 
                style="feedback_ok.TLabel" # Assumindo um estilo verde/sucesso
            )
        else:
            self.status_label.config(
                text="Houve um erro de Importação, por favor tente novamente.", 
                style="feedback_erro.TLabel" # Assumindo um estilo vermelho/erro
            )
            
        # Garante que o texto seja visível antes de fechar
        self.status_label.pack(pady=30) 
        
        # Retorna o controle para o Controller.

    #... (restante dos métodos aqui)...
    def _center_modal(self, window, width, height):
        # Implementação do helper de centralização (já corrigida)
        window.update_idletasks() 
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def destroy_modal(self):
        """Destrói o modal e restaura a transparência da janela principal."""
        self.progress_bar.stop() 
        self.modal.grab_release()
        self.modal.destroy()
        self.root.attributes('-alpha', 1.0)