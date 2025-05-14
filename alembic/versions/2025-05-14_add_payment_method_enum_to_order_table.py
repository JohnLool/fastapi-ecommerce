"""add payment method enum to order table

Revision ID: 1a60e8863adc
Revises: b744e5c904ad
Create Date: 2025-05-14 06:49:05.812523

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM as PGEnum


# revision identifiers, used by Alembic.
revision: str = '1a60e8863adc'
down_revision: Union[str, None] = 'b744e5c904ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    payment_method_enum = PGEnum(
        'card', 'sbp', 'crypto',
        name='payment_method_enum',
        create_type=True
    )
    payment_method_enum.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        'orders', 'payment_method',
        existing_type=sa.VARCHAR(length=50),
        type_=payment_method_enum,
        nullable=False,
        postgresql_using="payment_method::payment_method_enum"
    )


def downgrade() -> None:
    op.alter_column(
        'orders', 'payment_method',
        existing_type=PGEnum(
            'card', 'sbp', 'crypto',
            name='payment_method_enum'
        ),
        type_=sa.VARCHAR(length=50),
        nullable=True,
        postgresql_using="payment_method::text"
    )

    payment_method_enum = PGEnum(
        'card', 'sbp', 'crypto',
        name='payment_method_enum',
        create_type=False
    )
    payment_method_enum.drop(op.get_bind(), checkfirst=True)
