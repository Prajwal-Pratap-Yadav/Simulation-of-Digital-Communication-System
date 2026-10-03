import csv
import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from commsim.experiments import Config, Curve, simulate_point
from commsim.theory import wilson

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    "order,channel,snr", [(2, "awgn", 0), (4, "awgn", 4), (2, "rayleigh", 4)]
)
def test_fixed_budget_agrees_with_exact_theory(order, channel, snr):
    curve = Curve("test", "psk", order, channel)
    cfg = Config(17, (snr,), 1000000, 400000, 20000, (curve,))
    row = simulate_point(curve, snr, cfg, 17)
    # Six sigma is a predeclared CI regression tolerance, not a published 95% CI.
    # Fixed budget avoids optional-stopping ambiguity in this theory test.
    lo, hi = wilson(row["errors"], row["information_bits"], z=6)
    assert lo <= row["theory"] <= hi
    assert row["stop_reason"] == "bit_cap"


def test_repeatability_excluding_wall_clock():
    cfg = Config.load(ROOT / "configs/smoke.json")
    a = simulate_point(cfg.curves[0], 0, cfg, 23)
    b = simulate_point(cfg.curves[0], 0, cfg, 23)
    a.pop("elapsed_seconds")
    b.pop("elapsed_seconds")
    assert a == b


@pytest.mark.parametrize("coding", ["none", "repetition", "hamming"])
def test_complete_blocks_never_exceed_cap(coding):
    curve = Curve("bounded", "qam", 64, coding=coding)
    cfg = Config(1, (100,), 100, 101, 91, (curve,))
    row = simulate_point(curve, 100, cfg, 1)
    assert 0 < row["information_bits"] <= 101
    assert row["errors"] == 0


def test_invalid_config_fails_before_running():
    cfg = Config.load(ROOT / "configs/smoke.json")
    for values in [
        {"max_bits": 0},
        {"seed": -1},
        {"batch_bits": 1.5},
        {"ebn0_db": (np.nan,)},
        {"curves": ()},
    ]:
        with pytest.raises(ValueError):
            replace(cfg, **values)


def test_cli_generates_real_artifacts(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "commsim.cli",
            "--config",
            str(ROOT / "configs/smoke.json"),
            "--output",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Recorded 2 BER points" in result.stdout
    rows = list(csv.DictReader((tmp_path / "ber.csv").open()))
    assert len(rows) == 2
    assert (tmp_path / "figures/ber.png").stat().st_size > 1000
    manifest = json.loads((tmp_path / "run_manifest.json").read_text())
    assert manifest["environment"]["accelerator"] == "CPU"
    assert manifest["config"]["seed"] == 7
