"""Heroes of users model."""

from migrations import db


class HeroesOfUsers(db.Model):
    """Модель героев пользователей."""

    __tablename__ = "heroes_of_users"
    __table_args__ = {"extend_existing": True}

    id = db.Column(  # noqa: A003
        "id", db.Integer, primary_key=True, index=True, autoincrement=True
    )
    user_id = db.Column(
        "user_id", db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    name = db.Column("name", db.String, nullable=False)
    rock = db.Column(
        "rock",
        db.Integer,
        default=0,
        server_default=db.text("0"),
        nullable=False,
    )
    clan_id = db.Column(
        "clan_id",
        db.Integer,
        db.ForeignKey("clans.id"),
        nullable=True,
    )
    time_change_kz = db.Column(
        "time_change_kz",
        db.Integer,
        default=18,  # noqa: WPS432
        server_default=db.text("18"),
        nullable=False,
    )
    time_collection_energy = db.Column(
        "time_collection_energy",
        db.Integer,
        default=12,  # noqa: WPS432
        server_default=db.text("12"),
        nullable=False,
    )
    subscription_rock = db.Column(
        "subscription_rock",
        db.Boolean(),
        default=False,
        nullable=False,
        server_default=db.false(),
    )
    subscription_energy = db.Column(
        "subscription_energy",
        db.Boolean(),
        default=False,
        nullable=False,
        server_default=db.false(),
    )
    description_of_the_kz = db.Column(
        "description_of_the_kz",
        db.Boolean(),
        default=False,
        nullable=False,
        server_default=db.false(),
    )
    update_at = db.Column(
        "update_at",
        db.DateTime,
        server_default=db.func.now(),
    )
    created_at = db.Column(
        "created_at",
        db.DateTime,
        server_default=db.func.now(),
    )
