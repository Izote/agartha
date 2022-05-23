from __future__ import annotations
from random import randint
from numpy import pad, zeros
from typing import TYPE_CHECKING
from tcod.noise import Algorithm, Implementation, Noise, grid

if TYPE_CHECKING:
    from numpy import array


def get_noise(
        shape: tuple,
        seed: list,
        algorithm: Algorithm = Algorithm.SIMPLEX,
        implementation: Implementation = Implementation.FBM,
        lacunarity: float = 2.5,
        hurst: float = 1.0,
        octaves: int = 16,
        scale: float = 0.06
) -> list:
    noise = Noise(
        dimensions=2,
        algorithm=algorithm,
        implementation=implementation,
        lacunarity=lacunarity,
        hurst=hurst,
        octaves=octaves,
        seed=seed
    )

    return noise[grid(shape=shape, scale=scale, origin=(0, 0))]


def get_falloff(core: int) -> array:
    npad = int(core / 4)
    ctr_shape, pad_shape = (core, core), (npad, npad)
    center = zeros(shape=ctr_shape)

    return pad(center, pad_shape, "linear_ramp", end_values=(1.30, 1.50))


def get_values(shape: tuple, seed: list = None, core: int = 54) -> tuple:
    n = range(3)
    s = [randint(1, 10000) for _ in n] if seed is None else seed

    # Default get_noise parameterization provides noise for land masses.
    l, fo = get_noise(shape=shape, seed=s[0]), get_falloff(core=core)
    l = l - fo
    l[l < 0] = "nan"

    # Leaving room for goal-specific parameterization.
    o = get_noise(shape=shape, seed=s[1])
    b = get_noise(shape=shape, seed=s[2])

    l, o = [0.5*(x + 1) for x in [l, o]]

    return l, o, b
