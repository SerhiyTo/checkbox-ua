from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class User(Base):
    """
    User model.

    Attributes:
        id (int): Unique identifier for the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        login (str): Login of the user.
        password (str): Password of the user.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        index=True,
        autoincrement=True,
    )
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    login: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)

    checks: Mapped[list["Check"]] = relationship("Check", back_populates="user")
