"""Events model."""

from migrations import db


class Events(db.Model):
    """Модель проверки событий."""

    __tablename__ = "events"
    __table_args__ = {"extend_existing": True}

    name_event = db.Column(
        "name_event", db.String, nullable=False, unique=True
    )
    event_date = db.Column("event_date", db.Date, nullable=False)
    description = db.Column("description", db.String)
