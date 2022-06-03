from numpy import array, empty, isnan
from numpy.random import default_rng
from tcod.console import rgb_graphic
from geography.generation import get_values


def get_rgb(x: int, ch: str, biome: str) -> array:
    fg = {
        "desert": (int(0), int(0), int(0)),
        "mountain": (int(60*x + 25), int(50*x + 25), int(25*x + 25)),
        "plain": (int(40 * x), int(50 * x), int(20 * x)),
        "ocean": (int(0), int(0), int(0)),
        "river": (int(0), int(0), int(0))
    }

    bg = {
        "desert": (int(144*x + 50), int(128*x + 50), int(78*x + 50)),
        "mountain": (int(119*x + 50), int(103*x + 50), int(53*x + 50)),
        "plain": (int(90 * x + 30), int(120 * x + 30), int(50 * x + 30)),
        "ocean": (int(20*x), int(40*x + 20), int(50*x + 100)),
        "river": (int(20*x), int(40*x + 20), int(50*x + 100))
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

    def assign_land(mt_thresh: float = 0.88) -> None:
        for idx in indexes:
            if isnan(l[idx]):
                value, character, label = o[idx], " ", "ocean"
            else:
                value = l[idx]
                character = "^" if m[idx] > mt_thresh else " "
                label = "mountain" if m[idx] > mt_thresh else "plain"

            biome[idx] = label
            rgb[idx] = get_rgb(value, character, label)

    def desertify() -> None:
        settings = {
            "leeward": ("mountain", 3, 1),
            "surrounding": ("desert", 1, 3)
        }

        for version in ["leeward", "surrounding"]:
            bio, dist, threshold = settings[version]

            for idx in indexes:
                i, j = idx
                mt = version in {"leeward", "windward"}
                if (20 <= i <= 30 or 60 <= i <= 70) and mt or not mt:
                    count = 0
                    for adj in get_adjacencies(idx, version, dist):
                        try:
                            if biome[idx] == "plain" and biome[adj] == bio:
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

    def irrigate(probability: tuple) -> None:
        land = {"desert", "plain"}
        label = "river"
        for idx in indexes:
            for adj in get_adjacencies(idx, "riverhead"):
                try:
                    if biome[idx] in land and biome[adj] == "mountain":
                        if rng.choice([True, False], 1, p=probability)[0]:
                            biome[idx] = label
                            rgb[idx] = get_rgb(o[idx], " ", label)
                    else:
                        pass
                except IndexError:
                    pass

        for idx in indexes:
            if biome[idx] == label:
                adjacents = get_adjacencies(idx, "flow")
                adj_val = []
                for adj in adjacents:
                    try:
                        if biome[adj] in land:
                            adj_val.append(l[adj])
                        else:
                            adj_val.append(1.0)
                    except IndexError:
                        pass

                if len(adj_val) > 0 and not all([v == 1.0 for v in adj_val]):
                    min_val = min(adj_val)
                    if l[idx] > min_val:
                        adj_idx = adjacents[adj_val.index(min_val)]
                        biome[adj_idx] = label
                        rgb[adj_idx] = get_rgb(o[adj_idx], " ", label)
                    else:
                        pass
                else:
                    pass

        for idx in indexes:
            count = 0
            if biome[idx] == "river":
                for adj in get_adjacencies(idx, "surrounding"):
                    if biome[adj] == "ocean":
                        count += 1

                if count >= 2:
                    biome[idx] = "ocean"
                    rgb[idx] = get_rgb(o[idx], " ", "ocean")

    l, o, m, s = get_values(shape=shape, seed=seed)
    rgb = empty(l.shape, dtype=rgb_graphic)
    biome = empty(l.shape, dtype="U16")
    rng = default_rng(s)
    indexes = get_indexes(l)

    assign_land()
    desertify()
    irrigate((0.05, 0.95))

    return biome, rgb
