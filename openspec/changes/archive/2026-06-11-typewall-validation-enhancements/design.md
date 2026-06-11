## Context

This phase assumes the MVP schema protocol, immutable builders, parse context, and structured errors are complete. It expands the validation language while preserving strict core parsing and the existing `parse()` and `safe_parse()` contracts.

## Goals / Non-Goals

**Goals:**

- Cover common production constraints and composite data shapes.
- Allow controlled custom validation and output transformation.
- Improve static output typing and derive schemas from selected standard-library type declarations.
- Keep every new builder immutable and every failure path deterministic.

**Non-Goals:**

- Framework adapters, environment coercion, CLI behavior, or schema export.
- Full interpretation of every `typing` construct or arbitrary user classes.
- Async refinements or transforms.

## Decisions

1. **Represent constraints as ordered immutable rule objects.** Rule metadata supports both runtime validation and later schema export. Ad-hoc lambdas remain available only through explicit refinement APIs.

2. **Use standards-aware parsing for formatted strings.** Email validation uses the focused `email-validator` package with deliverability checks disabled, while URL and UUID checks use standard-library parsers. This keeps email syntax standards-aware without network-dependent parsing, and avoids a permissive handwritten regex.

3. **Evaluate union branches independently against the original value.** The first successful branch in declaration order wins. If all fail, a top-level union issue retains per-branch issues for inspection without flattening away branch context.

4. **Define intersections as validation by all members.** Non-mapping results must be equal; mapping results are merged only when overlapping keys have equal values. Conflicts fail explicitly.

5. **Run base validation and constraints before custom processing.** Refinements execute in declaration order, followed by transforms in declaration order. Transform output becomes the schema result. Unexpected user callback exceptions are wrapped as structured callback issues with the original exception chained.

6. **Make schemas generic in output type.** Builder methods preserve or intentionally change `Schema[T]`; transforms produce `Schema[U]`. Static conformance is checked with both MyPy and Pyright fixtures where their supported behavior overlaps.

7. **Limit `schema_from_type()` to explicit supported constructs.** Initial support includes primitive types, `Any`, `None`, `list`, `dict`, fixed tuples, unions/optionals, `Literal`, `TypedDict`, and dataclasses. Unsupported annotations fail at schema construction with a path to the unsupported annotation.

8. **Handle recursive typing declarations defensively.** Cache schemas under construction and use lazy references where required; irreducible cycles fail with a clear construction error rather than recursion overflow.

## Risks / Trade-offs

- [Email and URL standards contain edge cases] -> Use documented standards behavior and conformance fixtures.
- [Union errors can become large] -> Keep branch structure inspectable and provide concise default formatting.
- [Transforms make exported schemas incomplete] -> The integration phase must reject or explicitly annotate non-representable behavior.
- [Typing tools differ] -> Test a conservative shared contract and document tool-specific limitations.
- [Runtime annotation introspection changes across Python versions] -> Maintain a compatibility matrix and fixtures for every supported Python version.

## Migration Plan

Implement constraints first, then composition, then custom processing, and finally typing integration. Run the complete MVP regression suite after each group. The integration phase starts only after runtime, property-oriented, and static typing checks pass.

## Open Questions

- Decide whether transformed schemas expose both input and output generic parameters in a future typing revision.
