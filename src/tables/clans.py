"""Clans model."""

from migrations import db
from tables.handler_db import CREATED_AT_COLUMN, UPDATED_AT_COLUMN


class Clans(db.Model):
    """Модель клана."""

    __tablename__ = "clans"
    __table_args__ = {"extend_existing": True}

    id = db.Column(  # noqa: A003
        "id", db.Integer, primary_key=True, index=True, autoincrement=True
    )
    name_clan = db.Column("name_clan", db.String, nullable=False)
    time_kz = db.Column(
        "time_kz",
        db.Integer,
        default=18,  # noqa: WPS432
        server_default=db.text("18"),
        nullable=False,
    )
    chat_id = db.Column("chat_id", db.String, nullable=False)
    thread_id=db.Column(
        "thread_id",
        db.Integer,
        default=0,  # noqa: WPS432
        server_default=db.text("0"),
        nullable=False
    )
    news = db.Column(
        "news",
        db.Boolean(),
        default=True,
        nullable=False,
        server_default=db.true(),
    )
    start = db.Column(
        "start",
        db.Boolean(),
        default=True,
        nullable=False,
        server_default=db.true(),
    )
    description_of_the_kz = db.Column(
        "description_of_the_kz",
        db.Boolean(),
        default=True,
        nullable=False,
        server_default=db.true(),
    )
    subscription_rock = db.Column(
        "subscription_rock",
        db.Boolean(),
        default=True,
        nullable=False,
        server_default=db.true(),
    )
    remain_zero_rock = db.Column(
        "remain_zero_rock",
        db.Boolean(),
        default=True,
        nullable=False,
        server_default=db.true(),
    )
    update_at = UPDATED_AT_COLUMN()
    created_at = CREATED_AT_COLUMN()
