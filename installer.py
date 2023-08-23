import tkinter as tk
from pathlib import Path
import git
from tkinter import filedialog


root = tk.Tk()
screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
w, h = 400, 500
root.after(
    1,
    lambda: root.wm_iconbitmap(Path.cwd().joinpath("assets", "icon.ico")),
)
root.wm_title("Tangente Installer")
root.wm_geometry(f"{w}x{h}+{(screen_w - w) // 2}+{(screen_h - h) // 2}")
root.wm_resizable(False, False)


def _set_instalation_dir():
    variable = tk.StringVar(root, name="var_installation_dir")
    print(variable.get())


class ToolTip:
    def __init__(self, widget: tk.Widget, text, **kwargs):
        self.widget = widget
        self.text = text
        self.tipwindow = None

        self.width = kwargs.get("width", 200)
        self.height = kwargs.get("height", None)
        self._ready = True

        self.widget.bind(
            "<Enter>", lambda ev: self.widget.after(500, lambda: self.show(ev))
        )
        self.widget.bind("<Enter>", self._set_ready, add="+")

        self.widget.bind("<Leave>", self.hide)

    def show(self, event):
        if self.tipwindow or not self.text or self._ready:
            return

        x = self.widget.winfo_rootx() + self.widget.winfo_width()
        y = self.widget.winfo_rooty() + self.widget.winfo_height()

        self.tipwindow = tk.Toplevel(self.widget)
        self.tipwindow.wm_overrideredirect(True)
        self.label = tk.Label(
            self.tipwindow,
            text=self.text,
            width=self.width,
            wraplength=self.width,
            bg="#ffffe0",
            relief="solid",
            justify="left",
            bd=1,
            padx=0
        )
        self.label.pack(ipadx=1)
        self.label.update()
        self.height = self.label.winfo_height()

        self.tipwindow.wm_geometry(f"{self.width}x{self.height}+{x}+{y}")

    def hide(self, event):
        if self.tipwindow:
            self.tipwindow.destroy()

        self.tipwindow = None
        self._ready = True

    def _set_ready(self, event):
        self._ready = False


class App:
    def __init__(self, root):
        tk.Label(root, text="Tangente Neomatik Installation", font=("Arial", 15)).place(
            x=200, y=00, anchor="n"
        )
        tk.Label(root, text="Ordner").place(x=20, y=40)
        self.var_installation_dir = tk.StringVar(
            root,
            value=r"C:\Program Files\Tangente Neomatik",
            name="var_installation_dir",
        )
        self.e_installation_dir = tk.Entry(root, textvariable=self.var_installation_dir)
        self.b_choose_installation_dir = tk.Button(
            root, text="Auswählen", command=self._set_installation_dir
        )

        self.var_create_desktop_shortcut = tk.BooleanVar(
            root, value=True, name="var_create_desktop_shortcut"
        )
        self.b_create_desktop_shortcut = tk.Checkbutton(
            root,
            text="Desktopverknüpfung",
            variable=self.var_create_desktop_shortcut,
        )
        self.t_create_desktop_shortcut = ToolTip(
            self.b_create_desktop_shortcut,
            "Erstellt eine Verknüpfung auf dem Startbildschirm.",
        )

        self.var_autostart = tk.BooleanVar(root, value=True, name="var_autostart")
        self.b_create_autostart = tk.Checkbutton(
            root, text="Autostart", variable=self.var_autostart
        )
        self.t_create_autostart = ToolTip(
            self.b_create_autostart,
            "Startet das Programm sobald der PC hochgefahren ist.",
        )

        self.var_start_menu = tk.BooleanVar(root, value=True, name="var_start_menu")
        self.b_start_menu = tk.Checkbutton(
            root, text="Start Menü", variable=self.var_start_menu
        )

        self.e_installation_dir.place(x=25, y=70, width=281)
        self.b_choose_installation_dir.place(x=306, y=67.5)
        self.b_create_desktop_shortcut.place(x=20, y=100)
        self.b_create_autostart.place(x=20, y=130)
        self.b_start_menu.place(x=20, y=160)

        tk.Button(root, text="Abbrechen", command=root.quit).place(
            x=30, y=460, width=160
        )

    def _set_installation_dir(self):
        dir = filedialog.askdirectory(
            initialdir=self.var_installation_dir.get(), mustexist=False
        )
        if dir == "":
            return

        self.var_installation_dir.set(dir)


app = App(root)

root.mainloop()
