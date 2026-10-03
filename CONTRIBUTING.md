# Contributing

Use Python 3.11 or 3.12 and GNU Make on Linux/macOS. Run `make setup` then
`make lint typecheck test docs build`. Small synthetic tests are not benchmarks.
Use a feature branch and a pull request; include the command, seed, environment,
source commit and report for changed scientific claims. Run `make reproduce`
after modifying signal processing. Preserve `legacy/original/` byte for byte.

New channel/modulation/coding blocks need roundtrip or contract tests and a
stated energy convention. Keep incomplete work in an issue rather than empty
modules. Never commit credentials, private data, caches or unreviewed binaries.
Install staged-file checks with `.venv/bin/python -m pre_commit install`.
Regenerate lockfiles for the minimum supported Python version when dependencies
change, and verify both Python versions in CI. Security concerns go through
the reporting route in [SECURITY.md](SECURITY.md).
