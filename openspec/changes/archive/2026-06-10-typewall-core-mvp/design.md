## Context

TypeWall starts from an idea document rather than an existing implementation. The first phase must establish a small public API and internal validation protocol that later constraints, composition schemas, typing adapters, and framework integrations can extend without changing basic parse behavior.

## Goals / Non-Goals

**Goals:**

- Provide a framework-independent Python package with a compact builder API.
- Make schemas immutable and safe to reuse across requests and threads.
- Separate schema declaration from parsing state and error accumulation.
- Return parsed values while exposing deterministic, structured validation failures.
- Establish packaging and automated quality checks early.

**Non-Goals:**

- Coercion, transforms, custom refinements, advanced schema composition, or typing-derived schemas.
- JSON Schema, OpenAPI, environment, CLI, or web-framework integrations.
- Async validation or performance-specific native extensions.

## Decisions

1. **Use a root-level `typewall` package and `pyproject.toml` build configuration.** This keeps the package immediately visible in the small repository while package build and clean-wheel tests verify distribution behavior independently from local imports.

2. **Model schemas as immutable value objects.** Builder methods return new schema instances instead of mutating the receiver. This makes reusable schemas predictable and avoids cross-request state leakage. Mutable rule lists were considered because they are simpler initially, but they create aliasing problems.

3. **Use an internal parse context and a missing-value sentinel.** The context owns the current path and issue collection; a sentinel distinguishes an absent object field from an explicit `None`. Exceptions are created only at the public `parse()` boundary.

4. **Keep primitive parsing strict.** Core schemas validate runtime types and do not coerce strings or numbers. In particular, `bool` is not accepted as `int`, and `int` is not accepted as `float`. Coercion belongs in explicit boundary adapters so normal parsing remains predictable.

5. **Collect independent issues in one traversal.** Object fields and list elements continue after recoverable failures, preserving deterministic declaration/index order. This gives callers actionable results without repeated parse attempts.

6. **Reject unknown object keys by default.** Boundary validation should detect misspelled or unexpected input. Future policies can be added explicitly without weakening the MVP default.

7. **Copy default values when applied.** Mutable defaults must not be shared between parse calls. Factory defaults are deferred until there is a dedicated callable/default API.

8. **Expose typed issue and result objects.** `ValidationIssue` carries tuple paths, code, message, expected metadata, and a safe received-type description. `ValidationError` wraps ordered issues, and `ParseResult` provides mutually exclusive success and failure states.

## Risks / Trade-offs

- [Strict parsing can feel less convenient for boundary strings] -> Add coercion only in explicit adapters during the integration phase.
- [Rejecting unknown keys can be stricter than competing libraries] -> Document the policy and reserve an explicit policy API for a later proposal.
- [Collecting all issues uses more work than fail-fast parsing] -> Keep traversal linear and benchmark representative nested payloads before release.
- [Generic typing may be limited in the MVP] -> Keep runtime contracts stable and improve static output typing in the enhancement phase.

## Migration Plan

This is a greenfield package. Implement package foundations first, then schema protocol and errors, then primitives and structured schemas. Do not begin the enhancement phase until the MVP conformance and package-build checks pass.

## Open Questions

- Whether a future unknown-key option should support only reject/preserve or also strip behavior.
- Whether factory defaults should be a separate API or inferred from callable values.
