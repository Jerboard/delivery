from datetime import datetime
import typing as t
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_postgresql

from .base import METADATA, begin_connection
from config import Config
from init import log_error


class ReportRow(t.Protocol):
    id: int
    b: int
    c: int
    d: int
    e: int
    f: int
    g: int
    h: int
    i: int
    j: int
    clmn_k: int
    l: list[str]
    m: str
    n: str
    o: int
    p: str
    q: str
    r: int
    in_google: bool
    row_num: int


ReportTable: sa.Table = sa.Table(
    "report_ggl",
    METADATA,

    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('b', sa.Integer, default=0),
    sa.Column('c', sa.Integer, default=0),
    sa.Column('d', sa.Integer, default=0),
    sa.Column('e', sa.Integer, default=0),
    sa.Column('f', sa.Integer, default=0),
    sa.Column('g', sa.Integer, default=0),
    sa.Column('h', sa.Integer, default=0),
    sa.Column('i', sa.Integer, default=0),
    sa.Column('j', sa.Integer, default=0),
    # sa.Column('k', sa.Integer, default=0),
    sa.Column('clmn_k', sa.Integer, default=0),
    sa.Column('l', sa.ARRAY(sa.String(255))),
    sa.Column('m', sa.Text),
    sa.Column('n', sa.String(255)),
    sa.Column('o', sa.Integer),
    sa.Column('p', sa.String(255)),
    sa.Column('q', sa.String(255)),
    sa.Column('r', sa.Integer),
    sa.Column('in_google', sa.Boolean),
    sa.Column('row_num', sa.Integer),
    sa.Column ('time_update', sa.DateTime (timezone=True), default=datetime.now ().replace (microsecond=0))
)


# посмотреть траты курьера
async def get_reports_all_dlv(
        dlv_name: str = None,
        opr_name: str = None,
        get_wait_update: bool = False,
        exception_date: str = None,
        on_date: str = None
) -> tuple[ReportRow]:
    query = ReportTable.select()

    if get_wait_update:
        query = query.where (ReportTable.c.in_google == False)

    if dlv_name:
        query = query.where (ReportTable.c.n == dlv_name)

    if exception_date:
        query = query.where (ReportTable.c.m != exception_date)

    if on_date:
        query = query.where (ReportTable.c.m == on_date)

    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.all()


# возвращает запись из отчёта
async def get_report_dlv(dlv_name: str, exp_date: str = None) -> t.Optional[ReportRow]:
    query = ReportTable.select().where(ReportTable.c.n == dlv_name)
    if exp_date:
        query = query.where(ReportTable.c.m == exp_date)
    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.first()


# возвращает запись из отчёта
async def get_last_updated_report(last_row: bool = False) -> t.Optional[ReportRow]:
    query = ReportTable.select()
    if last_row:
        query = query.order_by(sa.desc(ReportTable.c.row_num)).limit(1)
    else:
        query = query.where(ReportTable.c.in_google == False).order_by(ReportTable.c.time_update)
    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.first()


# добавляет трату
# m - дата, n - курьер, l - комментарий, b-k - суммы
async def add_report_row(
        # entry_id: int = None,
        b: int = 0,
        c: int = 0,
        d: int = 0,
        e: int = 0,
        f: int = 0,
        g: int = 0,
        h: int = 0,
        i: int = 0,
        j: int = 0,
        k: int = 0,
        l: list [str] = None,
        m: str = None,
        n: str = None,
        o: int = 0,
        p: str = None,
        q: str = None,
        r: int = 0,
        add_row: bool = False,
        updated: bool = False,
        row_num: int = 0
) -> None:
    query = ReportTable.insert().values(
        b=b, c=c, d=d, e=e, f=f, g=g, h=h, i=i, j=j, clmn_k=k, l=l, m=m, n=n, o=o, p=p, q=q, r=r,
        row_num=row_num,
        in_google=updated
    )

    async with begin_connection() as conn:
        await conn.execute(query)


# обновляет трату
# m - дата, n - курьер, l - комментарий, b-k - суммы
async def update_expenses_dlv(
        entry_id: int,
        b: int = 0,
        c: int = 0,
        d: int = 0,
        e: int = 0,
        f: int = 0,
        g: int = 0,
        h: int = 0,
        i: int = 0,
        j: int = 0,
        k: int = 0,
        l: str = None,
        m: str = None,
        n: str = None,
        o: int = 0,
        p: str = None,
        q: str = None,
        r: int = 0,
        updated: bool = False,
        row_num: int = 0
) -> None:
    query = ReportTable.update ().where (ReportTable.c.id == entry_id).values (
        in_google=updated,
        time_update=datetime.now ().replace (microsecond=0)
    )
    if b:
        query = query.values(b=b)
    if c:
        query = query.values(c=c)
    if d:
        query = query.values(d=d)
    if e:
        query = query.values(e=e)
    if f:
        query = query.values(f=f)
    if g:
        query = query.values(g=g)
    if h:
        query = query.values(h=h)
    if i:
        query = query.values(i=i)
    if j:
        query = query.values(j=j)
    if k:
        query = query.values(clmn_k=k)
    if l:
        query = query.values(l=sa.func.array_append(ReportTable.c.l, l))
    # if close_partner_id:
    #     query = query.values (closed_partners=sa.func.array_append(OrderTable.c.closed_partners, close_partner_id))
    if m:
        query = query.values(m=m)
    if n:
        query = query.values(n=n)
    if o:
        query = query.values(o=o)
    if p:
        query = query.values(p=p)
    if q:
        query = query.values(q=q)
    if r:
        query = query.values(r=r)
    if row_num:
        query = query.values(row_num=row_num)

    async with begin_connection() as conn:
        await conn.execute(query)


# очищает таблицу трат
async def clear_report_table() -> None:
    query = ReportTable.delete()
    async with begin_connection() as conn:
        await conn.execute(query)

