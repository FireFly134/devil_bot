"""Users model."""

import sqlalchemy as sa

from src.migrations import db


class User(db.Model):
    """Модель пользователя."""

    __tablename__ = "user"

    id = sa.Column(
        "id", sa.Integer, primary_key=True, index=True, autoincrement=True
    )
    user_id = sa.Column(
        "user_id",
        sa.Integer,
        unique=True,
        nullable=False,
    )
    first_name = sa.Column("first_name", sa.String(64))
    last_name = sa.Column("last_name", sa.String(64))
    username = sa.Column("username", sa.String(64))
    language_code = sa.Column("language_code", sa.String(4))
    send_msg = sa.Column(
        "send_msg",
        sa.Boolean(),
        default=False,
        nullable=False,
        server_default=sa.false(),
    )
