import tkinter as tk
from tkinter import ttk
from user_controller import get_email
from utils import *
from style import configure_styles, load_logo, create_container

class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        configure_styles()
        
        container = create_container(self) 

        self.logo_photo = load_logo(container)
        
        ttk.Label(container, text="Usuário:", style="texto.TLabel").pack(pady=(45, 0), padx=(70, 0), anchor="w")
        self.username_entry = ttk.Entry(container, width=400, style="TEntry",font=("Arial", 18))
        self.username_entry.pack(pady=(17, 0), padx=70)

        ttk.Label(container, text="Senha:", style="texto.TLabel").pack(pady=(45, 0), padx=(70, 0), anchor="w")
        self.password_entry = ttk.Entry(container, show="•", width=400,font=("Arial", 18))
        self.password_entry.pack(pady=(17, 0), padx=70)

        self.show_password_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            container,
            text="Mostrar senha",
            variable=self.show_password_var,
            command=lambda: toggle_password_visibility(self.password_entry, self.show_password_var),
            style="TCheckbutton"
        ).pack(pady=(14, 0), padx=(0,73), anchor = "e")

        ttk.Button(
            container,
            text="Esqueceu a senha?",
            command=lambda: controller.show_frame("ForgotPasswordPage"),
            style="link.TButton",
            width=20
        ).pack(pady=(10,0))

        ttk.Button(
            container,
            text="Login",
            command=lambda: validate_login(
                self.username_entry.get(),
                self.password_entry.get(),
                self.feedback_label
            ),
            style="TButton",
            width = 400
        ).pack(pady=(40,10), padx=70, anchor="w")

        self.feedback_label = ttk.Label(container, text="",style="feedback_erro.TLabel")
        self.feedback_label.pack()

class ForgotPasswordPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        configure_styles()

        self.container = create_container(self)
        ttk.Button(
            self.container,
            text="Voltar ao Login",
            command=lambda: controller.show_frame("LoginPage"),
            style="back.TButton"
        ).pack(pady=(15,0), padx=(10,0), anchor="w")

        ttk.Label(self.container, text="Recuperação de Senha", style="titulo.TLabel").pack(pady=(20, 10))
        ttk.Label(self.container, text="Digite seu email:", style="texto.TLabel").pack(pady=(5,0))

        self.email_entry = ttk.Entry(self.container, width=400,font=("Arial", 18))
        self.email_entry.pack(pady=(17, 0), padx=70)


        self.submit_button = ttk.Button(
            self.container,
            text="Enviar",
            command=self.submit_email,
            style="TButton"
        )
        self.submit_button.pack(pady=(30,0))
        self.feedback_label = ttk.Label(self.container, text="",style="feedback_erro.TLabel")
        self.feedback_label.pack(pady=10)

        

    def submit_email(self):
        email = self.email_entry.get()
        if get_email() == email:
            self.feedback_label.config(style="feedback_ok.TLabel", text="Email verificado! Digite a nova senha:")
            self.submit_button.config(state="disabled")

            ttk.Label(self.container, text="Nova Senha:", style="texto.TLabel").pack()
            self.password_entry = ttk.Entry(self.container, show="•")
            self.password_entry.pack(pady=(15,0))

            self.show_password_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(
                self.container,
                text="Mostrar senha",
                variable=self.show_password_var,
                command=lambda: toggle_password_visibility(self.password_entry, self.show_password_var),
                style="TCheckbutton"
            ).pack(pady=(10,0))

            ttk.Button(
                self.container,
                text="Confirmar",
                command=lambda: update_password(
                    self.password_entry.get(),
                    self.dynamic_feedback_label,
                    self.controller
                ),
                style="TButton"
            ).pack(pady=(20,10))
            self.dynamic_feedback_label = ttk.Label(
                self.container,
                text="",  # Começa vazio
                style="feedback_ok.TLabel"
            )
            self.dynamic_feedback_label.pack(pady=(5, 0))
        else:
            self.feedback_label.config(style="feedback_erro.TLabel", text="Email não encontrado")








#ir para run.py
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema RX Hospitalar")
        self.geometry("800x800")

        # Guarda referência do frame atual
        self.current_frame = None

        # Mostra a primeira página
        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        """Cria a página do zero e exibe."""
        # Destroi o frame atual (se existir)
        if self.current_frame is not None:
            self.current_frame.destroy()

        # Mapeia o nome da página para a classe correspondente
        pages = {
            "LoginPage": LoginPage,
            "ForgotPasswordPage": ForgotPasswordPage
        }

        page_class = pages.get(page_name)
        if not page_class:
            print(f"[ERRO] Página '{page_name}' não encontrada.")
            return

        # Cria uma nova instância e mostra
        new_frame = page_class(self, self)
        new_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Atualiza a referência
        self.current_frame = new_frame



if __name__ == "__main__":
    app = App()
    app.mainloop()
