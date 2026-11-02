"""Analytical status in exported rows must describe an available comparison."""

import pytest

from commsim.experiments import Config, Curve, simulate_point
from commsim.theory import ber


@pytest.mark.parametrize(
    "family,order,channel,coding,expected",
    [
        ("psk", 2, "awgn", "none", "exact"),
        ("psk", 4, "rayleigh", "none", "exact"),
        ("qam", 16, "awgn", "none", "square-QAM approximation"),
        ("qam", 16, "rayleigh", "none", "not available"),
        ("qam", 16, "rician", "none", "not available"),
        ("qam", 16, "awgn", "hamming", "not available"),
        ("qam", 16, "awgn", "repetition", "not available"),
        ("psk", 8, "awgn", "none", "not available"),
    ],
)
def test_exported_theory_status(family, order, channel, coding, expected):
    curve = Curve("fixture", family, order, channel, coding)
    config = Config(17, (0,), 1000, 128, 64, (curve,))
    row = simulate_point(curve, 0, config, 17)
    assert row["theory_kind"] == expected
    if expected == "not available":
        assert row["theory"] is None
    else:
        assert row["theory"] == ber(0, family, order, channel)


@pytest.mark.parametrize("family", ["PSK", "PsK", "QAM", "QaM"])
def test_accepted_family_case_does_not_change_theory_or_random_results(family):
    mixed = Curve("fixture", family, 4)
    canonical = Curve("fixture", family.lower(), 4)
    assert mixed == canonical
    config = Config(17, (0,), 1000, 128, 64, (mixed,))
    first = simulate_point(mixed, 0, config, 17)
    second = simulate_point(canonical, 0, config, 17)
    first.pop("elapsed_seconds")
    second.pop("elapsed_seconds")
    assert first == second
    assert first["theory"] is not None
