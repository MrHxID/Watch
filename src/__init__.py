import os

import numpy as np
import pygame as pg
import win32con
import win32gui
import win32help


from . import sprites as spr

__all__ = ("core", "sprites")

pg.init()
SCREEN = pg.display.set_mode((1920, 1017), pg.RESIZABLE)
win32gui.ShowWindow(pg.display.get_wm_info()["window"], win32con.SW_MAXIMIZE)
BG = pg.Surface(SCREEN.get_size())

# pg.display.set_mode((1920, 1017))


os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"

running = True
CLOCK = pg.time.Clock()
FPS = 60
DT = 1 / FPS
BLIT_OFFSET = np.array((0, -26))

AXLE_POS = np.array((957, 536))
SECOND_POS = np.array((...))
DATE_POS = np.array((1287 + 10, 504 + 7))

BG.blit(spr.CASING, BLIT_OFFSET)
SCREEN.blit(BG, (0, 0))
pg.display.flip()
