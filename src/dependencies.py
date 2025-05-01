from typing import Annotated

from fastapi import Depends

from src.unit_of_work import SQLAlchemyUnitOfWorkManager, AbstractUnitOfWorkManager


async def get_uow() -> SQLAlchemyUnitOfWorkManager:
    """
    Dependency function to get an instance of SQLAlchemyUnitOfWorkManager.

    :return: An instance of SQLAlchemyUnitOfWorkManager.
    """
    async with SQLAlchemyUnitOfWorkManager() as uow:
        yield uow


UOWDep = Annotated[AbstractUnitOfWorkManager, Depends(get_uow)]
