"""Check events model."""

import sqlalchemy as sa

from src.migrations import db


class CheckEvents(db.Model):
    """Модель проверки событий."""

    __tablename__ = "check_events"

    name_event = sa.Column(
        "name_event", sa.String, nullable=False, unique=True
    )
    date = sa.Column("date", sa.DateTime, nullable=False)
    description = sa.Column("description", sa.String)
