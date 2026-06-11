from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _build_wheel() -> Path:
    subprocess.run(
        [sys.executable, "-m", "build"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    wheels = sorted((ROOT / "dist").glob("typewall-*.whl"))
    if not wheels:
        raise AssertionError("Expected built wheel in dist/")
    return wheels[-1]


def _create_venv(path: Path) -> Path:
    subprocess.run(
        ["uv", "venv", str(path)], check=True, capture_output=True, text=True
    )
    return path / ("Scripts" if os.name == "nt" else "bin")


def test_built_wheel_installs_and_imports_in_a_clean_venv(tmp_path: Path) -> None:
    wheel = _build_wheel()
    scripts = _create_venv(tmp_path / "venv")
    python = scripts / "python"

    subprocess.run(
        ["uv", "pip", "install", "--python", str(python), str(wheel)],
        check=True,
        capture_output=True,
        text=True,
    )
    completed = subprocess.run(
        [
            str(python),
            "-c",
            (
                "from typewall import w; "
                "print(w.object({'name': w.str()}).parse({'name': 'Ada'}))"
            ),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert completed.stdout.strip() == "{'name': 'Ada'}"
    absent = subprocess.run(
        [str(python), "-c", "import fastapi"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert absent.returncode != 0


def test_console_script_validates_from_the_built_wheel(tmp_path: Path) -> None:
    wheel = _build_wheel()
    scripts = _create_venv(tmp_path / "cli-venv")
    python = scripts / "python"
    console = scripts / "typewall"

    schema_module = tmp_path / "fixture_schema.py"
    schema_module.write_text(
        (
            "from typewall import w\n"
            "schema = w.object({'name': w.str(), 'age': w.int()})\n"
        ),
        encoding="utf-8",
    )

    subprocess.run(
        ["uv", "pip", "install", "--python", str(python), str(wheel)],
        check=True,
        capture_output=True,
        text=True,
    )
    env = dict(os.environ)
    env["PYTHONPATH"] = str(tmp_path)
    completed = subprocess.run(
        [str(console), "validate", "fixture_schema:schema", "-"],
        input='{"name":"Ada","age":37}',
        text=True,
        capture_output=True,
        check=True,
        env=env,
    )

    assert "Validation passed" in completed.stdout
