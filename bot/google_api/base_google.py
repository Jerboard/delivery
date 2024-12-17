import re
import asyncio

from datetime import datetime

import db
import google_api.utils_google as ug
from config import Config
from init import bot, log_error
# from utils.base_utils import get_dlv_name_dict, get_work_orders_list
from data.base_data import order_status_data, company_dlv, company_dlv
from enums import TypeOrderUpdate, UserRole, SheetsPage


# (a - 0, b - 1, c - 2, d - 3, e - 4, f - 5, g - 6, h - 7, i - 8, j - 9, k - 10,
#  l - 11, m - 12, n - 13, o - 14, p - 15, q - 16, r - 17, s - 18, t - 19, u - 20,
#  v - 21, w - 22, x - 23, y - 24, z - 25.)
test_table = '12Sm-PMgBy_ANC2WuesE8WWo_sawyaqx4QeMlkWTVfmM'


# обновляет таблицу по команде
async def save_new_order_table(table_id: str) -> str:
    sh = ug.get_google_connect (table_id)

    # new_orders = sh.sheet1.get_all_values ()
    new_orders = sh.worksheet(SheetsPage.BASE.value).get_all_values ()

    opr_dict = await ug.get_company_dict(UserRole.OPR.value)
    dlv_dict = await ug.get_company_dict(UserRole.DLV.value)

    rewrite_list = []
    exc_list = []

    new_row_num = 4
    for row in new_orders [4:]:
        new_row_num += 1
        if row [13].strip () != '':
            try:
                entry_id = int (row [0])
                order_user_name = row [5].strip () if row [5] else None
                order_status = order_status_data.get(row[6].strip())
                comp_opr = ug.check_comp_name(row [10].strip (), comp_dict=opr_dict)
                comp_dlv = ug.check_comp_name(order_user_name, comp_dict=dlv_dict)

                await db.add_row (
                    entry_id=entry_id,
                    row_num=new_row_num,
                    b=row [1].strip () if row [1] else None,
                    c=row [2].strip () if row [2] else None,
                    d=row [3].strip () if row [3] else None,
                    e=row [4].strip () if row [4] else None,
                    f=order_user_name,
                    g=order_status,
                    h=row [7].strip () if row [7] else None,
                    i=row [8].strip () if row [8] else None,
                    j=row [9].strip () if row [9] else None,
                    k=row [10].strip () if row [10] else None,
                    l=row [11].strip () if row [11] else None,
                    m=row [12].strip () if row [12] else None,
                    n=row [13].strip () if row [13] else None,
                    o=row [14].strip () if row [14] else '',
                    p=row [15].strip () if row [15] else None,
                    q=int (re.sub (r'\D+', '', row [16]) or 0),
                    r=int (re.sub (r'\D+', '', row [17]) or 0),
                    s=int (re.sub (r'\D+', '', row [18]) or 0),
                    t=int (re.sub (r'\D+', '', row [19]) or 0),
                    u=int (re.sub (r'\D+', '', row [20]) or 0),
                    v=int (re.sub (r'\D+', '', row [21]) or 0),
                    w=row [22].strip () if row [22] else None,
                    x=row [23].strip () if row [23] else None,
                    y=int (re.sub (r'\D+', '', row [24]) or 0),
                    z=row [25].strip () if row [25] else None,
                    aa=row [26].strip () if row [26] else None,
                    ab=row [27].strip () if row [27] else None,
                    ac=comp_dlv,
                    ad=row [29].strip () if row [29] else None,
                    ae=row [30].strip () if row [30] else None,
                    af=row [31].strip () if row [31] else None,
                    ag=row [32].strip () if row [32] else None,
                    ah=row [33].strip () if row [33] else None,
                    comp_opr=comp_opr,
                    type_update=TypeOrderUpdate.ADD.value,
                    updated=True
                )
            except Exception as ex:
                row[0] = new_row_num
                rewrite_list.append(row)

    # синхронизирует ID
    await db.syncing_id()

    for row in rewrite_list:
        try:
            comp_opr = ug.check_comp_name (row [10].strip (), comp_dict=opr_dict)
            comp_dlv = ug.check_comp_name (row [5].strip (), comp_dict=dlv_dict)
            order_status = order_status_data.get (row [6].strip ())
            await db.add_row (
                row_num=row [0],
                b=row [1].strip () if row [1] else None,
                c=row [2].strip () if row [2] else None,
                d=row [3].strip () if row [3] else None,
                e=row [4].strip () if row [4] else None,
                f=row [5].strip () if row [5] else None,
                g=order_status,
                h=row [7].strip () if row [7] else None,
                i=row [8].strip () if row [8] else None,
                j=row [9].strip () if row [9] else None,
                k=row [10].strip () if row [10] else None,
                l=row [11].strip () if row [11] else None,
                m=row [12].strip () if row [12] else None,
                n=row [13].strip () if row [13] else None,
                o=row [14].strip () if row [14] else '',
                p=row [15].strip () if row [15] else None,
                q=int (re.sub (r'\D+', '', row [16]) or 0),
                r=int (re.sub (r'\D+', '', row [17]) or 0),
                s=int (re.sub (r'\D+', '', row [18]) or 0),
                t=int (re.sub (r'\D+', '', row [19]) or 0),
                u=int (re.sub (r'\D+', '', row [20]) or 0),
                v=int (re.sub (r'\D+', '', row [21]) or 0),
                w=row [22].strip () if row [22] else None,
                x=row [23].strip () if row [23] else None,
                y=int (re.sub (r'\D+', '', row [24]) or 0),
                z=row [25].strip () if row [25] else None,
                aa=row [26].strip () if row [26] else None,
                ab=row [27].strip () if row [27] else None,
                ac=comp_dlv,
                ad=row [29].strip () if row [29] else None,
                ae=row [30].strip () if row [30] else None,
                af=row [31].strip () if row [31] else None,
                ag=row [32].strip () if row [32] else None,
                ah=row [33].strip () if row [33] else None,
                comp_opr=comp_opr,
                type_update=TypeOrderUpdate.ADD.value,
                updated=False
            )
        except Exception as ex:
            exc_list.append (row)
            log_error (ex)

    ex_text = ''
    for row in exc_list:
        ex_text += f'{row}\n'
    error_text = f'Всего ошибок: {len(exc_list)}'
    log_error (f'{error_text}\n{ex_text}', with_traceback=False)
    if len(exc_list):
        return error_text


