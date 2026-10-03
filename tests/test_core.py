"""Contract tests for mappings, coding, energy and channel noise."""

import numpy as np
import pytest

from commsim.channel import transmit
from commsim.coding import decode, encode
from commsim.modulation import binary, constellation
from commsim.theory import ber, wilson


@pytest.mark.parametrize(
    "family,order",
    [
        ("psk", 2),
        ("psk", 4),
        ("psk", 8),
        ("psk", 16),
        ("qam", 4),
        ("qam", 16),
        ("qam", 64),
        ("qam", 256),
    ],
)
def test_every_label_roundtrips_and_energy_is_one(family, order):
    c = constellation(family, order)
    np.testing.assert_allclose(np.mean(np.abs(c.points) ** 2), 1, atol=1e-14)
    assert len(np.unique(c.labels, axis=0)) == order
    np.testing.assert_array_equal(
        c.demodulate(c.modulate(c.labels.ravel())), c.labels.ravel()
    )


def test_gray_psk_neighbours_change_one_bit():
    c = constellation("psk", 16)
    assert np.all(np.sum(c.labels != np.roll(c.labels, 1, axis=0), axis=1) == 1)


@pytest.mark.parametrize("bad", [[0, 2], [0, -1], [0, 0.1], [[0, 1]], [np.nan]])
def test_reject_invalid_bits(bad):
    with pytest.raises(ValueError):
        binary(bad)


@pytest.mark.parametrize(
    "family,order", [("qam", 8), ("psk", 3), ("fsk", 4), ("psk", 512), ("psk", True)]
)
def test_reject_invalid_constellation(family, order):
    with pytest.raises(ValueError):
        constellation(family, order)


@pytest.mark.parametrize("kind", ["none", "repetition", "hamming"])
def test_coding_roundtrip(kind):
    bits = np.random.default_rng(43).integers(0, 2, 400)
    np.testing.assert_array_equal(decode(encode(bits, kind), kind), bits)


def test_hamming_corrects_any_single_error_in_every_codeword():
    bits = ((np.arange(16)[:, None] >> np.arange(3, -1, -1)) & 1).ravel()
    coded = encode(bits, "hamming").reshape(-1, 7)
    for position in range(7):
        damaged = coded.copy()
        damaged[:, position] ^= 1
        np.testing.assert_array_equal(decode(damaged.ravel(), "hamming"), bits)


def test_awgn_noise_scaling_and_qpsk_theory_equality():
    samples = np.ones(200000, dtype=np.complex128)
    noisy, gain = transmit(samples, 0, 2, np.random.default_rng(42))
    np.testing.assert_allclose(gain, 1)
    assert np.var((noisy - samples).real) == pytest.approx(0.25, rel=0.02)
    assert np.var((noisy - samples).imag) == pytest.approx(0.25, rel=0.02)
    assert ber(4, "psk", 2, "awgn") == ber(4, "psk", 4, "awgn")


@pytest.mark.parametrize("kind", ["rayleigh", "rician"])
def test_fading_mean_energy(kind):
    _, gain = transmit(
        np.ones(200000, dtype=np.complex128), 4, 1, np.random.default_rng(99), kind
    )
    assert np.mean(np.abs(gain) ** 2) == pytest.approx(1, rel=0.02)


def test_wilson_zero_events_has_positive_upper_bound():
    lo, hi = wilson(0, 1000)
    assert lo == pytest.approx(0, abs=1e-15)
    assert 0 < hi < 0.004
    with pytest.raises(ValueError):
        wilson(1, 0)
