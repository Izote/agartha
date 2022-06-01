from numpy import array, empty, isnan
from numpy.random import default_rng
from tcod.console import rgb_graphic
from geography.generation import get_values


def get_rgb(x: int, ch: str, biome: str) -> array:
    fg = {
        "desert": (int(0), int(0), int(0)),
        "grasslands": (int(40*x), int(50*x), int(20*x)),
        "mountain": (int(60*x + 25), int(50*x + 25), int(25*x + 25)),
        "ocean": (int(0), int(0), int(0))
    }

    bg = {
        "desert": (int(144*x + 50), int(128*x + 50), int(78*x + 50)),
        "grasslands": (int(90*x + 30), int(120*x + 30), int(50*x + 30)),
        "mountain": (int(119*x + 50), int(103*x + 50), int(53*x + 50)),
        "ocean": (int(20*x), int(40*x + 20), int(50*x + 100))
    }

    return array([(ord(ch), fg[biome], bg[biome])], dtype=rgb_graphic)


def generate_biomes(shape: tuple, seed: list = None) -> tuple:
    def get_indexes(x: array) -> list:
        idx = []
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                idx.append((i, j))

        return idx

    def get_adjacencies(idx: tuple, version: str, dist: int = 1) -> list:
        i, j = idx
        adjacencies = []

        if version == "leeward":
            for d in range(0, dist + 1):
                if i <= 45:
                    adjacencies += [(i - d, j + d), (i, j + d), (i + d, j + d)]
                else:
                    adjacencies += [(i - d, j - d), (i, j - d), (i + d, j - d)]
        elif version == "surrounding":
            for d in range(0, dist + 1):
                adjacencies += [(i - d, j - d), (i - d, j), (i - d, j + d),
                                (i, j - d), (i, j + d),
                                (i + d, j - d), (i + d, j), (i + d, j + d)]
        else:
            raise NotImplementedError

        return adjacencies

    def assign_land(mt: float = 0.88) -> None:
        for idx in indexes:
            if isnan(l[idx]):
                value, character, label = o[idx], " ", "ocean"
            else:
                value = l[idx]
                character = "^" if m[idx] > mt else " "
                label = "mountain" if m[idx] > mt else "grasslands"

            biome[idx] = label
            rgb[idx] = get_rgb(value, character, label)

    def desertify(version: str) -> None:
        if version not in {"leeward", "windward", "surrounding"}:
            raise ValueError("unsupported version for desertify function.")

        settings = {
            "leeward": ("mountain", 3, 1),
            "surrounding": ("desert", 1, 3)
        }

        bio, dist, threshold = settings[version]
        for idx in indexes:
            i, j = idx
            mt_based = version in {"leeward", "windward"}
            if (20 <= i <= 30 or 60 <= i <= 70) and mt_based or not mt_based:
                count = 0
                for adj in get_adjacencies(idx, version, dist):
                    try:
                        if biome[idx] == "grasslands" and biome[adj] == bio:
                            count += 1
                        else:
                            pass
                    except IndexError:
                        pass

                if count >= threshold:
                    biome[idx] = "desert"
                    rgb[idx] = get_rgb(l[idx], " ", "desert")
                else:
                    pass
            else:
                pass

    l, o, m, s = get_values(shape=shape, seed=seed)
    rgb = empty(l.shape, dtype=rgb_graphic)
    biome = empty(l.shape, dtype="U16")
    rng = default_rng(s)
    indexes = get_indexes(l)

    assign_land()
    desertify("leeward")
    desertify("surrounding")

    return biome, rgb
