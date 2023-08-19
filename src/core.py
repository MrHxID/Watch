import datetime as dt
import time

import numpy as np
import pygame as pg
import win32api
import win32con
import win32gui

from . import (
    AXLE_POS,
    BG,
    BLIT_OFFSET,
    CLOCK,
    DATE_POS,
    DT,
    FPS,
    SCREEN,
    SECOND_POS,
    running,
)
from . import sprites as spr
from . import utils as u


def wndProc(oldWndProc, draw_callback, hWnd, message, wParam, lParam):
    if message == win32con.WM_SIZE or message == win32con.WM_MOVE:
        SCREEN.blit(BG, (0, 0))
        draw_callback(True)
        win32gui.RedrawWindow(
            hWnd,
            None,
            None,
            win32con.RDW_INVALIDATE | win32con.RDW_ERASE,
        )

    return win32gui.CallWindowProc(oldWndProc, hWnd, message, wParam, lParam)


def main(ticking=False):
    global running

    def draw_watch(all=False):
        dirty_rects = []
        datetime = dt.datetime.now()

        for r in u.all.values():
            dirty_rects.append(r.rect.copy())
            SCREEN.blit(BG, r.rect, r.rect)

        for r in u.all.values():
            r.update(DT, datetime=datetime)
            dirty_rects.append(r.rect.copy())
            SCREEN.blit(r.image, r.rect)

        if all:
            pg.display.flip()
        else:
            pg.display.update(dirty_rects)

    hour = u.ClockHand(
        SCREEN, spr.HOUR_HAND, AXLE_POS + BLIT_OFFSET, "hour", 2, ticking=ticking
    )
    minute = u.ClockHand(
        SCREEN, spr.MINUTE_HAND, AXLE_POS + BLIT_OFFSET, "minute", 4, ticking=ticking
    )
    u.ClockHand(
        SCREEN, spr.SECONDS_HAND, SECOND_POS + BLIT_OFFSET, "second", 0, ticking=ticking
    )
    # u.BaseRender(SCREEN, u.date(18), DATE_POS + BLIT_OFFSET, 0, anchor="topleft")
    u.Shadow(
        SCREEN,
        spr.HOUR_HAND_SHADOW,
        AXLE_POS + BLIT_OFFSET,
        "hour",
        hour,
        1,
        offset=(0, 5),
    )
    u.Shadow(
        SCREEN,
        spr.MINUTE_HAND_SHADOW,
        AXLE_POS + BLIT_OFFSET,
        "minute",
        minute,
        3,
        offset=(0, 10),
    )
    u.Date(SCREEN, None, DATE_POS + BLIT_OFFSET, 0, anchor="topleft")

    oldWndProc = win32gui.SetWindowLong(
        pg.display.get_wm_info()["window"],
        win32con.GWL_WNDPROC,
        lambda *args: wndProc(oldWndProc, draw_watch, *args),
    )

    while running:
        events = pg.event.get()

        for ev in events:
            if ev.type == pg.QUIT:
                running = False

            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    running = False

        draw_watch()

        CLOCK.tick(FPS)

    pg.quit()
