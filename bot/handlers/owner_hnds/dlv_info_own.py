from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from datetime import datetime
from asyncio import sleep

import db
import keyboards as kb
from init import dp, bot, log_error
from utils import text_utils as txt
from utils.base_utils import get_today_date_str
from enums import OwnerCB, ShortText, OwnerStatus, OrderStatus, OrderAction, TypeOrderUpdate


# показывает список курьеров и количество заказов на руках
@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.VIEW_ORDERS_1.value))
async def view_orders_1(cb: CallbackQuery):
    # users = await db.get_users_group()
    # users = await db.get_orders_statistic (only_active=True)
    users = await db.get_users_orders_count ()
    await cb.message.edit_reply_markup (reply_markup=kb.get_orders_users_own_kb (users))


# показывает заказы курьера
@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.VIEW_ORDERS_2.value))
async def view_orders_2(cb: CallbackQuery):
    _, dlv_name = cb.data.split (':')
    # user_id = int(user_id_str)

    # orders = await db.get_work_orders (user_id=user_id, only_active=True)
    orders = await db.get_orders (dlv_name=dlv_name, get_active=True)

    await cb.message.answer (f'{orders[0].f}:')

    for order in orders:
        text = txt.get_short_order_row(order, for_=ShortText.ACTIVE.value)
        await cb.message.answer (text)


# предлагает список пустующих заказов если заказов больше 20 предлагает их по дням
@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.VIEW_FREE_ORDERS.value))
async def view_free_orders(cb: CallbackQuery, state: FSMContext):
    _, start_str = cb.data.split(':')
    start = int(start_str)
    free_orders = await db.get_orders(order_status=OrderStatus.NEW.value)

    if len(free_orders) < 20:
        await cb.message.answer('Страница 1/1')
        for order in free_orders:
            text = txt.get_short_order_row (order, for_=ShortText.FREE.value)
            await cb.message.answer (text, reply_markup=kb.get_free_order_own_kb (order_id=order.id))

    else:
        batch_size = 20
        counter = 0
        fin = start + batch_size
        num_page = (start // batch_size) + 1
        all_page = (len(free_orders) // batch_size) + 1
        len_pg = len(free_orders[start:fin])

        await state.set_state(OwnerStatus.VIEW_FREE_ORDERS)
        data = await state.get_data()
        old_messages = data.get('old_messages', [])
        title_message = data.get('title_message', 0)
        last_edit_message = len(old_messages)

        title_text = f'Страница {num_page}/{all_page}'
        if title_message:
            await bot.edit_message_text(chat_id=cb.message.chat.id, message_id=title_message, text=title_text)
        else:
            sent = await cb.message.answer (title_text)
            title_message = sent.message_id

        for order in free_orders[start:fin]:
            text = txt.get_short_order_row (order, for_=ShortText.FREE.value)

            if counter == batch_size - 1 or counter == len_pg - 1:
                keyboard = kb.get_view_free_order_own_kb(start=start, next_page=batch_size == len_pg, order_id=order.id)
            else:
                keyboard = kb.get_free_order_own_kb (order_id=order.id)

            if last_edit_message > counter:
                await bot.edit_message_text(
                    chat_id=cb.message.chat.id,
                    message_id=old_messages[counter],
                    text=text,
                    reply_markup=keyboard
                )
            else:
                sent = await cb.message.answer(text, reply_markup=keyboard, disable_notification=True)
                old_messages.append(sent.message_id)

            counter += 1

        # print(counter < len_pg)
        if counter < batch_size:
            # print(old_messages[counter:])
            for msg_id in old_messages[counter:]:
                await bot.delete_message(chat_id=cb.message.chat.id, message_id=msg_id)
                old_messages.remove(msg_id)

        await state.update_data(data={'old_messages': old_messages, 'title_message': title_message})
