# import base64
import enum
import logging
import os
import re
import shutil
import stat
import subprocess
import sys
import tkinter as tk
import traceback
import webbrowser
from pathlib import Path
from threading import Thread
from tkinter import filedialog
from winreg import HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, OpenKey, QueryValueEx

import pyuac
import win32com.client

icon_data = "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAxHpUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjabVDbDcMgDPz3FB0BbAfMOKRJpW7Q8XvEThSqnoRfh84P2j/vFz0GOCvpUq20UhKgTRt3BJYc/bA56WEPaFDIpzpdBKMk8OKplfh/1vMl4K4jWm5C9gxinYkWHdh+hKKRjIkYwRZCLYSEncgh0H2tVJrV+wrrnmaYPxqmlnns31wrrrct6CPMu2RJsCLqA8h4QtIRGKwIzoFPipjhR/1cCQf5d6cT9AXfiFkNABlJnAAAAYRpQ0NQSUNDIHByb2ZpbGUAAHicfZE9SMNAHMVfU6VFKg7NICKYoTrZRUUcSxWLYKG0FVp1MLn0C5q0JCkujoJrwcGPxaqDi7OuDq6CIPgB4uripOgiJf4vKbSI8eC4H+/uPe7eAUKryjSzLwZoumWkE3Epl1+VAq8IYgwhiAjLzKwnM4tZeI6ve/j4ehflWd7n/hyDasFkgE8ijrG6YRFvEM9uWnXO+8QiK8sq8TnxpEEXJH7kuuLyG+eSwwLPFI1sep5YJJZKPaz0MCsbGvEMcUTVdMoXci6rnLc4a9UG69yTvzBU0FcyXKc5igSWkEQKEhQ0UEEVFqK06qSYSNN+3MM/4vhT5FLIVQEjxwJq0CA7fvA/+N2tWZyecpNCcaD/xbY/xoHALtBu2vb3sW23TwD/M3Cld/21FjD3SXqzq0WOgKFt4OK6qyl7wOUOMPxUlw3Zkfw0hWIReD+jb8oD4VtgYM3trbOP0wcgS10t3wAHh8BEibLXPd4d7O3t3zOd/n4AnHlyt1OB1TIAAA12aVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/Pgo8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA0LjQuMC1FeGl2MiI+CiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIKICAgIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiCiAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgICB4bWxuczpHSU1QPSJodHRwOi8vd3d3LmdpbXAub3JnL3htcC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgeG1wTU06RG9jdW1lbnRJRD0iZ2ltcDpkb2NpZDpnaW1wOmJmMDZmNzQ5LWJjMGYtNGYxMi1iZTJlLWU2OTdlOGI5N2U4YSIKICAgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo1Yjg0Nzg3NC01NGZhLTRjZDQtOGJhZC1mOGE0YmUwYmZjYTMiCiAgIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDoxZTJlMjljZi0yNTc0LTRmOTQtOGU0NC0wZTAyN2NjMzNkMDEiCiAgIGRjOkZvcm1hdD0iaW1hZ2UvcG5nIgogICBHSU1QOkFQST0iMi4wIgogICBHSU1QOlBsYXRmb3JtPSJXaW5kb3dzIgogICBHSU1QOlRpbWVTdGFtcD0iMTY5MzQ4NDQ3MDkxNDc2MCIKICAgR0lNUDpWZXJzaW9uPSIyLjEwLjM0IgogICB0aWZmOk9yaWVudGF0aW9uPSIxIgogICB4bXA6Q3JlYXRvclRvb2w9IkdJTVAgMi4xMCIKICAgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMzowODozMVQxNDoyMTowMyswMjowMCIKICAgeG1wOk1vZGlmeURhdGU9IjIwMjM6MDg6MzFUMTQ6MjE6MDMrMDI6MDAiPgogICA8eG1wTU06SGlzdG9yeT4KICAgIDxyZGY6U2VxPgogICAgIDxyZGY6bGkKICAgICAgc3RFdnQ6YWN0aW9uPSJzYXZlZCIKICAgICAgc3RFdnQ6Y2hhbmdlZD0iLyIKICAgICAgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo4YzlhZTU1Zi0yN2Q0LTRlM2EtOGE5ZS0yNjAwYWY4NGRmYWIiCiAgICAgIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkdpbXAgMi4xMCAoV2luZG93cykiCiAgICAgIHN0RXZ0OndoZW49IjIwMjMtMDgtMzFUMTQ6MjE6MTAiLz4KICAgIDwvcmRmOlNlcT4KICAgPC94bXBNTTpIaXN0b3J5PgogIDwvcmRmOkRlc2NyaXB0aW9uPgogPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgIAo8P3hwYWNrZXQgZW5kPSJ3Ij8+Q6bIfgAAAAZiS0dEAAAAAAAA+UO7fwAAAAlwSFlzAAAuGAAALhgBKqonIAAAAAd0SU1FB+cIHwwVCiHle/wAABc5SURBVHjazZvZcxvX2eZ/p1c00EADIEiKuyVKomhLjj22lZqkcpGaqrnIn5DL/GG5ycVcuWrmu/qSmtjlzOfPil2JLVu7RJkiKe4LdvR6zlz0QlBLvMjJp3ahRAONRp/3vNvzPG+L0WikeMXjyZMNNre2KDslpqam0HUdTdPQNA0hRPHKD6XUC98f/yw/pJRIKYnjGCklh4eHgOCNN96gVqu+6q1j8BMcvu8T+CMs0ziz6Pxv4Mxixw0APHeeUurMefnnUkp6vS6+H9GanHx9DBBFIUCxS7quFwvIF5EvKj/GPeDZ8579jpSyuB4IEAJ/NPopbv2nMUC/3wcgCAL6/T62bZ/Z7fFDSlksTtO04t9nQyI3xHhoAGl4iZggCF4fA1iWRRzH3Lt3jwcPHqBpGgBhGCKlfC4fjOcIwzDQdR1d1wtj5N9XSiGlJEkSlFKFZ83O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"

