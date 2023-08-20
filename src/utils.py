import datetime as dt

import numpy as np
import pygame as pg

from . import sprites as spr

from scipy.ndimage import convolve


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

        self.offset = np.array(kwargs.get("offset", np.array((0, 0))), dtype=float)
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
        self.angle = 0

        if self.type == "hour":
            self.d_axle_center = 124
        elif self.type == "minute":
            self.d_axle_center = 203
        elif self.type == "second":
            self.d_axle_center = 43

    def update(self, dt, **kwargs):
        time = kwargs.get("datetime")

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

        # self.angle = (
        #     -self.angle
        # )  # negative angle because pygame rotates counter-clockwise

        if self.shadow is not None:
            self.shadow.angle = self.angle
            self.shadow._update(dt)

        self.image = pg.transform.rotozoom(self.sprite, -self.angle, 1)
        # self.rect = self.image.get_rect(**self._true_pos)
        self.rect = self.image.get_rect(**self._true_pos)

        offset_vec = pg.Vector2(0, -self.d_axle_center)

        rotated_offset_vec = offset_vec.rotate(self.angle)
        rotated_offset = np.array(rotated_offset_vec)

        # self.rect.topleft += np.floor(rotated_offset)

        # print(rotated_offset)

        self.image, rect = self._shift(self.image, rotated_offset)

        self.rect.topleft += np.array(rect.topleft)

    @staticmethod
    def _shift(image: pg.Surface, offset: tuple[float, float]):
        size = np.array(image.get_size())
        surface = pg.Surface(size + 1, pg.SRCALPHA)
        surface.blit(image, (1, 1))

        offset = np.array(offset, dtype=float)

        px_offset = np.floor(offset)
        sub_px_offset = offset % 1

        off_x, off_y = sub_px_offset

        kernel = np.array(
            [
                [(1 - off_x) * (1 - off_y), off_x * (1 - off_y)],
                [(1 - off_x) * off_y, off_x * off_y],
            ]
        )

        r = pg.surfarray.pixels_red(surface)
        g = pg.surfarray.pixels_green(surface)
        b = pg.surfarray.pixels_blue(surface)
        a = pg.surfarray.pixels_alpha(surface)

        true_r = r.transpose()
        true_g = g.transpose()
        true_b = b.transpose()
        true_a = a.transpose()

        convolve(true_r, kernel, true_r)
        convolve(true_g, kernel, true_g)
        convolve(true_b, kernel, true_b)
        convolve(true_a, kernel, true_a)

        r[:,:] = true_r.transpose()
        g[:,:] = true_g.transpose()
        b[:,:] = true_b.transpose()
        a[:,:] = true_a.transpose()

        rect = surface.get_rect(topleft=px_offset)

        return (surface, rect)

    # @staticmethod
    # def _shift(image: pg.Surface, offset: tuple[float, float]):
    #     offset = np.array(offset)

    #     px_offset = np.floor(offset)
    #     sub_px_offset = offset % 1

    #     off_x: float
    #     off_y: float
    #     off_x, off_y = sub_px_offset

    #     rgb = pg.surfarray.pixels3d(image)
    #     a = pg.surfarray.pixels_alpha(image)

    #     w, h = image.get_size()

    #     pixels = np.zeros((w, h, 4))

    #     pixels[:, :, :3] = rgb
    #     pixels[:, :, 3] = a

    #     # print(pixels)

    #     surface = np.zeros((h + 2, w + 2, 4))

    #     # intermediate surface array
    #     surface[1 : h + 1, 1 : w + 1, :] = pixels.transpose((1, 0, 2))
    #     # padded with the first and last row and column
    #     surface[0, :, :3] = surface[1, :, :3]
    #     surface[:, 0, :3] = surface[:, 1, :3]
    #     surface[-1, :, :3] = surface[-2, :, :3]
    #     surface[:, -1, :3] = surface[:, -2, :3]

    #     sa = surface[:-1, :-1]
    #     sb = surface[1:, :-1]
    #     sc = surface[:-1, 1:]
    #     sd = surface[1:, 1:]

    #     # return surface array

    #     s = (
    #         sa * off_x * off_y
    #         + sb * off_x * (1 - off_y)
    #         + sc * (1 - off_x) * off_y
    #         + sd * (1 - off_x) * (1 - off_y)
    #     )

    #     s = s.transpose((1, 0, 2))

    #     # print(s.shape, (w + 1, h + 1, 4))

    #     assert s.shape == (w + 1, h + 1, 4)

    #     ret_surf = pg.Surface((w + 1, h + 1), pg.SRCALPHA)

    #     ret_r = pg.surfarray.pixels_red(ret_surf)
    #     ret_g = pg.surfarray.pixels_green(ret_surf)
    #     ret_b = pg.surfarray.pixels_blue(ret_surf)
    #     ret_a = pg.surfarray.pixels_alpha(ret_surf)

    #     ret_r[:, :] = s[:, :, 0]
    #     ret_g[:, :] = s[:, :, 1]
    #     ret_b[:, :] = s[:, :, 2]
    #     ret_a[:, :] = s[:, :, 3]


    #     rect = ret_surf.get_rect(topleft=px_offset)

    #     # print(rect)

    #     return (ret_surf, rect)


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
        self.image = pg.transform.rotozoom(self.sprite, -self.angle, 1)
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
        self.activated = kwargs.get("activated", False)

        text = kwargs.get("text", "")
        atext = kwargs.get("atext", text)
        font = kwargs.get("font", pg.font.SysFont("Arial", 30))

        text_surface: pg.Surface = font.render(text, True, "#000000")
        atext_surface = font.render(atext, True, "#000000")
        text_pos = 0.5 * np.array(self.image.get_size())
        text_rect = text_surface.get_rect(center=text_pos)
        atext_rect = atext_surface.get_rect(center=text_pos)

        self.sprite.blit(text_surface, text_rect)
        self.asprite = kwargs.get("asprite", self.sprite)
        self.asprite.blit(atext_surface, atext_rect)
        self._rect = self.sprite.get_rect(**self._true_pos)
        self._arect = self.asprite.get_rect(**self._true_pos)

        self.image = self.sprite.copy()

        self.staged_changes = {}
        self.modes = {
            "normal": {"sprite": self.sprite, "rect": self._rect, "activated": False},
            "active": {"sprite": self.asprite, "rect": self._arect, "activated": True},
        }

        if self.activated:
            self.set_mode("active")

        buttons.append(self._id)

    def check_input(self, position):
        if not self.enabled:
            return

        if self.rect.collidepoint(position):
            self.command(*self.cargs, **self.ckwargs)

            if self.activated:
                self.set_mode("normal")
            else:
                self.set_mode("active")

    def set_mode(self, mode: str):
        self.staged_changes.update(self.modes[mode])

    def update(self, dt, **kwargs):
        for attr in self.staged_changes:
            setattr(self, attr, self.staged_changes[attr])

        self.image = self.sprite.copy()

        return super().update(dt, **kwargs)


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
