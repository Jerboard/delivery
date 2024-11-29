from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.enums.content_type import ContentType

from datetime import datetime
from asyncio import sleep

import db
import keyboards as kb
from init import dp, bot, log_error
from config import Config
from handlers.delivery_hnds.base_dlv import done_order, stop_state
from handlers.operator_hnds.base_opr import send_opr_report_msg
from data.base_data import work_chats
from utils import local_data_utils as dt
from utils.text_utils import get_dlv_refuse_text
from data.base_data import order_status_data, order_actions
from enums import DeliveryCB, OrderStatus, DataKey, UserActions, DeliveryStatus, OrderAction, TypeOrderUpdate


# Подтвердить отмену заказа
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.REF_ORDER_1.value))
async def ref_order_1(cb: CallbackQuery):
    _, order_id_str = cb.data.split(':')
    order_id = int(order_id_str)

    await cb.answer ('Нажмите кнопку "Подтвердить отказ", после этого заказ будет закрыт', show_alert=True)
    await cb.message.edit_reply_markup (
        reply_markup=kb.get_close_order_kb (order_id=order_id))


# Подтвердить отмену заказа. Запрос фото
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.REF_ORDER_2.value))
async def ref_order_2(cb: CallbackQuery, state: FSMContext):
    _, order_id_str = cb.data.split(':')
    order_id = int(order_id_str)

    await state.set_state(DeliveryStatus.REFUSE)
    await state.update_data(data={
        'order_id': order_id,
        'msg_id': cb.message.message_id,
        'msg_text': cb.message.text,
        'msg_entities': cb.message.entities,
        'step': 'photo'
    })
    await cb.message.answer('Приложите фото отказного заказа', reply_markup=kb.get_close_kb())


#  принимает фото просит коммент
@dp.message(StateFilter(DeliveryStatus.REFUSE))
async def ref_order_3(msg: Message, state: FSMContext):
    stop = await stop_state(msg)
    if stop:
        return

    data = await state.get_data()
    if data['step'] == 'photo':
        if msg.content_type == ContentType.PHOTO:
            await state.update_data (data={'photo_id': msg.photo[-1].file_id})
            await msg.answer ('Укажите причину отказа', reply_markup=kb.get_close_kb ())
            await state.update_data(data={'step': 'text'})
        else:
            sent = await msg.answer('❗️ Приложите фото отказного заказа')
            await sleep(3)
            await sent.delete()

    elif msg.content_type == ContentType.TEXT:
        # data = await state.get_data()
        await state.clear()

        await db.update_row_google (
            order_id=data['order_id'],
            status=OrderStatus.REF.value,
            note=msg.text,
            type_update=TypeOrderUpdate.STATE.value
        )
        # Отметил сообщение отказом
        await bot.edit_message_text(
            chat_id=msg.chat.id,
            message_id=data['msg_id'],
            text=f'{data["msg_text"]}\n\n✖️Отказ',
            entities=data['msg_entities'],
            parse_mode=None
        )
        await msg.answer('✖️ Заказ отменён')
        # отправить в чат отказов
        user_info = await db.get_user_info(user_id=msg.from_user.id)
        order_info = await db.get_order(data['order_id'])
        await bot.send_photo(
            chat_id=work_chats[f'refuse_{user_info.company}'],
            photo=data.get('photo_id'),
            caption=get_dlv_refuse_text(order=order_info, note=msg.text)
        )
        # отправить фото оператору
        await send_opr_report_msg (order_info, photo_id=data.get('photo_id'))

        # журнал действий
        await db.save_user_action (
            user_id=msg.from_user.id,
            dlv_name=order_info.f,
            action=UserActions.REFUSE_ORDER.value,
            comment=f'ID: {data["order_id"]} ROW: {order_info.row_num}')

    else:
        sent = await msg.answer('❗️ Некорректный формат сообщения')
        await sleep(3)
        await sent.delete()


#  принимает фото частичного отказа и закрывает заказ
@dp.message(StateFilter(DeliveryStatus.REFUSE_PART))
async def ref_order_3(msg: Message, state: FSMContext):
    if msg.content_type != ContentType.PHOTO:
        sent = await msg.answer('❗️ Приложите фото отказного заказа')
        await sleep(3)
        await sent.delete()

    else:
        data = await state.get_data()
        await state.clear()

        user_info = await db.get_user_info (user_id=msg.from_user.id)
        order_info = await db.get_order (data ['order_id'])

        old_note = order_info.ab or ''
        note = f'{old_note}\nЧастичный отказ'.strip()

        await bot.send_photo (
            chat_id=work_chats [f'refuse_{user_info.company}'],
            photo=msg.photo[-1].file_id,
            caption=get_dlv_refuse_text (order=order_info, note=msg.text)
        )

        await done_order (user_id=msg.from_user.id, order_id=data['order_id'], lit=data['lit'], node=note)
        await bot.edit_message_reply_markup (chat_id=msg.chat.id, message_id=data ['msg_id'], reply_markup=None)
