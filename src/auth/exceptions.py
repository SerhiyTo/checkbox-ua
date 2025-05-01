from starlette.status import HTTP_409_CONFLICT


class UserAlreadyExists(Exception):
    """Exception raised when a user already exists in the database."""

    def __init__(self, username: str):
        super().__init__(f"User with username '{username}' already exists.")
        self.username = username
        self.status_code = HTTP_409_CONFLICT