# сохраняет таблицу отчётов
async def save_new_report_table(table_id: str = None) -> None:
    sh = ug.get_google_connect (table_id)
    # table = sh.get_worksheet (Config.report_sheet_num).get_all_values ()
    table = sh.worksheet(SheetsPage.REPORT.value).get_all_values ()

    counter = 4
    for row in table [4:]:
        counter += 1
        try:
            if row [13]:
                l_list = row [11].split ('\n')
                await db.add_report_row (
                    b=int (re.sub (r'\D+', '', row [1]) or 0),
                    c=int (re.sub (r'\D+', '', row [2]) or 0),
                    d=int (re.sub (r'\D+', '', row [3]) or 0),
                    e=int (re.sub (r'\D+', '', row [4]) or 0),
                    f=int (re.sub (r'\D+', '', row [5]) or 0),
                    g=int (re.sub (r'\D+', '', row [6]) or 0),
                    h=int (re.sub (r'\D+', '', row [7]) or 0),
                    i=int (re.sub (r'\D+', '', row [8]) or 0),
                    j=int (re.sub (r'\D+', '', row [9]) or 0),
                    k=int (re.sub (r'\D+', '', row [10]) or 0),
                    l=l_list,
                    m=row [12].strip (),
                    n=row [13].strip (),
                    o=int (re.sub (r'\D+', '', row [14]) or 0),
                    p=row [15].strip (),
                    q=row [16].strip (),
                    r=int (re.sub (r'\D+', '', row [17]) or 0),
                    updated=True,
                    row_num=counter
                )
        except Exception as ex:
            log_error(ex)


