# Energy, bit order and channel conventions

The reference is a symbol-rate, coherent baseband experiment with perfect timing,
carrier phase and receiver channel-state knowledge. It does not model a complete
radio, bandwidth allocation, pulse shaping, interference or hardware impairments.

- Every maintained constellation has mean symbol energy `Es=1` over all points.
- `k=log2(M)` coded bits occupy each symbol. `R` is information bits / coded bits.
- `Eb=Es/(k R)` is energy per **information** bit. Consequently
  `Es/N0[dB]=Eb/N0[dB]+10 log10(k R)`. For uncoded signalling, `R=1`.
- Circular complex noise has variance `N0/2` in each real dimension, with
  `N0=1/(k R 10^(EbN0_dB/10))`. There is one sample per symbol; no unspecified
  sample-rate SNR conversion is used.
- Python uses adjacent bits, MSB first, and Gray labels around PSK and on both
  QAM axes. The corrected MATLAB script uses adjacent I/Q bits. Constellations
  can differ by a rotation/reflection while retaining the same BER.
- Rayleigh and Rician gains are independent per symbol, with `E[|h|²]=1`.
  Rician `K` is a **linear** power ratio. The receiver divides by the known gain.
- Repetition uses three transmissions and majority decisions. Hamming(7,4)
  corrects single errors, but can miscorrect multiple errors. Comparison uses
  information-bit energy, including the code rate; no coding gain is assumed.
- Complete blocks fit within the information-bit cap. A small unused remainder
  is possible for higher-order modulation or Hamming coding.

The original root experiment is archived unchanged in `legacy/original/`.
Its QPSK points have `Es=2`, yet its noise uses `Es=1` scaling. Its QPSK theory
also omits the factor two in the square root. The historical conclusion that
BPSK necessarily has lower BER at equal bit energy is therefore not retained.

## Monte Carlo interpretation

The default runner stops at a minimum error count or a maximum information-bit
count, checking after each batch. It can overshoot the error target by a batch.
Pointwise Wilson 95% intervals are descriptive; adaptive stopping does not
guarantee their nominal fixed-sample coverage. Bit errors within a QAM symbol,
fading QPSK symbol or decoded coding block can be correlated, so a binomial
interval can underestimate uncertainty there. Fixed-budget BPSK/uncoded-AWGN
tests use a predeclared six-sigma envelope to avoid flaky CI; that envelope is
separate from the plotted intervals. Zero observed errors produce a positive
upper bound, not proof of zero BER. No simultaneous-confidence claim is made.
