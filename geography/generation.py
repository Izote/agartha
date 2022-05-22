from __future__ import annotations
from random import randint
from numpy import pad, zeros
from typing import TYPE_CHECKING
from tcod.noise import Algorithm, Implementation, Noise, grid

if TYPE_CHECKING:
    from numpy import array


def get_noise(shape: tuple, seed: list) -> list:
    noise = Noise(
        dimensions=2,
        algorithm=Algorithm.SIMPLEX,
        implementation=Implementation.FBM,
        lacunarity=2.5,
        hurst=1.0,
        octaves=16,
        seed=seed
    )

    return noise[grid(shape=shape, scale=0.06, origin=(0, 0))]


def get_falloff(core: int) -> array:
    npad = int(core / 4)
    ctr_shape, pad_shape = (core, core), (npad, npad)
    center = zeros(shape=ctr_shape)

    return pad(center, pad_shape, "linear_ramp", end_values=(1.30, 1.50))


def get_values(shape: tuple, seed: list = None, core: int = 54) -> tuple:
    n = range(4)
    s = [randint(1, 10000) for _ in n] if seed is None else seed
    l, o, p, t = [get_noise(shape=shape, seed=s[0]) for i in n]
    fo = get_falloff(core=core)

    l = l - fo
    l[l < 0] = "nan"
    l, o = [0.5*(x + 1) for x in [l, o]]

    return l, o, p, t
