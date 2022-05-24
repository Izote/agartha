from numpy import array, empty, isnan
from numpy.random import default_rng
from tcod.console import rgb_graphic
from geography.generation import get_values


def get_rgb(x: int, ch: str, biome: str) -> array:
    fg = {
        "savanna": (int(70*x), int(80*x), int(50*x)),
        "ocean": (int(0), int(0), int(0))
    }

    bg = {
        "savanna": (int(110*x + 30), int(130*x + 30), int(70*x + 30)),
        "ocean": (int(20*x), int(40*x + 20), int(50*x + 100))
    }

    return array([(ord(ch), fg[biome], bg[biome])], dtype=rgb_graphic)


def generate_biomes(shape: tuple, seed: list = None) -> array:
    l, o, m, s = get_values(shape=shape, seed=seed)
    rgb = empty(l.shape, dtype=rgb_graphic)
    rng = default_rng(s)

    for i in range(l.shape[0]):
        for j in range(l.shape[1]):
            idx = i, j
            if isnan(l[idx]):
                x = o[idx]
                ch = " "
                biome = "ocean"
            else:
                x = l[idx]
                ch = "^" if m[idx] > 0.88 else " "
                biome = "savanna"

            rgb[idx] = get_rgb(x, ch, biome)

    return rgb
