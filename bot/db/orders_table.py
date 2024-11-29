from datetime import datetime, date
import typing as t

import sqlalchemy as sa

from config import Config
from .base import METADATA, begin_connection, ENGINE
from db.users import UserTable
from enums.base_enum import SearchType, TypeOrderUpdate, active_status_list, done_status_list, ref_status_list


class OrderRow(t.Protocol):
    id: int
    b: str
    c: str
    d: str
    e: str
    f: str
    g: str
    h: str
    i: str
    j: str
    k: str
    l: str
    m: str
    n: str
    o: str
    p: str
    q: int
    r: int
    s: int
    clmn_t: int
    u: int
    v: int
    w: str
    x: str
    y: int
    z: str
    aa: str
    ab: str
    ac: str
    ad: str
    ae: str
    af: str
    ag: str
    ah: str
    updated: bool
    time_update: datetime
    type_update: str
    discount: int
    row_num: int
    user_id: int
    phone: str
    company: str
    comp_opr: str


class OrderGroupRow(t.Protocol):
    status: str
    name: str
    orders_count: str


class OprReportRow(t.Protocol):
    date: str
    orders_count: str


OrderTable: sa.Table = sa.Table(
    "orders_ggl",
    METADATA,

    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('b', sa.String(255)),
    sa.Column('c', sa.String(255)),
    sa.Column('d', sa.String(255)),
    sa.Column('e', sa.String(255)),
    sa.Column('f', sa.String(255)),
    sa.Column('g', sa.String(255)),
    sa.Column('h', sa.String(255)),
    sa.Column('i', sa.String(255)),
    sa.Column('j', sa.String(255)),
    sa.Column('k', sa.String(255)),
    sa.Column('l', sa.String(255)),
    sa.Column('m', sa.Text()),
    sa.Column('n', sa.String(255)),
    sa.Column('o', sa.String(255)),
    sa.Column('p', sa.Text),
    sa.Column('q', sa.Integer),
    sa.Column('r', sa.Integer),
    sa.Column('s', sa.Integer),
    sa.Column('clmn_t', sa.Integer),
    sa.Column('u', sa.Integer),
    sa.Column('v', sa.Integer),
    sa.Column('w', sa.String(255)),
    sa.Column('x', sa.Text),
    sa.Column('y', sa.Integer),
    sa.Column('z', sa.String(255)),
    sa.Column('aa', sa.String(255)),
    sa.Column('ab', sa.String(255)),
    sa.Column('ac', sa.String(255)),
    sa.Column('ad', sa.String(255)),
    sa.Column('ae', sa.String(255)),
    sa.Column('af', sa.String(255)),
    sa.Column('ag', sa.String(255)),
    sa.Column('ah', sa.String(255)),
    sa.Column('comp_opr', sa.String(255)),
    sa.Column('updated', sa.Boolean, default=True),
    sa.Column('time_update', sa.DateTime(timezone=True), default=datetime.now()),
    sa.Column('type_update', sa.String(255)),
    sa.Column('discount', sa.Integer(), default=0),
    sa.Column('row_num', sa.Integer()),
)


# Индексируем таблицу
async def index_table():
    idx = sa.Index('idx_id', OrderTable.c.user_id)
    idx.create(ENGINE)


# синхронезирует автоинкримент с последним id
async def syncing_id():
    async with begin_connection() as conn:
        await conn.execute (sa.text ("SELECT setval('orders_ggl_id_seq', (SELECT MAX(id) FROM orders_ggl));"))


# добавляет строку
async def add_row(
    row_num: int,
    b: str = None,
    c: str = None,
    d: str = None,
    e: str = None,
    f: str = None,
    g: str = None,
    h: str = None,
    i: str = None,
    j: str = None,
    k: str = None,
    l: str = None,
    m: str = None,
    n: str = None,
    o: str = None,
    p: str = None,
    q: int = 0,
    r: int = 0,
    s: int = 0,
    t: int = 0,
    u: int = 0,
    v: int = 0,
    w: str = None,
    x: str = None,
    y: int = 0,
    z: str = None,
    aa: str = None,
    ab: str = None,
    ac: str = None,
    ad: str = None,
    ae: str = None,
    af: str = None,
    ag: str = None,
    ah: str = None,
    comp_opr: str = None,
    type_update: str = None,
    updated: bool = False,
    entry_id: int = None
):
    query = OrderTable.insert().values(
        row_num=row_num,
        b=b,
        c=c,
        d=d,
        e=e,
        f=f,
        g=g,
        h=h,
        i=i,
        j=j,
        k=k,
        l=l,
        m=m,
        n=n,
        o=o,
        p=p,
        q=q,
        r=r,
        s=s,
        clmn_t=t,
        u=u,
        v=v,
        w=w,
        x=x,
        y=y,
        z=z,
        aa=aa,
        ab=ab,
        ac=ac,
        ad=ad,
        ae=ae,
        af=af,
        ag=ag,
        ah=ah,
        comp_opr=comp_opr,
        type_update=type_update,
        time_update=datetime.now(),
        updated=updated
    )
    if entry_id:
        query = query.values(id=entry_id)
    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.inserted_primary_key[0]


