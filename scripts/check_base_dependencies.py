from __future__ import annotations

import argparse
import email.parser
import zipfile
from pathlib import Path

FORBIDDEN_BASE_REQUIREMENTS = {
    "fastapi",
    "httpx",
    "pytest",
    "pytest-benchmark",
}


def normalized_name(requirement: str) -> str:
    head = requirement.split(";", 1)[0]
    for separator in ("[", "<", ">", "=", "!", "~", " "):
        head = head.split(separator, 1)[0]
    return head.strip().lower().replace("_", "-")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("wheel", type=Path)
    args = parser.parse_args()

    with zipfile.ZipFile(args.wheel) as archive:
        metadata_name = next(
            name for name in archive.namelist() if name.endswith(".dist-info/METADATA")
        )
        parsed = email.parser.Parser().parsestr(
            archive.read(metadata_name).decode("utf-8")
        )

    violations = []
    for requirement in parsed.get_all("Requires-Dist", []):
        if "extra ==" in requirement:
            continue
        if normalized_name(requirement) in FORBIDDEN_BASE_REQUIREMENTS:
            violations.append(requirement)
    if violations:
        raise SystemExit(f"Forbidden base requirements: {violations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
