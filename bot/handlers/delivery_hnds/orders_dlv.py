from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from datetime import datetime
from asyncio import sleep

import db
import keyboards as kb
from init import dp, bot, log_error
from config import Config, DEBUG
from handlers.delivery_hnds.base_dlv import done_order, stop_state
from utils import local_data_utils as dt
from utils.base_utils import get_today_date_str
from utils import text_utils as txt
from data.base_data import order_status_data, order_actions
from enums import (DeliveryCB, OrderStatus, DataKey, UserActions, DeliveryStatus, OrderAction, TypeOrderUpdate,
                   TypeOrderButton, KeyWords, CompanyDLV, Action)


# кнопка взять заказ
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.ORDER_1.value))
async def dlv_order_1(cb: CallbackQuery, state: FSMContext):
    _, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    user_info = await db.get_user_info(user_id=cb.from_user.id)

    # добавить смену курьерской
    await db.update_row_google(
        order_id=order_id,
        dlv_name=user_info.name,
        status=OrderStatus.ACTIVE.value,
        take_date=get_today_date_str(),
        type_update=TypeOrderUpdate.STATE.value,
        company=user_info.company
    )
    order_info = await db.get_order(order_id=order_id)

    if user_info.company == CompanyDLV.POST:
        await db.add_post_order(user_id=cb.from_user.id, order_id=order_id)
        keyboard = kb.get_post_order_kb(order_id=order_id, order_status=OrderStatus.ACTIVE.value)
    else:
        keyboard = kb.get_dlv_main_order_kb (order_id=order_id, order_status=order_info.g)

    text = txt.get_order_text (order_info)
    await cb.message.edit_text(
        text=f'{text}\n\n✅ Принят',
        reply_markup=keyboard
    )

    # журнал действий
    await db.save_user_action(
        user_id=cb.from_user.id,
        dlv_name=user_info.name,
        action=UserActions.TAKE_ORDER.value,
        comment=f'{order_id}'
    )


# взять заказ на забор
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.TAKE_ORDER_2.value))
async def dlv_order_2(cb: CallbackQuery, state: FSMContext):
    _, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    order = await db.get_order(order_id)
    if not order:
        await cb.message.answer('❗️ОШИБКА. Что-то пошло не так - обратитесь к оператору')

    elif order.g != OrderStatus.NEW.value:
        await cb.message.answer ('❗️ОШИБКА. Заказ уже взял другой курьер')

    else:
        user_info = await db.get_user_info (cb.from_user.id)

        await db.update_row_google (
            order_id=order_id,
            dlv_name=user_info.name,
            status=OrderStatus.ACTIVE_TAKE.value,
            take_date=get_today_date_str(),
            company=user_info.company
        )

        key = f'{DataKey.ADD_OPR_ORDER.value}-{order_id}'
        data_order = dt.get_opr_msg_data(key)
        dt.del_opr_msg_data(key)

        for msg in data_order['sent_list']:
            try:
                await bot.delete_message(chat_id=msg['user_id'], message_id=msg['message_id'])
            except Exception as ex:
                log_error(ex)

        opr_info = await db.get_user_info(name=order.k)

        try:
            await cb.message.edit_text(
                text=f'{cb.message.text}\n\n✅ Принят',
                entities=cb.message.entities,
                parse_mode=None,
                reply_markup=kb.get_dlv_main_order_kb (order_id=order_id, order_status=OrderStatus.ACTIVE_TAKE.value)
            )
        except Exception as ex:
            log_error(ex)

        text = f'✅Заказ принят. {user_info.name}\n\n{cb.message.text}'
        await bot.send_message(opr_info.user_id, text)
        # журнал действий
        await db.save_user_action(
            user_id=cb.from_user.id,
            dlv_name=user_info.name,
            action=UserActions.TAKE_ORDER_TAKE.value,
            comment=str(order_id))


# Подтвердить доставку либо отмену заказа
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.ORDER_2.value))
async def dlv_order_2(cb: CallbackQuery, state: FSMContext):
    _, order_id_str, order_action = cb.data.split(':')
    order_id = int(order_id_str)

    if order_action == OrderAction.REF.value:
        await state.set_state(DeliveryStatus.REFUSE_PART)

    await cb.message.edit_reply_markup(reply_markup=kb.get_close_order_option_kb(order_id=order_id))


