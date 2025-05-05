from starlette.status import HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND


class UserAlreadyExists(Exception):
    """Exception raised when a user already exists in the database."""

    def __init__(self, username: str):
        super().__init__(f"User with username '{username}' already exists.")
        self.username = username
        self.status_code = HTTP_409_CONFLICT


class UserNotFound(Exception):
    """Exception raised when a user is not found in the database."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.status_code = HTTP_404_NOT_FOUND


class InvalidCredentials(Exception):
    """Exception raised when credentials are invalid."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.status_code = HTTP_401_UNAUTHORIZED
