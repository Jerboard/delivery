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
from enums import OperatorCB, CompanyOPR, TypeOrderUpdate, OrderStatus


# основное меню оператора
async def get_profile_opr(user_id: int, user_info: db.UserRow = None, msg_id: int = None):
    if not user_info:
        user_info = await db.get_user_info (user_id)

    orders = await db.get_orders_statistic (opr_name=user_info.name, own_text=True)
    # orders = await db.get_orders_statistic (opr_name='21', own_text=True)
    statistic_text = txt.get_statistic_text (orders)
    text = f'{user_info.name}\n\n{statistic_text}'

    if msg_id:
        await bot.edit_message_text (text, reply_markup=kb.get_main_opr_kb (), chat_id=user_id, message_id=msg_id)
    else:
        await bot.send_message (user_id, text, reply_markup=kb.get_main_opr_kb ())


# назад к профилю оператора
@dp.callback_query(lambda cb: cb.data.startswith(OperatorCB.BACK_MAIN.value))
async def back_main(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await get_profile_opr(user_id=cb.from_user.id, msg_id=cb.message.message_id)


# отправляет инфо о заказе
async def send_opr_report_msg(order: db.OrderRow, photo_id: str = None):
    user_info = await db.get_user_info (name=order.k)

    text = txt.get_opr_order_text (order)
    if user_info:
        if photo_id:
            await bot.send_photo(chat_id=user_info.user_id, caption=text, photo=photo_id)
        else:
            await bot.send_message(chat_id=user_info.user_id, text=text)

        if order.g == OrderStatus.SEND:
            await bot.send_message (chat_id=work_chats [f'post_{order.comp_opr}'], text=text)

    else:
        if order.g == OrderStatus.SEND:
            if order.k.isdigit ():
                await bot.send_message (chat_id=work_chats [f'post_{CompanyOPR.VLADA.value}'], text=text)
            else:
                await bot.send_message (chat_id=work_chats [f'post_{CompanyOPR.VERA.value}'], text=text)

