"""Text table model."""

import sqlalchemy as sa

from migrations import db


class TextTable(db.Model):
    """Модель таблицы текстов."""

    __tablename__ = "text_table"

    name_text = sa.Column(
        "name_text", sa.String, nullable=False, unique=True, primary_key=True
    )
    text = sa.Column("text", sa.Text)
    comment = sa.Column("comment", sa.Text)
