import tkinter as tk
from pathlib import Path
import pyuac
import sys


class App:
    def __init__(self, **kwargs):
        self.home_path = Path(kwargs.get("home_path", Path.home()))

        self.root = tk.Tk()
        self.root.wm_geometry(f"400x500+{(1920 - 400) // 2}+{(1080 - 500) // 2}")
        self.root.wm_title("Tangente Neomatik Deinstallieren")
        try:
            # make use of pyinstallers --add-data assets\icon.ico
            base_path = Path(sys._MEIPASS)
        except:
            base_path = Path.cwd()

        self.root.after(
            1, lambda: self.root.wm_iconbitmap(base_path / "assets" / "icon.ico")
        )
        self.root.wm_resizable(False, False)

        tk.Label(
            self.root, text="Tangente Neomatik Deinstallation", font=("Arial", 15)
        ).place(x=200, y=20, anchor="n")

        self.var_desktop = tk.BooleanVar(self.root)
        self._find_file(
            self.home_path.joinpath("Desktop", "Tangente Neomatik.lnk"),
            self.var_desktop,
        )

        self.b_desktop = tk.Checkbutton(
            self.root,
            text="Desktop Verknüpfung",
            variable=self.var_desktop,
            state="disabled",
        )

        self.var_autostart = tk.BooleanVar(self.root)
        self._find_file(
            self.home_path.joinpath(
                "AppData",
                "Roaming",
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs",
                "Startup",
                "Tangente Neomatik.lnk",
            ),
            self.var_autostart,
        )

        self.b_autostart = tk.Checkbutton(
            self.root, text="Autostart", variable=self.var_autostart, state="disabled"
        )

        self.var_start_menu = tk.BooleanVar(self.root)
        self._find_file(
            self.home_path.joinpath(
                "AppData",
                "Roaming",
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs",
                "Tangente Neomatik.lnk",
            ),
            self.var_start_menu,
        )

        self.b_start_menu = tk.Checkbutton(
            self.root, text="Start Menü", variable=self.var_start_menu, state="disabled"
        )

        self.b_desktop.place(x=25, y=60)
        self.b_autostart.place(x=25, y=90)

    @staticmethod
    def _find_file(path, variable: tk.BooleanVar = None):
        path = Path(path)
        if path.exists():
            if variable:
                variable.set(True)

            return True

        return False


if not pyuac.isUserAdmin():
    pyuac.runAsAdmin(cmdLine=[sys.executable] + sys.argv + ["--home-path", Path.home()])
else:
    if "--home-path" in sys.argv:
        home_path = sys.argv[sys.argv.index("--home-path") + 1]
    else:
        home_path = Path.home()

    app = App(home_path=home_path)
    app.root.mainloop()
