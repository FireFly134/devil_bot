"""add_event_table

Revision ID: 0b00650b103a
Revises: bda03662ca07
Create Date: 2025-01-29 09:21:09.317218

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0b00650b103a'
down_revision = 'bda03662ca07'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_write():
    connection = op.get_bind()
    connection.execute(
        """
           INSERT INTO events (name_event, event_date, description) VALUES
           ('2x heros', '2024-07-19', 'х2 в героическом режиме кампании на осколки героев'),
           ('3x','2024-07-23','х3 в легендарном режиме кампании'),
           ('2x resources','2025-02-07','х2 в героическом режиме кампании на осколки героев');
        """
    )


def downgrade_write():
    connection = op.get_bind()
    connection.execute(
        sa.text(
            "DELETE FROM events WHERE name_event in ('2x heros', '3x', '2x resources');"
        ),
    )


def upgrade_read():
    pass


def downgrade_read():
    pass

