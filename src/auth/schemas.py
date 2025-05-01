from enum import Enum
from typing import Optional

from pydantic import Field, BaseModel


class RegisterRequest(BaseModel):
    """
    User registration schema.

    Attributes:
        first_name (str): The first name of the user. Must be between 2 and 32 characters.
        last_name (str): The last name of the user. Must be between 2 and 32 characters.
        login (str): The login of the user. Must be between 16 and 32 characters.
        password (str): The password of the user. Must be between 8 and 32 characters.
    """

    first_name: str = Field(..., min_length=2, max_length=64, examples=["John"])
    last_name: str = Field(..., min_length=2, max_length=64, examples=["Doe"])
    login: str = Field(..., min_length=16, max_length=64, examples=["username"])
    password: str = Field(..., min_length=8, max_length=64, examples=["password"])


class RegisterResponse(BaseModel):
    """
    User response schema.

    Attributes:
        id (int): The ID of the created user.
        first_name (str): The first name of the user. Must be between 2 and 32 characters.
        last_name (str): The last name of the user. Must be between 2 and 32 characters.
        login (str): The login of the user. Must be between 16 and 32 characters.
    """

    id: int = Field(..., examples=[1])
    first_name: str = Field(..., min_length=2, max_length=64, examples=["John"])
    last_name: str = Field(..., min_length=2, max_length=64, examples=["Doe"])
    login: str = Field(..., min_length=16, max_length=64, examples=["username"])


class LoginRequest(BaseModel):
    """
    User login schema.

    Attributes:
        login (str): The login of the user. Must be between 16 and 32 characters.
        password (str): The password of the user. Must be between 8 and 32 characters.
    """

    login: str = Field(..., min_length=16, max_length=32, examples=["username"])
    password: str = Field(..., min_length=8, max_length=32, examples=["password"])


class LoginResponse(BaseModel):
    """
    User login response schema.

    Attributes:
        access_token (str): The access token of the user.
        refresh_token (str): The refresh token of the user.
    """

    access_token: str = Field(..., description="Access JWT token")
    refresh_token: Optional[str] = Field(None, description="Refresh JWT token")
