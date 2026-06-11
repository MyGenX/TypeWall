from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _uv_env() -> dict[str, str]:
    return {**os.environ, "UV_CACHE_DIR": str(ROOT / ".uv-cache")}


def _built_wheel() -> Path:
    wheels = sorted((ROOT / "dist").glob("typewall-*.whl"))
    if not wheels:
        raise AssertionError("Expected a prior package build in dist/")
    return wheels[-1]


def _built_sdist() -> Path:
    archives = sorted((ROOT / "dist").glob("typewall-*.tar.gz"))
    if not archives:
        raise AssertionError("Expected a prior package build in dist/")
    return archives[-1]


def _create_venv(path: Path) -> Path:
    subprocess.run(
        ["uv", "venv", str(path)],
        check=True,
        capture_output=True,
        text=True,
        env=_uv_env(),
    )
    return path / ("Scripts" if os.name == "nt" else "bin")


def test_built_wheel_installs_and_imports_in_a_clean_venv(tmp_path: Path) -> None:
    wheel = _built_wheel()
    scripts = _create_venv(tmp_path / "venv")
    python = scripts / "python"

    subprocess.run(
        [
            "uv",
            "pip",
            "install",
            "--python",
            str(python),
            str(wheel),
        ],
        check=True,
        capture_output=True,
        text=True,
        env=_uv_env(),
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
    wheel = _built_wheel()
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
        [
            "uv",
            "pip",
            "install",
            "--python",
            str(python),
            str(wheel),
        ],
        check=True,
        capture_output=True,
        text=True,
        env=_uv_env(),
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


def test_source_distribution_installs_independently(tmp_path: Path) -> None:
    sdist = _built_sdist()
    source_dir = tmp_path / "source"
    wheel_dir = tmp_path / "rebuilt"
    shutil.unpack_archive(sdist, source_dir)
    unpacked_root = next(source_dir.iterdir())
    subprocess.run(
        [
            sys.executable,
            "-m",
            "build",
            "--wheel",
            "--no-isolation",
            "--outdir",
            str(wheel_dir),
            str(unpacked_root),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rebuilt_wheel = next(wheel_dir.glob("typewall-*.whl"))
    scripts = _create_venv(tmp_path / "sdist-venv")
    python = scripts / "python"

    subprocess.run(
        [
            "uv",
            "pip",
            "install",
            "--python",
            str(python),
            str(rebuilt_wheel),
        ],
        check=True,
        capture_output=True,
        text=True,
        env=_uv_env(),
    )
    completed = subprocess.run(
        [str(python), "-c", "from typewall import w; print(w.int().parse(7))"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert completed.stdout.strip() == "7"


def test_examples_run_against_installed_wheel(tmp_path: Path) -> None:
    wheel = _built_wheel()
    scripts = _create_venv(tmp_path / "examples-venv")
    python = scripts / "python"
    console = scripts / "typewall"
    shutil.copytree(ROOT / "examples", tmp_path / "examples")

    subprocess.run(
        [
            "uv",
            "pip",
            "install",
            "--python",
            str(python),
            f"{wheel}[fastapi]",
        ],
        check=True,
        capture_output=True,
        text=True,
        env=_uv_env(),
    )
    subprocess.run(
        [str(python), "examples/config_validation.py"], cwd=tmp_path, check=True
    )
    example_env = {**os.environ, "PYTHONPATH": str(tmp_path)}
    subprocess.run(
        [
            str(console),
            "validate",
            "examples.cli.schema:User",
            "examples/cli/user.json",
        ],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
        env=example_env,
    )
    completed = subprocess.run(
        [
            str(python),
            "-c",
            (
                "from examples.fastapi_app import app; "
                "assert '/users' in app.openapi()['paths']"
            ),
        ],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    assert completed.stderr == ""
