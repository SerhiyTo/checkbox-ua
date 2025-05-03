from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from starlette.templating import Jinja2Templates

from src.auth.dependencies import CurrentUser
from src.checks.exceptions import CheckNotFound
from src.checks.schemas import CheckCreate, CheckResponse, CheckFilter
from src.checks.services import CheckService
from src.dependencies import UOWDep

router = APIRouter(
    prefix="/checks",
    tags=["Checks"],
)

templates = Jinja2Templates(directory="templates")


@router.post("", response_model=CheckResponse, status_code=HTTP_201_CREATED)
async def create_check(
    uow: UOWDep,
    user: CurrentUser,
    check: CheckCreate,
) -> CheckResponse:
    """
    Create a new check.

    :param uow: Unit of Work dependency.
    :param user: current user information.
    :param check: check data to create.
    :return: created check data.
    """
    try:
        user_id = int(user["sub"])
        created_check = await CheckService(uow).create_check(
            user_id,
            check.model_dump(),
        )
        return created_check

    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Error occurred while creating check: {str(e)}",
        )


@router.get("", response_model=list[CheckResponse])
async def get_check(
    uow: UOWDep,
    user: CurrentUser,
    filter_data: CheckFilter = Depends(),
) -> list[CheckResponse]:
    """
    Get check by filters.

    :param uow: Unit of Work dependency.
    :param user: current user information.
    :param filter_data: filter data for check.
    :return: check data.
    """
    try:
        filters = filter_data.model_dump()
        filters["user_id"] = int(user["sub"])

        check = await CheckService(uow).get_check_by_filters(filters)
        return check

    except CheckNotFound as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Error occurred while getting check: {str(e)}",
        )


@router.get("/{check_id}", response_model=CheckResponse)
async def get_check_by_id(
    uow: UOWDep,
    user: CurrentUser,
    check_id: int,
) -> CheckResponse:
    """
    Get check by ID.

    :param uow: Unit of Work dependency.
    :param user: current user information.
    :param check_id: check ID to get check.
    :return: check data.
    """
    try:
        user_id = int(user["sub"])
        check = await CheckService(uow).get_check_by_id(
            user_id=user_id,
            check_id=check_id,
        )
        return check

    except CheckNotFound as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Error occurred while getting check: {str(e)}",
        )


@router.get("/public/{public_uuid}", response_class=HTMLResponse)
async def get_rendered_check(request: Request, uow: UOWDep, public_uuid: str):
    """
    Get rendered check by ID.

    :param request: HTTP request object.
    :param uow: Unit of Work dependency.
    :param public_uuid: Public UUID of the check.
    :return: HTML response with the rendered check.
    """
    try:
        check = await CheckService(uow).get_check_by_public_uuid(
            public_uuid=public_uuid
        )
        formatted_created_at = check.created_at.strftime("%d.%m.%Y %H:%M")
        return templates.TemplateResponse(
            request=request,
            name="check.html",
            context={
                "check": check,
                "created_at": formatted_created_at,
                "payment_type": check.payment.type.value.capitalize(),
            },
        )

    except CheckNotFound as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Error occurred while rendering check: {str(e)}",
        )
