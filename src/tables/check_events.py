"""Check events model."""

import sqlalchemy as sa

from migrations import db


class CheckEvents(db.Model):
    """Модель проверки событий."""

    __tablename__ = "check_events"
    __table_args__ = {"extend_existing": True}

    name_event = sa.Column(
        "name_event", sa.String, nullable=False, unique=True
    )
    date = sa.Column("date", sa.DateTime, nullable=False)
    description = sa.Column("description", sa.String)
