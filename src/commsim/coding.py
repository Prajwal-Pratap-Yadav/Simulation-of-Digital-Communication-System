"""Optional hard-decision repetition and Hamming(7,4) coding."""

import numpy as np
from numpy.typing import ArrayLike

from .modulation import Bits, binary


def code_rate(kind: str) -> float:
    rates = {"none": 1.0, "repetition": 1 / 3, "hamming": 4 / 7}
    if kind not in rates:
        raise ValueError("coding must be none, repetition or hamming")
    return rates[kind]


def encode(bits: ArrayLike, kind: str) -> Bits:
    data = binary(bits)
    code_rate(kind)
    if kind == "none":
        return data.copy()
    if kind == "repetition":
        return np.repeat(data, 3)
    if len(data) % 4:
        raise ValueError("Hamming input needs complete four-bit blocks")
    d = data.reshape(-1, 4)
    c = np.zeros((len(d), 7), dtype=np.uint8)
    c[:, [2, 4, 5, 6]] = d
    c[:, 0] = d[:, 0] ^ d[:, 1] ^ d[:, 3]
    c[:, 1] = d[:, 0] ^ d[:, 2] ^ d[:, 3]
    c[:, 3] = d[:, 1] ^ d[:, 2] ^ d[:, 3]
    return c.ravel()


def decode(bits: ArrayLike, kind: str) -> Bits:
    data = binary(bits)
    code_rate(kind)
    if kind == "none":
        return data.copy()
    if kind == "repetition":
        if len(data) % 3:
            raise ValueError("repetition codeword length must be divisible by three")
        return (data.reshape(-1, 3).sum(axis=1) >= 2).astype(np.uint8)
    if len(data) % 7:
        raise ValueError("Hamming codeword length must be divisible by seven")
    c = data.reshape(-1, 7).copy()
    syndrome = np.zeros(len(c), dtype=np.int64)
    for bit, columns in enumerate(([0, 2, 4, 6], [1, 2, 5, 6], [3, 4, 5, 6])):
        syndrome += np.bitwise_xor.reduce(c[:, columns], axis=1) * (1 << bit)
    rows = np.flatnonzero(syndrome)
    c[rows, syndrome[rows] - 1] ^= 1
    return c[:, [2, 4, 5, 6]].ravel()
