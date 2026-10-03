"""Figures rendered from actual recorded symbol-rate experiments."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .channel import transmit
from .modulation import constellation


def figures(rows: list[dict], config: object, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    with plt.style.context("seaborn-v0_8-whitegrid"):
        fig, ax = plt.subplots(figsize=(10, 6), layout="constrained")
        names = list(dict.fromkeys(r["curve"] for r in rows))
        for name in names:
            rr = [r for r in rows if r["curve"] == name]
            x = np.array([r["ebn0_db"] for r in rr])
            y = np.array([r["ber"] for r in rr])
            lo = np.array([r["wilson_low"] for r in rr])
            hi = np.array([r["wilson_high"] for r in rr])
            displayed = np.where(y > 0, y, hi)
            line = ax.plot(x, displayed, "o-", ms=4, lw=1, label=name)[0]
            positive = y > 0
            ax.errorbar(
                x[positive],
                y[positive],
                yerr=[y[positive] - lo[positive], hi[positive] - y[positive]],
                fmt="none",
                capsize=3,
                color=line.get_color(),
            )
            if np.any(~positive):
                ax.scatter(
                    x[~positive], hi[~positive], marker="v", color=line.get_color()
                )
            theory = np.array(
                [r["theory"] if r["theory"] is not None else np.nan for r in rr]
            )
            if np.any(np.isfinite(theory)):
                ax.plot(x, theory, "--", color=line.get_color(), alpha=0.8)
        ax.set(
            yscale="log",
            xlabel=r"$E_b/N_0$ per information bit (dB)",
            ylabel="Bit error rate",
            title="Measured BER with pointwise Wilson 95% intervals",
        )
        ax.legend(fontsize=8, ncols=2)
        ax.text(
            0.02,
            0.02,
            "Dashed: theory (QAM: approximation). ▼: zero-event upper bound.\n"
            "Perfect coherent detection; adaptive stopping; intervals are descriptive.",
            transform=ax.transAxes,
            fontsize=8,
            bbox={"facecolor": "white", "alpha": 0.85},
        )
        fig.savefig(output / "ber.png", dpi=180)
        fig.savefig(output / "ber.svg")
        plt.close(fig)

        fig, axes = plt.subplots(1, 3, figsize=(12, 4), layout="constrained")
        for ax, (family, order) in zip(
            axes, [("psk", 2), ("psk", 4), ("qam", 16)], strict=True
        ):
            modem = constellation(family, order)
            rng = np.random.default_rng(2026 + order)
            bits = rng.integers(0, 2, 1500 * modem.k, dtype=np.uint8)
            noisy, _ = transmit(modem.modulate(bits), 8, modem.k, rng)
            ax.scatter(noisy.real, noisy.imag, s=3, alpha=0.18)
            ax.scatter(
                modem.points.real, modem.points.imag, marker="x", color="black", s=50
            )
            ax.set(
                title=f"{order}-{family.upper()}, AWGN, 8 dB",
                xlabel="In-phase",
                ylabel="Quadrature",
                aspect="equal",
            )
        fig.savefig(output / "constellations.png", dpi=180)
        plt.close(fig)
