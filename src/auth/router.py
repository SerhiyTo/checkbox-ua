from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.status import HTTP_201_CREATED

from src.auth.dependencies import validate_auth_user
from src.auth.exceptions import UserAlreadyExists
from src.auth.schemas import (
    RegisterResponse,
    RegisterRequest,
    LoginResponse,
    LoginRequest,
)
from src.auth.services import UserService
from src.auth.utils import hash_password, create_access_token, create_refresh_token
from src.dependencies import UOWDep

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register", response_model=RegisterResponse, status_code=HTTP_201_CREATED)
async def register(uow: UOWDep, user: RegisterRequest) -> RegisterResponse:
    """
    Register new user.

    :param uow: Unit of work dependency.
    :param user: user data.
    :return: created user data.
    """
    try:
        user.password = hash_password(user.password)
        created_user = await UserService(uow).create_user(user.model_dump())
        return RegisterResponse(**created_user)

    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/login", response_model=LoginResponse)
async def login(uow: UOWDep, user: LoginRequest) -> LoginResponse:
    """
    Login user.

    :param uow: Unit of work dependency.
    :param user: user data to login.
    :return: access and refresh tokens.
    """
    try:
        user_data = await validate_auth_user(
            uow=uow,
            login=user.login,
            password=user.password,
        )
        access_token = create_access_token(user_data)
        refresh_token = create_refresh_token(user_data)
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
