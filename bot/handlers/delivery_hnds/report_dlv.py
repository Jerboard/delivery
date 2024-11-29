from aiogram.types import Message, CallbackQuery

from datetime import datetime

import db
import keyboards as kb
from init import dp, bot, log_error
from config import Config
from utils.base_utils import get_order_cost, send_long_msg, get_today_date_str
from utils.text_utils import get_short_order_row
from utils import local_data_utils as ld
from data import base_data as dt
from enums import (DeliveryCB, OrderStatus, UserActions, ShortText, Letter, active_status_list, done_status_list,
                   KeyWords, CompanyDLV, Action)


# отчёт по дням
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.REPORT_1.value))
async def report_dvl_1(cb: CallbackQuery):
    user_info = await db.get_user_info(user_id=cb.from_user.id)
    date_str = datetime.now().date ().strftime (Config.day_form)
    dlv_reports = await db.get_reports_all_dlv(dlv_name=user_info.name, exception_date=date_str)

    await cb.message.edit_reply_markup(reply_markup=kb.report_view_days_kb(dlv_reports))


# 6600572025 - мияги, 5766385456 - Ян, 5051573626 - Мел, 1970050747 - Николь, 5378481086 - Ярик
# отчёт за день
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.REPORT_2.value))
async def report_dvl_2(cb: CallbackQuery):
    _, date_str = cb.data.split(':')

    user_info = await db.get_user_info (user_id=cb.from_user.id)
    # user_info = await db.get_user_info (user_id=5378481086)
    if date_str == 'today':
        # date_str = datetime.now().date().strftime(Config.day_form)
        date_str = get_today_date_str()

    dlv_orders = await db.get_orders(user_id=user_info.user_id, on_date=date_str)

    dlv_report = await db.get_report_dlv(dlv_name=user_info.name, exp_date=date_str)

    suc_text, refuse_text, active_text, not_come, send_text = '', '', '', '', ''
    cost_prod, cost_dlv = 0, 0
    salary = {Letter.D.value: 0, Letter.V.value: 0, Letter.A.value: 0}

    for order in dlv_orders:
        # print(order)
        row_text = get_short_order_row(order=order, for_=ShortText.REPORT.value)

        if order.g in done_status_list:
            cost_prod += get_order_cost(order, with_t=True)
            suc_text += row_text
            if order.d:
                summary = salary.get(order.d, 0)
                salary[order.d] = summary + 1

        elif order.g == OrderStatus.REF.value:
            refuse_text += row_text

        elif order.d == KeyWords.NOT_COME.value:
            not_come += row_text

        elif order.g in active_status_list:
            if order.g == OrderStatus.SEND.value:
                send_text += row_text
            else:
                active_text += row_text

    if dlv_report:
        # print(dlv_report.b, dlv_report.c, dlv_report.d, dlv_report.e, dlv_report.f, dlv_report.g, dlv_report.h, dlv_report.i, dlv_report.j, dlv_report.k)
        total_expenses = (dlv_report.b + dlv_report.c + dlv_report.d + dlv_report.e + dlv_report.f + dlv_report.g +
                          dlv_report.h + dlv_report.i + dlv_report.j + dlv_report.clmn_k)
    else:
        total_expenses = 0

    salary_str = ''
    for k, v in salary.items():
        if v:
            salary_str += f'{dt.letters.get(k)} - {v}\n'

    if user_info.company == CompanyDLV.POST:
        not_come = send_text

    # print(total_expenses)
    total = cost_prod - total_expenses
    expenses = '\n'.join(dlv_report.l) if dlv_report else ''

    spt = '\n---------------------------\n'
    text = (f'{user_info.name}\n\n'
            f'{date_str}\n'
            f'{salary_str}\n'
            f'{suc_text}{spt}'
            f'{refuse_text}{spt}'
            f'{active_text}{spt}'
            f'{not_come}{spt}'
            f'Касса: {cost_prod}\n\n'
            f'{expenses}\n\n'
            f'Итог: {total}')

    if len(text) < 4096:
        await cb.message.answer(text, reply_markup=kb.get_send_day_report_kb())
    else:
        await send_long_msg(chat_id=user_info.user_id, text=text, keyboard=kb.get_send_day_report_kb())

    # await db.save_user_action(user_id=cb.from_user.id, dlv_name=user_info.name, action=UserActions.VIEW_REPORT.value)


# подтверждение отчёта
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.REPORT_3.value))
async def report_dvl_3(cb: CallbackQuery):
    text = f'‼️Перед отправкой отчёта проверьте траты'

    await cb.message.edit_reply_markup(reply_markup=kb.get_day_report_kb())
    await cb.answer(text, show_alert=True)


# Отчёт за день. Отправляет в группу
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.REPORT_4.value))
async def report_dvl_4(cb: CallbackQuery):
    user_info = await db.get_user_info(user_id=cb.from_user.id)

    if user_info.company == CompanyDLV.POST:
        orders = await db.get_post_orders(user_id=cb.from_user.id, only_suc=True)
        suc_orders = [order.id for order in orders]
        await db.mark_del_orders(suc_orders)

    await bot.send_message(dt.work_chats[f'report_{user_info.company}'], cb.message.text)
    await cb.message.edit_text(f'{cb.message.text}\n\n✅ Отчёт отправлен')

    await db.save_user_action (user_id=cb.from_user.id, dlv_name=user_info.name, action=UserActions.SEND_REPORT.value)
