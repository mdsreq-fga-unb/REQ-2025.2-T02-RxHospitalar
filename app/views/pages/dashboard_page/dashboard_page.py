import tkinter as tk
from tkinter import ttk

class DashboardView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Dashboard", foreground="white").grid(padx=20, pady=20)