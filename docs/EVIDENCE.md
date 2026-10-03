# Evidence register

All experimental values come from generated artifacts. No original prose claim
is promoted to a corrected measurement. Source commit `ab49971d23ad55cf27fc7417322339fa06a2a4f1`
is the published implementation used for the measured run below.

| Claim | Value | Command | Source commit | Date | Environment | Artifact |
|---|---|---|---|---|---|---|
| BER curves and counts | Per-point values, not a rounded headline | `make reproduce` | `ab49971d23ad55cf27fc7417322339fa06a2a4f1` | In manifest | Linux, CPU, Python/NumPy/SciPy versions in manifest | [ber.csv](../reports/ber.csv), [manifest](../reports/run_manifest.json) |
| Plotted uncertainty | Pointwise descriptive Wilson intervals; no simultaneous or stopping-aware claim | `make reproduce` | Same | In manifest | Same | [BER figure](../reports/figures/ber.png) |
| Constellation geometry and noise | Generated samples at the settings labelled in the plot | `make reproduce` | Same | In manifest | Same | [Constellations](../reports/figures/constellations.png) |
| Automated contracts and theory tolerance | Exact test counts and outcomes in JUnit | `.venv/bin/python -m pytest --junitxml=reports/test-results.xml -q` | Same | In JUnit | Same installed environment | [test-results.xml](../reports/test-results.xml) |
| Full-history secret scan | No detected findings; regex scan is not proof of absence | `gitleaks detect --log-opts="--all" --redact` | Same implementation, plus unpublished local duplicates | 2026-10-03 | Gitleaks v8.30.1 on Linux | [history-secrets.json](../reports/history-secrets.json) |
| Runtime dependency audit | Findings listed explicitly; feed-dependent | `.venv/bin/python -m pip_audit -r requirements-runtime.lock --strict` | Same | 2026-10-03 | pip-audit 2.9.0, locked dependency set | [dependency-audit.json](../reports/dependency-audit.json) |
| Fresh-clone quickstart | Timings and cache condition in JSON; no general installation-speed claim | Clone the branch, then `make setup run` | `0f18b13a0e1eb6f91e9dca9633031be049cd6308` | 2026-10-03 | Fresh virtual environment, cached wheels, Linux CPU | [quality-gates.json](../reports/quality-gates.json) |

CI uses a fixed-budget, predeclared wider statistical tolerance for the exact
AWGN and Rayleigh cases. The plotted adaptive runs use a different purpose and
are not required to put every theoretical point inside a nominal 95% interval.
No confidence claim is made for all curves jointly. QAM theory is approximate,
and block/fading errors can correlate. Coding gain is not reported as a headline.

The MATLAB-compatible reference is exercised in its separate CI job. Local
MATLAB/Octave is unavailable. A green remote job is required before saying that
the reference was executed; the Python transliteration alone is not that evidence.
