"""Update transactions table

Revision ID: cd8ff8a347ad
Revises: 03c563cdbaa5
Create Date: 2024-02-18 16:19:47.419416

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd8ff8a347ad'
down_revision: Union[str, None] = '03c563cdbaa5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('product_id', sa.Integer(), nullable=True))
    op.drop_constraint('transactions_company_id_fkey', 'transactions', type_='foreignkey')
    op.create_foreign_key(None, 'transactions', 'products', ['product_id'], ['product_id'])
    op.drop_column('transactions', 'company_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('company_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.create_foreign_key('transactions_company_id_fkey', 'transactions', 'companies', ['company_id'], ['company_id'])
    op.drop_column('transactions', 'product_id')
    # ### end Alembic commands ###
