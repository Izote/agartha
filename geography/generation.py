from __future__ import annotations
from random import randint
from numpy import pad, zeros
from typing import TYPE_CHECKING
from tcod.noise import Algorithm, Implementation, Noise, grid

if TYPE_CHECKING:
    from numpy import array


def noise_map(shape: tuple, seed: int) -> array:
    noise = Noise(
        dimensions=2,
        algorithm=Algorithm.SIMPLEX,
        implementation=Implementation.FBM,
        lacunarity=2.5,
        hurst=1.0,
        octaves=16,
        seed=seed
    )

    return noise[grid(shape=shape, scale=0.1, origin=(0, 0))]


def falloff(core: int) -> array:
    npad = int(core / 2)
    ctr_shape, pad_shape = (core, core), (npad, npad)
    center = zeros(shape=ctr_shape)

    return pad(center, pad_shape, "linear_ramp", end_values=(1.30, 1.50))


def get_map(shape: tuple, seed: int = None, core: int = 40) -> array:
    s = randint(1, 10000) if seed is None else seed
    nmap, fo = noise_map(shape=shape, seed=s), falloff(core=core)

    return nmap - fo
