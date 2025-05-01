from src.checks.exceptions import CheckNotFound
from src.checks.schemas import CheckResponse
from src.unit_of_work import AbstractUnitOfWorkManager


class CheckService:
    """
    Check Service class.

    This class is responsible for managing check operations.
    It includes creating new checks and handling check items.

    Attributes:
        uow (AbstractUnitOfWorkManager): Unit of Work Manager for database transactions.

    Methods:
        create_check(user_id: int, data: dict) -> dict:
            Creates a new check with the provided user ID and data.

        get_check(check_id: int) -> dict:
            Retrieves a check by its ID.

    """

    def __init__(self, uow: AbstractUnitOfWorkManager):
        self.uow = uow

    async def create_check(self, user_id: int, data: dict) -> CheckResponse:
        """
        Create new check.

        :param user_id: User ID.
        :param data: Check data.

        :return: Check data.
        """
        products = data.pop("products")
        payment = data.get("payment")

        total, rest = self._calculate_totals(products, payment)
        check_data = self._build_check_data(user_id, payment, total, rest)

        async with self.uow:
            check = await self.uow.checks.add(data=check_data)
            products = await self._add_check_items(products, check["id"])
            await self.uow.commit()

            return CheckResponse(
                id=check["id"],
                products=products,
                payment=payment,
                total=total,
                rest=rest,
                created_at=check["created_at"],
            )

    async def get_check_by_public_uuid(self, public_uuid: str) -> CheckResponse:
        """
        Get check by public UUID.

        :param public_uuid: Public UUID of the check.

        :return: Check data.
        """
        filters = {"public_uuid": public_uuid}
        checks = await self._get_checks(filters)

        if not checks:
            raise CheckNotFound("Check not found.")

        return checks[0]

    async def get_check_by_id(self, check_id: int, user_id: int = None) -> CheckResponse:
        """
        Get check by ID.

        :param check_id: Check ID.
        :param user_id: User ID.

        :return: Check data.
        """
        filters = {"id": check_id, "user_id": user_id}
        checks = await self._get_checks(filters)

        if not checks:
            raise CheckNotFound("Check not found.")

        return checks[0]

    async def get_check_by_filters(self, filters: dict) -> list[CheckResponse]:
        """
        Get check by filters.

        :param filters: Filters for retrieving checks.

        :return: Check data.
        """
        return await self._get_checks(filters)

    async def _get_checks(self, filters: dict) -> list[CheckResponse]:
        """
        Retrieve a check based on the provided filters.

        :param filters: Filters for retrieving checks.
        :return: Check data.
        """
        async with self.uow:
            checks = await self.uow.checks.get_by_data(data=filters)

            if not checks:
                raise []

            return [
                CheckResponse(
                    id=check["id"],
                    products=check["products"],
                    payment={
                        "type": check["type"],
                        "amount": check["amount"],
                    },
                    total=check["total"],
                    rest=check["rest"],
                    created_at=check["created_at"],
                ) for check in checks
            ]

    async def _add_check_items(self, products: list, check_id: int) -> list[dict]:
        """
        Add check items to the database.

        :param products: List of products to be added.
        :param check_id: ID of the associated check.
        """
        product_data = [
            {
                "name": product["name"],
                "price": product["price"],
                "quantity": product["quantity"],
                "total": product["price"] * product["quantity"],
                "check_id": check_id,
            }
            for product in products
        ]

        created_products = await self.uow.check_items.bulk_add(data=product_data)
        return created_products

    @staticmethod
    def _calculate_totals(products: list, payment: dict) -> tuple:
        """
        Calculate the total amount and the remaining balance.

        :param products: List of products in the check.
        :param payment: Payment information.

        :return: Tuple containing total amount and remaining balance.
        """
        total = sum(product["price"] * product["quantity"] for product in products)
        amount = payment.get("amount")
        rest = amount - total
        return total, rest

    @staticmethod
    def _build_check_data(
            user_id: int, payment: dict, total: float, rest: float
    ) -> dict:
        """
        Build the check data dictionary.

        :param user_id: User ID.
        :param payment: Payment information.
        :param total: Total amount of the check.
        :param rest: Remaining balance.

        :return: Dictionary containing check data.
        """
        return {
            "type": payment.get("type"),
            "amount": payment.get("amount"),
            "total": total,
            "rest": rest,
            "user_id": user_id,
        }
