"""Cli entry point.

Used for both the python -m snip-lab and as package script i.e. snip-lab.

"""

import logging

import typer
from rich.logging import RichHandler

from .token.__main__ import token_app

logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    handlers=[RichHandler(show_time=False, show_path=False)],
)

app = typer.Typer(
    rich_markup_mode="rich",
    help="Command line tool for [bold italic]snip[/bold italic] - our digital lab book.",
)

# Add subcommands
app.add_typer(token_app)


# Add global verbose option
@app.callback()
def select_verbose(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output."),
):
    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.WARNING

    logging.getLogger().setLevel(log_level)
    logging.debug("Verbose output.")


if __name__ == "__main__":
    app()
