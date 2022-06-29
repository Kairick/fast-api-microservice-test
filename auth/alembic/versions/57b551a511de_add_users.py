"""add users

Revision ID: 57b551a511de
Revises: cb0dfd1b5880
Create Date: 2022-06-29 11:07:56.980285

"""
from uuid import uuid4

from passlib.hash import bcrypt
# revision identifiers, used by Alembic.
from sqlalchemy import table, column, String

from alembic import op

revision = '57b551a511de'
down_revision = 'cb0dfd1b5880'
branch_labels = None
depends_on = None


def upgrade() -> None:
    users_table = table(
        'users',
        column('first_name', String),
        column('last_name', String),
        column('email', String),
        column('uuid', String),
        column('hashed_password', String),
    )

    op.bulk_insert(users_table,
                   [
                       {
                           'first_name': 'John',
                           'last_name': 'Dow',
                           'email': 'john@mail.ru',
                           'uuid': str(uuid4()),
                           'hashed_password': bcrypt.hash('John_123')
                       },
                       {
                           'first_name': 'Ivan',
                           'last_name': 'Ivanov',
                           'email': 'ivan@mail.ru',
                           'uuid': str(uuid4()),
                           'hashed_password': bcrypt.hash('Ivan_123')
                       },
                       {
                           'first_name': 'Semen',
                           'last_name': 'Semenov',
                           'email': 'semen@mail.ru',
                           'uuid': str(uuid4()),
                           'hashed_password': bcrypt.hash('Semen_123')
                       },
                       {
                           'first_name': 'Ilona',
                           'last_name': 'Maskova',
                           'email': 'ilona@mail.ru',
                           'uuid': str(uuid4()),
                           'hashed_password': bcrypt.hash('Ilona_123')
                       },
                   ]
                   )


def downgrade() -> None:
    pass
