"""initial migration

Revision ID: 2d3389abdc18
Revises: 
Create Date: 2020-04-06 13:02:02.218949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d3389abdc18'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=10), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('fns_login', sa.String(length=12), nullable=True),
    sa.Column('fns_password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_role'), 'user', ['role'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('purchase',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('fn_number', sa.String(), nullable=True),
    sa.Column('fd_number', sa.String(), nullable=True),
    sa.Column('fpd_number', sa.String(), nullable=True),
    sa.Column('receipt_type', sa.String(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('sum', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('fn_number')
    )
    op.create_table('receipt',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('receipt_id', sa.Integer(), nullable=True),
    sa.Column('product', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.DECIMAL(), nullable=True),
    sa.Column('sum', sa.Integer(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('subcategory', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['receipt_id'], ['purchase.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('receipt')
    op.drop_table('purchase')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_role'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
