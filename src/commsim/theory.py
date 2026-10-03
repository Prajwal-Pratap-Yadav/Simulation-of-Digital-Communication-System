"""Exact BPSK/QPSK BER and explicitly approximate Gray square-QAM BER."""

import numpy as np
from scipy.special import erfc


def ber(ebn0_db: float, family: str, order: int, channel: str) -> float | None:
    gamma = 10 ** (ebn0_db / 10)
    if family == "psk" and order in {2, 4}:
        if channel == "awgn":
            return float(0.5 * erfc(np.sqrt(gamma)))
        if channel == "rayleigh":
            return float(0.5 * (1 - np.sqrt(gamma / (1 + gamma))))
    if family == "qam" and channel == "awgn":
        k = np.log2(order)
        return float(
            2
            / k
            * (1 - 1 / np.sqrt(order))
            * erfc(np.sqrt(3 * k * gamma / (2 * (order - 1))))
        )
    return None


def wilson(errors: int, bits: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """Pointwise binomial interval; sequential stopping changes nominal coverage."""
    if bits < 1 or errors < 0 or errors > bits or not np.isfinite(z) or z <= 0:
        raise ValueError("invalid binomial counts or z score")
    p = errors / bits
    denominator = 1 + z * z / bits
    centre = (p + z * z / (2 * bits)) / denominator
    half = z * np.sqrt(p * (1 - p) / bits + z * z / (4 * bits * bits)) / denominator
    return max(0.0, float(centre - half)), min(1.0, float(centre + half))
