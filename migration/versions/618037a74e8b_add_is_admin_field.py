"""add_is_admin_field

Revision ID: 618037a74e8b
Revises: 81bfe00bee9a
Create Date: 2024-11-18 08:51:44.193446

"""
from alembic import op
import sqlalchemy as sa

from project.core.config import settings


# revision identifiers, used by Alembic.
revision = '618037a74e8b'
down_revision = '81bfe00bee9a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'users',
        sa.Column(
            'is_admin',
            sa.Boolean(),
            server_default=sa.text('false'),
            nullable=False
        ),
        schema=settings.POSTGRES_SCHEMA,
    )


def downgrade():
    op.drop_column('users', 'is_admin', schema=settings.POSTGRES_SCHEMA)
