"""Clans model."""

import sqlalchemy as sa

from migrations import db


class Clans(db.Model):
    """Модель клана."""

    __tablename__ = "clans"

    id = sa.Column(
        "id", sa.Integer, primary_key=True, index=True, autoincrement=True
    )
    name_clan = sa.Column("name_clan", sa.String, nullable=False)
    time_kz = sa.Column(
        "time_kz",
        sa.Integer,
        default=18,
        server_default=sa.text("18"),
        nullable=False,
    )
    chat_id = sa.Column("chat_id", sa.String, nullable=False)
    news = sa.Column(
        "news",
        sa.Boolean(),
        default=True,
        nullable=False,
        server_default=sa.true(),
    )
    start = sa.Column(
        "start",
        sa.Boolean(),
        default=False,
        nullable=False,
        server_default=sa.false(),
    )
    description_of_the_kz = sa.Column(
        "description_of_the_kz",
        sa.Boolean(),
        default=True,
        nullable=False,
        server_default=sa.true(),
    )
    subscription_rock = sa.Column(
        "subscription_rock",
        sa.Boolean(),
        default=True,
        nullable=False,
        server_default=sa.true(),
    )
    remain_zero_rock = sa.Column(
        "remain_zero_rock",
        sa.Boolean(),
        default=True,
        nullable=False,
        server_default=sa.true(),
    )
