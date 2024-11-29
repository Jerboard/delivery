from datetime import datetime
import typing as t
import sqlalchemy as sa

from config import Config
from .base import METADATA, begin_connection


class ActionRow(t.Protocol):
    id: int
    created_at: datetime
    user_id: int
    dlv_name: str
    action: str
    comment: str


ActionTable: sa.Table = sa.Table(
    "action_journal",
    METADATA,

    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('created_at', sa.DateTime(timezone=True)),
    sa.Column('user_id', sa.BigInteger),
    sa.Column('dlv_name', sa.String(255)),
    sa.Column('action', sa.String(255)),
    sa.Column('comment', sa.String(255))
)


# Сохраняет действие пользователя
async def save_user_action(user_id: int, dlv_name: str, action: str, comment: str = None) -> None:
    query = ActionTable.insert().values(
        created_at=datetime.now().replace(microsecond=0),
        user_id=user_id,
        dlv_name=dlv_name,
        action=action,
        comment=comment
    )
    async with begin_connection() as conn:
        await conn.execute(query)
