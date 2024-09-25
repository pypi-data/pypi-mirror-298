import logging
from typing import Optional, cast

import click
import typer
from keyring import get_keyring
from keyring.backend import KeyringBackend, get_all_keyring
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

from . import Token, file_store, keyring_store

token_app = typer.Typer(
    name="token",
    help="Manage your tokens for authentication.",
)

selected_keyring: KeyringBackend | None = None


def parse_keyring(value: str | KeyringBackend = "default") -> KeyringBackend:
    if isinstance(value, KeyringBackend):
        logging.debug(f"No keyring selected. Using default keyring {value.name}")
        return value

    if value == "default":
        return get_keyring()

    all_backends = get_all_keyring()
    keyring = None
    for backend in all_backends:
        if value in backend.name.replace(" ", "."):
            keyring = backend

    if keyring is None:
        raise typer.BadParameter("Keyring not found.")

    return keyring


def shell_complete_keyring(ctx: click.Context, param: click.Parameter, incomplete: str):
    all_backends = get_all_keyring()
    return [
        backend.name.replace(" ", ".")
        for backend in all_backends
        if incomplete in backend.name.replace(" ", ".")
    ]


@token_app.callback()
def select_keyring(
    kr: Optional[KeyringBackend] = typer.Option(
        None,
        "--keyring",
        "-k",
        help="Select a keyring backend.",
        parser=parse_keyring,
        shell_complete=shell_complete_keyring,
    ),
):
    global selected_keyring
    if kr is not None:
        selected_keyring = kr
    else:
        selected_keyring = get_keyring()


@token_app.command("list")
def list():
    """List all available tokens."""
    if selected_keyring is None:
        raise typer.BadParameter("No keyring selected.")

    # From keyring
    tokens = keyring_store.get_all_tokens(selected_keyring)
    sources = ["keyring"] * len(tokens)

    # From file(s)
    tokens_from_file, sources_from_file = file_store.get_all_tokens()
    tokens += tokens_from_file
    sources += sources_from_file

    if len(tokens) == 0:
        logging.warning(
            "No tokens found! Add a token with 'snip-lab token add' or add an '.sniprc' file with tokens."
        )
        return

    console = Console()
    table = Table(show_edge=False)
    table.add_column("Name", style="bold cyan")
    table.add_column("Book ID", style="cyan")
    table.add_column("Deployment", style="cyan")
    table.add_column("Token", style="cyan")
    table.add_column("Source", style="cyan")

    for token in tokens:
        table.add_row(
            token.name,
            token.book_id,
            token.deployment_url,
            token.token,
            "keyring",
        )

    console.print(table)


def valid_name(name: str | None, kr: KeyringBackend) -> str:
    if name is None or name == "":
        raise typer.BadParameter("Name cannot be empty.")
    if " " in name:
        raise typer.BadParameter("Name cannot contain spaces.")
    if keyring_store.token_exists(name, kr):
        raise typer.BadParameter("Token with this name already exists!")
    return name


@token_app.command()
def add(
    token: Annotated[str, typer.Argument(help="The token to add to the keyring.")],
    name: Annotated[
        str | None,
        typer.Option(
            help="The name of the token, should be unique.",
        ),
    ] = None,
    book_id: Annotated[
        int | None,
        typer.Option(
            help="The book ID for the token.",
        ),
    ] = None,
    deployment_url: Annotated[
        str, typer.Option(help="The deployment URL i.e. the URL of the snip instance.")
    ] = "https://snip.roentgen.physik.uni-goettingen.de/",
):
    """Add a new token to the keyring storage.

    If --book-id or --name are not provided, they will be prompted for.
    """
    if selected_keyring is None:
        raise typer.BadParameter("No keyring selected.")

    # Check promptvalues
    if name is None:
        name = typer.prompt(
            "Name of the token, should be unique (e.g. MyTokenForBook1)",
            value_proc=lambda x: valid_name(x, cast(KeyringBackend, selected_keyring)),
        )
    if book_id is None:
        book_id = typer.prompt("Book ID for the token", type=int)

    # Save token
    t = Token.from_unsafe(str(name), str(book_id), token, deployment_url)

    # Save token
    keyring_store.save_token(t, selected_keyring)
    logging.debug(
        f"Saved token '{t}' to keyring '{selected_keyring.name.replace(' ', '.')}'!"
    )


def all_token_names(ctx: click.Context, param: click.Parameter, incomplete: str):
    kr = get_keyring()
    if kr is None:
        raise typer.BadParameter("No keyring selected.")

    return [token.name for token in keyring_store.get_all_tokens(kr)]


@token_app.command()
def remove(
    name: Annotated[
        str,
        typer.Argument(
            help="The name of the token to remove.", shell_complete=all_token_names
        ),
    ],
):
    """Remove a token from the keyring storage."""
    if selected_keyring is None:
        raise typer.BadParameter("No keyring selected.")

    if not keyring_store.token_exists(name, selected_keyring):
        raise typer.BadParameter("Token not found.")

    keyring_store.remove_token(name, selected_keyring)
    logging.debug(f"Removed token '{name}' from keyring '{selected_keyring.name}'!")
