"Installer for the program"

import enum
import logging
import os
import re
import subprocess
import sys
import tkinter as tk
import traceback
import webbrowser
from pathlib import Path
from threading import Thread
from tkinter import filedialog
from winreg import HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, OpenKey, QueryValueEx

import pythoncom
import pyuac
import win32com.client

log_pyuac = logging.getLogger("pyuac")
log_pyuac.setLevel(logging.DEBUG)
log_pyuac.addHandler(logging.StreamHandler(sys.stdout))


log = logging.getLogger("tangente neomatik")
log.setLevel(logging.DEBUG)


os.environ["PATH"] += r";C:\Program Files (x86)\Microsoft\Edge\Application"

# print(os.getlogin())


def get_default_browser():
    "Returns the file path of the default browser."

    def get_browser_name() -> str:
        register_path = r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice"
        with OpenKey(HKEY_CURRENT_USER, register_path) as key:
            return str(QueryValueEx(key, "ProgId")[0])

    def format_cmd(command: str) -> str:
        exe_path = re.sub(r"(^.+exe)(.*)", r"\1", command)
        return exe_path.replace('"', "")

    def get_exe_path(name: str) -> str:
        register_path = rf"{name}\shell\open\command"
        fullpath = ""
        with OpenKey(HKEY_CLASSES_ROOT, register_path) as key:
            cmd = str(QueryValueEx(key, "")[0])
            fullpath = format_cmd(cmd)
        return fullpath

    prog_name = get_browser_name()
    return get_exe_path(prog_name)


class InstallFlags(enum.IntFlag):
    inprogress = 0b0000
    finished = 0b0001
    failed = 0b0010


