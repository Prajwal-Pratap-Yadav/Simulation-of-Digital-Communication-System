# Architecture

```mermaid
flowchart TD
  config[Experiment configuration]:::input --> runner[Seeded batch runner]:::proc
  runner --> coding[Optional block code]:::proc
  coding --> mapper[Unit-energy Gray constellation]:::proc
  mapper --> channel[AWGN or normalized fading]:::proc
  channel --> receiver[Known-gain coherent receiver]:::proc
  receiver --> decoder[Optional hard-decision decoder]:::proc
  decoder --> counts[Information-bit error counts]:::store
  counts --> csv[CSV and run manifest]:::store
  csv --> plots[BER intervals and constellation plots]:::out
  theory[Analytical reference]:::input --> plots
  classDef input fill:#0b1220,stroke:#38bdf8,color:#e2e8f0;
  classDef proc fill:#111827,stroke:#a78bfa,color:#e2e8f0;
  classDef store fill:#111827,stroke:#34d399,color:#e2e8f0;
  classDef out fill:#0b1220,stroke:#fbbf24,color:#e2e8f0;
```

`Config` validates settings before work begins. Each curve/SNR pair receives an
independent child seed, and batch sizes bound memory. The modem separates labels
from constellation geometry; the receiver makes minimum-distance decisions.
Code rate enters the channel energy calculation. Error counts and stopping
reasons are exported before plots are generated. Original evidence is isolated
from maintained implementations and is never used to establish corrected results.

The MATLAB-compatible reference is a separate BPSK/QPSK AWGN implementation.
Both it and the Python tests compare against the same stated analytical model.
Cross-language random streams and individual sample trajectories are not identical.
