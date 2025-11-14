import tkinter as tk
from tkinter import ttk

from app.views.components.navbar import Header

class DashboardView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # ===== Header =====
        self.header = Header(self, controller)
        self.header.pack(side="top", fill="x")
        ttk.Label(self, text="Dashboard", foreground="white").pack(padx=20, pady=20)