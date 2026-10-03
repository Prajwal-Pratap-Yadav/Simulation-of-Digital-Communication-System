"""Characterize the original experiment without changing its historical evidence."""

import hashlib
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def test_original_source_preserved():
    source = (ROOT / "legacy/original/code.m").read_bytes()
    assert len(source) == 1780
    assert hashlib.sha1(b"blob 1780\0" + source).hexdigest() == (
        "dd3d77b4cc0a37f3ce72475be32eb5a5f0f56187"
    )


def test_original_matlab_column_major_bit_roundtrip():
    # MATLAB reshape and (:): the root script groups the first/second half.
    bits = np.random.default_rng(31).integers(0, 2, 1000)
    pairs = bits.reshape(-1, 2, order="F")
    symbols = (2 * pairs[:, 0] - 1) + 1j * (2 * pairs[:, 1] - 1)
    recovered = np.column_stack((symbols.real > 0, symbols.imag > 0))
    np.testing.assert_array_equal(recovered.ravel(order="F"), bits)
    # This energy is precisely why Es=1 noise cannot be used unchanged.
    np.testing.assert_allclose(np.mean(np.abs(symbols) ** 2), 2)
