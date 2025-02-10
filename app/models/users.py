import typing

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database import Base

if typing.TYPE_CHECKING:
    from app.models.accounts import AccountsORM


class UsersORM(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    is_admin: Mapped[bool] = mapped_column(default=False)
    accounts: Mapped[list["AccountsORM"]] = relationship(back_populates="user")