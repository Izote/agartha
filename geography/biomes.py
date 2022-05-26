from numpy import array, empty, isnan
from numpy.random import default_rng
from tcod.console import rgb_graphic
from geography.generation import get_values


def get_rgb(x: int, ch: str, biome: str) -> array:
    fg = {
        "grasslands": (int(40*x), int(50*x), int(20*x)),
        "mountain": (int(220), int(250), int(250)),
        "ocean": (int(0), int(0), int(0))
    }

    bg = {
        "grasslands": (int(90*x + 30), int(120*x + 30), int(50*x + 30)),
        "mountain": (int(90*x + 30), int(120*x + 30), int(50*x + 30)),
        "ocean": (int(20*x), int(40*x + 20), int(50*x + 100))
    }

    return array([(ord(ch), fg[biome], bg[biome])], dtype=rgb_graphic)


def generate_biomes(shape: tuple, seed: list = None) -> tuple:
    l, o, m, s = get_values(shape=shape, seed=seed)
    rgb = empty(l.shape, dtype=rgb_graphic)
    biome = empty(l.shape, dtype="U16")
    rng = default_rng(s)

    for i in range(l.shape[0]):
        for j in range(l.shape[1]):
            idx = i, j
            if isnan(l[idx]):
                x, ch, bio = o[idx], " ", "ocean"
            else:
                x = l[idx]
                ch = "^" if m[idx] > 0.88 else " "
                bio = "mountain" if m[idx] > 0.94 else "grasslands"

            biome[idx] = bio
            rgb[idx] = get_rgb(x, ch, bio)

    return biome, rgb
