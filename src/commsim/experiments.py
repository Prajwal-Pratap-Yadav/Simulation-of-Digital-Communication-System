"""Validated Monte Carlo experiments; never interpret no errors as a zero BER."""

import csv
import hashlib
import json
import math
import platform
import subprocess
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import scipy

from .channel import transmit
from .coding import code_rate, decode, encode
from .modulation import constellation
from .theory import ber, wilson


@dataclass(frozen=True)
class Curve:
    name: str
    family: str
    order: int
    channel: str = "awgn"
    coding: str = "none"
    rician_k: float = 5.0

    def __post_init__(self) -> None:
        if not self.name or len(self.name) > 80:
            raise ValueError("curve name must contain 1 to 80 characters")
        constellation(self.family, self.order)
        code_rate(self.coding)
        if self.channel not in {"awgn", "rayleigh", "rician"}:
            raise ValueError("unknown channel")
        if not math.isfinite(self.rician_k) or self.rician_k < 0:
            raise ValueError("Rician K must be finite and nonnegative")


@dataclass(frozen=True)
class Config:
    seed: int
    ebn0_db: tuple[float, ...]
    min_errors: int
    max_bits: int
    batch_bits: int
    curves: tuple[Curve, ...]

    def __post_init__(self) -> None:
        for name in ("seed", "min_errors", "max_bits", "batch_bits"):
            value = getattr(self, name)
            if type(value) is not int or value < (0 if name == "seed" else 1):
                raise ValueError(f"{name} must be an integer in range")
        if not self.ebn0_db or not all(
            math.isfinite(x) and -100 <= x <= 100 for x in self.ebn0_db
        ):
            raise ValueError("provide finite Eb/N0 values within [-100,100]")
        if not self.curves or len({c.name for c in self.curves}) != len(self.curves):
            raise ValueError("provide uniquely named curves")
        if self.batch_bits > 100000 or self.max_bits > 100000000:
            raise ValueError("batch/bit cap exceeds the documented resource limit")
        for c in self.curves:
            k = constellation(c.family, c.order).k
            align = alignment(k, c.coding)
            if min(self.batch_bits, self.max_bits) < align:
                raise ValueError("bit budget cannot hold one complete coding block")

    @classmethod
    def load(cls, path: Path) -> "Config":
        raw = json.loads(path.read_text())
        raw["curves"] = tuple(Curve(**c) for c in raw["curves"])
        raw["ebn0_db"] = tuple(raw["ebn0_db"])
        return cls(**raw)


def alignment(k: int, coding: str) -> int:
    if coding == "hamming":
        return 4 * k // math.gcd(7, k)
    if coding == "repetition":
        return k // math.gcd(3, k)
    return k


def simulate_point(curve: Curve, ebn0_db: float, config: Config, seed: Any) -> dict:
    rng = np.random.default_rng(seed)
    modem = constellation(curve.family, curve.order)
    align = alignment(modem.k, curve.coding)
    errors = bits = 0
    started = time.perf_counter()
    while errors < config.min_errors and bits + align <= config.max_bits:
        n = min(config.batch_bits, config.max_bits - bits) // align * align
        source = rng.integers(0, 2, n, dtype=np.uint8)
        symbols = modem.modulate(encode(source, curve.coding))
        received, gain = transmit(
            symbols,
            ebn0_db,
            modem.k,
            rng,
            curve.channel,
            code_rate(curve.coding),
            curve.rician_k,
        )
        decided = decode(modem.demodulate(received / gain), curve.coding)
        errors += int(np.count_nonzero(decided != source))
        bits += n
    low, high = wilson(errors, bits)
    theoretical = (
        None
        if curve.coding != "none"
        else ber(ebn0_db, curve.family, curve.order, curve.channel)
    )
    return {
        "curve": curve.name,
        "family": curve.family,
        "order": curve.order,
        "channel": curve.channel,
        "coding": curve.coding,
        "ebn0_db": ebn0_db,
        "errors": errors,
        "information_bits": bits,
        "ber": errors / bits,
        "wilson_low": low,
        "wilson_high": high,
        "theory": theoretical,
        "theory_kind": (
            "square-QAM approximation"
            if curve.family == "qam"
            else ("exact" if theoretical is not None else "not available")
        ),
        "stop_reason": "error_target" if errors >= config.min_errors else "bit_cap",
        "elapsed_seconds": time.perf_counter() - started,
    }


def run(config: Config, output: Path) -> list[dict]:
    output.mkdir(parents=True, exist_ok=True)
    count = len(config.curves) * len(config.ebn0_db)
    seeds = np.random.SeedSequence(config.seed).spawn(count)
    rows = [
        simulate_point(curve, snr, config, seeds[i * len(config.ebn0_db) + j])
        for i, curve in enumerate(config.curves)
        for j, snr in enumerate(config.ebn0_db)
    ]
    with (output / "ber.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    try:
        sha = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        sha = "unavailable"
    manifest = {
        "commit": sha,
        "date_utc": datetime.now(UTC).isoformat(),
        "config": asdict(config),
        "config_sha256": hashlib.sha256(
            json.dumps(asdict(config), sort_keys=True).encode()
        ).hexdigest(),
        "environment": {
            "os": platform.platform(),
            "python": platform.python_version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "accelerator": "CPU",
        },
        "elapsed_seconds": sum(r["elapsed_seconds"] for r in rows),
        "interval_note": (
            "Pointwise Wilson intervals; nominal coverage is not guaranteed "
            "under adaptive stopping or correlated errors."
        ),
    }
    (output / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    from .plotting import figures

    figures(rows, config, output / "figures")
    return rows
