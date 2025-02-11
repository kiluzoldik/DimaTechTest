import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database import Base

if typing.TYPE_CHECKING:
    from app.models.users import UsersORM
    from app.models.payments import PaymentsORM


class AccountsORM(Base):
    __tablename__ = "accounts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[float]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    transactions: Mapped[list["PaymentsORM"]] = relationship(back_populates="account")
    user: Mapped["UsersORM"] = relationship(back_populates="accounts")