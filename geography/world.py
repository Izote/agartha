from __future__ import annotations
from typing import TYPE_CHECKING
from matplotlib.pyplot import subplots, show
from geography.generation import get_map

if TYPE_CHECKING:
    from tcod.console import Console


class World:
    __SHAPE = (80, 80)

    def __init__(self) -> None:
        self.__map = get_map(World.__SHAPE)

    @property
    def shape(self) -> tuple:
        return self.__map.shape

    def render(self, console: Console) -> None:
        height, width = self.shape
        for i in range(height):
            for j in range(width):
                value = self.__map[i, j]
                if value <= 0:
                    console.rgb[i, j] = ord(" "), (0, 0, 0), (0, 0, 120)
                else:
                    v = round(value * 255)
                    console.rgb[i, j] = ord(" "), (0, 0, 0), (v, v, v)

    def show(self) -> None:
        fig, ax = subplots()
        img = ax.imshow(self.__map, origin="lower")
        show()
