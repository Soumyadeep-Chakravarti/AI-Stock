# Development Conventions

- Use `Decimal` for monetary values and returns.
- Use UTC-aware `datetime` values for normalized provider timestamps.
- Use frozen, slotted dataclasses for value models.
- Use protocols at dependency boundaries.
- Keep provider schemas and identifiers out of generic analysis.
- Prefer standard-library functionality unless a dependency has a concrete benefit.
- Keep pure analysis and scanner orchestration separately testable.
- Treat live scans as evidence for design decisions, not as test fixtures.

When adding a new external source, translate it at the provider boundary first. Do not expand the generic model until the source semantics justify a new shared concept.

When adding policy, distinguish mathematical detection from confidence, cost, and execution assumptions. This separation is what lets the same gross detector support different regions and future providers.
