import datetime as dt
import os

import numpy as np
import pygame as pg
import win32con
import win32gui

import src

from . import sprites as spr
from . import utils as u
from . import settings

_default_settings = settings.default()

SCREEN = pg.display.set_mode((1920, 1017), pg.RESIZABLE)
win32gui.ShowWindow(pg.display.get_wm_info()["window"], win32con.SW_MAXIMIZE)
BG = pg.Surface(SCREEN.get_size())

pg.display.set_caption("Tangente Neomatik")

# pg.display.set_mode((1920, 1017))


os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"

running = True
CLOCK = pg.time.Clock()
BLIT_OFFSET = np.array((0, -26))

AXLE_POS = np.array((957, 536))
SECOND_POS = np.array((956, 717))
DATE_POS = np.array((1287 + 10, 504 + 7))

BG.blit(spr.CASING, BLIT_OFFSET)
SCREEN.blit(BG, (0, 0))
pg.display.flip()


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

    sleeping = False
    DT = 0

    def draw_watch(all=False, no_update=False):
        nonlocal sleeping, DT
        if sleeping:
            dirty_rects = []

            for id in u.buttons:
                b = u.all[id]
                dirty_rects.append(b.rect.copy())
                SCREEN.blit(BG, b.rect, b.rect)

            for id in u.buttons:
                b = u.all[id]
                b.update(DT)
                dirty_rects.append(b.rect.copy())
                SCREEN.blit(b.image, b.rect)

            pg.display.update(dirty_rects)
            return

        dirty_rects = []
        dirty_rects.append([pg.Rect(0, 0, 10, 10), pg.Rect(10, 0, 20, 20)])
        datetime = dt.datetime.now()

        for r in u.all.values():
            dirty_rects.append(r.rect.copy())
            r.surface.blit(BG, r.rect, r.rect)

        for r in u.all.values():
            r.update(DT, datetime=datetime)
            dirty_rects.append(r.rect.copy())
            r.surface.blit(r.image, r.rect)

        if no_update:
            return

        dirty_rects = u.flatten(dirty_rects)

        if all:
            pg.display.flip()
        else:
            pg.display.update(dirty_rects)

    def sleep():
        nonlocal sleeping
        # global SCREEN, BG

        if sleeping:
            sleeping = False
            SCREEN.blit(BG, (0, 0))
            draw_watch(True, True)

        else:
            sleeping = True
            overlay = pg.Surface(SCREEN.get_size(), pg.SRCALPHA)
            overlay.fill("#ffffff")
            overlay.set_alpha(100)
            SCREEN.blit(overlay, (0, 0))

        pg.display.flip()

    def toggle_slumber_enabled():
        nonlocal slumber_enabled

        settings.update({"slumber enabled": not slumber_enabled})

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

    u.Button(
        SCREEN,
        **spr.BUTTON,
        position=(300, 800),
        priority=0,
        command=sleep,
        text="Schlafen",
        atext="Wecken",
    )

    b_toggle_slumber = u.Button(
        SCREEN,
        **spr.BUTTON,
        position=(300, 870),
        priority=0,
        command=toggle_slumber_enabled,
        text="Schlummern deaktiviert",
        atext="Schlummern aktiviert",
    )

    if src.settings_dict["slumber enabled"]:
        b_toggle_slumber.set_mode("active")

    oldWndProc = win32gui.SetWindowLong(
        pg.display.get_wm_info()["window"],
        win32con.GWL_WNDPROC,
        lambda *args: wndProc(oldWndProc, draw_watch, *args),
    )

    timing = []

    while running:
        slumber_enabled = src.settings_dict["slumber enabled"]

        events = pg.event.get()

        for ev in events:
            if ev.type == pg.QUIT:
                running = False

            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    running = False

            # pos = pg.mouse.get_pos()

            if ev.type == pg.ACTIVEEVENT:
                slumbering = not bool(ev.gain)

            for id in u.buttons:
                b = u.all[id]
                if ev.type == pg.MOUSEBUTTONUP:
                    if ev.button == pg.BUTTON_LEFT:
                        b.check_input(ev.pos)

        draw_watch()

        # print(slumbering, slumber_enabled)

        if slumber_enabled and slumbering:
            DT = CLOCK.tick(src.settings_dict["slumber fps"])

        elif sleeping:
            DT = CLOCK.tick(src.settings_dict["sleep fps"])

        else:
            DT = CLOCK.tick(src.settings_dict["fps"])

        DT *= 0.001

        timing.append(DT)

    mean_dt = np.mean(timing)
    mean_fps = 1 / mean_dt
    print(mean_fps)

    pg.quit()