# обновляет таблицу по команде
async def update_google_table(user_id: int) -> None:
    sh = ug.get_google_connect()

    # основные параметры
    # new_orders = sh.get_worksheet(1).get_all_values()
    new_orders = sh.worksheet(SheetsPage.EDIT.value).get_all_values ()

    last_row = await db.get_max_row_num()
    new_row = last_row + 1 if last_row else 5

    opr_dict = await ug.get_company_dict (UserRole.OPR.value)
    dlv_dict = await ug.get_company_dict (UserRole.DLV.value)

    ug.clear_new_order_table(sh, len(new_orders))
    exception_list = []

    for row in new_orders[1:]:
        if row[13].strip() != '':
            if row[0].isdigit():
                try:
                    # print(row)
                    order_id = int (row [0])
                    order_user_name = row [5].strip () if row [5] else None
                    order_status = order_status_data.get (row [6].strip ())
                    comp_opr = ug.check_comp_name (row [10].strip (), comp_dict=opr_dict)
                    comp_dlv = ug.check_comp_name (order_user_name, comp_dict=dlv_dict)

                    await db.update_row_google(
                        order_id=order_id,
                        all_row=True,
                        type_update=TypeOrderUpdate.UPDATE_ROW.value,
                        b=row[1].strip() if row[1] else None,
                        c=row[2].strip() if row[2] else None,
                        d=row[3].strip() if row[3] else None,
                        e=row[4].strip() if row[4] else None,
                        f=order_user_name,
                        g=order_status,
                        h=row[7].strip() if row[7] else None,
                        i=row[8].strip() if row[8] else None,
                        j=row[9].strip() if row[9] else None,
                        k=row[10].strip() if row[10] else None,
                        l=row[11].strip() if row[11] else None,
                        m=row[12].strip() if row[12] else None,
                        n=row[13].strip() if row[13] else None,
                        o=row[14].strip() if row[14] else '',
                        p=row[15].strip() if row[15] else None,
                        q=int (re.sub (r'\D+', '', row [16]) or 0),
                        r=int (re.sub (r'\D+', '', row [17]) or 0),
                        s=int (re.sub (r'\D+', '', row [18]) or 0),
                        t=int (re.sub (r'\D+', '', row [19]) or 0),
                        u=int (re.sub (r'\D+', '', row [20]) or 0),
                        v=int (re.sub (r'\D+', '', row [21]) or 0),
                        w=row[22].strip() if row[22] else None,
                        x=row[23].strip() if row[23] else None,
                        y=int(row[24]) if row[24] else 0,
                        z=row[25].strip() if row[25] else None,
                        aa=row[26].strip() if row[26] else None,
                        ab=row[27].strip() if row[27] else None,
                        ac=comp_dlv,
                        ad=row[29].strip() if row[29] else None,
                        ae=row[30].strip() if row[30] else None,
                        af=row[31].strip() if row[31] else None,
                        ag=row[32].strip() if row[32] else None,
                        ah=row[33].strip() if row[33] else None,
                        comp_opr=comp_opr
                    )
                except Exception as ex:
                    exception_list.append(row[:24])
                    log_error (ex)
                    text = f'Не удалось обновить заказ ID {row[0]}'
                    await bot.send_message(user_id, text, disable_notification=True)

            else:
                try:
                    comp_opr = ug.check_comp_name (row [10].strip (), comp_dict=opr_dict)
                    await db.add_row(
                        row_num=new_row,
                        b=row[1].strip() if row[1] else None,
                        c=row[2].strip() if row[2] else None,
                        d=row[3].strip() if row[3] else None,
                        e=row[4].strip() if row[4] else None,
                        f=row[5].strip() if row[5] else None,
                        g=order_status_data.get (row [6].strip ()),
                        h=row[7].strip() if row[7] else None,
                        i=row[8].strip() if row[8] else None,
                        j=row[9].strip() if row[9] else None,
                        k=row[10].strip() if row[10] else None,
                        l=row[11].strip() if row[11] else None,
                        m=row[12].strip() if row[12] else None,
                        n=row[13].strip() if row[13] else None,
                        o=row[14].strip() if row[14] else '',
                        p=row[15].strip() if row[15] else None,
                        q=int (re.sub (r'\D+', '', row [16]) or 0),
                        r=int (re.sub (r'\D+', '', row [17]) or 0),
                        s=int (re.sub (r'\D+', '', row [18]) or 0),
                        t=int (re.sub (r'\D+', '', row [19]) or 0),
                        u=int (re.sub (r'\D+', '', row [20]) or 0),
                        v=int (re.sub (r'\D+', '', row [21]) or 0),
                        w=row[22].strip() if row[22] else None,
                        x=row[23].strip() if row[23] else None,
                        y=int (re.sub (r'\D+', '', row [24]) or 0),
                        z=row[25].strip() if row[25] else None,
                        aa=row[26].strip() if row[26] else None,
                        ab=row[27].strip() if row[27] else None,
                        ac=row[28].strip() if row[28] else None,
                        ad=row[29].strip() if row[29] else None,
                        ae=row[30].strip() if row[30] else None,
                        af=row[31].strip() if row[31] else None,
                        ag=row[32].strip() if row[32] else None,
                        ah=row[33].strip() if row[33] else None,
                        type_update=TypeOrderUpdate.ADD.value,
                        comp_opr=comp_opr
                    )
                    new_row += 1

                except Exception as ex:
                    exception_list.append (row)
                    log_error(ex)
                    text = f'Не удалось добавить заказ {row.n} {row.m}'
                    await bot.send_message (user_id, text, disable_notification=True)

    if exception_list:
        try:
            cell = f'a2:ah{len(exception_list) + 1}'
            # sh.get_worksheet(1).update(cell, exception_list)
            sh.worksheet(SheetsPage.EDIT.value).update(cell, exception_list)

        except Exception as ex:
            log_error(message=f'Ошибка при возвращении ошибок таблицы: {ex}\n\n'
                              f'{exception_list}', with_traceback=False)
    # print (datetime.now () - time_start)


