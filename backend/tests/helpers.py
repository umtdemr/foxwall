from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from tests.client import APIClient


def login_with_client(
    client: "APIClient",
    token: str
):
    client.credentials(
        HTTP_AUTHORIZATION='Bearer ' + token
    )

    return client
