from datetime import datetime
import typing as t
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_postgresql

from .base import METADATA, begin_connection


class LinkRow(t.Protocol):
    id: int
    link: str


LinkTable: sa.Table = sa.Table(
    "temp_links",
    METADATA,

    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('link', sa.String(255))
)


# Добавляет cсылку
async def add_temp_link(link: str) -> None:
    query = LinkTable.insert().values(link=link)
    async with begin_connection() as conn:
        await conn.execute(query)


# Возвращает ссылку
async def get_temp_link(link: str) -> LinkRow:
    query = LinkTable.select().where(LinkTable.c.link == link)
    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.first()


# удаляет ссылку
async def delete_temp_link(link: str) -> None:
    query = LinkTable.delete ().where (LinkTable.c.link == link)
    async with begin_connection () as conn:
        await conn.execute (query)
