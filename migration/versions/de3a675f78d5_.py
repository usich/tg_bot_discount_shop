"""empty message

Revision ID: de3a675f78d5
Revises: 28b6e27aa7d4
Create Date: 2024-02-14 20:04:12.516277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de3a675f78d5'
down_revision: Union[str, None] = '28b6e27aa7d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_1c',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ref_1c', sa.String(length=36), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('discount_card_number', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('users_1C')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_1C',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"users_1C_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('ref_1c', sa.VARCHAR(length=36), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('discount_card_number', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='users_1C_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='users_1C_pkey')
    )
    op.drop_table('users_1c')
    # ### end Alembic commands ###
