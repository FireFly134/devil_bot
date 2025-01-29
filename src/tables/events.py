"""Events model."""

import sqlalchemy as sa

from migrations import db


class Events(db.Model):
    """Модель проверки событий."""

    __tablename__ = "events"
    __table_args__ = {"extend_existing": True}

    name_event = sa.Column(
        "name_event", sa.String, nullable=False, unique=True
    )
    event_date = sa.Column("event_date", sa.Date, nullable=False)
    description = sa.Column("description", sa.String)
