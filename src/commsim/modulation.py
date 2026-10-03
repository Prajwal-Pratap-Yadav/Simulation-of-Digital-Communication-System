"""Gray-labelled constellations and coherent nearest-neighbour demapping."""

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

Bits = NDArray[np.uint8]
Symbols = NDArray[np.complex128]


def binary(bits: ArrayLike) -> Bits:
    """Validate before casting so invalid numeric values cannot silently wrap."""
    value = np.asarray(bits)
    if value.ndim != 1 or not np.all((value == 0) | (value == 1)):
        raise ValueError("bits must be a one-dimensional binary array")
    return value.astype(np.uint8)


@dataclass(frozen=True)
class Constellation:
    family: str
    order: int
    points: Symbols
    labels: Bits
    k: int

    def modulate(self, bits: ArrayLike) -> Symbols:
        data = binary(bits)
        if len(data) % self.k:
            raise ValueError("bit count must be divisible by bits per symbol")
        powers = 2 ** np.arange(self.k - 1, -1, -1)
        values = data.reshape(-1, self.k) @ powers
        label_values = self.labels @ powers
        inverse = np.argsort(label_values)
        return self.points[inverse[values]]

    def demodulate(self, received: ArrayLike) -> Bits:
        samples = np.asarray(received, dtype=np.complex128)
        if samples.ndim != 1 or not np.all(np.isfinite(samples)):
            raise ValueError("received symbols must be finite and one-dimensional")
        # Bounded chunks avoid allocating a received-length by M matrix at once.
        decisions = []
        for start in range(0, len(samples), 4096):
            distance = np.abs(samples[start : start + 4096, None] - self.points)
            decisions.append(self.labels[np.argmin(distance, axis=1)].ravel())
        return np.concatenate(decisions) if decisions else np.empty(0, dtype=np.uint8)


def constellation(family: str, order: int) -> Constellation:
    """Return PSK or square QAM with mean symbol energy exactly one."""
    if type(order) is not int or order < 2 or order > 256 or order & (order - 1):
        raise ValueError("order must be a power of two between 2 and 256")
    family = family.lower()
    k = order.bit_length() - 1
    indices = np.arange(order, dtype=np.int64)
    if family == "psk":
        gray = indices ^ (indices >> 1)
        points = np.exp(2j * np.pi * indices / order)
        labels = ((gray[:, None] >> np.arange(k - 1, -1, -1)) & 1).astype(np.uint8)
    elif family == "qam":
        side = int(np.sqrt(order))
        if side * side != order:
            raise ValueError("QAM requires a square power-of-two order")
        axes = np.arange(side)
        levels = 2 * axes - side + 1
        xx, yy = np.meshgrid(levels, levels)
        points = (xx + 1j * yy).ravel() / np.sqrt(2 * (order - 1) / 3)
        gx, gy = np.meshgrid(axes ^ (axes >> 1), axes ^ (axes >> 1))
        values = (gx.ravel() << (k // 2)) | gy.ravel()
        labels = ((values[:, None] >> np.arange(k - 1, -1, -1)) & 1).astype(np.uint8)
    else:
        raise ValueError("family must be psk or qam")
    return Constellation(family, order, points.astype(np.complex128), labels, k)
