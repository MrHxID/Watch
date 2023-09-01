import sys
from pathlib import Path

import pygame as pg


def load_sheet(file: str):
    try:
        try:
            # use pyinstallers --add-data
            base_path = Path(sys._MEIPASS)
        except:
            base_path = Path.cwd()

        path = base_path / "assets" / file

        sheet = pg.image.load(path)
    except FileNotFoundError as err:
        raise FileNotFoundError(f"Could not find the sprite sheet: {''.join(err.args)}")

    except:
        sheet = pg.Surface((0, 0), pg.SRCALPHA)

    return sheet


def load_sprite(*rect, sheet, transparent: bool = True):
    rect = pg.Rect(*rect)

    flags = pg.SRCALPHA * transparent
    sprite = pg.Surface(rect.size, flags)
    sprite.blit(sheet, (0, 0), rect)

    return sprite


_sprite_sheet = load_sheet("Sprites.png")

CASING = load_sprite(0, 0, 1920, 1080, transparent=False, sheet=_sprite_sheet)
HOUR_HAND = load_sprite(1920, 0, 73, 323, sheet=_sprite_sheet)
HOUR_HAND_SHADOW = load_sprite(1993, 0, 73, 323, sheet=_sprite_sheet)
MINUTE_HAND = load_sprite(2066, 0, 63, 471, sheet=_sprite_sheet)
MINUTE_HAND_SHADOW = load_sprite(2129, 0, 63, 471, sheet=_sprite_sheet)
AXLE = load_sprite(2192, 0, 23, 23, sheet=_sprite_sheet)
SECONDS_HAND = load_sprite(2192, 23, 31, 167, sheet=_sprite_sheet)
N_0 = load_sprite(1920, 471, 39, 56, sheet=_sprite_sheet)
N_1 = load_sprite(1959, 471, 39, 56, sheet=_sprite_sheet)
N_2 = load_sprite(1998, 471, 39, 56, sheet=_sprite_sheet)
N_3 = load_sprite(2037, 471, 39, 56, sheet=_sprite_sheet)
N_4 = load_sprite(2076, 471, 39, 56, sheet=_sprite_sheet)
N_5 = load_sprite(1920, 528, 39, 56, sheet=_sprite_sheet)
N_6 = load_sprite(1959, 528, 39, 56, sheet=_sprite_sheet)
N_7 = load_sprite(1998, 528, 39, 56, sheet=_sprite_sheet)
N_8 = load_sprite(2037, 528, 39, 56, sheet=_sprite_sheet)
N_9 = load_sprite(2076, 528, 39, 56, sheet=_sprite_sheet)

NUMBERS: dict[str, pg.Surface] = {
    "0": N_0,
    "1": N_1,
    "2": N_2,
    "3": N_3,
    "4": N_4,
    "5": N_5,
    "6": N_6,
    "7": N_7,
    "8": N_8,
    "9": N_9,
}

B_NORMAL = load_sprite(1920, 584, 300, 50, sheet=_sprite_sheet)
B_ACTIVE = load_sprite(1920, 634, 300, 50, sheet=_sprite_sheet)

ICON = load_sheet("icon.ico")

BUTTON = {"sprite": B_NORMAL, "asprite": B_ACTIVE}
