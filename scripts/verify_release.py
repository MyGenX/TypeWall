from __future__ import annotations

import argparse
import email.parser
import hashlib
import tarfile
import zipfile
from pathlib import Path
from typing import Any, Dict

try:
    import tomllib
except ImportError:  # pragma: no cover - Python 3.9 and 3.10
    import tomli as tomllib


def project_data(root: Path) -> Dict[str, Any]:
    return tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))[
        "project"
    ]


def wheel_metadata(path: Path) -> email.message.Message:
    with zipfile.ZipFile(path) as archive:
        metadata_name = next(
            name for name in archive.namelist() if name.endswith(".dist-info/METADATA")
        )
        return email.parser.Parser().parsestr(
            archive.read(metadata_name).decode("utf-8")
        )


def verify_contents(wheel: Path, sdist: Path) -> None:
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
        required = {
            "typewall/__init__.py",
            "typewall/py.typed",
            "typewall/core/schema.py",
            "typewall/schemas/builder.py",
            "typewall/adapters/cli.py",
        }
        missing = required - names
        if missing:
            raise SystemExit(f"Wheel is missing: {sorted(missing)}")
    with tarfile.open(sdist) as archive:
        names = {name.split("/", 1)[-1] for name in archive.getnames()}
        required = {"README.md", "CHANGELOG.md", "mkdocs.yml", "docs/index.md"}
        missing = required - names
        if missing:
            raise SystemExit(f"Source distribution is missing: {sorted(missing)}")


def write_hashes(paths: tuple[Path, ...], output: Path) -> None:
    lines = []
    for path in paths:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.name}")
    output.write_text("\n".join(lines) + "\n", encoding="ascii")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--tag")
    parser.add_argument("--wheel", type=Path)
    parser.add_argument("--sdist", type=Path)
    parser.add_argument("--hashes", type=Path)
    args = parser.parse_args()

    project = project_data(args.root)
    version = project["version"]
    changelog = (args.root / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## [{version}]" not in changelog:
        raise SystemExit(f"CHANGELOG.md has no {version} release entry")
    if args.tag and args.tag.removeprefix("v") != version:
        raise SystemExit(f"tag {args.tag} does not match project version {version}")
    if args.wheel:
        metadata_version = wheel_metadata(args.wheel)["Version"]
        if metadata_version != version:
            raise SystemExit(
                f"wheel version {metadata_version} does not match project {version}"
            )
    if args.wheel and args.sdist:
        verify_contents(args.wheel, args.sdist)
        if args.hashes:
            write_hashes((args.wheel, args.sdist), args.hashes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
