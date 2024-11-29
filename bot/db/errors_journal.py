from datetime import datetime
import typing as t
import sqlalchemy as sa

from config import Config
from .base import METADATA, begin_connection


class ErrorsRow(t.Protocol):
    id: int
    created_at: datetime
    user_id: int
    error: str


ErrorsTable: sa.Table = sa.Table(
    "errors_journal",
    METADATA,

    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('created_at', sa.DateTime(timezone=True)),
    sa.Column('user_id', sa.BigInteger),
    sa.Column('error', sa.String),
)


# Сохраняет действие пользователя
async def save_error(user_id: int, error: str) -> None:
    query = ErrorsTable.insert().values(
        created_at=datetime.now().replace(microsecond=0),
        user_id=user_id,
        error=error
    )
    async with begin_connection() as conn:
        await conn.execute(query)
