"""Users model."""

import sqlalchemy as sa

from migrations import db


class User(db.Model):
    """Модель пользователя."""

    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    id = sa.Column(  # noqa: A003
        "id", sa.Integer, primary_key=True, index=True, autoincrement=True
    )
    user_id = sa.Column(
        "user_id",
        sa.Integer,
        unique=True,
        nullable=False,
    )
    first_name = sa.Column("first_name", sa.String(64))  # noqa: WPS432
    last_name = sa.Column("last_name", sa.String(64))  # noqa: WPS432
    username = sa.Column("username", sa.String(64))  # noqa: WPS432
    language_code = sa.Column("language_code", sa.String(4))
    send_msg = sa.Column(
        "send_msg",
        sa.Boolean(),
        default=False,
        nullable=False,
        server_default=sa.false(),
    )
    subscription_event = sa.Column(
        "subscription_event",
        sa.Boolean(),
        default=False,
        nullable=False,
        server_default=sa.false(),
    )
