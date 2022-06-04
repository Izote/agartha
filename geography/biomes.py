from numpy import array, empty, isnan
from numpy.random import default_rng
from tcod.console import rgb_graphic
from geography.generation import get_values


def get_rgb(x: int, ch: str, biome: str) -> array:
    fg = {
        "desert": (int(96*x + 16), int(88*x + 16), int(31*x + 8)),
        "plains": (int(81*x + 16), int(73*x + 16), int(24*x + 8)),
        "ocean": (10, int(8*x + 22), int(8*x + 72)),
        "river": (10, int(8*x + 22), int(8*x + 72))
    }

    bg = {
        "desert": (int(100*x + 94), int(100*x + 78), int(85*x + 43)),
        "plains": (int(90*x + 30), int(90*x + 52), int(60*x + 20)),
        "ocean": (int(5*x + 15), int(15*x + 45), int(40*x + 102)),
        "river": (int(5*x + 15), int(15*x + 45), int(40*x + 102))
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
                    adj_list = [(i - d, j + d), (i, j + d), (i + d, j + d)]
                else:
                    adj_list = [(i - d, j - d), (i, j - d), (i + d, j - d)]

                adjacencies += adj_list
        elif version == "riverhead":
            adj_list = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1)]
            adjacencies += adj_list
        elif version == "flow":
            adj_list = [(i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]
            adjacencies += adj_list
        elif version == "surrounding":
            for d in range(0, dist + 1):
                adj_list = [(i - d, j - d), (i - d, j), (i - d, j + d),
                            (i, j - d), (i, j + d),
                            (i + d, j - d), (i + d, j), (i + d, j + d)]

                adjacencies += adj_list
        else:
            raise NotImplementedError

        return adjacencies

    def assign_land(mountain_threshold: float) -> None:
        for idx in indexes:
            if isnan(l[idx]):
                rgb_val, terr, terr_chr, bio_lab = o[idx], "nan", " ", "ocean"
            else:
                rgb_val = l[idx]
                terr = "mountain" if m[idx] > mountain_threshold else "nan"
                terr_chr = "^" if m[idx] > mountain_threshold else " "
                bio_lab = "plains"

            biome[idx] = bio_lab
            terrain[idx] = terr
            rgb[idx] = get_rgb(rgb_val, terr_chr, bio_lab)

    def desertify() -> None:
        settings = {
            "leeward": (terrain, "mountain", 3, 1),
            "surrounding": (biome, "desert", 1, 3)
        }

        for version in ["leeward", "surrounding"]:
            arr, lab, dist, threshold = settings[version]

            for idx in indexes:
                i, j = idx
                if rng.integers(18, 22) <= i <= rng.integers(28, 32) or \
                        rng.integers(58, 62) <= i <= rng.integers(68, 72):
                    count = 0
                    for adj in get_adjacencies(idx, version, dist):
                        try:
                            if biome[idx] == "plains" and arr[adj] == lab:
                                count += 1
                            else:
                                pass
                        except IndexError:
                            pass

                    if count >= threshold:
                        biome[idx] = "desert"
                        rgb_chr = chr(rgb[idx]["ch"])
                        rgb[idx] = get_rgb(l[idx], rgb_chr, "desert")
                    else:
                        pass
                else:
                    pass

    l, o, m, s = get_values(shape=shape, seed=seed)
    biome = empty(l.shape, dtype="U16")
    terrain = empty(l.shape, dtype="U16")
    rgb = empty(l.shape, dtype=rgb_graphic)

    rng = default_rng(s)
    indexes = get_indexes(l)

    assign_land(mountain_threshold=0.90)
    desertify()
    # irrigate((0.075, 0.925))

    return biome, terrain, rgb
