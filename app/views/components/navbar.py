import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path
from app.utils.navbar_utils import ToolTip, attach_update_tooltip, attach_hover_image, update, logout

class Header(ttk.Frame):
    def __init__(self, parent, controller=None):

        # --- Frame externo (borda) ---
        border_frame = tk.Frame(parent, bg="#046C62", height=100)
        border_frame.pack(side="top", fill="x")
        border_frame.pack_propagate(False)

        super().__init__(border_frame, style='Header.TFrame')
        self.controller = controller
        self.pack(fill="both", expand=True, padx=0, pady=(0,9))

        # === Estilos ===
        style = ttk.Style()
        style.configure('Header.TFrame', background="#01252A", side="top")
        style.configure('HeaderTitle.TLabel', font=('Arial', 16, 'bold'))

        # --- Estilo para botões de imagem ---
        style.configure(
            "Icon.TButton",
            background="#01252A",
            borderwidth=0,
            relief="flat"
        )
        style.map("Icon.TButton",
                background=[("active", "#01252A")],
                relief=[("pressed", "flat"), ("active", "flat")])

        # === Ícone navbar ===
        img_path = Path(__file__).resolve().parent.parent / "images" / "Logo=NavBar.png"
        img = Image.open(img_path).resize((171, 80))
        self.logo = ImageTk.PhotoImage(img)

        logo_label = ttk.Label(self, image=self.logo, background="#01252A",cursor="hand2")
        logo_label.pack(side="left", padx=(80,0) )

        logo_label.bind("<Button-1>", lambda e: self.controller.show_frame("DashboardView"))

        # --- Carregar icones de navegação ---
        img_dir = Path(__file__).resolve().parent.parent / "images"

        notifi_off = ImageTk.PhotoImage(Image.open(img_dir / "Notification=Off.png").resize((60, 60)))
        profile_default = ImageTk.PhotoImage(Image.open(img_dir / "profile=Default.png").resize((60, 60)))
        update_default = ImageTk.PhotoImage(Image.open(img_dir / "Update=Default.png").resize((60, 60)))
        notifi_off_hover = ImageTk.PhotoImage(Image.open(img_dir / "Notification=Off Hover.png").resize((60, 60)))
        profile_hover = ImageTk.PhotoImage(Image.open(img_dir / "profile=Selected.png").resize((60, 60)))
        update_hover = ImageTk.PhotoImage(Image.open(img_dir / "Update=Selected.png").resize((60, 60)))
        # Guardar imagens para não serem destruídas
        self.notifi_off = notifi_off
        self.profile_default = profile_default
        self.update_default = update_default
        self.notifi_off_hover = notifi_off_hover
        self.profile_hover = profile_hover
        self.update_hover = update_hover

        # === Conteúdo ===
        buttons_frame = ttk.Frame(self, style="Header.TFrame")
        buttons_frame.pack(side="right")

        # atualizar
        update_btn = ttk.Button(buttons_frame, image=self.update_default, command=lambda:update(self.controller),
                                style="Icon.TButton",cursor="hand2")
        update_btn.grid(row=0, column=0, padx=5)
        self.update_tooltip = attach_update_tooltip(update_btn, self.controller, self.update_hover, self.update_default)


        # dropdown 1: notificacao
        config_btn = ttk.Menubutton(buttons_frame, image=self.notifi_off,style="Icon.TButton",cursor="hand2")
        config_btn.bind("<Enter>", lambda e: config_btn.configure(image=self.notifi_off_hover))
        config_btn.bind("<Leave>", lambda e: config_btn.configure(image=self.notifi_off))
        config_menu = tk.Menu(config_btn, tearoff=0)
        config_menu.add_command(label="Notificações", command=lambda: print("Notif"))
        config_btn["menu"] = config_menu
        config_btn.grid(row=0, column=1, padx=5)

        # dropdown 2: sair
        profile_btn = ttk.Menubutton(buttons_frame, image=self.profile_default,style="Icon.TButton", cursor="hand2")
        profile_btn.bind("<Enter>", lambda e: profile_btn.configure(image=self.profile_hover))
        profile_btn.bind("<Leave>", lambda e: profile_btn.configure(image=self.profile_default))

        profile_menu = tk.Menu(profile_btn, tearoff=0,
                               bg="#FBFFFC",
                               fg="#01252A",
                               activebackground="#45934C",
                               activeforeground="#FBFFFC",
                               font=("Arial", 15, "bold"),
                               bd=2,
                               relief="solid")
        profile_menu.add_command(label="Sair", command=lambda: logout(self.controller))
        profile_btn["menu"] = profile_menu
        profile_btn.grid(row=0, column=2, padx=5)