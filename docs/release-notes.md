# Digital Communication Simulation 0.1.0

The first maintained experimental release corrects the original QPSK energy and
theory mismatch, preserves historical files unchanged, and adds a reproducible
Python package with normalized PSK/QAM, noise/fading channels, optional block
codes and measured diagnostic figures.

Requirements: Python 3.11 or 3.12 on Linux/macOS for the tested Make workflow.
Install from the repository with `make setup`, run `make run`, and regenerate
the evidence with `make reproduce`. The wheel/sdist are built by the validated
release job; SHA256SUMS records their checksums. Keep the repository's `configs/`
files available when using the CLI, or pass an explicit configuration path.

Validation: Python contract/CLI/theory tests, lint, types, documentation, build,
dependency audit and history scan; the MATLAB-compatible reference is checked
in GNU Octave. The exact CI run is visible on the tagged source commit.

Known limitations: experimental symbol-rate coherent model; perfect timing and
channel knowledge; QAM theory approximation; descriptive intervals under
adaptive stopping/correlated errors; no pulse-shaped or hardware validation.
Scientific claims trace to `docs/EVIDENCE.md`, the CSV and run manifest.
