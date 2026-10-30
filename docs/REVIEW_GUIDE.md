# Digital communications simulation: review guide

Inspect how energy normalization, channel noise, coding, and theoretical references support a reproducible BER experiment.

## Follow the implementation

| Start here | File | What to inspect |
| --- | --- | --- |
| Modulation | [src/commsim/modulation.py](../src/commsim/modulation.py) | Symbol mapping and normalization. |
| Channel | [src/commsim/channel.py](../src/commsim/channel.py) | Noise injection and signal-to-noise conventions. |
| Coding | [src/commsim/coding.py](../src/commsim/coding.py) | Encoding/decoding behavior. |
| Theory | [src/commsim/theory.py](../src/commsim/theory.py) | Analytic reference curves. |
| Experiment tests | [tests/test_experiments.py](../tests/test_experiments.py) | End-to-end simulation contracts. |
| Conventions | [docs/conventions.md](../docs/conventions.md) | Definitions needed to compare numerical results. |

## Run the checks

Run from the repository root after the setup described in the [README](../README.md). Review fixtures and recorded evidence before starting any full experiment.

```bash
make setup
make test docs
make reproduce
```

## Interpret the evidence

Use the README's Python and MATLAB/Octave setup for the reference path. BER estimates use finite simulated bit budgets and confidence intervals. They are not measurements from a radio link, hardware receiver, or a field channel.

The linked reports retain their original experiment dates and protocols. A new passing CI run verifies its named checks; it does not silently refresh historical measurements.

## Discuss the design

- When does confusing Eb/N0 and Es/N0 shift an entire curve?
- How should a zero-error finite run be reported without claiming zero true error probability?
