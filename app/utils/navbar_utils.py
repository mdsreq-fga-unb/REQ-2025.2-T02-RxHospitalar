import tkinter as tk
from app.views.components.loading_import_modal import LoadingImportModal
class ToolTip:
    def __init__(self, widget, text=""):
        self.widget = widget
        self.text = text
        self.tip_window = None

        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        """Exibe o tooltip ao passar o mouse."""
        if self.tip_window or not self.text:
            return

        x = self.widget.winfo_rootx() - 170
        y = self.widget.winfo_rooty() + self.widget.winfo_height() // 2

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            tw,
            text=self.text,
            justify=tk.LEFT,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Arial", 10,"bold")
        )
        label.pack(ipadx=5, ipady=3)

    def hide_tip(self, event=None):
        """Remove o tooltip ao sair do botão."""
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()


# Funções utilitárias para Header
def attach_update_tooltip(button, controller, update_hover, update_default):
    """
    Associa tooltip e hover ao botão de atualização
    """
    tooltip = ToolTip(button, "Nenhuma atualização realizada ainda.")

# Atualiza botao update ao passar o mouse

    def on_enter(event):
        button.configure(image=update_hover)
        if controller.last_update_time:
            tooltip.text = (
                "Última atualização:\n"
                + controller.last_update_time.strftime("%d/%m/%Y às %H:%M:%S")
            )
        else:
            tooltip.text = "Nenhuma atualização realizada ainda."

    def on_leave(event):
        button.configure(image=update_default)
    button.bind("<Enter>", on_enter, add="+")
    button.bind("<Leave>", on_leave, add="+")
    return tooltip

def attach_hover_image(widget, default_img, hover_img):
    """
    Associa hover simples de troca de imagem para qualquer widget
    """
    widget.bind("<Enter>", lambda e: widget.configure(image=hover_img))
    widget.bind("<Leave>", lambda e: widget.configure(image=default_img))

# Atualizar dados
def update(controller):
    if controller:
        controller.loading_import_modal = LoadingImportModal(controller)
        controller.start_data_loading(None, None)
#Sair - voltar para login
def logout(controller):
    if controller:
        controller.show_frame("LoginPage")