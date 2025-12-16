import typer

from .calculator import add_numbers, subtract, multiply, divide

app = typer.Typer(no_args_is_help=True)


@app.command("add")
def add_cmd(a: float, b: float) -> None:
    typer.echo(add_numbers(a, b))


@app.command()
def sub(a: float, b: float) -> None:
    typer.echo(subtract(a, b))


@app.command()
def mul(a: float, b: float) -> None:
    typer.echo(multiply(a, b))


@app.command()
def div(a: float, b: float) -> None:
    try:
        typer.echo(divide(a, b))
    except ValueError as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(code=2)


def main() -> None:
    app()