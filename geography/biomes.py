from numpy import array, empty, isnan
from tcod.console import rgb_graphic


def rgb(biome: str, x: int = 0) -> array:
    ch = {
        "land": " ",
        "ocean": " "
    }

    fg = {
        "land": (0, 0, 0),
        "ocean": (0, 0, 0)
    }

    bg = {
        "land": (0, 255*x, 0),
        "ocean": (0, 125*x, 255*x)
    }

    return array([(ord(ch[biome]), fg[biome], bg[biome])], dtype=rgb_graphic)


def assign_rgb(l: array, o: array) -> array:
    biomes = empty(l.shape, dtype=rgb_graphic)

    for i in range(l.shape[0]):
        for j in range(l.shape[1]):
            if isnan(l[i, j]):
                rgb_value = rgb("ocean", o[i, j])
            else:
                rgb_value = rgb("land", l[i, j])

            biomes[i, j] = rgb_value

    return biomes
