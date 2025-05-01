from src.auth.exceptions import UserAlreadyExists
from src.unit_of_work import AbstractUnitOfWorkManager


class UserService:
    """
    User Service class.

    This class is responsible for user-related operations such as creating a new user
    and retrieving user information by login.

    Attributes:
        uow (AbstractUnitOfWorkManager): Unit of work manager for database operations.

    Methods:
        create_user(data: dict) -> dict:
            Create a new user with the provided data.

        get_user_by_login(login: str) -> dict:
            Retrieve user information by login.
    """

    def __init__(self, uow: AbstractUnitOfWorkManager):
        self.uow = uow

    async def create_user(self, data: dict) -> dict:
        """
        Create new user.

        :param data: user data.
        :return: created user data.
        """
        async with self.uow:
            username = data.get("login")
            if await self.get_user_by_login(login=username):
                raise UserAlreadyExists(username=username)

            user = await self.uow.users.add(data)
            await self.uow.commit()
            return user

    async def get_user_by_login(self, login: str) -> dict:
        """
        Get user by login.

        :param login: login to get user.
        :return: user data.
        """
        async with self.uow:
            user = await self.uow.users.get(data={"login": login})
            return user

    async def get_user_by_id(self, user_id: int) -> dict:
        """
        Get user by id.

        :param user_id: user id to get user.
        :return: user data.
        """
        async with self.uow:
            user = await self.uow.users.get(data={"id": user_id})
            return user
