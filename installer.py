import shutil
import stat
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

import win32com.client
from git import Repo

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
            padx=0,
        )
        self.label.pack(side="left")
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
    def __init__(self, root: tk.Tk):
        self.main_frame = tk.Frame(root, name="main")
        self.finished_frame = tk.Frame(root, name="finished")

        tk.Label(
            self.main_frame, text="Tangente Neomatik Installation", font=("Arial", 15)
        ).place(x=200, y=00, anchor="n")
        tk.Label(self.main_frame, text="Ordner").place(x=20, y=40)
        self.var_installation_dir = tk.StringVar(
            self.main_frame,
            value=r"C:\Program Files\Tangente Neomatik",
            name="var_installation_dir",
        )
        self.e_installation_dir = tk.Entry(
            self.main_frame, textvariable=self.var_installation_dir
        )
        self.b_choose_installation_dir = tk.Button(
            self.main_frame, text="Auswählen", command=self._set_installation_dir
        )

        self.var_create_desktop_shortcut = tk.BooleanVar(
            self.main_frame, value=True, name="var_create_desktop_shortcut"
        )
        self.b_create_desktop_shortcut = tk.Checkbutton(
            self.main_frame,
            text="Desktopverknüpfung",
            variable=self.var_create_desktop_shortcut,
        )
        self.t_create_desktop_shortcut = ToolTip(
            self.b_create_desktop_shortcut,
            "Erstellt eine Verknüpfung auf dem Startbildschirm.",
        )

        self.var_autostart = tk.BooleanVar(
            self.main_frame, value=True, name="var_autostart"
        )
        self.b_create_autostart = tk.Checkbutton(
            self.main_frame, text="Autostart", variable=self.var_autostart
        )
        self.t_create_autostart = ToolTip(
            self.b_create_autostart,
            "Startet das Programm sobald der PC hochgefahren ist.",
        )

        self.var_start_menu = tk.BooleanVar(
            self.main_frame, value=True, name="var_start_menu"
        )
        self.b_start_menu = tk.Checkbutton(
            self.main_frame, text="Start Menü", variable=self.var_start_menu
        )
        self.t_start_menu = ToolTip(
            self.b_start_menu, text="Zeigt das Programm im Windows Start Menü an."
        )

        self.b_cancel = tk.Button(self.main_frame, text="Abbrechen", command=root.quit)
        self.b_install = tk.Button(
            self.main_frame,
            text="Installieren",
            command=lambda: root.after(1, self.install),
        )

        root.update()
        root.wm_deiconify()
        root.focus_set()

        self.main_frame.place(
            x=0, y=0, width=root.winfo_width(), height=root.winfo_height()
        )
        self.e_installation_dir.place(x=25, y=70, width=281)
        self.b_choose_installation_dir.place(x=306, y=67.5)
        self.b_create_desktop_shortcut.place(x=20, y=100)
        self.b_create_autostart.place(x=20, y=130)
        self.b_start_menu.place(x=20, y=160)

        self.b_cancel.place(x=30, y=460, width=160)
        self.b_install.place(x=210, y=460, width=160)

    def _set_installation_dir(self):
        dir = filedialog.askdirectory(
            initialdir=self.var_installation_dir.get(), mustexist=False
        )
        if dir == "":
            return

        self.var_installation_dir.set(dir)

    def install(self):
        directory = Path(self.var_installation_dir.get())
        if directory.exists():
            for file in directory.rglob("*"):
                file.chmod(stat.S_IRWXU)

            shutil.rmtree(directory)

        Repo.clone_from(
            r"https://github.com/MrHxID/Watch",
            directory,
        )

        if self.var_create_desktop_shortcut.get():
            self._create_shortcut(
                Path.home().joinpath("Desktop", "Tangente Neomatik.lnk")
            )

        if self.var_autostart.get():
            self._create_shortcut(
                Path.home().joinpath(
                    "AppData",
                    "Roaming",
                    "Microsoft",
                    "Windows",
                    "Start Menu",
                    "Programs",
                    "Startup",
                    "Tangente Neomatik.lnk",
                )
            )

        if self.var_start_menu.get():
            start_menu = Path.home().joinpath(
                "AppData",
                "Roaming",
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs",
            )
            start_menu.mkdir(exist_ok=True)

            self._create_shortcut(start_menu.joinpath("Tangente Neomatik.lnk"))

    def _create_shortcut(self, path: Path):
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(path))
        shortcut.targetpath = str(
            Path(self.var_installation_dir.get()).joinpath("Tangente Neomatik.exe")
        )
        shortcut.save()


app = App(root)


root.mainloop()
