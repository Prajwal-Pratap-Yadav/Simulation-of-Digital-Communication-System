# ADR 0001: retain MATLAB and add a tested Python extension

Status: accepted.

The original experiment is MATLAB. Its files must remain readable evidence,
yet the code depends on toolbox functions and has an energy/theory mismatch.
The maintained reference uses base MATLAB/Octave functions. A Python package
adds bounded, swappable experiments, tests and portable report generation.

Replacing all MATLAB code would discard the project's origin. Leaving only
the uploaded script would prevent reproducible validation. A full radio stack
would require assumptions and validation beyond this project's scope.

Trade-off: two implementations require independent checks. They are compared
against theory, rather than expected to produce identical random sample streams.
