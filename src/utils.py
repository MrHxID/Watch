import numpy as np
import pygame as pg
import datetime

from . import AXLE_POS, DATE_POS, SECOND_POS
from . import sprites as spr


class BaseRender:
    def __init__(
        self,
        surface: pg.Surface,
        sprite: pg.Surface | None,
        position: tuple[int, int],
        priority: int = 0,
        **kwargs,
    ):
        self.surface = surface

        if sprite is None:
            self.sprite = pg.Surface((0, 0), pg.SRCALPHA)
        else:
            self.sprite = sprite.copy()

        self.image = self.sprite.copy()

        self.offset = kwargs.get("offset", np.array((0, 0)))
        self.position = position + self.offset
        self.priority = priority
        self._id = next(self.GenID)

        self.anchor = kwargs.get("anchor", "center")
        true_pos = {self.anchor: self.position}

        self.rect = self.image.get_rect(**true_pos)

        all[self._id] = self
        all_sorted = sorted(all.items(), key=lambda x: x[1].priority)
        all.clear()
        all.update(all_sorted)

    @staticmethod
    def _generate_id():
        i = 0
        while True:
            yield i
            i += 1

    GenID = _generate_id()

    def update(self, dt):
        return


class ClockHand(BaseRender):
    def __init__(
        self,
        surface: pg.Surface,
        sprite: pg.Surface | None,
        position: tuple[int, int],
        type: str,
        priority: int = 0,
        **kwargs,
    ):
        super().__init__(surface, sprite, position, priority, **kwargs)
        assert type in ("hour", "minute", "second"), f"Invalid type parameter: {type}"
        self.type = type

        time = datetime.datetime.now()
        print(time)


def date(date: int):
    temp = list(str(date))
    if len(temp) == 1:
        temp.insert(0, "0")

    surface = pg.Surface((77, 56), pg.SRCALPHA)
    surface.blit(spr.NUMBERS[temp[0]], (0, 0))
    surface.blit(spr.NUMBERS[temp[1]], (39, 0))

    return surface


all: dict[int, BaseRender] = {}
