from datetime import timedelta, datetime, timezone, UTC

import bcrypt
import jwt
from fastapi import HTTPException
from starlette import status

from src.config import settings


def hash_password(password: str) -> str:
    """
    Get password hash.

    :param password: password to hash.

    :return: hashed password.
    """
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt).decode()
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password.

    :param plain_password: password to verify.
    :param hashed_password: hashed password.

    :return: True if password is correct, False otherwise.
    """
    encoded_password = plain_password.encode()
    encoded_hashed_password = hashed_password.encode()
    return bcrypt.checkpw(encoded_password, encoded_hashed_password)


def create_jwt(
    token_type: str,
    user_data: dict,
    expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None,
) -> str:
    """
    Create JWT token.

    :param token_type: token type.
    :param user_data: user data.
    :param expire_minutes: time to expire in minutes.
    :param expire_timedelta: time to expire as timedelta.

    :return: JWT token.
    """
    jwt_payload = {"type": token_type}
    jwt_payload.update(user_data)
    return encode_jwt(
        user_data=user_data,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def encode_jwt(
    user_data: dict,
    private_key: str = settings.SECRET_KEY,
    algorithm: str = settings.ALGORITHM,
    expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None,
) -> str:
    """
    Create access token.

    :param user_data: user data.
    :param private_key: private key.
    :param algorithm: algorithm.
    :param expire_minutes: time to expire in minutes.
    :param expire_timedelta: time to expire as timedelta.

    :return: access token.
    """
    payload = user_data.copy()
    issued_at = datetime.now(timezone.utc)

    if expire_timedelta:
        expire = datetime.now(timezone.utc) + expire_timedelta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)

    payload.update({"exp": expire, "iat": issued_at})

    encoded_jwt = jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=algorithm,
    )
    return encoded_jwt


def decode_token(
    token: str,
    private_key: str = settings.SECRET_KEY,
    algorithm: str = settings.ALGORITHM,
) -> dict:
    """
    Decode access token.

    :param token: token to decode.
    :param private_key: private key.
    :param algorithm: algorithm.

    :return: decoded token.
    """
    decoded_jwt = jwt.decode(
        token,
        private_key,
        algorithms=[algorithm],
    )
    return decoded_jwt


def create_access_token(user: dict) -> str:
    """
    Create access token.

    :param user: user data.

    :return: jwt access token
    """
    jwt_payload = {
        "sub": str(user.get("id")),
        "login": user.get("login"),
    }
    return create_jwt(
        token_type=settings.ACCESS_TOKEN_TYPE,
        user_data=jwt_payload,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def create_refresh_token(user: dict) -> str:
    """
    Create refresh token.

    :param user: user data.

    :return: jwt refresh token
    """
    jwt_payload = {
        "sub": str(user.get("id")),
    }
    return create_jwt(
        token_type=settings.REFRESH_TOKEN_TYPE,
        user_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


async def validate_token(token: str) -> None:
    """
    Validate token.

    :param token: token to validate.

    :return:
    """
    try:
        payload = decode_token(token)
        if datetime.fromtimestamp(payload["exp"], UTC) < datetime.now(UTC):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )

    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
