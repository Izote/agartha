from numpy import array, empty, isnan
from tcod.console import rgb_graphic


def tile(ch: str = " ", fg: tuple = (0, 0, 0), bg: tuple = (0, 0, 0)) -> array:
    return array([(ord(ch), fg, bg)], dtype=rgb_graphic)


def assign_tiles(noise: array) -> array:
    biomes = empty(noise.shape, dtype=rgb_graphic)

    for i in range(noise.shape[0]):
        for j in range(noise.shape[1]):
            value = noise[i, j]
            if isnan(value):
                biomes[i, j] = tile(" ", (50, 50, 90), (0, 100, 180))
            else:
                biomes[i, j] = tile(" ", (20, 60, 20), (0, 255*value, 0))

    return biomes
