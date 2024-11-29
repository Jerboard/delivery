from datetime import datetime
import typing as t
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_postgresql

from .base import METADATA, begin_connection


class UserRow(t.Protocol):
    id: int
    user_id: int
    full_name: str
    username: str
    role: str
    name: str
    company: str
    phone: str


UserTable: sa.Table = sa.Table(
    "users",
    METADATA,

    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('user_id', sa.BigInteger, unique=True),
    sa.Column('full_name', sa.String(255)),
    sa.Column('username', sa.String(255)),
    sa.Column('role', sa.String(255)),
    sa.Column('name', sa.String(255)),
    sa.Column('company', sa.String(255)),
    sa.Column('phone', sa.String(255)),
)


# Добавляет пользователя
async def add_user(user_id: int, full_name: str, username: str, role: str, company: str = None) -> None:
    query = (
        sa_postgresql.insert(UserTable)
        .values(
            user_id=user_id,
            full_name=full_name,
            username=username,
            role=role,
            company=company
        )
        .on_conflict_do_update(
            index_elements=[UserTable.c.user_id],
            set_={"full_name": full_name, 'username': username}
        )
    )
    async with begin_connection() as conn:
        await conn.execute(query)


# возвращает пользователя
async def get_user_info(user_id: int = None, name: str = None, phone: str = None) -> UserRow:
    query = UserTable.select()

    if user_id:
        query = query.where(UserTable.c.user_id == user_id)
    if name:
        query = query.where(UserTable.c.name == name)

    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.first()


# возвращает пользователей
async def get_users(exc_user_id: int = None, company: str = None, role: str = None) -> tuple[UserRow]:
    query = UserTable.select()

    if exc_user_id:
        query = query.where(UserTable.c.user_id != exc_user_id)
    if company:
        query = query.where(UserTable.c.company == company)
    if role:
        query = query.where(UserTable.c.role == role)

    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.all()


# обновляет данные пользователя
async def update_user_info(
        user_id: int,
        name: str = None,
        company: str = None,
        phone: str = None,
) -> None:
    query = UserTable.update().where(UserTable.c.user_id == user_id)

    if name:
        query = query.values(name=name)
    if company:
        query = query.values(company_id=company)
    if phone:
        query = query.values(phone=phone)

    async with begin_connection() as conn:
        await conn.execute(query)


# удаляет пользователя
async def delete_user(user_id: int) -> None:
    query = UserTable.delete().where(UserTable.c.user_id == user_id)
    async with begin_connection() as conn:
        await conn.execute(query)
