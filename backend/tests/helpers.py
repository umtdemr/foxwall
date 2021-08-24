from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from tests.client import APIClient
    from user.models import User


def login_with_client(
    client: "APIClient",
    user: "User"
):
    client.login(
        username=user.username,
        password="password",
    )
    client.credentials(
        HTTP_AUTHORIZATION='Bearer ' + user.token
    )

    return client
