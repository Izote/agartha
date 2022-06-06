from numpy import array, empty, isnan
from numpy.random import default_rng
from tcod.console import rgb_graphic
from geography.generation import get_values


def get_rgb(x: int, ch: str, biome: str) -> array:
    """
    Compiles a tile for console rendering, assigning the tile's RGB color
    value based on its biome label and noise value.

    :param x: The tile's noise value.
    :param ch: The tile's assigned character.
    :param biome: The tile's assigned biome.
    :return: An array of the tcod.console.rgb_graphic data type.
    """

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


def generate_biomes(shape: tuple, seed: int = None) -> tuple:
    """
    Outputs several matrices representing the game's world map.

    :param shape: The dimensions of the map itself.
    :param seed: An integer to determine the noise generator's random state.
    :return:
    """
    def get_indexes(x: array) -> list:
        """
        Wrapper for common process of looping through an array's indexes.

        :param x: The array to loop through.
        :return: A list of tuples, one for each of the array's indexes.
        """
        idx = []
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                idx.append((i, j))

        return idx

    def get_adjacencies(idx: tuple, version: str, dist: int = 1) -> list:
        """
        Returns adjacent indexes, finding them based on the version and
        dist parameter values.

        Specific version details pending.

        :param idx: The origin index.
        :param version: One of "leeward", "riverhead", "flow" or "surrounding".
        :param dist: How far to look for and compile adjacent indexes.
        :return: A tuple of biome, terrain and RGB matrices.
        """

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

    def assign_land(height_threshold: float) -> None:
        """
        Checks whether a given tile should be considered land versus ocean and
        then assigns terrain features appropriately.

        :param height_threshold: A [0, 1] value that assigns mountain terrain.
        :return: None
        """

        for idx in indexes:
            if isnan(land[idx]):
                rgb_val = ocean[idx]
                terr = "nan"
                terr_chr = " "
                bio_lab = "ocean"
            else:
                rgb_val = land[idx]
                terr = "mountain" if height[idx] > height_threshold else "nan"
                terr_chr = "^" if height[idx] > height_threshold else " "
                bio_lab = "plains"

            biome[idx] = bio_lab
            terrain[idx] = terr
            rgb[idx] = get_rgb(rgb_val, terr_chr, bio_lab)

    def desertify() -> None:
        """
        Converts plains tiles to desert tiles first based on their location
        relative first to mountains and then to other, existing deserts.

        :return: None
        """
        settings = {
            "leeward": (terrain, "mountain", 3, 1),
            "surrounding": (biome, "desert", 1, 3)
        }

        for version in ["leeward", "surrounding"]:
            arr, lab, dist, threshold = settings[version]

            for idx in indexes:
                i, j = idx
                if rng.integers(19, 22) <= i <= rng.integers(29, 32) or \
                        rng.integers(59, 62) <= i <= rng.integers(69, 72):
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
                        rgb[idx] = get_rgb(land[idx], rgb_chr, "desert")
                    else:
                        pass
                else:
                    pass

    land, ocean, height = get_values(shape=shape, seed=seed)
    biome = empty(land.shape, dtype="U16")
    terrain = empty(land.shape, dtype="U16")
    rgb = empty(land.shape, dtype=rgb_graphic)

    rng = default_rng(seed)
    indexes = get_indexes(land)

    assign_land(height_threshold=0.90)
    desertify()

    return biome, terrain, rgb
