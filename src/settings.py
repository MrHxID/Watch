from pathlib import Path
import json
import src
from typing import Any


def _file():
    return Path.cwd().joinpath("settings", "settings.json")


def load() -> dict[str, Any]:
    try:
        with open(_file(), "r") as file:
            settings = json.load(file)
    except FileNotFoundError:
        set(default())
        return load()

    ret = default()
    ret.update(settings)

    return ret


def set(new_settings: dict):
    """Puts `new_settings` into the `settings.json` file 1:1 and makes
    them available in `src.settings_dict`."""

    new_settings = dict(new_settings)
    with open(_file(), "w") as file:
        json.dump(new_settings, file, indent=4)
        set_str = """// Die 'fps' - Werte geben Maximalwerte für die Bildfrequenz des Programms an.
// Höhere Werte entsprechen einer geschmeidigeren Anzeige, niedrige Werte
// reduzieren den Stromverbrauch und die benötigte Rechenleistung.
// Für unbegrenzte Bildfrequenz (beste Anzeige, höchster Stromverbrauch) setze den
// entsprechenden Wert auf 0.
"""

    ret = default()
    ret.update(new_settings)

    src.settings_dict = ret


def update(new_settings):
    """Puts `new_settings` into the `settings.json` file and copies
    all settings not explicitly specified."""

    src.settings_dict.update(new_settings)

    set(src.settings_dict)


def reset():
    set(default())


def default():
    return {
        "fps": 30,
        "slumber fps": 5,
        "sleep fps": 30,
        "slumber enabled": True,
    }
