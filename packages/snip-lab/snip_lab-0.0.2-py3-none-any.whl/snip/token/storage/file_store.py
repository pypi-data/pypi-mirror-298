"""Functionalities to save and retrieve tokens from files.

We basically implement a simple configparser to read ini files
and parse contained tokens.

.. code-block:: ini
    [any_name]
    deployment = https://snip.roentgen.physik.uni-goettingen.de/
    book_id = 123
    token = token

Section names can be arbitrary, but should be unique and are parsed as the token name.

If not files are given we retrieve the tokens from the default locations.
- local: .sniprc
- user: ~/.sniprc
- global: /etc/snip_lab/.sniprc
- environment variable: SNIPRC
"""

import logging
import os
from collections import defaultdict
from configparser import ConfigParser
from typing import Dict, Sequence

from ..token import Token

File = str | os.PathLike
Files = File | Sequence[File]


def get_all_tokens(
    files: Files | None = None,
) -> tuple[
    list[Token],
    list[File],
]:
    """Get all available tokens from a file or list of files.

    Allows to read tokens from multiple files using the python
    builtin configparser.

    Parameters
    ----------
    files : str | os.PathLike | Sequence[str] | Sequence[os.PathLike] | None
        The file or list of files to read the tokens from. Defaults to all default locations.

    Returns
    -------
    Sequence[Token], Sequence[File]
        The list of tokens and the list of files they were read from.

    """
    files = __parse_files(files)

    # Even tho we could read multiple files at once we do it sequentially
    # to keep usable error messages and point out the file that is causing the issue
    tokens: list[Token] = []
    sources: list[File] = []
    for file in files:
        conf = ConfigParser()
        logging.debug(f"Reading tokens from file '{file}' if exists.")
        conf.read(file)

        for section in conf.sections():
            token = None
            if conf.has_option(section, "book_id") and conf.has_option(
                section, "token"
            ):
                book_id = conf.get(section, "book_id")
                token = conf.get(section, "token")
                deployment_url = conf.get(
                    section, "deployment", fallback=Token.deployment_url
                )
                token = Token(
                    section,
                    book_id,
                    token,
                    deployment_url,
                )
                sources.append(file)
            else:
                logging.warning(
                    f"Section '{section}' in file '{file}' does not contain book_id or token. Skipping."
                )
                continue

            tokens.append(token)

    # Warn on duplicate tokens names
    names = [t.name for t in tokens]
    duplicates = __duplicates_value_index(names)

    if len(duplicates) > 0:
        for name, idxs in duplicates.items():
            files = [sources[i] for i in idxs]
            logging.warning(
                f"Duplicate token names! This can lead to unexpected behavior! Found {len(idxs)} duplicates. Duplicate name '{name}' found in files {files}."
            )

    return tokens, sources


def get_token(
    name: str,
    files: Files | None = None,
) -> Token | None:
    """Get a token from a file or list of files given its name.

    Parameters
    ----------
    name : str
        The name of the token.
    files : str | os.PathLike | Sequence[str] | Sequence[os.PathLike]
        The file or list of files to read the token from. Defaults to all default locations.

    """
    raise NotImplementedError("Not implemented yet.")


def token_exists(
    name: str,
    files: Files | None = None,
) -> bool:
    """Check if a token with a given name exists in a file or list of files.

    Parameters
    ----------
    name : str
        The name of the token.
    files : str | os.PathLike | Sequence[str] | Sequence[os.PathLike]
        The file or list of files to read the token from. Defaults to all default locations.

    """
    raise NotImplementedError("Not implemented yet.")


def __parse_files(files: Files | None = None) -> Sequence[File]:
    """Parse the files and adds the default locations if None is given.

    - local: .sniprc
    - user: ~/.sniprc
    - global: /etc/snip_lab/.sniprc
    - environment variable: SNIPRC

    """
    if files is None:
        files = [
            ".sniprc",
            "~/.sniprc",
            "/etc/snip_lab/.sniprc",
        ]
        env = os.getenv("SNIPRC")
        if env is not None:
            files.append(env)

    if not isinstance(files, Sequence):
        files = [files]

    files = [os.path.expanduser(f) for f in files]

    # Absolute paths
    files = [os.path.abspath(f) for f in files]

    return files


def __duplicates_value_index(lst: list) -> Dict[str, list[int]]:
    """Find duplicates in a list including indexes."""
    D = defaultdict(list)
    for i, item in enumerate(lst):
        D[item].append(i)
    D = {k: v for k, v in D.items() if len(v) > 1}
    return D
