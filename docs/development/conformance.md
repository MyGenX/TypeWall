---
title: "Integration Conformance Inventory"
description: "Capability scenarios and their verification targets"
---

| Capability scenario | Verification |
| --- | --- |
| Environment mapping, coercion, defaults, safety | `tests/integration/test_environment.py` |
| CLI targets, inputs, outputs, and exit codes | `tests/integration/test_cli.py` |
| Installed CLI smoke test | `tests/distribution/test_distribution_smoke.py` |
| JSON Schema and OpenAPI export | `tests/integration/test_export.py` |
| FastAPI request, 422, and OpenAPI behavior | `tests/integration/test_fastapi_integration.py` |
| Cross-feature adapter behavior | `tests/conformance/test_cross_feature.py` |
| Sensitive-value handling | `tests/conformance/test_sensitive_values.py` |
| Package metadata and optional dependency isolation | `tests/distribution/` and `scripts/check_base_dependencies.py` |
| Versioned artifact verification | `scripts/verify_release.py` |

The CI Python and FastAPI matrices execute these targets under the documented compatibility ranges.
