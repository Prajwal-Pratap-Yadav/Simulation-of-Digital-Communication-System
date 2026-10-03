"""Symbol-rate channel models with perfect receiver channel-state knowledge."""

import numpy as np
from numpy.random import Generator

from .modulation import Symbols


def transmit(
    symbols: Symbols,
    ebn0_db: float,
    k: int,
    rng: Generator,
    kind: str = "awgn",
    rate: float = 1.0,
    rician_k: float = 5.0,
) -> tuple[Symbols, Symbols]:
    """Es=1; Eb is energy per information bit, hence N0=1/(k*R*EbN0)."""
    if not np.isfinite(ebn0_db) or not -100 <= ebn0_db <= 100:
        raise ValueError("Eb/N0 must be finite and within [-100,100] dB")
    if k < 1 or not 0 < rate <= 1:
        raise ValueError("invalid bits per symbol or code rate")
    if not np.isfinite(rician_k) or rician_k < 0:
        raise ValueError("Rician K must be finite and nonnegative")
    if kind == "awgn":
        gain = np.ones(len(symbols), dtype=np.complex128)
    elif kind in {"rayleigh", "rician"}:
        scatter = rng.normal(size=len(symbols)) + 1j * rng.normal(size=len(symbols))
        scatter /= np.sqrt(2)
        gain = (
            scatter
            if kind == "rayleigh"
            else (np.sqrt(rician_k / (rician_k + 1)) + scatter / np.sqrt(rician_k + 1))
        )
    else:
        raise ValueError("channel must be awgn, rayleigh or rician")
    n0 = 1 / (k * rate * 10 ** (ebn0_db / 10))
    noise = np.sqrt(n0 / 2) * (
        rng.normal(size=len(symbols)) + 1j * rng.normal(size=len(symbols))
    )
    return (gain * symbols + noise).astype(np.complex128), gain
