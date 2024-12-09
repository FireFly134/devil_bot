"""Users model."""

import sqlalchemy as sa

from migrations import db


class PostNews(db.Model):
    """Модель новостей."""

    __tablename__ = "news"

    id = sa.Column(
        "id",
        sa.Integer,
        primary_key=True,
        index=True,
        unique=True,
    )
    text = sa.Column(
        "text",
        sa.String,
        nullable=True,
    )
    photos = sa.Column(
        "photos",
        sa.ARRAY(sa.String),
        nullable=True,
    )
    date_pub = sa.Column(
        "date_pub",
        sa.DateTime,
        nullable=True,
    )
    is_send = sa.Column("is_send", sa.Boolean, server_default=sa.false())
    created_at = sa.Column(
        "created_at",
        sa.DateTime,
        server_default=sa.func.now(),
    )
