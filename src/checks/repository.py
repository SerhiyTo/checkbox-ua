from sqlalchemy import insert, select, and_
from sqlalchemy.orm import joinedload

from src.checks.models import Check, CheckItem
from src.repository import SQLAlchemyRepository


class CheckRepository(SQLAlchemyRepository):
    """
    Check Repository class.
    """

    model = Check

    def _build_filters(self, filters: dict) -> list:
        """
        Build filters.

        :param filters: Filters.
        :return: Filters.
        """
        query_filters = []

        for key, value in filters.items():
            if value is None:
                continue

            if "__" in key:
                field, operator = key.split("__", 1)
                column = getattr(self.model, field, None)
                if column is not None:
                    if operator == "gte":
                        query_filters.append(column >= value)
                    elif operator == "lt":
                        query_filters.append(column < value)
            else:
                column = getattr(self.model, key, None)
                if column is not None:
                    query_filters.append(column == value)

        return query_filters

    async def get_by_data(self, data: dict) -> list[dict]:
        """
        Get check by data.

        :param data: Check data.
        :return: check.
        """
        query_filters = self._build_filters(data)

        statement = (
            select(self.model)
            .filter(and_(*query_filters))
            .options(joinedload(self.model.items))
        )
        result = await self.session.execute(statement)
        checks = result.unique().scalars().all()
        return [check.as_dict(include_products=True) for check in checks]


class CheckItemRepository(SQLAlchemyRepository):
    """
    Check item Repository class.
    """

    model = CheckItem

    async def bulk_add(self, data: list) -> list[dict]:
        """
        Bulk add check items to database.

        :param data: Check item data.
        :return: added check items.
        """
        statement = insert(self.model).values(data).returning(self.model)
        result = await self.session.execute(statement)
        all_result = result.scalars().all()
        return [item.as_dict() for item in all_result]