# добавляет одно последнее изменение в таблицу
async def update_google_row() -> None:
    order = await db.get_order(for_update=True)

    if order:
        sh = ug.get_google_connect()
        # изменяет статус заказа
        try:
            # print(order)
            cell = f'A{order.row_num}:Z{order.row_num}'
            new_row_str = [
                [
                    str(order.id) if order.id else '', str(order.b) if order.b else '',
                    str(order.c) if order.c else '', str(order.d) if order.d else '',
                    str(order.e) if order.e else '', str(order.f) if order.f else '-',
                    order_status_data.get (order.g), str(order.h) if order.h else '',
                    str(order.i).lower() if order.i else '', str(order.j).lower() if order.j else '',
                    str(order.k).lower() if order.k else '', str(order.l).lower() if order.l else '',
                    str(order.m).lower() if order.m else '', str(order.n).lower() if order.n else '',
                    str(order.o).lower() if order.o else '', str(order.p).lower() if order.p else '',
                    str (order.q).lower() if order.q else '0', str (order.r).lower() if order.r else '',
                    str (order.s).lower() if order.s else '', str (order.clmn_t).lower() if order.clmn_t else '0',
                    str (order.u).lower() if order.u else '', str (order.v).lower() if order.v else '',
                    str(order.w).lower() if order.w else '', str(order.x).lower() if order.x else '',
                    str(order.y).lower() if order.y else '', str(order.z).lower() if order.z else ''
                ]
            ]
            # sh.sheet1.update (cell, new_row_str)
            sh.worksheet(SheetsPage.BASE.value).update (cell, new_row_str)
            ab = order.ab if order.ab else ''
            # sh.sheet1.update(f'AB{order.row_num}', [[ab]])
            sh.worksheet(SheetsPage.BASE.value).update(f'AB{order.row_num}', [[ab]])
            if order.type_update == TypeOrderUpdate.STATE.value:
                color = ug.choice_color(order.g)
                cell_form = f'E{order.row_num}:G{order.row_num}'
                # sh.sheet1.format(cell_form, {"backgroundColor": color})
                sh.worksheet(SheetsPage.BASE.value).format(cell_form, {"backgroundColor": color})

            # изменяет стоимость заказа
            elif order.type_update == TypeOrderUpdate.EDIT_COST.value:
                color = {"red": 1.0, "green": 0.0, "blue": 0.0}
                # sh.sheet1.update(f'AB{order.row_num}', [[order.ab]])
                # sh.sheet1.format(f'AB{order.row_num}', {"backgroundColor": color})
                sh.worksheet(SheetsPage.BASE.value).format(f'AB{order.row_num}', {"backgroundColor": color})

            # изменяет стоимость доставки
            elif order.type_update == TypeOrderUpdate.EDIT_COST_DELIVERY.value:
                color = {"red": 2.0, "green": 0.0, "blue": 0.0}
                # sh.sheet1.update(f'AB{order.row_num}', [[order.ab]])
                # sh.sheet1.format(f'AB{order.row_num}', {"backgroundColor": color})
                sh.worksheet(SheetsPage.BASE.value).format(f'AB{order.row_num}', {"backgroundColor": color})

            elif order.type_update == TypeOrderUpdate.ADD_OPR.value:
                col = {"red": 0.0, "green": 1.0, "blue": 1.0}
                # sh.sheet1.update (f'AB{order.row_num}', [[order.ab]])
                cell = f'J{order.row_num}:Z{order.row_num}'
                # sh.sheet1.format (cell, {"backgroundColor": col})
                sh.worksheet(SheetsPage.BASE.value).format (cell, {"backgroundColor": col})

                color = ug.choice_color(order.g)
                cell_form = f'E{order.row_num}:G{order.row_num}'
                # sh.sheet1.format(cell_form, {"backgroundColor": color})
                sh.worksheet(SheetsPage.BASE.value).format(cell_form, {"backgroundColor": color})

            # elif order.type_update == TypeOrderUpdate.UPDATE_ROW.value:
            #     sh.sheet1.update(f'AB{order.row_num}', [[order.ab]])

            await db.update_row_google(order_id=order.id, update_row=True)

        except Exception as ex:
            log_error(f'Заказ не добавлен из таблицы темп ошибка:\n{order}', with_traceback=False)
            log_error(ex)

    else:
        # записывает данные в отчёт курьера
        # async def insert_google_expenses():
        new_row = await db.get_last_updated_report()
        if new_row:
            sh = ug.get_google_connect()
            try:
                cell = f"B{new_row.row_num}:R{new_row.row_num}"
                l_str = '\n'.join(new_row.l)
                new_row_str = [
                    [
                        str(new_row.b) if new_row.b else '',
                        str(new_row.c) if new_row.c else '', str(new_row.d) if new_row.d else '',
                        str(new_row.e) if new_row.e else '', str(new_row.f) if new_row.f else '',
                        str(new_row.g) if new_row.g else '', str(new_row.h) if new_row.h else '',
                        str(new_row.i) if new_row.i else '', str(new_row.j) if new_row.j else '',
                        str(new_row.clmn_k) if new_row.clmn_k else '', l_str,
                        str(new_row.m) if new_row.m else '', str(new_row.n) if new_row.n else '',
                        str(new_row.o) if new_row.o else '', str(new_row.p) if new_row.p else '',
                        str(new_row.q) if new_row.q else '', str(new_row.r) if new_row.r else ''
                    ]
                ]

                # sh.get_worksheet(Config.report_sheet_num).update(cell, new_row_str)
                sh.worksheet(SheetsPage.REPORT.value).update(cell, new_row_str)
                await db.update_expenses_dlv(entry_id=new_row.id, updated=True)
            except Exception as ex:
                log_error(f'Не получилось обновить отчёт {new_row.m} {new_row.n}', with_traceback=False)
                log_error(ex)