# обновляет строку в таблице
# e - дата, f - курьер, g - статус, k - оператор, ab - примечание, f - курьер, y - скидка
async def update_row_google(
        order_id: int,
        b: str = None,
        c: str = None,
        d: str = None,
        e: str = None,
        f: str = None,
        g: str = None,
        h: str = None,
        i: str = None,
        j: str = None,
        k: str = None,
        l: str = None,
        m: str = None,
        n: str = None,
        o: str = None,
        p: str = None,
        q: int = None,
        r: int = None,
        s: int = None,
        t: int = None,
        u: int = None,
        v: int = None,
        w: str = None,
        x: str = None,
        y: int = None,
        z: str = None,
        aa: str = None,
        ab: str = None,
        ac: str = None,
        ad: str = None,
        ae: str = None,
        af: str = None,
        ag: str = None,
        ah: str = None,
        comp_opr: str = None,
        update_row: bool = False,
        all_row: bool = False,
        take_date: str = None,
        dlv_name: str = None,
        status: str = None,
        note: str = None,
        type_update: str = None,
        discount: int = None,
        cost_delivery: int = None,
        letter: str = None,
        company: str = None,
):
    query = (OrderTable.update().where(OrderTable.c.id == order_id).
             values(updated=update_row,
                    time_update=datetime.now()))

    if take_date:
        query = query.values(e=take_date)
    if dlv_name:
        query = query.values(f=dlv_name)
    if status:
        query = query.values(g=status)
    if note:
        query = query.values(ab=note) if note != 'del' else query.values(ab=None)
    if type_update:
        query = query.values(type_update=type_update)
    if discount is not None:
        query = query.values(y=discount)
    if cost_delivery:
        query = query.values(clmn_t=cost_delivery) if cost_delivery != 'del' else query.values(clmn_t=0)
    if letter:
        query = query.values(d=letter) if letter != 'del' else query.values(d=None)
    if company:
        query = query.values(ac=company) if company != 'del' else query.values(ac=None)
    if all_row:
        query = query.values(b=b, c=c, d=d, e=e, f=f, g=g, h=h, i=i, j=j, k=k, l=l, m=m, n=n, o=o, p=p,
                             q=q, r=r, s=s, clmn_t=t, u=u, v=v, w=w, x=x, y=y, z=z, aa=aa, ab=ab, ac=ac, ad=ad, ae=ae,
                             af=af, ag=ag, ah=ah, comp_opr=comp_opr)

    async with begin_connection() as conn:
        await conn.execute(query)


# обновляет несколько заказов
async def update_multi_orders(
        date_str: str = None,
        type_update: str = TypeOrderUpdate.EDIT.value,
        test: bool = False
) -> None:
    # if type_update == TypeOrderUpdate.UP_DATE.value:
    if test:
        query = OrderTable.update ().where (OrderTable.c.g.in_ (active_status_list [:-1])).values (e=date_str)
    else:
        query = OrderTable.update().where(OrderTable.c.g.in_ (active_status_list[:-1])).values(
            updated=False,
            time_update=datetime.now(),
            type_update=type_update,
            e=date_str,
            d=None
        )

    async with begin_connection() as conn:
        await conn.execute(query)


# обновляет несколько заказов
async def hard_order_update() -> None:
    query = OrderTable.update ().values (updated=True)

    async with begin_connection() as conn:
        await conn.execute(query)


# возвращает строки таблицы
async def get_orders(
        user_id: int = None,
        dlv_name: str = None,
        opr_name: str = None,
        order_status: str = None,
        get_active: bool = False,
        get_done: bool = False,
        get_ref: bool = False,
        get_wait_update: bool = False,
        on_date: str = None,
        search_query: str = None,
        search_on: str = None,
        company_dlv: str = None,
        company_opr: str = None,
) -> tuple[OrderRow]:
    query = (sa.select(
        OrderTable.c.id,
        OrderTable.c.b,
        OrderTable.c.c,
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
        OrderTable.c.aa,
        OrderTable.c.ab,
        OrderTable.c.ac,
        OrderTable.c.ad,
        OrderTable.c.ae,
        OrderTable.c.af,
        OrderTable.c.ag,
        OrderTable.c.ah,
        OrderTable.c.updated,
        OrderTable.c.time_update,
        OrderTable.c.type_update,
        OrderTable.c.discount,
        OrderTable.c.row_num,
        OrderTable.c.id,
        OrderTable.c.comp_opr,
        UserTable.c.user_id,
        UserTable.c.phone,
        UserTable.c.company,
    ).select_from (OrderTable.join (UserTable, OrderTable.c.f == UserTable.c.name, isouter=True)).
             order_by(OrderTable.c.row_num))

    if get_active:
        query = query.where (OrderTable.c.g.in_ (active_status_list[:-1]))
    elif get_done:
        query = query.where (OrderTable.c.g.in_ (done_status_list))
    elif get_ref:
        query = query.where (OrderTable.c.g.in_ (ref_status_list))
    elif order_status:
        query = query.where(OrderTable.c.g == order_status)
    elif get_wait_update:
        query = query.where (OrderTable.c.updated.is_(False))

    if company_dlv:
        query = query.where (OrderTable.c.ac == company_dlv)
    elif company_opr:
        query = query.where (OrderTable.c.comp_opr == company_opr)

    if dlv_name:
        query = query.where(OrderTable.c.f == dlv_name)
    elif opr_name:
        query = query.where(OrderTable.c.k == opr_name)
    elif user_id:
        query = query.where(UserTable.c.user_id == user_id)

    if on_date:
        query = query.where(OrderTable.c.e == on_date)

    if search_on == SearchType.PHONE:
        query = query.where(sa.or_(OrderTable.c.n.like(f'%{search_query}%'), OrderTable.c.o.like(f'%{search_query}%')))
    elif search_on == SearchType.NAME:
        query = query.where(OrderTable.c.m.like(f'%{search_query}%'))
    elif search_on == SearchType.METRO:
        query = query.where(OrderTable.c.w.like(f'%{search_query}%'))
    elif search_on == SearchType.POST:
        query = query.where(OrderTable.c.ab.like(f'%{search_query}%'))

    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.all()