# закрытие заказа буквы
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.ORDER_7.value))
async def dlv_order_7(cb: CallbackQuery, state: FSMContext):
    _, order_id_str, action = cb.data.split (':')
    order_id = int (order_id_str)

    await cb.message.edit_reply_markup(
        reply_markup=kb.get_done_order_letters_kb(order_id=order_id, order_action=action)
    )


# закрытие заказа
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.ORDER_4.value))
async def dlv_order_4(cb: CallbackQuery, state: FSMContext):
    _, order_id_str, order_action, lit = cb.data.split (':')
    order_id = int (order_id_str)

    current_state = await state.get_state()

    if order_action == OrderAction.NOT_COME.value:
        await db.update_row_google (
            order_id=order_id,
            letter=KeyWords.NOT_COME.value,
            type_update=TypeOrderUpdate.STATE.value
        )
        order_info = await db.get_order (order_id)
        text = txt.get_order_text(order_info)
        await cb.message.edit_text (text=text)

    elif current_state == DeliveryStatus.REFUSE_PART:
        await state.update_data(data={
            'lit': lit,
            'msg_id': cb.message.message_id,
            'order_id': order_id
        })
        await cb.message.answer('Приложите фото отказного заказа', reply_markup=kb.get_close_kb())

    else:
        await done_order(user_id=cb.from_user.id, order_id=order_id, lit=lit, msg_id=cb.message.message_id)


# Закрытие заказа с изменениями. Запрос суммы изменений
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.ORDER_6.value))
async def edit_order_close_0(cb: CallbackQuery, state: FSMContext):
    _, action, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    current_state = await state.get_state ()
    await state.set_state(DeliveryStatus.EDIT_ORDER_CLOSE_1)

    if action == OrderAction.COST.value:
        text = '📝 Введите сумму скидки'
    else:
        text = '📝 Введите фактическую стоимость доставки'

    sent = await cb.message.answer(text)
    await cb.message.edit_reply_markup(text, reply_markup=kb.get_back_close_order_kb(order_id))
    await state.update_data (data={
        'order_id': order_id,
        'action': action,
        'messages': [sent.message_id],
        'old_state': current_state
    })


# Закрытие заказа с изменениями. Запрос причины изменений
@dp.message(StateFilter(DeliveryStatus.EDIT_ORDER_CLOSE_1))
async def edit_order_close_1(msg: Message, state: FSMContext):
    stop = await stop_state(msg)
    if stop:
        return

    if msg.text.isdigit():
        data = await state.get_data()

        if data['action'] == OrderAction.COST.value:
            await state.update_data(data={'discount': int(msg.text)})
        else:
            await state.update_data(data={'cost_dlv': int(msg.text)})

        await state.set_state(DeliveryStatus.EDIT_ORDER_CLOSE_2)

        sent = await msg.answer('Причина изменения стоимости')
        messages: list = data.get('messages', [])
        messages.append(msg.message_id)
        messages.append(sent.message_id)
        await state.update_data (data={'messages': messages})

    else:
        sent = await msg.answer('‼️Отправьте целое число')
        await sleep(3)
        await sent.delete()


# Закрытие заказа с изменениями. Закрытие
@dp.message(StateFilter(DeliveryStatus.EDIT_ORDER_CLOSE_2))
async def edit_order_close_2(msg: Message, state: FSMContext):
    stop = await stop_state(msg)
    if stop:
        return

    data = await state.get_data()
    await state.clear()

    if data.get('old_state') == DeliveryStatus.REFUSE_PART:
        await state.set_state (DeliveryStatus.REFUSE_PART)

    order_info = await db.get_order(order_id=data['order_id'])

    old_note = order_info.ab or ''
    amount = data.get('discount') or data.get('cost_dlv')
    note = f'{old_note}\n{order_actions.get(data["action"])} ({amount}) {msg.text}'.strip()
    if data ['action'] == OrderAction.COST.value:
        await db.update_row_google (
            order_id=data ['order_id'],
            type_update=data ['action'],
            discount=data ['discount'],
            note=note
        )
        user_action = UserActions.ADD_DISCOUNT.value
    else:
        await db.update_row_google (
            order_id=data ['order_id'],
            type_update=data ['action'],
            cost_delivery=data ['cost_dlv'] or 'del',
            note=note
        )
        user_action = UserActions.ADD_DISCOUNT_DLV.value

    order_info = await db.get_order(data['order_id'])
    text = txt.get_order_text(order_info)
    # action = OrderAction.SUC_TAKE.value if order_info.g == OrderStatus.ACTIVE_TAKE.value else OrderAction.SUC.value
    await msg.answer(text, reply_markup=kb.get_close_order_option_kb(data['order_id']))

    # журнал действий
    await db.save_user_action(
        user_id=msg.from_user.id,
        dlv_name=order_info.f,
        action=user_action,
        comment=f'ID {data["order_id"]}')


