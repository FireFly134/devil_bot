"""Users model."""

from migrations import db


class PostNews(db.Model):
    """Модель новостей."""

    __tablename__ = "news"
    __table_args__ = {"extend_existing": True}

    id = db.Column(  # noqa: A003
        "id",
        db.Integer,
        primary_key=True,
        index=True,
        unique=True,
    )
    text = db.Column(
        "text",
        db.String,
        nullable=True,
    )
    photos = db.Column(
        "photos",
        db.ARRAY(db.String),
        nullable=True,
    )
    date_pub = db.Column("date_pub", db.DateTime, server_default=db.func.now())
    is_send = db.Column("is_send", db.Boolean, server_default=db.false())
    created_at = db.Column(
        "created_at",
        db.DateTime,
        server_default=db.func.now(),
    )
