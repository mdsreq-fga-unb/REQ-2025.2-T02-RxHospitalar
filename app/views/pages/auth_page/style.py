import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

CONTAINER_WIDTH = 540
CONTAINER_HEIGHT = 745
def create_container(parent):
    container = ttk.Frame(parent, width=CONTAINER_WIDTH, height=CONTAINER_HEIGHT, relief="flat", style="container.TFrame")
    container.place(relx=0.5, rely=0.5, anchor="center")
    container.pack_propagate(False)
    return container


def configure_styles():
    style = ttk.Style()
  
     # === PALETA DE CORES ===
    cor_fundo = "#FFFFFF"
    cor_container = "#01252A"
    cor_texto = "#FFFFFF"
    cor_texto_entry = "#3A3939"
    cor_botao = "#0BC0AF"
    cor_entry= "#ACADAD"
    cor_feedback_ok = "#20F87E"
    cor_feedback_erro = "#E73522"
    cor_destaque = "#00FFE6"
    
    # === CONTAINER ===
    style.configure("container.TFrame", 
                    background=cor_container,
                    )

    # === TÍTULOS ===
    style.configure("titulo.TLabel",
                    font=("Arial", 24, "bold"),
                    foreground=cor_texto,
                    background=cor_container)

    # === TEXTOS ===
    style.configure("texto.TLabel",
                    font=("Arial", 18, "bold"),
                    foreground=cor_texto,
                    background=cor_container)
    
    # === ENTRY ===
    style.configure(
        "TEntry",
        foreground=cor_texto_entry,
        fieldbackground=cor_entry,  
        borderwidth=0,
        padding=10
    )

    style.map(
        "TEntry",
        fieldbackground=[
            ("focus", cor_fundo),      
            ("active", cor_fundo),
            ("!focus", cor_entry)
        ]
    )


    # === msg.FEEDBACK ===
    style.configure("feedback_ok.TLabel",
                    font=("Arial", 12, "bold"),
                    foreground=cor_feedback_ok,
                    background=cor_container,
                    
                    borderwidth=0
                    )
    
    style.configure("feedback_erro.TLabel",
                    font=("Arial", 12, "bold"),
                    foreground=cor_feedback_erro,
                    background=cor_container,
                   
                    borderwidth=0)

    # === LINK BUTTON ===
    style.configure("link.TButton",
                    font=("Arial", 12, "bold"),
                    foreground=cor_texto,
                    background=cor_container,
                    borderwidth=0,
                    relief="flat",
                    padding=2,
                    focuscolor="none")

    style.map("link.TButton",
              background=[("active", cor_container), ("!active", cor_container)],
              font=[("active", ("Arial", 12, "bold"))],
              foreground=[("active", (cor_destaque))]
              )
    
    # === VOLTAR BUTTON ===
    style.configure("back.TButton",
                    font=("Arial", 12, "bold"),
                    foreground=cor_texto,
                    background="#014B50",
                    padding=6,
                    focuscolor="none")
    style.map("back.TButton",
        background=[
        ("active","#011F22" )
        ],
        foreground=[
        ("active", "#00FFE6")
        ]
    )


  # === CHECKBOX ===
    style.configure("TCheckbutton",
                    background=cor_container,
                    foreground=cor_texto,
                    font=("Arial", 12),
                    borderwidth=2,
                    relief="flat",
                    focuscolor="none"
                    )
    style.map("TCheckbutton",
            background=[("active", cor_container), ("!active", cor_container)],
            foreground=[("active", cor_texto), ("!active", cor_texto)],
            indicatorcolor=[("selected", cor_botao), ("!selected", cor_fundo)])
    
    # === BUTTON ===
    style.configure(
        "TButton",
        font=("Arial", 16, "bold"),
        foreground="#FFFFFF",
        background=cor_botao,     
        borderwidth=0,
        padding=12,
        focuscolor="none"
    )

    # ====== Estado ativo (hover, pressionado) ======
    style.map(
        "TButton",
        background=[
        ("active", cor_destaque),
        ("pressed", "#009688"),
        ("disabled", "#2C2C2C")
    ],
        foreground=[
            ("disabled", "#666666"), ("active", "#000000")
        ]
    )
    

def load_logo(container, image_name="Based.png", size=(171, 196)):

    try:
        image_path = os.path.join("app", "views", "images", image_name)
        logo_image = Image.open(image_path)
        
        # Redimensiona a imagem
        logo_image = logo_image.resize(size, Image.Resampling.LANCZOS)
        
        # Converte para PhotoImage
        logo_photo = ImageTk.PhotoImage(logo_image)
        
        # Cria e empacota o label
        logo_label = tk.Label(container, image=logo_photo,bg="#01252A")
        logo_label.image = logo_photo  # Mantém referência para evitar garbage collection
        logo_label.pack(pady=(50,0))
        
        return logo_photo
    except FileNotFoundError:
        print(f"[ERRO] Imagem não encontrada: {image_path}")
        return None
    except Exception as e:
        print(f"[ERRO] Erro ao carregar imagem: {e}")
        return None