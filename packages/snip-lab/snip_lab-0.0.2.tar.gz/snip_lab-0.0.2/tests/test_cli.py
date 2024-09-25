from typer.testing import CliRunner

from snip.__main__ import app
from snip.token import keyring_store

runner = CliRunner()


def test_rm_token(monkeypatch, dummy_keyring, tokens):
    monkeypatch.setattr("snip.token.__main__.get_keyring", lambda: dummy_keyring)
    for token in tokens:
        keyring_store.save_token(token, dummy_keyring)

    assert len(keyring_store.get_all_tokens(dummy_keyring)) == len(tokens)

    result = runner.invoke(app, ["token", "remove", tokens[0].name])

    print(result.stdout)
    assert result.exit_code == 0

    b_tokens = keyring_store.get_all_tokens(dummy_keyring)
    assert len(b_tokens) == len(tokens) - 1


def test_rm_token_nonexistent(monkeypatch, dummy_keyring, tokens):
    monkeypatch.setattr("snip.token.__main__.get_keyring", lambda: dummy_keyring)
    for token in tokens:
        keyring_store.save_token(token, dummy_keyring)

    assert len(keyring_store.get_all_tokens(dummy_keyring)) == len(tokens)

    result = runner.invoke(app, ["token", "remove", "nonexistent"])

    assert result.exit_code == 2
    assert "not found" in result.stdout


def test_list_tokens(monkeypatch, dummy_keyring, caplog):
    monkeypatch.setattr("snip.token.__main__.get_keyring", lambda: dummy_keyring)
    result = runner.invoke(app, ["token", "list"])
    assert result.exit_code == 0
    assert "No tokens found!" in caplog.records[0].message


def test_list_no_keyring(monkeypatch, dummy_keyring, tokens):
    monkeypatch.setattr("snip.token.__main__.get_keyring", lambda: None)
    result = runner.invoke(app, ["token", "list"])

    assert "No keyring selected." in result.stdout


def test_add_token(monkeypatch, dummy_keyring):
    monkeypatch.setattr("snip.token.__main__.get_keyring", lambda: dummy_keyring)

    result = runner.invoke(
        app,
        [
            "token",
            "add",
            "TEST",
            "--name",
            "foo",
            "--book-id",
            "1",
        ],
    )
    print(result.stdout)
    assert result.exit_code == 0

    token = keyring_store.get_token("foo", dummy_keyring)
    assert token is not None
