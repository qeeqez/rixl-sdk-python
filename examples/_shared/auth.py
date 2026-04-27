"""AuthenticationProvider implementations that skip Kiota's HTTPS-only
check, so the examples can run against a local plaintext server.
"""
from kiota_abstractions.authentication.authentication_provider import (
    AuthenticationProvider,
)


class ApiKeyHeaderAuth(AuthenticationProvider):
    def __init__(self, key: str) -> None:
        self.key = key

    async def authenticate_request(self, request, additional_authentication_context=None):
        request.headers.add("X-API-Key", self.key)


class BearerAuth(AuthenticationProvider):
    def __init__(self, token: str) -> None:
        self.token = token

    async def authenticate_request(self, request, additional_authentication_context=None):
        request.headers.add("Authorization", f"Bearer {self.token}")
