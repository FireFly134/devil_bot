"""Heroes of users model."""

import sqlalchemy as sa

from migrations import db


class HeroesOfUsers(db.Model):
    """Модель героев пользователей."""

    __tablename__ = "heroes_of_users"
    __table_args__ = {"extend_existing": True}

    id = sa.Column(
        "id", sa.Integer, primary_key=True, index=True, autoincrement=True
    )
    user_id = sa.Column(
        "user_id", sa.Integer, sa.ForeignKey("user.id"), nullable=False
    )
    name = sa.Column("name", sa.String, nullable=False)
    rock = sa.Column(
        "rock",
        sa.Integer,
        default=0,
        server_default=sa.text("0"),
        nullable=False,
    )
    clan_id = sa.Column(
        "clan_id",
        sa.Integer,
        sa.ForeignKey("clans.id"),
        nullable=True,
    )
    time_change_kz = sa.Column(
        "time_change_kz",
        sa.Integer,
        default=18,
        server_default=sa.text("18"),
        nullable=False,
    )
    time_collection_energy = sa.Column(
        "time_collection_energy",
        sa.Integer,
        default=12,
        server_default=sa.text("12"),
        nullable=False,
    )
    subscription_rock = sa.Column(
        "subscription_rock",
        sa.Boolean(),
        default=False,
        nullable=False,
        server_default=sa.false(),
    )
    subscription_energy = sa.Column(
        "subscription_energy",
        sa.Boolean(),
        default=False,
        nullable=False,
        server_default=sa.false(),
    )
    description_of_the_kz = sa.Column(
        "description_of_the_kz",
        sa.Boolean(),
        default=False,
        nullable=False,
        server_default=sa.false(),
    )
