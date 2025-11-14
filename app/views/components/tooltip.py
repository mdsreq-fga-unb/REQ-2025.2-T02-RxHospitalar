import tkinter as tk

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

        x = self.widget.winfo_rootx() + 40
        y = self.widget.winfo_rooty() + 25

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # remove bordas
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            tw,
            text=self.text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Arial", 10)
        )
        label.pack(ipadx=5, ipady=3)

    def hide_tip(self, event=None):
        """Remove o tooltip ao sair do botão."""
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()
