"""add_table_news

Revision ID: 60bd0a8b023c
Revises: 5a46f5026091
Create Date: 2024-12-08 16:10:10.502758

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '60bd0a8b023c'
down_revision = '5a46f5026091'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_write():
    op.create_table('news',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('text', sa.String(), nullable=True),
                    sa.Column('photos', sa.ARRAY(sa.String()),
                              nullable=True),
                    sa.Column('date_pub', sa.TIMESTAMP(),
                              server_default=sa.text('now()'), nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP(),
                              server_default=sa.text('now()'), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_news_id'), 'news', ['id'],
                    unique=True)
    # ### end Alembic commands ###


def downgrade_write():
    op.drop_index(op.f('ix_news_id'), table_name='news')
    op.drop_table('news')


def upgrade_read():
    pass


def downgrade_read():
    pass