# async def update_report_table():
#     sh = ug.get_google_connect()
#     table = sh.get_worksheet(Config.report_sheet_num).get_all_values()
#     counter = 4
#     for row in table[5:]:
#         counter += 1
#         if row[13]:
#             l_list = row[11].split('\n')
#             await db.add_report_row(
#                 b=int (re.sub (r'\D+', '', row [1]) or 0),
#                 c=int (re.sub (r'\D+', '', row [2]) or 0),
#                 d=int (re.sub (r'\D+', '', row [3]) or 0),
#                 e=int (re.sub (r'\D+', '', row [4]) or 0),
#                 f=int (re.sub (r'\D+', '', row [5]) or 0),
#                 g=int (re.sub (r'\D+', '', row [6]) or 0),
#                 h=int (re.sub (r'\D+', '', row [7]) or 0),
#                 i=int (re.sub (r'\D+', '', row [8]) or 0),
#                 j=int (re.sub (r'\D+', '', row [9]) or 0),
#                 k=int (re.sub (r'\D+', '', row [10]) or 0),
#                 l=l_list,
#                 m=row[12].strip(),
#                 n=row[13].strip(),
#                 o=int (re.sub (r'\D+', '', row [14]) or 0),
#                 p=row[15].strip(),
#                 q=row[16].strip(),
#                 r=int (re.sub (r'\D+', '', row [17]) or 0),
#                 updated=True,
#                 row_num=counter
#             )


# добавляет курьеров и компании в таблицу
# async def add_users_table():
#     dlv_table = await db.get_users(role=UserRole.DLV.value)
#
#     sh = ug.get_google_connect()
#     table = []
#     for user in dlv_table:
#         table.append([user.user_id, user.name, user.company, company_dlv.get(user.company)])
#
#     sh.get_worksheet(7).update(f'a3:d{len(table) + 3}', table)
#
#     table = []
#     for k, v in company_dlv.items():
#         table.append([k, v])
#
#     sh.get_worksheet(7).update(f'f3:g{len(table) + 3}', table)


# обновляет данные по курьерам
# def update_users_table():
#     sh = ug.get_google_connect()
#     all_table = sh.get_worksheet(7).get_all_values()
#
#     result = db.get_all_users_id()
#     list_exception = [user_id[0] for user_id in result]
#
#     for row in all_table[2:]:
#         if row[0] in list_exception:
#             db.update_user_data(row)
#
#         elif row[0] is not None or row[0] != '':
#             db.add_user_data(row)
#
#     result = db.get_all_comp_id()
#     list_exception = [comp_id[0] for comp_id in result]
#
#     for row in all_table[2:]:
#         try:
#             if int(row[5]) in list_exception:
#                 db.update_comp_dlv(row)
#
#         except Exception as ex:
#             logging.warning(f'update_users_table 495:\n{ex}')
