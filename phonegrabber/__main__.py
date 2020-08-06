"""CLI entrypoint."""
import typer

from .base import cli_handler


typer.run(cli_handler)
