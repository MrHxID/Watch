from pathlib import Path
import json
import src
from typing import Any


def _file():
    return Path.cwd().joinpath("settings", "settings.json")


def load() -> dict[str, Any]:
    with open(_file(), "r") as file:
        settings = json.load(file)

    ret = default()
    ret.update(settings)

    return ret


def set(new_settings):
    with open(_file(), "w") as file:
        json.dump(new_settings, file, indent=4)

    ret = default()
    ret.update(new_settings)

    src.settings_dict = ret


def reset():
    set(default())


def default():
    return {
        "fps": 30,
        "slumber fps": 5,
        "sleep fps": 30,
        "slumber enabled": True,
    }
