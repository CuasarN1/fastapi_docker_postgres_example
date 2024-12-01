"""initial

Revision ID: 9d09e1cb9b76
Revises: 
Create Date: 2024-10-14 09:33:50.162970

"""
from alembic import op
import sqlalchemy as sa

from project.core.config import settings


# revision identifiers, used by Alembic.
revision = '9d09e1cb9b76'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('last_name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('email', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False, unique=True),
    sa.Column('password', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('phone_number', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    schema=settings.POSTGRES_SCHEMA
    )


def downgrade():
    op.drop_table('users', schema=settings.POSTGRES_SCHEMA)
