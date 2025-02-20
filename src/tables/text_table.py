"""Text table model."""

from migrations import db


class TextTable(db.Model):
    """Модель таблицы текстов."""

    __tablename__ = "text_table"
    __table_args__ = {"extend_existing": True}

    name_text = db.Column(
        "name_text", db.String, nullable=False, primary_key=True
    )
    text = db.Column("text", db.Text)
    comment = db.Column("comment", db.Text)
