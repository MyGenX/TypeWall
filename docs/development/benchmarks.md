---
title: "Benchmarks"
description: "Run and compare deterministic benchmark workloads"
---

Install the benchmark group and run the deterministic workloads:

```shell
uv sync --group benchmark
uv run pytest benchmarks --benchmark-only --benchmark-json=benchmark-results/local.json
```

Compare with an earlier result using `uv run pytest-benchmark compare benchmark-results/*.json`. Results include interpreter, platform, plugin configuration, and source revision metadata. CI publishes JSON artifacts for trend analysis but does not enforce a fixed timing threshold.
