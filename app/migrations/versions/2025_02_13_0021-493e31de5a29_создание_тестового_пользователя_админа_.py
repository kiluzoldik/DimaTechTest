"""Создание тестового пользователя, админа и счета пользователя

Revision ID: 493e31de5a29
Revises: 782c72ec8800
Create Date: 2025-02-13 00:21:26.357071

"""

from typing import Sequence, Union

from alembic import op
from passlib.context import CryptContext
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "493e31de5a29"
down_revision: Union[str, None] = "782c72ec8800"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


USER_ID = 1
ADMIN_ID = 2
ACCOUNT_ID = 1

def upgrade():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    op.execute(
        sa.text("""
            INSERT INTO users (id, full_name, email, hashed_password, is_admin)
            VALUES 
                (:user_id, 'yabloko_zelenoe', 'example@mail.ru', :user_password, FALSE),
                (:admin_id, 'administrator', 'example_admin@mail.ru', :admin_password, TRUE)
        """).bindparams(
            user_id=USER_ID,
            admin_id=ADMIN_ID,
            user_password=pwd_context.hash("Test_user12345"),
            admin_password=pwd_context.hash("Admin_test_password12345"),
        )
    )

    op.execute(
        sa.text("""
            INSERT INTO accounts (id, balance, user_id)
            VALUES (:account_id, 0, :user_id)
        """).bindparams(
            account_id=ACCOUNT_ID,
            user_id=USER_ID
        )
    )


def downgrade():
    op.execute("DELETE FROM accounts WHERE id = :account_id", {"account_id": ACCOUNT_ID})
    op.execute("DELETE FROM users WHERE id IN (:user_id, :admin_id)", {"user_id": USER_ID, "admin_id": ADMIN_ID})
