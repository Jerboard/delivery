from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from datetime import datetime
from asyncio import sleep

import db
import keyboards as kb
from init import dp, bot, log_error
from config import Config
from utils.base_utils import get_random_code
from data.base_data import order_status_data
from enums import OwnerCB, UserRole, UserActions, OwnerStatus, OrderAction, TypeOrderUpdate


# меняет клавиатуру на клаву с курьерскими
@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.ADD_USER_1.value))
async def add_user_1(cb: CallbackQuery, state: FSMContext):
    _, role = cb.data.split (':')
    await cb.message.edit_reply_markup(reply_markup=kb.get_add_dlv_comp_kb(role))


# отправляет ссылку для вступления
@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.ADD_USER_2.value))
async def add_user_2(cb: CallbackQuery, state: FSMContext):
    _, role, comp_id = cb.data.split(':')
    code_verif = get_random_code()

    link = f'https://t.me/{Config.bot_name}?start={comp_id}-{code_verif}-{role}'

    await db.add_temp_link(code_verif)
    text = f'Для начала работы перейдите по ссылке и пройдите простую регистрацию\n\n' \
           f'{link}'

    await cb.message.answer(text)


@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.DEL_USER_1.value))
async def del_user_1(cb: CallbackQuery):
    _, user_role = cb.data.split(':')
    users = await db.get_users(role=user_role)

    text = f'❗️Чтобы удалить сотрудника нажмите на его имя'
    await cb.message.edit_text(text, reply_markup=kb.get_del_user_kb(users=users, user_role=user_role))


# удаляет пользователя
@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.DEL_USER_2.value))
async def del_user_2(cb: CallbackQuery):
    _, user_id_str, user_role = cb.data.split(':')
    user_id = int(user_id_str)

    await db.delete_user(user_id)
    users = await db.get_users (role=user_role)

    text = f'✅Пользователь удалён'
    await cb.answer(text, show_alert=True)
    await cb.message.edit_reply_markup(reply_markup=kb.get_del_user_kb(users=users, user_role=user_role))