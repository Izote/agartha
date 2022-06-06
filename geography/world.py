from __future__ import annotations
from typing import TYPE_CHECKING
from geography.biomes import generate_biomes

if TYPE_CHECKING:
    from numpy import array
    from tcod.console import Console


class World:
    """
    Simulates a (game) world.
    """
    __SHAPE = (80, 80)

    def __init__(self, seed: int = None) -> None:
        """
        Constructs a World class instance complete with its various members.

        :param seed: Determines the random state for various generators.
        """
        if seed is None:
            raise ValueError("An integer must be provided for World seed.")

        else:
            self.__biome, self.__terrain, self.__rgb = \
                generate_biomes(World.__SHAPE, seed=seed)

    @property
    def biome(self) -> array:
        """
        Read-only access to the instance's biome matrix.

        :return: A str matrix of representations for each tile's biome.
        """

        return self.__biome

    @property
    def terrain(self) -> array:
        """
        Read-only access to the instance's terrain matrix.

        :return: A str matrix of representations for each tile's terrain.
        """

        return self.__terrain

    @property
    def rgb(self) -> array:
        """
        Read-only access to the instance's RGB matrix.

        :return: A rgb_graphic matrix of values for each tile.
        """

        return self.__rgb

    @property
    def shape(self) -> tuple:
        """
        Read-only access to the instance's map dimensions.

        :return: A tuple representing the map's dimensions.
        """
        return self.__rgb.shape

    def render(self, console: Console) -> None:
        """
        Renders the instance's map to the console.

        :param console: The current console.
        :return: None
        """

        i, j = World.__SHAPE
        console.rgb[:i, :j] = self.__rgb
