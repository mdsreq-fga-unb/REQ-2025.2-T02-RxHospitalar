#funções auxiliares login

from app.controllers.login_controller import get_user, change_password

def toggle_password_visibility(password_entry, show_password_var):
    if show_password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="•")

def validate_login(username, password, feedback_label):
    if get_user(username, password):
        feedback_label.config(style="feedback_ok.TLabel", text="Login bem-sucedido!")
        return True
    else:
        feedback_label.config(style="feedback_erro.TLabel",text="Usuário ou senha incorretos.")
        return False


def update_password(password_entry, feedback_label, controller):
    new_password = password_entry
    if change_password(new_password):                          #futuramente validação da senha
        feedback_label.config(style="feedback_ok.TLabel", text="Senha alterada com sucesso!")
        feedback_label.after(1000, lambda: controller.show_frame("LoginPage"))
        return True
    else:
        feedback_label.config(style="feedback_erro.TLabel", text="Erro ao alterar a senha.")
        return False
