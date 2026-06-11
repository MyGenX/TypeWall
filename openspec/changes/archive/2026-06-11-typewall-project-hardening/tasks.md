## 1. Package Architecture

- [x] 1.1 Create `core`, `schemas`, `adapters`, and `integrations` implementation packages with Python 3.9-compatible exports
- [x] 1.2 Move core parsing contracts, errors, context, and sentinels into `typewall.core`
- [x] 1.3 Move schema builders and implementations into `typewall.schemas` and enforce dependency direction
- [x] 1.4 Move environment, export, and CLI boundaries into `typewall.adapters`
- [x] 1.5 Move FastAPI support into `typewall.integrations` without adding framework imports to lower layers
- [x] 1.6 Add legacy-path compatibility shims and preserve the root public API and console entry point
- [x] 1.7 Add identity, isolated-import, optional-dependency, and circular-import regression tests

## 2. Repository and Test Organization

- [x] 2.1 Create stable `docs`, `examples`, `benchmarks`, and responsibility-specific test directories
- [x] 2.2 Reorganize unit, property, integration, conformance, distribution, and typing tests without losing collection
- [x] 2.3 Define pytest markers and commands for focused suites plus the complete suite
- [x] 2.4 Extend `.gitignore` for documentation builds, benchmark output, coverage formats, environments, caches, and distributions
- [x] 2.5 Verify focused and unfiltered test collection after the move

## 3. Documentation and Examples

- [x] 3.1 Configure MkDocs Material, mkdocstrings, strict navigation, and version metadata
- [x] 3.2 Rewrite the README for current capabilities, extras, Python support, quick start, errors, and documentation links
- [x] 3.3 Add guides for constraints, composition, custom processing, typing, environment parsing, CLI, export, and FastAPI
- [x] 3.4 Add generated API reference pages for the complete supported public surface
- [x] 3.5 Add runnable configuration, CLI, and FastAPI example projects with declared dependencies
- [x] 3.6 Add automated documentation build, link, snippet, and built-wheel example checks

## 4. Packaging and Quality Automation

- [x] 4.1 Complete project metadata, URLs, classifiers, typed marker inclusion, changelog, and artifact inclusion rules
- [x] 4.2 Add CI jobs for formatting, linting, MyPy, Pyright, negative typing, and branch coverage
- [x] 4.3 Add Python 3.9-3.14 unit, property, integration, and conformance matrix coverage
- [x] 4.4 Add independent wheel and source-distribution installation checks across the supported Python matrix
- [x] 4.5 Add optional dependency and build metadata checks that reject framework, docs, benchmark, or test dependencies from the base install
- [x] 4.6 Add project-version, built-metadata, release-tag, and changelog consistency verification

## 5. Benchmark Suite

- [x] 5.1 Add deterministic primitive, flat-object, nested-collection, successful, and aggregated-failure benchmark workloads
- [x] 5.2 Record interpreter, platform, dependency, configuration, and source-revision metadata in JSON output
- [x] 5.3 Add a CI benchmark job that uploads comparison artifacts without a fixed timing threshold
- [x] 5.4 Document local benchmark execution, recording, and comparison

## 6. Integration Conformance

- [x] 6.1 Add a maintained inventory mapping every integration specification scenario to an executable verification
- [x] 6.2 Add cross-feature tests for typing-derived exports, environment defaults, CLI structured errors, and FastAPI OpenAPI output
- [x] 6.3 Add security tests proving environment, CLI, and framework errors do not expose complete sensitive values
- [x] 6.4 Run the complete MVP, enhancement, integration, and conformance suites with branch coverage

## 7. Final Verification

- [x] 7.1 Build strict documentation and execute all examples against the built wheel
- [x] 7.2 Build and inspect wheel and sdist, then run isolated base and optional-integration smoke tests
- [x] 7.3 Run Ruff formatting and linting, MyPy, Pyright, negative typing checks, full tests, and benchmarks
- [x] 7.4 Validate `typewall-project-hardening` and `typewall-integrations-release` with strict OpenSpec validation
- [x] 7.5 Confirm external TestPyPI and PyPI operations remain deferred to `typewall-0-2-0-release`
