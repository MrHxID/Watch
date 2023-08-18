import pygame as pg
from . import sprites as spr, running, CLOCK, FPS, SCREEN, BLIT_OFFSET


def main():
    global running
    SCREEN.blit(spr.CASING, (0, 0) + BLIT_OFFSET)

    while running:
        events = pg.event.get()

        for ev in events:
            if ev.type == pg.QUIT:
                running = False

            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    running = False

        # SCREEN.fill("#ff0000")
        # print(SCREEN.get_size())

        pg.display.flip()

        CLOCK.tick(FPS)

    pg.quit()
