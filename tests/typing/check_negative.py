import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NEGATIVE = ROOT / "tests" / "typing" / "negative.py"


def require_failure(command: list[str], expected: str) -> None:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    output = completed.stdout + completed.stderr
    if completed.returncode == 0:
        raise SystemExit(f"Expected type checker failure: {' '.join(command)}")
    if expected not in output:
        raise SystemExit(f"Expected {expected!r} in type checker output:\n{output}")


require_failure(
    [sys.executable, "-m", "mypy", "--strict", str(NEGATIVE)],
    "Incompatible types in assignment",
)
require_failure(
    [
        sys.executable,
        "-m",
        "pyright",
        "--project",
        str(ROOT / "tests" / "typing" / "pyright-negativeconfig.json"),
    ],
    "is not assignable to declared type",
)
