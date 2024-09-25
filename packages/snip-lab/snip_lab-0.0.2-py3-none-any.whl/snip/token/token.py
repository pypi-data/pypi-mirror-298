from dataclasses import dataclass


@dataclass
class Token:
    """Token object, holds information about the token."""

    name: str
    book_id: str
    token: str
    deployment_url: str = "https://snip.roentgen.physik.uni-goettingen.de/"

    @classmethod
    def from_unsafe(
        cls, name: str, book_id: str, token: str, deployment_url: str | None
    ) -> "Token":
        """Create a token object from unsafe input."""
        if deployment_url is None:
            deployment_url = cls.deployment_url

        return cls(name, book_id, token, deployment_url)

    def __repr__(self):
        """Return a string representation of the token."""
        return f"Token(name={self.name}, book_id={self.book_id}, deployment_url={self.deployment_url})"
