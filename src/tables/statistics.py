"""Statistics model."""

from migrations import db
from tables.handler_db import CREATED_AT_COLUMN


class Statistics(db.Model):
    """Модель логов статистики."""

    __tablename__ = "statistics"
    __table_args__ = {"extend_existing": True}

    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
    tg_user_id = db.Column("tg_user_id", db.BigInteger)
    action = db.Column("action", db.Text)
    created_at = CREATED_AT_COLUMN()
