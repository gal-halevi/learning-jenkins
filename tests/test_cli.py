import subprocess
import sys
from typer.testing import CliRunner
from calculator.cli import app

runner = CliRunner()


def test_cli_add():
    r = runner.invoke(app, ["add", "2", "3"])
    assert r.exit_code == 0
    assert r.stdout.strip() == "5.0"


def test_cli_sub():
    r = runner.invoke(app, ["sub", "5", "3"])
    assert r.exit_code == 0
    assert r.stdout.strip() == "2.0"


def test_cli_mul():
    r = runner.invoke(app, ["mul", "3", "4"])
    assert r.exit_code == 0
    assert r.stdout.strip() == "12.0"


def test_cli_div():
    r = runner.invoke(app, ["div", "10", "2"])
    assert r.exit_code == 0
    assert r.stdout.strip() == "5.0"


def test_cli_div_by_zero():
    r = runner.invoke(app, ["div", "10", "0"])
    assert r.exit_code != 0
    # Typer/Click puts the message in stdout/stderr depending on config;
    # this keeps the assertion robust.
    assert "divide" in (r.stdout + r.stderr).lower()


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