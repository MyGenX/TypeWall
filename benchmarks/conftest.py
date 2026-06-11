from __future__ import annotations

import importlib.metadata
import os
import platform
import subprocess
import sys
from typing import Any, Dict


def _revision() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip()


def pytest_benchmark_update_json(
    config: Any, benchmarks: Any, output_json: Dict[str, Any]
) -> None:
    output_json["typewall"] = {
        "python": sys.version,
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "revision": os.environ.get("GITHUB_SHA") or _revision(),
        "dependencies": {
            name: importlib.metadata.version(name)
            for name in ("typewall", "pytest", "pytest-benchmark")
        },
        "configuration": {
            "timer": config.getoption("benchmark_timer"),
            "min_rounds": config.getoption("benchmark_min_rounds"),
        },
    }
