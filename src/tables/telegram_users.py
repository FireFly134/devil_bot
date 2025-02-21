"""Users model."""

from migrations import db
from tables.handler_db import CREATED_AT_COLUMN, UPDATED_AT_COLUMN


class User(db.Model):
    """Модель пользователя."""

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = db.Column(  # noqa: A003
        "id", db.Integer, primary_key=True, index=True, autoincrement=True
    )
    user_id = db.Column(
        "user_id",
        db.BigInteger,
        unique=True,
        nullable=False,
    )
    first_name = db.Column("first_name", db.String(64))  # noqa: WPS432
    last_name = db.Column("last_name", db.String(64))  # noqa: WPS432
    username = db.Column("username", db.String(64))  # noqa: WPS432
    language_code = db.Column("language_code", db.String(4))
    send_msg = db.Column(
        "send_msg",
        db.Boolean(),
        default=False,
        nullable=False,
        server_default=db.false(),
    )
    subscription_event = db.Column(
        "subscription_event",
        db.Boolean(),
        default=False,
        nullable=False,
        server_default=db.false(),
    )
    update_at = UPDATED_AT_COLUMN()
    created_at = CREATED_AT_COLUMN()
