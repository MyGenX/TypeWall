from pathlib import Path
from typing import Dict

import pytest

SUITE_MARKERS: Dict[str, str] = {
    "unit": "unit",
    "property": "property",
    "integration": "integration",
    "conformance": "conformance",
    "distribution": "distribution",
    "typing": "typing",
}


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        relative = Path(str(item.path)).parts
        for directory, marker in SUITE_MARKERS.items():
            if directory in relative:
                item.add_marker(getattr(pytest.mark, marker))
                break
