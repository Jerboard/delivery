from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

import db
import keyboards as kb
from init import dp
from .base_dlv import get_profile_dlv,stop_state
from enums import DeliveryCB, DeliveryStatus


# возвращает в лк курьера
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.BACK_MAIN.value))
async def expenses_dvl_0(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await get_profile_dlv(cb.from_user.id, msg_id=cb.message.message_id)


# смена имени курьера запрос имени
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.EDIT_PROFILE.value))
async def edit_dlv_name(cb: CallbackQuery, state: FSMContext):
    _, action = cb.data.split(':')
    user_info = await db.get_user_info(cb.from_user.id)

    if action == 'name':
        text = f'Ваше имя: {user_info.name}\n' \
               f'Введите новое имя\n' \
               f'❗️Ваше имя будет отображаться в таблице администратора'
    else:
        text = f'Ваш телефон: {user_info.phone}\n' \
               f'Введите новое номер телефона\n' \
               f'❗️Ваше телефон будет отображаться в таблице администратора'

    await state.set_state(DeliveryStatus.EDIT_PROFILE)
    await state.update_data(data={'msg_id': cb.message.message_id, 'action': action})
    await cb.message.edit_text(text, reply_markup=kb.get_main_dlv_menu_kb())


# смена имени курьера сохранение
@dp.message(StateFilter(DeliveryStatus.EDIT_PROFILE))
async def com_start(msg: Message, state: FSMContext):
    stop = await stop_state(msg)
    if stop:
        return

    data = await state.get_data()
    await state.clear()
    await msg.delete()

    if data['action'] == 'name':
        await db.update_user_info(user_id=msg.from_user.id, name=msg.text)
    else:
        await db.update_user_info(user_id=msg.from_user.id, phone=msg.text)

    await get_profile_dlv (user_id=msg.from_user.id, msg_id=data['msg_id'])
