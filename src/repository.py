from abc import ABC, abstractmethod
from typing import TypeVar, Optional, Type, Generic

from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=BaseModel)


class AbstractRepository(ABC):
    """
    Abstract class for Repository Interface.
    """

    @abstractmethod
    async def add(self, data: dict) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get(self, **data: dict) -> T:
        raise NotImplementedError

    @abstractmethod
    async def list(self, **data: dict) -> list[T]:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository, Generic[T]):
    """
    Repository class for SQLAlchemy ORM.
    """

    model: Optional[Type[T]] = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, data: dict, **kwargs) -> T:
        """
        Add entity to database.

        :param data: dictionary with entity data.

        :return: dictionary with created entity data.
        """
        statement = insert(self.model).values(**data).returning(self.model)
        added_data = await self.session.execute(statement)
        await self.session.commit()
        result = added_data.scalar_one_or_none()
        return result.as_dict(**kwargs) if result else None

    async def get(self, data: dict) -> dict:
        """
        Get entity from database.

        :param data: dictionary with filter parameters.

        :return: None
        """
        statement = select(self.model).filter_by(**data)
        received_data = await self.session.execute(statement)
        result = received_data.scalar_one_or_none()
        return result.as_dict() if result else None

    async def list(self, data: dict) -> list[dict]:
        """
        List all records from the database.

        :return: List of dictionaries containing record data.
        """
        statement = select(self.model).filter_by(**data)
        received_data = await self.session.execute(statement)
        result = received_data.scalars().all()
        return [record.as_dict() for record in result]
