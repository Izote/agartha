from __future__ import annotations
from numpy import pad, zeros
from typing import TYPE_CHECKING
from tcod.noise import Algorithm, Implementation, Noise, grid

if TYPE_CHECKING:
    from numpy import array


def get_noise(shape: tuple, algorithm: int = 2, implementation: int = 1,
              lacunarity: float = None, hurst: float = None,
              octaves: int = None, scale: float = None,
              seed: int = None) -> list:
    """
    Essentially a wrapper around the noise generation procedure provided by
    the `tcod` library. Takes the provided parameter values and generates
    an matrix of noise values.

    :param shape: A tuple representing the shape of the output noise matrix.
    :param algorithm: 1 (Perlin), 2 (Simplex, default), 4 (Wavelet).
    :param implementation: 0 (Simple), 1 (FBM, default), 2 (Turbulence).
    :param lacunarity: lacunarity value, defaults to 2.5.
    :param hurst: hurst value, defaults to 1.0.
    :param octaves: octaves value, defaults to 16.
    :param scale: scale value, defaults to 0.07.
    :param seed: An integer to set the noise generator's random state.
    :return: An array of noise values, bound between [-1, 1].
    """

    if seed is None:
        raise ValueError("get_noise `seed` must be a valid int value.")

    lacunarity = 2.5 if lacunarity is None else lacunarity
    hurst = 1.0 if hurst is None else hurst
    octaves = 16 if octaves is None else octaves
    scale = 0.07 if scale is None else scale

    noise = Noise(
        dimensions=2,
        algorithm=Algorithm(algorithm),
        implementation=Implementation(implementation),
        lacunarity=lacunarity,
        hurst=hurst,
        octaves=octaves,
        seed=seed
    )

    return noise[grid(shape=shape, scale=scale, origin=(0, 0))]


def get_falloff(core: int, gradient_end: tuple = (1.30, 1.50)) -> array:
    """
    Generates a falloff matrix, meaning an array with a core region of
    zero-valued cells and cells valued along a gradient out towards the
    matrix's edges.

    :param core: The width/height of the zero-valued region.
    :param gradient_end: The end values for each axis.
    :return: A falloff matrix.
    """

    npad = int(core / 4)
    ctr_shape, pad_shape = (core, core), (npad, npad)
    center = zeros(shape=ctr_shape)

    return pad(center, pad_shape, "linear_ramp", end_values=gradient_end)


def get_values(shape: tuple, core: int = 54, seed: int = None) -> list:
    """
    Generates a list of noise value matrices, applying a falloff matrix to the
    first such matrix.

    :param shape: A tuple representing the shape of the output noise matrix.
    :param core: The width/height of the fallout matrix's zero-valued region.
    :param seed: An integer to set the noise generator's random state.
    :return: A list of noise matrices.
    """

    o = [None, None, 2]
    s = [None, None, 0.49]

    value = [get_noise(shape=shape, octaves=o[i], scale=s[i], seed=seed)
             for i in range(3)]

    value[0] -= get_falloff(core=core)
    value[0][value[0] < 0] = "nan"

    value = [0.5*(v + 1) for v in value]

    return value
