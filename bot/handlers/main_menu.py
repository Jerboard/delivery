from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.enums.content_type import ContentType

import asyncio
import csv

import db
import keyboards as kb
from init import dp
from handlers.delivery_hnds.base_dlv import delivery_start, get_profile_dlv
from handlers.owner_hnds.orders_own import add_new_order
from handlers.owner_hnds.owner_base import owner_start
from handlers.operator_hnds.base_opr import get_profile_opr
from data.base_data import company_dlv
from enums import UserRole, DeliveryStatus, BaseCB, CompanyDLV


@dp.message(CommandStart())
async def com_start(msg: Message, state: FSMContext):
    await state.clear()
    user_info = await db.get_user_info(msg.from_user.id)

    if len(msg.text) > 6:
        comp_id, veryf_code, role = msg.text[7:].split('-')
        check_link = await db.get_temp_link(veryf_code)
        if check_link:
            await db.add_user (
                user_id=msg.from_user.id,
                full_name=msg.from_user.full_name,
                username=msg.from_user.username,
                role=role,
                company=comp_id
            )
            await state.set_state(DeliveryStatus.REG_NAME)
            await state.update_data (data={'role': role, 'comp_id': comp_id})
            await msg.answer('Введите ваше имя')
            await db.delete_temp_link(veryf_code)

        else:
            await msg.answer('❌Ссылка не действительна')

    else:
        if not user_info:
            await msg.answer('❌ У вас нет доступа. Для получения доступа обратитесь к администратору')

        elif user_info.role == UserRole.DLV.value:
            if not user_info.name:
                await state.set_state (DeliveryStatus.REG_NAME)
                await msg.answer ('Введите ваше имя')

            elif not user_info.phone:
                await state.set_state (DeliveryStatus.REG_PHONE)
                await msg.answer (f'Отправьте актуальный номер телефона', reply_markup=kb.get_send_contact_kb ())

            else:
                await delivery_start (user_id=msg.from_user.id, user_info=user_info)

        elif user_info.role == UserRole.OPR.value:

            text = f'Для поиска заказов отправьте номер телефона, имя получателя или часть адреса'
            await msg.answer(text, reply_markup=ReplyKeyboardRemove())

        elif user_info.role == UserRole.OWN.value:
            await owner_start(msg.from_user.id)

        else:
            await msg.answer('❌ У вас нет доступа. Для получения доступа обратитесь к администратору')


# регистрирует имя
@dp.message(StateFilter(DeliveryStatus.REG_NAME))
async def reg_dlv_1(msg: Message, state: FSMContext):
    await db.update_user_info(
        user_id=msg.from_user.id,
        name=msg.text,
    )
    data = await state.get_data()
    if data.get('role') == UserRole.DLV.value and data.get('comp_id') != CompanyDLV.POST.value:
        await state.set_state (DeliveryStatus.REG_PHONE)
        text = f'Отправьте актуальный номер телефона'
        await msg.answer (text, reply_markup=kb.get_send_contact_kb ())

    else:
        await state.clear ()
        text = f'Вы зарегистрированы. Для поиска заказов отправьте номер получателя или часть адреса сообщением'
        await msg.answer (text)


# регистрирует телефон
@dp.message(StateFilter(DeliveryStatus.REG_PHONE))
async def reg_dlv_2(msg: Message, state: FSMContext):
    await state.clear()

    phone = msg.contact.phone_number if msg.content_type == ContentType.CONTACT.value else msg.text
    if phone:
        await db.update_user_info(
            user_id=msg.from_user.id,
            phone=phone,
        )
        text = f'Вы зарегистрированы. Для поиска заказов отправьте номер получателя или часть адреса сообщением'
        await msg.answer(text, reply_markup=ReplyKeyboardRemove())
    else:
        sent = await msg.answer('❗️Некорректный номер телефона')
        await asyncio.sleep(5)
        await sent.delete()


# Личный кабинет
@dp.message(Command('main'))
async def com_main(msg: Message, state: FSMContext):
    await state.clear()

    user_info = await db.get_user_info(msg.from_user.id)

    if user_info and user_info.role == UserRole.DLV.value:
        await get_profile_dlv(user_id=msg.from_user.id, user_info=user_info)

    elif user_info and user_info.role == UserRole.OPR.value:
        await get_profile_opr(user_id=msg.from_user.id, user_info=user_info)

    elif user_info and user_info.role == UserRole.OWN.value:
        await add_new_order(msg.from_user.id, state)

    else:
        await msg.answer('❌ У вас нет доступа. Для получения доступа обратитесь к администратору')


# отмена
@dp.callback_query(lambda cb: cb.data.startswith(BaseCB.CLOSE.value))
async def close(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.delete()
    await cb.answer('❌Отменено')
