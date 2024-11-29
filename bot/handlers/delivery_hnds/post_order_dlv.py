from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.enums.content_type import ContentType

import asyncio

import db
import keyboards as kb
from config import DEBUG
from init import dp, bot, log_error
from handlers.operator_hnds.base_opr import send_opr_report_msg
from .base_dlv import stop_state
from data.base_data import work_chats
from enums import DeliveryCB, OrderStatus, CompanyDLV, UserActions, DeliveryStatus, TypeOrderUpdate


# запрашивает трек номер
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.POST_1.value))
async def post_1(cb: CallbackQuery, state: FSMContext):
    _, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    await state.set_state(DeliveryStatus.POST_ID)
    sent = await cb.message.answer('Отправьте трек заказа', reply_markup=kb.get_close_kb())
    await state.update_data(data={
        'order_id': order_id,
        'msg_id': cb.message.message_id,
        'sent_id': sent.message_id
    })


# Изменяет заказ на отправлен
@dp.message (StateFilter (DeliveryStatus.POST_ID))
async def post_id(msg: Message, state: FSMContext):
    stop = await stop_state(msg)
    if stop:
        return

    data = await state.get_data ()
    await state.clear ()

    # добавить смену курьерской
    await db.update_row_google(
        order_id=data['order_id'],
        status=OrderStatus.SEND.value,
        type_update=TypeOrderUpdate.STATE.value,
        note=msg.text
    )

    order_info = await db.get_order(data['order_id'])

    await bot.edit_message_reply_markup (chat_id=msg.chat.id, message_id=data['msg_id'], reply_markup=None)
    await msg.answer('✅ Заказ отправлен')

    # отправить трек оператору
    if not DEBUG:
        await send_opr_report_msg(order_info)
    await bot.delete_message(chat_id=msg.chat.id, message_id=data['sent_id'])

    # журнал действий
    await db.save_user_action(
        user_id=msg.from_user.id,
        dlv_name=order_info.f,
        action=UserActions.SEND_POST_ORDER.value,
        comment=f'{data["order_id"]}'
    )


# Заказ доставлен
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.POST_2.value))
async def post_2(cb: CallbackQuery, state: FSMContext):
    _, order_id_str = cb.data.split (':')
    # order_id = int (order_id_str)

    await state.set_state(DeliveryStatus.REFUSE_POST)
    sent = await cb.message.answer('Укажите причину отказа', reply_markup=kb.get_close_kb())
    await state.update_data(data={
        'order_id': int(order_id_str),
        'msg_id': cb.message.message_id,
        'del_msg_id': sent.message_id,
        'text': cb.message.text,
        'entities': cb.message.entities,
    })


# принимает фото отменяет заказ
@dp.message(StateFilter(DeliveryStatus.REFUSE_POST))
async def refuse_post(msg: Message, state: FSMContext):
    stop = await stop_state(msg)
    if stop:
        return

    if msg.content_type != ContentType.TEXT:
        sent = await msg.answer('❗️ Отправьте причину отказа текстом')
        await asyncio.sleep(3)
        await sent.delete()
        return

    await msg.delete()
    data = await state.get_data()
    await state.clear()

    user_info = await db.get_user_info (msg.from_user.id)
    await db.update_row_google(
        order_id=data['order_id'],
        status=OrderStatus.REF.value,
        type_update=TypeOrderUpdate.STATE.value
    )
    await bot.delete_message(chat_id=msg.chat.id, message_id=data['del_msg_id'])
    await bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=data['msg_id'],
        text=f'{data["text"]}\n\n❌ Отказ',
        entities=data["entities"],
        parse_mode=None
    )
    await bot.send_message(
        chat_id=work_chats[f'refuse_{CompanyDLV.POST.value}'],
        text=f'{data["text"]}\n\n❌ Отказ\n\n{msg.text}',
        entities=msg.entities,
        parse_mode=None
    )

    # журнал действий
    await db.save_user_action(
        user_id=msg.from_user.id,
        dlv_name=user_info.name,
        action=UserActions.SEND_POST_ORDER.value,
        comment=str(data['order_id'])
    )