# icon_path = Path.cwd() / "assets" / "logo.png"

# binary_data = open(icon_path, "rb").read()
# base64_utf8 = base64.b64encode(binary_data).decode("utf-8")

# with open(Path.cwd() / "assets" / "temp.txt", "w") as file:
#     file.write(base64_utf8)

log_pyuac = logging.getLogger("pyuac")
log_pyuac.setLevel(logging.DEBUG)
log_pyuac.addHandler(logging.StreamHandler(sys.stdout))


log = logging.getLogger("tangente neomatik")
log.setLevel(logging.DEBUG)


os.environ["PATH"] += ";C:\Program Files (x86)\Microsoft\Edge\Application"

# print(os.getlogin())


def get_default_browser():
    def get_browser_name() -> str:
        register_path = r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice"
        with OpenKey(HKEY_CURRENT_USER, register_path) as key:
            return str(QueryValueEx(key, "ProgId")[0])

    def format_cmd(s: str) -> str:
        exe_path = re.sub(r"(^.+exe)(.*)", r"\1", s)
        return exe_path.replace('"', "")

    def get_exe_path(name: str) -> str:
        register_path = r"{}\shell\open\command".format(name)
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
    def __init__(self):
        self.root = tk.Tk()
        screen_w, screen_h = (
            self.root.winfo_screenwidth(),
            self.root.winfo_screenheight(),
        )
        w, h = 400, 500
        # ? What was I even thinking? The installer should be a standalone program
        # ? that does not rely on outside data like icon files
        # self.root.after(
        #     1,
        #     lambda: self.root.wm_iconbitmap(Path.cwd().joinpath("assets", "icon.ico")),
        # )
        self.root.after(
            1, lambda: self.root.wm_iconphoto(True, tk.PhotoImage(data=icon_data))
        )

        self.root.wm_title("Tangente Installer")
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
            self.failed_frame, text="Installation fehlgeschlagen", font=("Arial", 15)
        ).place(x=200, y=20, anchor="n")
        tk.Label(
            self.failed_frame,
            text='Mehr Informationen: Öffnen Sie die Datei "Tangente Neomatik.log". Reichen Sie den Inhalt'
            "der Datei als Problem unter",
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
        # subprocess.run("start /max firefox https://www.python.org", shell=True)
        tk.Label(
            self.failed_frame,
            text="ein zusammen mit einer Beschreibung, was Sie versucht haben.",
        ).place(x=10, y=100)

        self.e_github_link.place(x=10, y=80)

        self.root.wm_deiconify()
        # root.focus_set()
        # root.lift()

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
            except:
                log.addHandler(
                    logging.StreamHandler(open("Tangente Neomatik.log", "a"))
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

                # Clean up temporary files
                directory = Path(self.var_installation_dir.get())
                (directory / "downloaded.zip").unlink(missing_ok=True)

                temp_dir = directory / "downloaded"

                for file in temp_dir.rglob("*"):
                    file.chmod(stat.S_IRWXU)

                shutil.rmtree(temp_dir)

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

    def install(self):
        # ! Remove for download. The inevitable RuntimeError is for developing
        # ! self.failed_frame
        # TODO Remove "raise RuntimeError"
        raise RuntimeError
        directory = Path(self.var_installation_dir.get())
        if directory.exists():
            for file in directory.rglob("*"):
                # print(file)
                file.chmod(stat.S_IRWXU)

            directory.chmod(stat.S_IRWXU)
            shutil.rmtree(directory)

        directory.mkdir(exist_ok=True)

        subprocess.run(
            [
                "powershell",
                "-Command",
                "wget",
                "-UseBasicParsing",
                "-Uri",
                '"https://github.com/MrHxID/Watch/archive/refs/heads/main.zip"',
                "-OutFile",
                f'"{directory / "downloaded.zip"}"',
            ]
        )

        subprocess.run(
            [
                "powershell",
                "-Command",
                "cd",
                f'"{directory}";&',
                "Expand-Archive",
                "downloaded.zip",
                "-Force",
            ]
        )

        repo = next((directory / "downloaded").glob("*"))

        # * Hardcoded version
        # ! deprecated
        # for file in (temp_dir / "downloaded" / "Watch-main").glob("*"):
        # * when unpacking there is only one subdirectory "Watch-main". However since the
        # * name of this directory might change it's better to use the first subdirectory
        # * instead

        for file in repo.glob("*"):
            # ///     print(file)
            shutil.move(file, directory)

        # ! deprecated no longer includes ".git" folder
        # // for file in (directory / ".git").rglob("*"):
        # //     file.chmod(stat.S_IRWXU)

        # // shutil.rmtree(directory / ".git")

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


if not pyuac.isUserAdmin():
    pyuac.runAsAdmin(
        cmdLine=[sys.executable] + sys.argv + ["--browser", get_default_browser()]
    )

else:
    if "--browser" in sys.argv:
        os.environ["PATH"] += ";" + str(
            Path(sys.argv[sys.argv.index("--browser") + 1]).parent
        )

    app = App()
    app.root.mainloop()
