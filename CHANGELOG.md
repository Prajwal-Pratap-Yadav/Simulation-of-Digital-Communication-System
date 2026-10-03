# Changelog

Changes follow the Keep a Changelog categories. Versioning uses Semantic Versioning.

## 0.1.0

### Added
- Portable Python package with Gray PSK/QAM, AWGN/Rayleigh/Rician channels,
  optional repetition and Hamming coding, bounded Monte Carlo runs and real plots.
- Configuration validation, error counts, stopping reasons, run manifests and
  explicitly limited Wilson intervals.
- Unit, CLI, legacy-characterization and theory-agreement tests; pinned CI,
  dependency locks, security checks and contributor documentation.

### Fixed
- MATLAB QPSK energy normalization and the bit-error theory expression.
- Removed unsupported current conclusions while preserving the original files.

### Known limitations
- Symbol-rate coherent model with perfect synchronization and channel knowledge.
- Statistical intervals are descriptive under adaptive stopping/correlated errors.
- No pulse shaping, hardware validation or convolutional coding.
