# ADR 0002: expose stopping rules and uncertainty limitations

Status: accepted.

The runner uses error-event stopping with a bit cap to avoid wasting computation
at high BER and producing misleading zero-error points at low BER. It records
both counts and stopping reasons. Wilson intervals communicate finite sampling
but are explicitly descriptive under adaptive stopping and correlated errors.

A fixed small bit count was rejected because it hides very low BER; a guarantee
of nominal sequential coverage was rejected because that requires a confidence
sequence or separately validated stopping-aware inference. Exact-theory
regression tests use fixed budgets and a predeclared wider tolerance.

Trade-off: the plots are useful diagnostics, not simultaneous statistical
certificates. A confidence-sequence enhancement remains a roadmap item.
