"""generate million points

Revision ID: 6973257e41fd
Revises: 486a371e0899
Create Date: 2022-06-29 14:17:26.149949

"""
import random
import string

# revision identifiers, used by Alembic.
from sqlalchemy import column, Float, String, table

from alembic import op

LATITUDE_RANGE = (-89.9, 89.9)
LONGITUDE_RANGE = (-179.9, 179.9)
LETTERS = string.ascii_lowercase

revision = '6973257e41fd'
down_revision = '486a371e0899'
branch_labels = None
depends_on = None


def upgrade() -> None:
    points_table = table(
        'points',
        column('name', String),
        column('latitude', Float),
        column('longitude', Float),
    )
    for _ in range(100):
        op.bulk_insert(points_table,
                       [dict(
                           latitude=random.uniform(*LATITUDE_RANGE),
                           longitude=random.uniform(*LONGITUDE_RANGE),
                           name=''.join(random.choice(LETTERS)
                                        for _ in range(random.randint(5, 9)))
                       )
                           for _ in range(10000)])


def downgrade() -> None:
    pass
