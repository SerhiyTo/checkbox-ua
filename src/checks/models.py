import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Integer, TIMESTAMP, func, Enum, Numeric, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.checks.schemas import PaymentMethod
from src.models import Base


class Check(Base):
    """
    Check model.

    Attributes:
        id (int): Unique identifier for the check.
        type (PaymentMethod): Type of payment method.
        amount (Decimal): Amount of the check.
        total (Decimal): Total amount of the check.
        rest (Decimal): Remaining amount of the check.
        created_at (datetime): Timestamp when the check was created.
    """

    __tablename__ = "checks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        index=True,
        autoincrement=True,
    )
    type: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod, name="payment_method_enum"),
        nullable=False,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    rest: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    public_uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        index=True,
        server_default=func.gen_random_uuid(),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="checks")
    items: Mapped[list["CheckItem"]] = relationship("CheckItem", back_populates="check")

    def as_dict(self, **kwargs) -> dict:
        data = super().as_dict()
        include_products = kwargs.get("include_products", False)
        if include_products and hasattr(self, "items") and self.items:
            data["products"] = [item.as_dict() for item in self.items]
        return data


class CheckItem(Base):
    """
    Check item model.
    """

    __tablename__ = "check_items"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        index=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    check_id: Mapped[int] = mapped_column(ForeignKey("checks.id"), nullable=False)

    check: Mapped["Check"] = relationship("Check", back_populates="items")
