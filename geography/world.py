from __future__ import annotations
from typing import TYPE_CHECKING
from geography.biomes import assign_rgb

if TYPE_CHECKING:
    from numpy import array
    from tcod.console import Console


class World:
    __SHAPE = (80, 80)

    def __init__(self, seed: list = None) -> None:
        self.__rgb = assign_rgb(World.__SHAPE, seed=seed)

    @property
    def rgb(self) -> array:
        return self.__rgb

    @property
    def shape(self) -> tuple:
        return self.__rgb.shape

    def render(self, console: Console) -> None:
        i, j = World.__SHAPE
        console.rgb[:i, :j] = self.__rgb
