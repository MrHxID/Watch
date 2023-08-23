import tkinter as tk
from pathlib import Path

root = tk.Tk()
root.wm_iconbitmap(Path.cwd().joinpath("assets", "icon.ico"))
root.wm_title("Tangente Installer")


root.mainloop()
