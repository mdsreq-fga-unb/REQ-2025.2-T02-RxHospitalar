'''import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.views.components.estoque_filters import EstoqueFilterFrame
import tkinter as tk
from tkinter import ttk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Teste — Filtros de Estoque")
    root.geometry("320x640")

    style = ttk.Style()
    style.configure("Card.TFrame", background="#f4f9f4")
    style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))
    style.configure("Subtitle.TLabel", font=("Segoe UI", 11))

    frame = EstoqueFilterFrame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    root.mainloop()
'''