import datetime as dt

import numpy as np
import pygame as pg

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

        self.offset = np.array(kwargs.get("offset", np.array((0, 0))))
        self.position = position + self.offset
        self.priority = priority
        self._id = next(self.GenID)

        self.anchor = kwargs.get("anchor", "center")
        self._true_pos = {self.anchor: self.position}

        self.rect = self.image.get_rect(**self._true_pos)

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

    def update(self, dt, *args, **kwargs):
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
        self.ticking = kwargs.get("ticking", False)
        self.shadow = None

    def update(self, dt, **kwargs):
        time = kwargs.get("datetime")

        self.angle = 0

        if self.type == "hour":
            self.angle = 30 * time.hour + 0.5 * time.minute + 0.008333333 * time.second
        elif self.type == "minute":
            self.angle = (
                6 * time.minute
                + 0.1 * time.second
                + (0 if self.ticking else 1e-7 * time.microsecond)
            )
        elif self.type == "second":
            self.angle = 6 * time.second + (
                0 if self.ticking else 6e-6 * time.microsecond
            )
        else:
            # Never happens
            raise ValueError("wtf")

        self.angle = (
            -self.angle
        )  # negative angle because pygame rotates counter-clockwise

        if self.shadow is not None:
            self.shadow.angle = self.angle
            self.shadow._update(dt)

        self.image = pg.transform.rotozoom(self.sprite, self.angle, 1)

        self.rect = self.image.get_rect(**self._true_pos)


class Shadow(ClockHand):
    def __init__(
        self,
        surface: pg.Surface,
        sprite: pg.Surface | None,
        position: tuple[int, int],
        type: str,
        parent: ClockHand,
        priority: int = 0,
        **kwargs,
    ):
        super().__init__(surface, sprite, position, type, priority, **kwargs)
        parent.shadow = self

    def update(self, dt, **kwargs):
        # self.image = pg.transform.rotozoom(self.sprite, self.angle, 1)
        # self.rect = self.image.get_rect(**self._true_pos)
        return

    def _update(self, dt):
        self.image = pg.transform.rotozoom(self.sprite, self.angle, 1)
        self.rect = self.image.get_rect(**self._true_pos)


class Date(BaseRender):
    def __init__(
        self,
        surface: pg.Surface,
        sprite: pg.Surface | None,
        position: tuple[int, int],
        priority: int = 0,
        **kwargs,
    ):
        sprite = date(dt.date.today().day)
        super().__init__(surface, sprite, position, priority, **kwargs)

    def update(self, dt, **kwargs):
        day = kwargs.get("datetime").day

        self.image = date(day)


class Button(BaseRender):
    def __init__(
        self,
        surface: pg.Surface,
        sprite: pg.Surface | None,
        position: tuple[int, int],
        priority: int = 0,
        **kwargs,
    ):
        super().__init__(surface, sprite, position, priority, **kwargs)
        self.command = kwargs.get("command", lambda *_, **__: None)
        self.cargs = kwargs.get("cargs", ())
        self.ckwargs = kwargs.get("ckwargs", {})
        self.enabled = kwargs.get("enabled", True)

        self.text = kwargs.get("text", "")
        self.font = kwargs.get("font", pg.font.SysFont("Arial", 30))

        text_surface: pg.Surface = self.font.render(self.text, True, "#000000")
        text_pos = 0.5 * np.array(self.image.get_size())
        text_rect = text_surface.get_rect(center=text_pos)

        self.sprite.blit(text_surface, text_rect)
        self.image = self.sprite.copy()

        buttons.append(self._id)

    def check_input(self, position):
        if not self.enabled:
            return

        if self.rect.collidepoint(position):
            self.command(*self.cargs, **self.ckwargs)


def date(date: int):
    temp = list(str(date))
    if len(temp) == 1:
        temp.insert(0, "0")

    surface = pg.Surface((77, 56), pg.SRCALPHA)
    surface.blit(spr.NUMBERS[temp[0]], (0, 0))
    surface.blit(spr.NUMBERS[temp[1]], (39, 0))

    return surface


def flatten(array: list | tuple | set):
    if not isinstance(array, (list, tuple)):
        return [array]

    flat_list = []

    for i in array:
        flat_list.extend(flatten(i))

    return type(array)(flat_list)


all: dict[int, BaseRender] = {}
buttons: list[int] = []
