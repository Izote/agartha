from numpy import array, empty, isnan
from numpy.random import default_rng
from tcod.console import rgb_graphic
from geography.generation import get_values


def rgb(x: int, biome: str) -> array:
    fg = {
        "savanna": (int(0), int(0), int(0)),
        "ocean": (int(0), int(0), int(0))
    }

    bg = {
        "savanna": (int(140*x), int(160*x), int(100*x)),
        "ocean": (int(20*x), int(40*x + 20), int(50*x + 100))
    }

    # should communicate tile info, therefore be based on *some* value
    ch = " "

    return array([(ord(ch), fg[biome], bg[biome])], dtype=rgb_graphic)


def assign_rgb(shape: tuple, seed: list = None) -> array:
    l, o, s = get_values(shape=shape, seed=seed)
    biomes = empty(l.shape, dtype=rgb_graphic)
    rng = default_rng(s)

    for i in range(l.shape[0]):
        for j in range(l.shape[1]):
            if isnan(l[i, j]):
                x = o[i, j]
                biome = "ocean"
            else:
                x = l[i, j]
                biome = "savanna"

            biomes[i, j] = rgb(x, biome)

    return biomes
