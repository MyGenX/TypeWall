from importlib.metadata import metadata, version
from pathlib import Path

import typewall


def test_installed_distribution_metadata_and_import() -> None:
    assert version("typewall") == "0.1.0"
    assert metadata("typewall")["Requires-Python"] == ">=3.9"
    assert typewall.w.str().parse("installed") == "installed"


def test_typed_package_marker_is_installed() -> None:
    package_root = Path(typewall.__file__).parent
    assert (package_root / "py.typed").is_file()
