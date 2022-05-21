from __future__ import annotations
from random import randint
from numpy import pad, zeros
from typing import TYPE_CHECKING
from tcod.noise import Algorithm, Implementation, Noise, grid

if TYPE_CHECKING:
    from numpy import array


def noise_map(seed: int = randint(0, 1000)) -> array:
    n = 360
    noise = Noise(
        dimensions=2,
        algorithm=Algorithm.SIMPLEX,
        implementation=Implementation.FBM,
        lacunarity=2.0,
        hurst=1.0,
        octaves=14,
        seed=seed
    )

    return noise[grid(shape=(n, n), scale=0.01, origin=(0, 0))]


def falloff(ctr: int = 90) -> array:
    npad = 225 - ctr
    ctr_shape, pad_shape = (ctr, ctr), (npad, npad)
    center = zeros(shape=ctr_shape)

    return pad(center, pad_shape, 'linear_ramp', end_values=(1.30, 1.50))


# import matplotlib.pyplot as plt
# fo = falloff()
# nmap = noise_map()
# wmap = (nmap - fo >= 0).astype(int)
#
# fig, ax = plt.subplots()
# img = ax.imshow(wmap, origin="lower")
# plt.show()
