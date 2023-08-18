import pygame as pg


class BaseRender:
    def __init__(
        self,
        surface: pg.Surface,
        sprite: pg.Surface | None,
        position: tuple[int, int],
        priority: int = 0,
        **kwargs
    ):
        self.surface = surface

        if sprite is None:
            self.sprite = pg.Surface((0, 0), pg.SRCALPHA)
        else:
            self.sprite = sprite.copy()

        self.image = self.sprite.copy()

        self.position = position
        self.priority = priority
        self._id = next(self.GenID)

        self.anchor = kwargs.get("anchor", "center")
        true_pos = {self.anchor: self.position}

        self.rect = self.sprite.get_rect(**true_pos)

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


all: dict[int, BaseRender] = {}
