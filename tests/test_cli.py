import subprocess
import sys


def run_cli(*args: str):
    return subprocess.run(
        [sys.executable, "-m", "calculator", *args],
        text=True,
        capture_output=True,
    )


def test_cli_add():
    p = run_cli("add", "2", "3")
    assert p.returncode == 0
    assert p.stdout.strip() == "5.0"