"""Module for db handlers, helpers and other classes and functions."""
import sqlalchemy as sa
from sqlalchemy import func

CREATED_AT_COLUMN = lambda: sa.Column(  # noqa E731
    "created_at", sa.TIMESTAMP, server_default=func.now(tz=True)
)

UPDATED_AT_COLUMN = lambda: sa.Column(  # noqa E731
    "updated_at",
    sa.TIMESTAMP,
    server_default=func.now(tz=True),
    server_onupdate=func.now(tz=True),
    default=func.now(tz=True),
    onupdate=func.now(tz=True),
)
