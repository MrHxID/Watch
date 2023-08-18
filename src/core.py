import pygame as pg
import time

from . import (
    sprites as spr,
    utils as u,
    running,
    CLOCK,
    FPS,
    SCREEN,
    BG,
    BLIT_OFFSET,
    DT,
)


def main():
    global running

    while running:
        events = pg.event.get()

        for ev in events:
            if ev.type == pg.QUIT:
                running = False

            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    running = False

        dirty_rects = []

        for r in u.all.values():
            dirty_rects.append(r.rect.copy())
            SCREEN.blit(BG, r.rect, r.rect)

        for r in u.all.values():
            r.update(DT)
            dirty_rects.append(r.rect.copy())
            SCREEN.blit(r.image, r.rect)

        CLOCK.tick(FPS)

    pg.quit()
