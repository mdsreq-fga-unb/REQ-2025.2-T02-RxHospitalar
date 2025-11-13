# run.py
import tkinter as tk
# Importa o AppController do diretório de controllers dentro do pacote 'app'
from app.controllers.app_controller import AppController

if __name__ == "__main__":
    app = AppController()
    app.mainloop()