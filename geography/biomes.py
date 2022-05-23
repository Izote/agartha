from random import randint
from numpy import array, empty, isnan
from tcod.console import rgb_graphic


def rgb(biome: str, x: int = 0) -> array:
    ch = {
        "desert": " ",
        "forest": " ",
        "icecap": " ",
        "ocean": " ",
        "plains": " ",
        "rainforest": " ",
        "tundra": " "
    }

    bg = {
        "desert": (int(100*x + 100), int(125*x + 60), int(125*x + 15)),
        "forest": (int(30*x), int(120*x), int(30*x)),
        "icecap": (int(20*x + 180), int(20*x + 180), int(20*x + 180)),
        "ocean": (0, int(100 * x), int(125 * x + 60)),
        "plains": (int(60*x), int(140*x), int(60*x)),
        "rainforest": (int(25*x), int(75*x), int(25*x)),
        "tundra": (int(30*x), int(120*x), int(80*x))
    }
    return array([(ord(ch[biome]), (0, 0, 0), bg[biome])], dtype=rgb_graphic)


def assign_rgb(l: array, o: array, b: array) -> array:
    biomes = empty(l.shape, dtype=rgb_graphic)

    for i in range(l.shape[0]):
        for j in range(l.shape[1]):
            x = l[i, j]
            if isnan(x):
                biome = "ocean"
                x = o[i, j]
            else:
                arctic = i <= randint(18, 20) or i >= randint(60, 62)
                equatorial = i in range(randint(28, 30), randint(46, 48))

                if -1.00 <= b[i, j] <= -0.5:
                    if arctic:
                        biome = "tundra"
                    elif equatorial:
                        biome = "desert"
                    else:
                        biome = "plains"
                elif -0.5 < b[i, j] <= 0.5:
                    if arctic:
                        biome = "tundra"
                    else:
                        biome = "forest"
                else:
                    if arctic:
                        pole = i <= randint(9, 10) or i >= randint(69, 70)
                        if pole:
                            biome = "icecap"
                        else:
                            biome = "tundra"
                    else:
                        biome = "rainforest"

            biomes[i, j] = rgb(biome, x)

    return biomes
