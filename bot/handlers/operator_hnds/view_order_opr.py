from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime

import db
import keyboards as kb
from init import dp, bot, log_error
from config import Config
from utils import text_utils as txt
from utils.base_utils import get_today_date_str
from data.base_data import company_dlv, order_status_data, work_chats
from enums import OperatorCB, active_status_list, done_status_list, ref_status_list, OrderStatus


# выбор даты заказа
@dp.callback_query(lambda cb: cb.data.startswith(OperatorCB.VIEW_ORDER_1.value))
async def take_order_1(cb: CallbackQuery, state: FSMContext):
    _, order_status = cb.data.split (':')

    user_info = await db.get_user_info(user_id=cb.from_user.id)
    # user_info = await db.get_user_info(name='21')
    if order_status in active_status_list[:-1]:
        report_days = await db.get_opr_report_days(opr_name=user_info.name, get_active=True)
    elif order_status in done_status_list:
        report_days = await db.get_opr_report_days(opr_name=user_info.name, get_done=True)
    elif order_status in ref_status_list:
        report_days = await db.get_opr_report_days (opr_name=user_info.name, get_ref=True)
    else:
        report_days = await db.get_opr_report_days(opr_name=user_info.name, order_status=order_status)

    await cb.message.edit_reply_markup(reply_markup=kb.get_opr_day_report_kb(report_days, order_status))


# отчёт
@dp.callback_query(lambda cb: cb.data.startswith(OperatorCB.VIEW_ORDER_2.value))
async def take_order_2(cb: CallbackQuery, state: FSMContext):
    _, order_status, date_str = cb.data.split (':')

    user_info = await db.get_user_info (user_id=cb.from_user.id)
    # user_info = await db.get_user_info(name='21')
    if order_status == OrderStatus.NEW:
        orders = await db.get_orders(opr_name=user_info.name, order_status=order_status)
    elif order_status in active_status_list[:-1]:
        orders = await db.get_orders (opr_name=user_info.name, on_date=date_str, get_active=True)
    elif order_status in done_status_list:
        orders = await db.get_orders (opr_name=user_info.name, on_date=date_str, get_done=True)
    elif order_status in ref_status_list:
        orders = await db.get_orders (opr_name=user_info.name, on_date=date_str, get_ref=True)
    else:
        orders = await db.get_orders(opr_name=user_info.name, on_date=date_str, order_status=order_status)

    text = ''
    counter = 0
    for order in orders:
        counter += 1
        text += f'{txt.get_opr_report_text(order)}\n\n'
        if counter % 10 == 0 or counter == len(orders):
            await cb.message.answer(text)
            text = ''
