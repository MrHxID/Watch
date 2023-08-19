import pygame as pg
from pathlib import Path
import numpy as np

try:
    path = Path(__file__)
    _sheet = pg.image.load(path.parent.parent.joinpath("assets", "Sprites.png"))
except FileNotFoundError as err:
    raise FileNotFoundError(f"Could not find the sprite sheet: {''.join(err.args)}")


def load_sprite(*rect, sheet=_sheet, transparent: bool = True):
    rect = pg.Rect(*rect)

    flags = pg.SRCALPHA * transparent
    sprite = pg.Surface(rect.size, flags)
    sprite.blit(sheet, (0, 0), rect)

    return sprite


CASING = load_sprite(0, 0, 1920, 1080, transparent=False)
HOUR_HAND = load_sprite(1920, 0, 569, 569)
HOUR_HAND_SHADOW = load_sprite(2489, 0, 569, 569)
MINUTE_HAND = load_sprite(1920, 569, 879, 879)
MINUTE_HAND_SHADOW = load_sprite(2799, 569, 879, 879)
AXLE = load_sprite(3058, 0, 23, 23)
SECONDS_HAND = load_sprite(3081, 0, 253, 253)
N_0 = load_sprite(3334, 0, 39, 56)
N_1 = load_sprite(3373, 0, 39, 56)
N_2 = load_sprite(3412, 0, 39, 56)
N_3 = load_sprite(3451, 0, 39, 56)
N_4 = load_sprite(3490, 0, 39, 56)
N_5 = load_sprite(3529, 0, 39, 56)
N_6 = load_sprite(3568, 0, 39, 56)
N_7 = load_sprite(3607, 0, 39, 56)
N_8 = load_sprite(3334, 57, 39, 56)
N_9 = load_sprite(3373, 57, 39, 56)

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

BUTTON = pg.Surface((300, 50))
BUTTON.fill("#aa0000")
