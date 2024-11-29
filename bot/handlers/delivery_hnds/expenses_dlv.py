from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.enums.content_type import ContentType

from asyncio import sleep

import db
import keyboards as kb
from config import Config
from init import dp, bot
from .base_dlv import save_expenses, stop_state
from data.base_data import expensis_dlv, letters
from utils.base_utils import get_today_date_str
from enums import DeliveryCB, DeliveryStatus, UserActions


# смена клавиатуры на клавиатуру с тратами
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.EXPENSES_1.value))
async def expenses_dvl_1(cb: CallbackQuery):
    user_info = await db.get_user_info(user_id=cb.from_user.id)
    await cb.message.edit_reply_markup(reply_markup=kb.expenses_dvl_kb(user_info.company))


# запрос подтверждения траты 1 Просит отправить сумму
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.EXPENSES_2.value))
async def expenses_dvl_2(cb: CallbackQuery, state: FSMContext):
    _, ex_id_str = cb.data.split(':')
    ex_id = int(ex_id_str)

    await state.set_state(DeliveryStatus.EXPENSES_3)
    await state.update_data(data={'ex_id': ex_id})
    await cb.message.answer('Отправьте сумму расходов', reply_markup=kb.get_close_kb())


# принимает сумму
@dp.message(StateFilter(DeliveryStatus.EXPENSES_3))
async def expenses_dvl_3(msg: Message, state: FSMContext):
    stop = await stop_state(msg)
    if stop:
        return

    if msg.text and msg.text.isdigit():
        data = await state.get_data()
        ex_info = expensis_dlv[data['ex_id']]

        await state.update_data(data={ex_info['column']: int(msg.text), 'exp_sum': int(msg.text)})
        await state.set_state(DeliveryStatus.EXPENSES_4)

        if ex_info['comment']:
            text = f'Отправьте комментарий'
        elif ex_info['photo']:
            text = f'Отправьте фото подтверждение траты'
        else:
            data = await state.get_data ()
            await state.clear()
            await save_expenses(msg.from_user.id, data)
            return

        await msg.answer(text, reply_markup=kb.get_close_kb())

    else:
        sent = await msg.answer('❗️ Отправьте сумму цифрой')
        await sleep(3)
        await sent.delete()


# принимает фото или коммент по трате
@dp.message(StateFilter(DeliveryStatus.EXPENSES_4))
async def expenses_dvl_4(msg: Message, state: FSMContext):
    stop = await stop_state(msg)
    if stop:
        return

    if msg.content_type == ContentType.PHOTO:
        await state.update_data(data={'photo_id': msg.photo[-1].file_id})

        data = await state.get_data ()
        await state.clear ()
        await save_expenses (msg.from_user.id, data)
    else:
        await state.update_data (data={'comment': msg.text})
        data = await state.get_data()
        await state.clear()
        await save_expenses (msg.from_user.id, data)


# сохраняем зп
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.EXPENSES_5.value))
async def expenses_dvl_5(cb: CallbackQuery, state: FSMContext):
    _, letter = cb.data.split(':')

    if letter == 'start':
        await cb.message.answer ('Время работы: ', reply_markup=kb.get_expensis_let_kb ())
    else:
        await state.set_state (DeliveryStatus.EXPENSES_3)
        ex_info = expensis_dlv [1]
        await state.update_data (data={'ex_id': 1, 'comment': f'{ex_info["text"]} {letters[letter]}'})
        await cb.message.edit_text ('Отправьте сумму расходов', reply_markup=kb.get_close_kb ())


# посмотреть траты за сегодня
@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.EXPENSES_VIEW.value))
async def expenses_dvl_view(cb: CallbackQuery):
    user_info = await db.get_user_info(user_id=cb.from_user.id)
    expenses = await db.get_report_dlv(dlv_name=user_info.name, exp_date=get_today_date_str())
    if not expenses:
        text = 'Нет трат'
    else:
        expenses_str = '\n'.join(expenses.l)
        text = f'💸Траты за сегодня:\n\n{expenses_str}'
    await cb.message.answer(text)
