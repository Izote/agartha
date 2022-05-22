from __future__ import annotations
from typing import TYPE_CHECKING
from matplotlib.pyplot import subplots, show
from geography.generation import get_values
from geography.biomes import assign_rgb

if TYPE_CHECKING:
    from numpy import array
    from tcod.console import Console


class World:
    __SHAPE = (80, 80)

    def __init__(self, seed: list = None) -> None:
        self.__land, self.__ocean, self.__precipitation, self.__temperature = \
            get_values(World.__SHAPE, seed=seed)
        self.__rgb = assign_rgb(self.__land, self.__ocean)

    @property
    def rgb(self) -> array:
        return self.__rgb

    @property
    def shape(self) -> tuple:
        return self.__land.shape

    def render(self, console: Console) -> None:
        i, j = World.__SHAPE
        console.rgb[:i, :j] = self.__rgb

    def show(self) -> None:
        fig, ax = subplots()
        img = ax.imshow(self.__land, origin="lower")
        show()
