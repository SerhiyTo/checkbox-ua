from datetime import datetime, UTC
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_serializer


class PaymentMethod(str, Enum):
    """
    Enum for payment methods.
    """

    CASH = "cash"
    CASHLESS = "cashless"


class Product(BaseModel):
    """
    Product model for the application.

    Attributes:
        name (str): The name of the product. Must be between 2 and 32 characters.
        price (float): The price of the product. Must be greater than 0.
        quantity (int): The quantity of the product. Must be greater than 0.
    """

    name: str = Field(..., min_length=2, max_length=32, examples=["Product Name"])
    price: float = Field(..., gt=0, examples=[10.0], description="Product price")
    quantity: int = Field(..., gt=0, examples=[1], description="Product quantity")


class Payment(BaseModel):
    """
    Payment model for the application.

    Attributes:
        type (PaymentMethod): The type of payment. Must be either "cash" or "cashless".
        amount (float): The amount of payment. Must be greater than 0.
    """

    type: PaymentMethod = Field(
        ...,
        examples=["cash", "cashless"],
        description="Payment type. Must be either 'cash' or 'cashless'",
    )
    amount: float = Field(..., gt=0, examples=[100.0])


class CheckCreate(BaseModel):
    """
    Check creation model for the application.

    Attributes:
        products (list[Product]): The list of products in the check.
        payment (Payment): The payment information for the check.
    """

    products: list[Product] = Field(...)
    payment: Payment = Field(...)


class CheckResponse(BaseModel):
    """
    Check response model for the application.

    Attributes:
        id (int): The ID of the check.
        products (list[Product]): The list of products in the check.
        payment (Payment): The payment information for the check.
        total (float): The total amount of the check.
        rest (float): The remaining amount after payment.
        created_at (str): The creation date and time of the check.
    """

    id: int = Field(..., examples=[1])
    products: list[Product] = Field(...)
    payment: Payment = Field(...)
    total: float = Field(
        ...,
        gt=0,
        examples=[100.0],
        description="Total amount of the check",
    )
    rest: float = Field(
        ...,
        gt=0,
        examples=[0.0],
        description="Remaining amount after payment",
    )
    created_at: datetime = Field(
        ...,
        examples=["2023-10-01T12:00:00Z"],
        description="Creation date and time of the check",
    )

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        """
        Serialize the created_at field to a string format.

        Args:
            value (str): The datetime value to be serialized.

        Returns:
            str: The serialized datetime string.
        """
        return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


class CheckFilter(BaseModel):
    """
    Check filter model for the application.

    Attributes:
        created_at__lt (str): Filter by creation date less than.
        created_at__gte (str): Filter by creation date greater than or equal to.
        amount__lt (float): Filter by amount less than.
        amount__gte (float): Filter by amount greater than or equal to.
        type (PaymentMethod): Filter by payment type.
    """

    created_at__lt: Optional[str] = Field(
        None,
        examples=["2023-10-01T12:00:00Z"],
        description="Filter by creation date less than",
    )
    created_at__gte: Optional[str] = Field(
        None,
        examples=["2023-10-01T12:00:00Z"],
        description="Filter by creation date greater than or equal to",
    )
    amount__lt: Optional[float] = Field(
        None,
        examples=[100.0],
        description="Filter by amount less than",
    )
    amount__gte: Optional[float] = Field(
        None,
        examples=[100.0],
        description="Filter by amount greater than or equal to",
    )
    type: Optional[PaymentMethod] = Field(
        None,
        examples=["cash", "cashless"],
        description="Filter by payment type",
    )