# кнопка передать заказ
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.ORDER_3.value))
async def dlv_order_3(cb: CallbackQuery, state: FSMContext):
    _, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    user_info = await db.get_user_info(cb.from_user.id)
    delivers = await db.get_users(exc_user_id=cb.from_user.id, company=user_info.company)

    await cb.message.edit_reply_markup(reply_markup=kb.get_transfer_order_kb(delivers, order_id))
    
    
# передаёт заказ
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.TRANS_ORDER.value))
async def trans_order(cb: CallbackQuery, state: FSMContext):
    user_id, order_id = map(int, cb.data.split(':')[1:])

    user = await db.get_user_info(cb.from_user.id)
    recip = await db.get_user_info(user_id)

    await db.update_row_google (
        order_id=order_id,
        dlv_name=recip.name,
        type_update=TypeOrderUpdate.TRANS.value,
        letter='del',
        discount=0,
        note='del',
    )
    # await db.update_work_order(order_id=order_id, user_id=recip.user_id)
    order_info = await db.get_order(order_id=order_id)
    order_text = txt.get_order_text(order_info)

    text = f'{user.name} передал вам заказ:\n\n{order_text}'
    await bot.send_message(
        chat_id=recip.user_id,
        text=text,
        reply_markup=kb.get_dlv_main_order_kb(
            order_id=order_info.id,
            order_status=order_info.g
        ))
    await cb.message.edit_text(
        text=f'{cb.message.text}\n\n✅ Заказ передан',
        entities=cb.message.entities,
        parse_mode=None
    )
    # журнал действий
    await db.save_user_action(
        user_id=cb.from_user.id,
        dlv_name=user.name,
        action=UserActions.TRANSFER_ORDER.value,
        comment=f'Получатель: {recip.name}')


# подтверждения забрать заказ у другого курьера
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.PICKUP_ORDER_1.value))
async def pickup_order_1(cb: CallbackQuery, state: FSMContext):
    _, order_id_str, action = cb.data.split(':')
    order_id = int(order_id_str)

    if action == 'back':
        order_info = await db.get_order(order_id=order_id)
        await cb.message.edit_reply_markup(reply_markup=kb.get_free_order_kb(
            order_id=order_id,
            type_order=TypeOrderButton.PICKUP.value,
            dlv_name=order_info.f
        ))
    else:
        await cb.message.edit_reply_markup(reply_markup=kb.get_pickup_order_kb(order_id))


# подтверждения забрать заказ у другого курьера
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.PICKUP_ORDER_2.value))
async def pickup_order_2(cb: CallbackQuery, state: FSMContext):
    _, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)

    order_info = await db.get_order (order_id=order_id)
    user_info = await db.get_user_info(user_id=cb.from_user.id)

    await db.update_row_google (
        order_id=order_id,
        dlv_name=user_info.name,
        type_update=TypeOrderUpdate.PICKUP.value,
        discount=0,
        note='del',
        letter='del'
    )
    # order_text = get_order_text (order_info)
    order_text = txt.get_order_text(order_info)

    if not DEBUG:
        text = f'{user_info.name} <b>забрал</b> заказ:\n\n{order_text}'.replace('None', '')
        await bot.send_message (
            chat_id=order_info.user_id,
            text=text,
        )

    await cb.message.edit_reply_markup (reply_markup=kb.get_dlv_main_order_kb (order_id, order_info.g))


# кнопка вернуть старую кб к заказу
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.BACK_MAIN_ORDER.value))
async def back_main_order(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    _, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)
    order_info = await db.get_order(order_id=order_id)
    text = txt.get_order_text (order_info)
    await cb.message.edit_text(text=text, reply_markup=kb.get_dlv_main_order_kb(order_id, order_info.g))


# возвращает к закрывающемуся заказу
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.BACK_CLOSE_ORDER.value))
async def back_close_order(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    _, order_id_str = cb.data.split (':')
    order_id = int (order_id_str)
    order_info = await db.get_order(order_id=order_id)

    messages = data.get('messages', [])
    for message in messages:
        await bot.delete_message(chat_id=cb.message.chat.id, message_id=message)

    text = txt.get_order_text (order_info)
    await cb.message.edit_text(text=text, reply_markup=kb.get_close_order_option_kb(order_id=order_id))
