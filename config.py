# config.py

import tkinter as tk

root = tk.Tk()
root.withdraw()  # Oculta a janela principal do Tkinter


SCREEN_WIDTH = root.winfo_screenwidth() 
SCREEN_HEIGHT = root.winfo_screenheight()
FPS = 60

CORES = {
    "vermelho": (255, 0, 0),
    "azul": (0, 0, 255),
    "amarelo": (255, 255, 0),
}