class ToolTip:
    def __init__(self, widget, text, **kwargs):
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
    def __init__(self, **kwargs):
        self.home_path = Path(kwargs.get("home_path", Path.home()))

        self.root = tk.Tk()
        screen_w, screen_h = (
            self.root.winfo_screenwidth(),
            self.root.winfo_screenheight(),
        )
        w, h = 400, 500
        try:
            # make use of pyinstallers --add-data assets\icon.ico
            base_path = Path(sys._MEIPASS)
        except:
            base_path = Path.cwd()

        self.root.after(
            1, lambda: self.root.wm_iconbitmap(base_path / "assets" / "icon.ico")
        )

        self.root.wm_title("Tangente Neomatik Installieren")
        self.root.wm_geometry(f"{w}x{h}+{(screen_w - w) // 2}+{(screen_h - h) // 2}")
        self.root.wm_resizable(False, False)

        self.main_frame = tk.Frame(self.root, name="main")
        self.finished_frame = tk.Frame(self.root, name="finished")
        self.failed_frame = tk.Frame(self.root, name="failed")

        tk.Label(
            self.main_frame, text="Tangente Neomatik Installation", font=("Arial", 15)
        ).place(x=200, y=20, anchor="n")
        tk.Label(self.main_frame, text="Ordner").place(x=20, y=60)
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

        self.b_cancel = tk.Button(
            self.main_frame, text="Abbrechen", command=self.root.quit
        )
        self.b_install = tk.Button(
            self.main_frame,
            text="Installieren",
            command=self._wrap_install,
        )

        self.root.update()

        self.main_frame.place(
            x=0, y=0, width=self.root.winfo_width(), height=self.root.winfo_height()
        )
        self.e_installation_dir.place(x=25, y=90, width=281)
        self.b_choose_installation_dir.place(x=306, y=87.5)
        self.b_create_desktop_shortcut.place(x=20, y=120)
        self.b_create_autostart.place(x=20, y=150)
        self.b_start_menu.place(x=20, y=180)

        self.b_cancel.place(x=30, y=460, width=160)
        self.b_install.place(x=210, y=460, width=160)

        # finished Frame

        tk.Label(
            self.finished_frame, text="Installation abgeschlossen", font=("Arial", 15)
        ).place(x=200, y=20, anchor="n")

        tk.Button(self.finished_frame, text="Schließen", command=self.root.quit).place(
            x=210, y=460, width=160
        )

        # failed frame
        tk.Label(
            self.failed_frame,
            text="Installation fehlgeschlagen",
            font=("Arial", 15),
        ).place(x=200, y=20, anchor="n")
        tk.Label(
            self.failed_frame,
            text='Mehr Informationen: Öffnen Sie die Datei "Tangente Neomatik.log". Melden Sie den '
            "Inhalt der Datei als Problem unter",
            wraplength=self.root.winfo_width() - 20,
            justify="left",
        ).place(x=10, y=60)
        self.e_github_link = tk.Label(
            self.failed_frame,
            text="https://github.com/MrHxID/Watch/issues",
            fg="#0000ff",
        )
        self.e_github_link.bind(
            "<Button-1>",
            lambda _: webbrowser.open_new_tab("https://github.com/MrHxID/Watch/issues"),
        )

        tk.Label(
            self.failed_frame,
            text="zusammen mit einer Beschreibung, was Sie versucht haben.",
            wraplength=self.root.winfo_width() - 20,
            justify="left",
        ).place(x=10, y=130)

        tk.Button(self.failed_frame, text="Abbrechen", command=self.root.quit).place(
            x=30, y=460, width=160
        )
        tk.Button(self.failed_frame, text="Wiederholen", command=self._retry).place(
            x=210, y=460, width=160
        )

        self.e_github_link.place(x=10, y=100)

        self.root.wm_deiconify()
        # root.focus_set()
        # root.lift()

    def start(self):
        self.root.mainloop()

    def _set_installation_dir(self):
        dir = filedialog.askdirectory(
            initialdir=self.var_installation_dir.get(), mustexist=False
        )
        if dir == "":
            return

        self.var_installation_dir.set(dir)

    def _wrap_install(self):
        self.root.attributes("-disabled", True)
        self.e_installation_dir.configure(state="disabled")
        self.b_choose_installation_dir.configure(state="disabled")
        self.b_create_desktop_shortcut.configure(state="disabled")
        self.b_create_autostart.configure(state="disabled")
        self.b_start_menu.configure(state="disabled")
        self.b_cancel.configure(state="disabled")
        self.b_install.configure(state="disabled")

        flags = [InstallFlags.inprogress]

        def try_install(flags):
            try:
                self.install()
            except Exception:
                if not log.handlers:
                    log.addHandler(
                        logging.StreamHandler(
                            open("Tangente Neomatik.log", "a", encoding="utf-8")
                        )
                    )

                log.debug(traceback.format_exc())
                log.debug(
                    "Installation directory:\n"
                    f"{self.var_installation_dir.get()}\n\n"
                    "Options:\n"
                    f"  -desktop: {self.var_create_desktop_shortcut.get()}\n"
                    f"  -auto start: {self.var_autostart.get()}\n"
                    f"  -start menu: {self.var_start_menu.get()}\n"
                    f"==================================================\n"
                )

                flags[0] |= InstallFlags.failed
            finally:
                flags[0] |= InstallFlags.finished

        Thread(target=try_install, daemon=True, kwargs={"flags": flags}).start()

        def _check_flags():
            nonlocal flags

            if flags[0] & InstallFlags.failed:
                # The installation failed
                print("failed")
                self.root.attributes("-disabled", False)
                self.main_frame.place_forget()
                self.failed_frame.place(
                    x=0,
                    y=0,
                    width=self.root.winfo_width(),
                    height=self.root.winfo_height(),
                )
            elif (
                flags[0] & InstallFlags.finished and not flags[0] & InstallFlags.failed
            ):
                # The installation is complete
                self.root.attributes("-disabled", False)
                self.main_frame.place_forget()
                self.finished_frame.place(
                    x=0,
                    y=0,
                    width=self.root.winfo_width(),
                    height=self.root.winfo_height(),
                )
            else:
                # Check again
                self.root.after(100, _check_flags)

        _check_flags()

    def _retry(self):
        self.e_installation_dir.configure(state="normal")
        self.b_choose_installation_dir.configure(state="normal")
        self.b_create_desktop_shortcut.configure(state="normal")
        self.b_create_autostart.configure(state="normal")
        self.b_start_menu.configure(state="normal")
        self.b_cancel.configure(state="normal")
        self.b_install.configure(state="normal")

        self.failed_frame.place_forget()

        self.main_frame.place(
            x=0,
            y=0,
            width=self.root.winfo_width(),
            height=self.root.winfo_height(),
        )

    def install(self):
        directory = Path(self.var_installation_dir.get())
        directory.mkdir(exist_ok=True)

        self._download_file("Tangente Neomatik.exe")
        # ? Don't need to download installer
        # self._download_file("Installer.exe")

        (directory / "settings").mkdir(exist_ok=True)

        self._download_file("settings/settings.json")

        # Desktop Shortcut
        if self.var_create_desktop_shortcut.get():
            self._create_shortcut(
                self.home_path.joinpath("Desktop", "Tangente Neomatik.lnk")
            )

        # Auto Start
        if self.var_autostart.get():
            self._create_shortcut(
                self.home_path.joinpath(
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

        # Start Menu
        if self.var_start_menu.get():
            self._create_shortcut(
                self.home_path.joinpath(
                    "AppData",
                    "Roaming",
                    "Microsoft",
                    "Windows",
                    "Start Menu",
                    "Programs",
                    "Tangente Neomatik.lnk",
                )
            )

    def _download_file(self, rel_path: Path, timeout=180):
        directory = Path(self.var_installation_dir.get())

        github_base = "https://raw.githubusercontent.com/MrHxID/Watch/main/"

        uri = github_base + Path(rel_path).as_posix()
        subprocess.run(
            [
                "powershell",
                "-Command",
                "wget",
                "-UseBasicParsing",
                "-Uri",
                f'"{uri}"',
                "-OutFile",
                f'"{directory / rel_path}"',
            ],
            shell=True,
            timeout=timeout,
            check=True,
        )

    def _create_shortcut(self, path: Path):
        shell = win32com.client.Dispatch("WScript.Shell", pythoncom.CoInitialize())
        shortcut = shell.CreateShortCut(str(path))
        shortcut.Targetpath = str(
            Path(self.var_installation_dir.get()).joinpath("Tangente Neomatik.exe")
        )
        shortcut.WorkingDirectory = self.var_installation_dir.get()
        shortcut.save()


if not pyuac.isUserAdmin():
    pyuac.runAsAdmin(
        cmdLine=[sys.executable]
        + sys.argv
        + ["--browser", get_default_browser(), "--home-path", Path.home()]
    )

else:
    if "--browser" in sys.argv:
        os.environ["PATH"] += ";" + str(
            Path(sys.argv[sys.argv.index("--browser") + 1]).parent
        )

    if "--home-path" in sys.argv:
        home_path = sys.argv[sys.argv.index("--home-path") + 1]

    else:
        home_path = Path.home()

    app = App(home_path=home_path)
    app.start()