# возвращает одну строку таблицы
async def get_order(order_id: int = 0, for_update: bool = False) -> t.Union[OrderRow, None]:
    query = sa.select (
        OrderTable.c.id,
        OrderTable.c.b,
        OrderTable.c.c,
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
        OrderTable.c.aa,
        OrderTable.c.ab,
        OrderTable.c.ac,
        OrderTable.c.ad,
        OrderTable.c.ae,
        OrderTable.c.af,
        OrderTable.c.ag,
        OrderTable.c.ah,
        OrderTable.c.updated,
        OrderTable.c.time_update,
        OrderTable.c.type_update,
        OrderTable.c.discount,
        OrderTable.c.row_num,
        OrderTable.c.id,
        OrderTable.c.comp_opr,
        UserTable.c.user_id,
        UserTable.c.phone,
    ).select_from (OrderTable.join (UserTable, OrderTable.c.f == UserTable.c.name, isouter=True))

    if order_id:
        query = query.where (OrderTable.c.id == order_id)
    elif for_update:
        query = query.where(OrderTable.c.updated.is_(False)).order_by(OrderTable.c.time_update)

    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.first()


# показывает максимальный номер строки
async def get_max_row_num() -> int:
    query = sa.select(sa.func.max(OrderTable.c.row_num))
    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.scalar()


# очищает таблицу
async def delete_orders():
    query = OrderTable.delete()
    async with begin_connection() as conn:
        await conn.execute(query)


# статистика заказов
async def get_orders_statistic(
        dlv_name: str = None,
        opr_name: str = None,
        on_date: str = None,
        only_active: bool = False,
        own_text: bool = False,
        list_id: list[int] = None
) -> tuple[OrderGroupRow]:
    if own_text:
        query = (OrderTable.select ().
                 with_only_columns (
            OrderTable.c.g.label ('status'),
            sa.func.count ().label ('orders_count')).group_by (OrderTable.c.g).order_by(
            sa.desc(sa.func.count ())
        ))
    else:
        query = (OrderTable.select().
                 with_only_columns(
            OrderTable.c.g.label('status'),
            OrderTable.c.f.label('name'),
            sa.func.count().label('orders_count')
        ).group_by(OrderTable.c.g, OrderTable.c.f))

    if dlv_name:
        query = query.where(OrderTable.c.f == dlv_name)
    if opr_name:
        query = query.where(OrderTable.c.k == opr_name)
    if on_date:
        query = query.where(OrderTable.c.e == on_date)
    if only_active:
        query = query.where(OrderTable.c.g.in_(active_status_list))
    if list_id:
        query = query.where(OrderTable.c.id.in_(list_id))

    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.all()


# заказы "у курьера"
async def get_users_orders_count() -> tuple[OrderGroupRow]:
    query = (
        OrderTable.select().
        with_only_columns(
            OrderTable.c.f.label('name'),
            sa.func.count().label('orders_count')
        ).group_by(OrderTable.c.f)
        .where(OrderTable.c.g.in_(active_status_list)).order_by(OrderTable.c.f)
    )

    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.all()


# дни для отчёта оператору
async def get_opr_report_days(
        opr_name: str,
        order_status: str = None,
        get_active: bool = False,
        get_done: bool = False,
        get_ref: bool = False,
) -> tuple[OprReportRow]:
    query = (OrderTable.select ().with_only_columns (
        OrderTable.c.e.label ('date'),
        sa.func.count ().label ('orders_count')
    ).group_by (OrderTable.c.e).where(
        OrderTable.c.k == opr_name,
        OrderTable.c.e != None
    ))
    if get_active:
        query = query.where (OrderTable.c.g.in_ (active_status_list[:-1]))
    elif get_done:
        query = query.where (OrderTable.c.g.in_ (done_status_list))
    elif get_ref:
        query = query.where (OrderTable.c.g.in_ (ref_status_list))
    elif order_status:
        query = query.where (OrderTable.c.g == order_status)

    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.all()