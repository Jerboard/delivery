from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.enums.chat_type import ChatType
from aiogram.enums.content_type import ContentType

import db
import keyboards as kb
import utils as ut
from init import bot
from init import dp, log_error
# from utils import text_utils as txt
from enums import UserRole, SearchType, OrderStatus, TypeOrderButton, active_status_list, CompanyDLV, CompanyOPR


# обработка заказа для курьера
async def processing_dlv(order: db.OrderRow, user_info: db.UserRow) -> int:
    counter = 0
    try:
        text = ut.get_order_text (order)
        if order.g in active_status_list:
            # мой заказ на руках
            if order.user_id == user_info.user_id:
                counter += 1

                keyboard = kb.get_dlv_main_order_kb (order_id=order.id, order_status=order.g)
                if user_info.company == CompanyDLV.POST.value:
                    keyboard = kb.get_post_order_kb (order_id=order.id, order_status=order.g)

                await bot.send_message(chat_id=user_info.user_id, text=text, reply_markup=keyboard)
            # забрать заказ у курьера
            elif order.f != user_info.name and order.ac == user_info.company:
                counter += 1
                await bot.send_message (
                    chat_id=user_info.user_id,
                    text=text, reply_markup=kb.get_free_order_kb (
                        order_id=order.id,
                        type_order=TypeOrderButton.PICKUP.value,
                        dlv_name=order.f
                    ))
        elif order.g == OrderStatus.NEW.value:
            counter += 1
            # type_order = TypeOrderButton.POST.value \
            #     if user_info.company == CompanyDLV.POST.value else TypeOrderButton.BASE.value
            await bot.send_message (
                chat_id=user_info.user_id,
                text=text,
                reply_markup=kb.get_free_order_kb (order_id=order.id, type_order=TypeOrderButton.BASE.value))
    except Exception as ex:
        log_error (ex)
    finally:
        return counter


# обработка заказа для админа
async def processing_admin(order: db.OrderRow, user_info: db.UserRow):
    text = ut.get_admin_order_text (order)
    keyboard = None
    if user_info.role == UserRole.OWN.value:
        if order.g in active_status_list:
            keyboard = kb.get_busy_order_own_kb (order_id=order.id)

        elif order.g == OrderStatus.NEW.value:
            keyboard = kb.get_free_order_own_kb (order_id=order.id)

        else:
            keyboard = kb.get_close_order_own_kb (order_id=order.id, dlv_name=order.f, user_id=order.user_id)

    await bot.send_message (chat_id=user_info.user_id, text=text, reply_markup=keyboard)


# поиск заказов
# @dp.message(StateFilter(default_state))
@dp.message()
async def search(msg: Message, state: FSMContext):
    await state.clear ()
    if msg.chat.type != ChatType.PRIVATE:
        return

    if msg.content_type != ContentType.TEXT:
        return

    if len(msg.text) < 5:
        await msg.answer ('❗️Запрос должен быть не меньше 5и символов')
        return

    user_info = await db.get_user_info(msg.from_user.id)
    if not user_info:
        await msg.answer('❌ У вас нет доступа. Для получения доступа обратитесь к администратору')
        return

    query = msg.text.lower()
    search_on = SearchType.PHONE if query.isdigit() else SearchType.METRO
    comp_opr = None
    if user_info.role == UserRole.OPR.value and user_info.company != CompanyOPR.BOSS.value:
        comp_opr = user_info.company

    orders = await db.get_orders (search_query=query, search_on=search_on, company_opr=comp_opr)
    if not orders:
        orders = await db.get_orders (search_query=query, search_on=SearchType.NAME, company_opr=comp_opr)

    if not orders:
        if user_info.role != UserRole.DLV.value or user_info.company == CompanyDLV.POST.value:
            # orders = await db.get_orders (search_query=query, search_on=SearchType.POST, company_opr=comp_opr)
            orders = await db.get_orders (search_query=query.upper(), search_on=SearchType.POST)

    if not orders:
        await msg.answer ('❌ По вашему запросу ничего не найдено')
        return

    if user_info.role == UserRole.DLV.value:
        counter = 0
        for order in orders:
            counter += await processing_dlv(order, user_info)

        if counter == 0:
            await msg.answer('❌ По вашему запросу ничего не найдено')

    elif user_info.role in [UserRole.OPR.value, UserRole.OWN.value]:
        # order_phone = [order.n for order in orders]
        # one_number = True if len(set(order_phone)) == 1 else False
        one_number = ut.check_one_number(orders)

        if len(orders) <= 3 or one_number:
            for order in orders:
                await processing_admin(order, user_info)

        elif len(orders) > 30:
            await msg.answer(f'❗️По вашему запросу найдено {len(orders)}. Задайте более чёткие критерии поиска')

        else:
            orders_text = ''
            spt = '---------------------------\n'
            for order in orders:
                short_order = ut.get_short_order_row(order, for_=user_info.role)
                orders_text = f'{orders_text}{short_order}{spt}'

            text = f'Заказы ({len(orders)}):\n' \
                   f'{orders_text}'

            await msg.answer(text)
