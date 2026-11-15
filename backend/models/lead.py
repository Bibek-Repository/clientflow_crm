
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.session import Base


class Lead(Base):
    # Database table name
    __tablename__ = "leads"

    # Primary key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    # Lead information
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    company: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="New",
        nullable=False
    )
