"""role request table added

Revision ID: 405c2da7fb0d
Revises: ffe902a27888
Create Date: 2025-05-01 14:37:47.630495

"""
from typing import Sequence, Union
from sqlalchemy.dialects.postgresql import ENUM as PGEnum

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '405c2da7fb0d'
down_revision: Union[str, None] = 'ffe902a27888'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    role_enum = PGEnum(
        'owner', 'admin', 'seller', 'customer',
        name='role_enum',
        create_type=False
    )

    request_status = PGEnum(
        'pending', 'approved', 'rejected',
        name='requeststatus',
        create_type=True
    )

    op.create_table(
        'role_requests',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('desired_role', role_enum, nullable=False),
        sa.Column('status', request_status, nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('processed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
    )
    op.create_index(op.f('ix_role_requests_id'), 'role_requests', ['id'])
    op.create_index(op.f('ix_role_requests_user_id'), 'role_requests', ['user_id'])

def downgrade() -> None:
    op.drop_index(op.f('ix_role_requests_user_id'), table_name='role_requests')
    op.drop_index(op.f('ix_role_requests_id'), table_name='role_requests')
    op.drop_table('role_requests')

    op.execute("DROP TYPE requeststatus")