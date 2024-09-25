import pytest
from snip.token.storage import file_store, keyring_store


class TestFileStore:
    def test_get_all_tokens(self, config_file):
        config_file, compare_tokens = config_file

        tokens, sources = file_store.get_all_tokens([config_file])

        assert len(tokens) == len(compare_tokens)
        assert len(sources) == len(compare_tokens)
        for i, token in enumerate(tokens):
            assert token.name == compare_tokens[i].name
            assert token.token == compare_tokens[i].token
            assert token.book_id == compare_tokens[i].book_id
            assert token.deployment_url == compare_tokens[i].deployment_url

    def test_get_all_tokens_invalid(self, invalid_config_file, caplog):
        config_file, compare_tokens = invalid_config_file

        tokens, sources = file_store.get_all_tokens([config_file])

        assert len(tokens) == len(compare_tokens)
        assert len(sources) == len(compare_tokens)

        # Check that we had a logging.warning
        assert len(caplog.records) == 1
        assert (
            "does not contain book_id or token. Skipping." in caplog.records[0].message
        )

    def test_duplicates(self, config_file, another_config_file, caplog):
        config_file, compare_tokens = config_file
        another_config_file, compare_tokens_another = another_config_file

        tokens, sources = file_store.get_all_tokens([config_file, another_config_file])

        assert len(tokens) == len(compare_tokens) + len(compare_tokens_another)
        assert len(sources) == len(compare_tokens) + len(compare_tokens_another)

        # Check that we had a logging.warning
        assert len(caplog.records) == 1
        assert "Duplicate token names!" in caplog.records[0].message


class TestKeyringStore:
    def test_get_all_tokens(self, dummy_keyring, tokens):
        for token in tokens:
            keyring_store.save_token(token, dummy_keyring)

        tokens = keyring_store.get_all_tokens(dummy_keyring)
        assert len(tokens) == len(tokens)

    def test_invalid_kr_state(self, dummy_keyring, tokens, caplog):
        for token in tokens:
            keyring_store.save_token(token, dummy_keyring)

        dummy_keyring.delete_password(
            keyring_store.SNIP_KR_IDENTIFIER,
            tokens[0].name.encode("utf-8").hex() + ":book_id",
        )

        tokens_b = keyring_store.get_all_tokens(dummy_keyring)

        assert len(caplog.records) == 1
        assert "is invalid" in caplog.records[0].message
        assert len(tokens_b) == len(tokens) - 1

    def test_get_token(self, dummy_keyring, tokens):
        for token in tokens:
            keyring_store.save_token(token, dummy_keyring)

        for token in tokens:
            t = keyring_store.get_token(token.name, dummy_keyring)
            assert t is not None
            assert t.name == token.name
            assert t.token == token.token
            assert t.book_id == token.book_id
            assert t.deployment_url == token.deployment_url

    def test_remove_token(self, dummy_keyring, tokens):
        for token in tokens:
            keyring_store.save_token(token, dummy_keyring)

        keyring_store.remove_token(tokens[0].name, dummy_keyring)

        tokens_b = keyring_store.get_all_tokens(dummy_keyring)

        assert len(tokens_b) == len(tokens) - 1

        # Remove non existing token
        with pytest.raises(ValueError):
            keyring_store.remove_token("nonexistent", dummy_keyring)

    def test_token_exists(self, dummy_keyring, tokens):
        for token in tokens:
            keyring_store.save_token(token, dummy_keyring)

        for token in tokens:
            assert keyring_store.token_exists(token.name, dummy_keyring)

        assert not keyring_store.token_exists("nonexistent", dummy_keyring)

    def test_save_with_overwrite(self, dummy_keyring, tokens):
        for token in tokens:
            keyring_store.save_token(token, dummy_keyring)

        for token in tokens:
            keyring_store.save_token(token, dummy_keyring, overwrite=True)

        # Expect error on duplicate
        for token in tokens:
            with pytest.raises(ValueError):
                keyring_store.save_token(token, dummy_keyring)
