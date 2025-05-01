from abc import ABC, abstractmethod

from src.auth.repository import UserRepository
from src.checks.repository import CheckRepository, CheckItemRepository
from src.database import async_session_maker


class AbstractUnitOfWorkManager(ABC):
    """
    Abstract class for Unit of Work Manager that will be used to manage the transactions in the database.
    """

    users: UserRepository
    checks: CheckRepository
    check_items: CheckItemRepository

    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> "AbstractUnitOfWorkManager":
        return self

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        return await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError


class SQLAlchemyUnitOfWorkManager(AbstractUnitOfWorkManager):
    """
    Unit of Work Manager for SQLAlchemy ORM.
    """

    def __init__(self) -> None:
        self.session_factory = async_session_maker

    async def __aenter__(self) -> AbstractUnitOfWorkManager:
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        self.checks = CheckRepository(self.session)
        self.check_items = CheckItemRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
