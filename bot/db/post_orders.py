from datetime import datetime
import typing as t
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_postgresql

from .base import METADATA, begin_connection
from db.orders_table import OrderRow, OrderTable, OrderGroupRow
from db.action_journal import save_user_action
from enums import OrderStatus, active_status_list


WorkTable: sa.Table = sa.Table(
    "post_orders",
    METADATA,

    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('user_id', sa.BigInteger),
    sa.Column('order_id', sa.Integer, unique=True),
    sa.Column('flag_del', sa.Boolean, default=False),
)


# возвращает заказы курьера
async def get_post_orders(user_id: int = None, only_active: bool = False, only_suc: bool = False) -> tuple[OrderRow]:
    query = (
        sa.select (
            OrderTable.c.id,
            OrderTable.c.d,
            OrderTable.c.e,
            OrderTable.c.f,
            OrderTable.c.g,
            OrderTable.c.h,
            OrderTable.c.i,
            OrderTable.c.j,
            OrderTable.c.k,
            OrderTable.c.l,
            OrderTable.c.m,
            OrderTable.c.n,
            OrderTable.c.o,
            OrderTable.c.p,
            OrderTable.c.q,
            OrderTable.c.r,
            OrderTable.c.s,
            OrderTable.c.clmn_t,
            OrderTable.c.u,
            OrderTable.c.v,
            OrderTable.c.w,
            OrderTable.c.x,
            OrderTable.c.y,
            OrderTable.c.z,
            OrderTable.c.ab,
            OrderTable.c.ac,
        )
        .select_from (WorkTable.join (OrderTable, WorkTable.c.order_id == OrderTable.c.id))
    )
    if user_id:
        query = query.where(WorkTable.c.user_id == user_id)

    if only_active:
        query = query.where(OrderTable.c.g.in_(active_status_list))
    elif only_suc:
        query = query.where(OrderTable.c.g == OrderStatus.SUC)

    async with begin_connection () as conn:
        result = await conn.execute (query)

    return result.all ()


# возвращает заказы курьера
async def get_statistic_post_dlv(user_id: int) -> list[OrderGroupRow]:
    query = (
        sa.select (
            OrderTable.c.g.label ('status'),
            OrderTable.c.f.label ('name'),
            sa.func.count ().label ('orders_count')
        )
        .select_from (WorkTable.join (OrderTable, WorkTable.c.order_id == OrderTable.c.id)).
        where(WorkTable.c.user_id == user_id).
        group_by(OrderTable.c.g, OrderTable.c.f)
    )

    async with begin_connection () as conn:
        result = await conn.execute (query)

    return result.all ()


# добавляет заказ
async def add_post_order(user_id: int, order_id: int) -> None:
    query = (
        sa_postgresql.insert (WorkTable)
        .values (
            user_id=user_id,
            order_id=order_id
        )
        .on_conflict_do_update (
            index_elements=[WorkTable.c.order_id],
            set_={"user_id": user_id}
        )
    )
    async with begin_connection() as conn:
        await conn.execute(query)

    await save_user_action(
        user_id=user_id,
        dlv_name=str(user_id),
        action='add post order',
        comment=str(order_id)
    )


# добавляет заказ
async def mark_del_orders(list_id: list[int]) -> None:
    query = WorkTable.update().where(WorkTable.c.order_id.in_(list_id)).values(flag_del=True)
    async with begin_connection() as conn:
        await conn.execute(query)


# добавляет заказ
async def delete_post_order(order_id: int = None, flag_del: bool = False) -> None:
    query = WorkTable.delete ()
    if order_id:
        query = query.where(WorkTable.c.order_id == order_id)
    elif flag_del:
        query = query.where(WorkTable.c.flag_del == True)

    async with begin_connection() as conn:
        await conn.execute(query)


# возвращает курьеров и количество их заказов
# async def get_users_group() -> tuple[OrderGroupRow]:
#     query = (
#         sa.select (
#             WorkTable.c.user_id,
#             OrderTable.c.f.label('name'),
#             sa.func.count ().label ('count_orders')
#         )
#         .select_from (WorkTable.join (OrderTable, WorkTable.c.order_id == OrderTable.c.id)).
#         group_by (WorkTable.c.user_id, OrderTable.c.f)
#     ).where(sa.or_(OrderTable.c.g == OrderStatus.ACTIVE.value, OrderTable.c.g == OrderStatus.ACTIVE_TAKE.value))
#
#     async with begin_connection() as conn:
#         result = await conn.execute(query)
#
#     return result.all()