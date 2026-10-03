# Analytical comparisons

Let `γ=Eb/N0` on a linear scale and `Q(x)=erfc(x/√2)/2`.

| Setting | Bit error probability | Status |
|---|---|---|
| Coherent BPSK / AWGN | `Q(√(2γ))` | Exact under the conventions |
| Gray QPSK / AWGN | `Q(√(2γ))` | Exact; same bit-energy curve as BPSK |
| BPSK / independent Rayleigh, known gain | `(1−√(γ/(1+γ)))/2` | Exact average over fading |
| Gray square M-QAM / AWGN | `(4/k)(1−1/√M)Q(√(3kγ/(M−1)))` | Nearest-neighbour approximation; most useful at moderate/high SNR |

QPSK Rayleigh uses the BPSK marginal expression under perfect coherent detection,
although its symbol's bit errors share a gain. Higher-order PSK, Rician and coded
cases have no theory overlay in this implementation. Their simulation is not
claimed to have an independently verified analytical match. QAM approximations
are labelled in the CSV and should not be read as low-SNR exact predictions.

Primary references:

- [MathWorks analytical expressions for AWGN](https://www.mathworks.com/help/comm/ug/analytical-expressions-used-in-berawgn-function-and-bit-error-rate-analysis-app.html)
- [MathWorks analytical expressions for fading](https://www.mathworks.com/help/comm/ug/analytical-expressions-used-in-berfading-function-and-bit-error-rate-analysis-app.html)
- [NIST binomial proportion intervals](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm)

These links document the conventions and formulas. Measured values are generated
by this repository's runner and are never copied from a reference curve.
