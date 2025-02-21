"""add_in_clans_update_and_create_at

Revision ID: 83b560c54101
Revises: eaf7b0c20552
Create Date: 2025-02-20 11:34:25.984203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83b560c54101'
down_revision = 'eaf7b0c20552'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_write():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clans', sa.Column('update_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('clans', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade_write():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('clans', 'created_at')
    op.drop_column('clans', 'update_at')
    # ### end Alembic commands ###


def upgrade_read():
    pass


def downgrade_read():
    pass

