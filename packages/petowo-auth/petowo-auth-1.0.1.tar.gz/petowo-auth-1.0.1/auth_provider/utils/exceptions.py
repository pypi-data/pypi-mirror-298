from typing import Any


class AuthProviderError(Exception):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(detail)


class AuthStorageError(Exception):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(detail)
