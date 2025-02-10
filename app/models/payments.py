import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database import Base

if typing.TYPE_CHECKING:
    from app.models.accounts import AccountsORM


class PaymentsORM(Base):
    __tablename__ = "payments"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_id: Mapped[int] = mapped_column(unique=True)
    amount: Mapped[float]
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    account: Mapped["AccountsORM"] = relationship(back_populates="transactions")