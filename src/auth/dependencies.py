from typing import Annotated

import jwt
from fastapi import HTTPException, Depends
from starlette import status

from src.auth.services import UserService
from src.auth.utils import verify_password, decode_token, validate_token
from src.config import oauth2_scheme
from src.dependencies import UOWDep


async def validate_auth_user(
    uow: UOWDep,
    login: str,
    password: str,
) -> dict:
    """
    Validate user data.

    :param uow: Unit of work dependency.
    :param login: user login.
    :param password: user password.

    :return: user data.
    """
    exising_user = await UserService(uow).get_user_by_login(login=login)
    if not exising_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    if not verify_password(password, exising_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password.",
        )

    return exising_user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Get current user.
    :param token: token to get user.

    :return: user data.
    """

    try:
        await validate_token(token)
        payload = decode_token(token)
        return payload

    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )


CurrentUser = Annotated[dict, Depends(get_current_user)]
