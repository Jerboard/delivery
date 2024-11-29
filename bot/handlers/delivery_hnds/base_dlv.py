from aiogram.types import ReplyKeyboardRemove, CallbackQuery, Message

from datetime import datetime

import db
from init import bot, dp, log_error
from config import Config
import keyboards as kb
from handlers.operator_hnds.base_opr import send_opr_report_msg
from utils import text_utils as txt
from utils.base_utils import get_today_date_str, send_long_msg
from data.base_data import expensis_dlv, work_chats
from enums import UserActions, UserRole, OrderStatus, CompanyDLV, TypeOrderUpdate, DeliveryCB


# старт курьера
async def delivery_start(user_id: int, user_info: db.UserRow = None, msg_id: int = None):
    if not user_info:
        user_info = await db.get_user_info (user_id)
        # user_info = await db.get_user_info (user_id=1970050747)

    if user_info.company == CompanyDLV.POST:
        orders = await db.get_post_orders(user_id=user_id, only_active=True)
        # orders = await db.get_post_orders(user_id=1970050747, only_active=True)

    else:
        orders = await db.get_orders(user_id=user_id, get_active=True)

    active_text = ''
    send_date_dict = {}
    counter = 0
    for order in orders:
        counter += 1
        if order.g == OrderStatus.SEND.value:
            order_count = send_date_dict.get(order.e, 0)
            order_count_new = order_count + 1
            send_date_dict[order.e] = order_count_new
        else:
            active_text += txt.get_short_order_row(order, for_=UserRole.DLV.value)

    text = (f'{user_info.name}\n\n' 
            f'Заказы:\n' 
            f'{active_text}')

    if counter == 0:
        text = 'У вас нет активных заказов'

    if msg_id:
        await bot.edit_message_text(text, chat_id=user_id, message_id=msg_id)
    else:
        if user_info.company == CompanyDLV.POST:
            await bot.send_message (user_id, text, reply_markup=kb.get_view_send_orders(send_date_dict))
        else:
            await bot.send_message (user_id, text, reply_markup=ReplyKeyboardRemove())


@dp.callback_query(lambda cb: cb.data.startswith(DeliveryCB.SEND_ORDERS.value))
async def send_orders_view(cb: CallbackQuery):
    _, date_str = cb.data.split (':')

    user_info = await db.get_user_info (user_id=cb.from_user.id)
    # user_info = await db.get_user_info (user_id=1970050747)
    orders = await db.get_orders (dlv_name=user_info.name, on_date=date_str, order_status=OrderStatus.SEND.value)

    order_text = ''
    for order in orders:
        order_text += txt.get_short_order_row (order, for_=UserRole.DLV.value)

    text = f'Отправлены {date_str}:\n\n{order_text}'
    await send_long_msg(chat_id=cb.from_user.id, text=text)


async def get_profile_dlv(user_id: int, user_info: db.UserRow = None, msg_id: int = None):
    if not user_info:
        user_info = await db.get_user_info (user_id)

    if user_info.company == CompanyDLV.POST:
        orders = await db.get_statistic_post_dlv(user_id=user_id)

    else:
        orders = await db.get_orders_statistic (dlv_name=user_info.name, on_date=get_today_date_str())
    statistic_text = txt.get_statistic_text (orders)
    text = f'{user_info.name}\n\n{statistic_text}'

    if msg_id:
        await bot.edit_message_text (text, reply_markup=kb.main_dvl_kb (), chat_id=user_id, message_id=msg_id)
    else:
        await bot.send_message (user_id, text, reply_markup=kb.main_dvl_kb ())


async def save_expenses(
        user_id: int,
        data: dict
):
    # log_error(f'Трата дата {user_id}\n{data}', with_traceback=False)

    user_info = await db.get_user_info (user_id)

    today_str = get_today_date_str ()
    exp_today = await db.get_report_dlv(user_info.name, today_str)

    ex_info = expensis_dlv [data ['ex_id']]
    comment = data["comment"] if data.get('comment') else ex_info ["text"]
    comment = f'{data ["exp_sum"]} - {comment}'

    if exp_today:
        await db.update_expenses_dlv(
            entry_id=exp_today.id,
            l=comment,
            b=exp_today.b + (data.get('b', 0)),
            c=exp_today.c + (data.get('c', 0)),
            d=exp_today.d + (data.get('d', 0)),
            e=exp_today.e + (data.get('e', 0)),
            f=exp_today.f + (data.get('f', 0)),
            g=exp_today.g + (data.get('g', 0)),
            h=exp_today.h + (data.get('h', 0)),
            i=exp_today.i + (data.get('i', 0)),
            j=exp_today.j + (data.get('j', 0)),
            k=exp_today.clmn_k + (data.get('k', 0)),
        )
        await db.save_user_action (user_id, user_info.name, 'Обновил трату', str(exp_today)[:250])

    else:
        last_row = await db.get_last_updated_report(last_row=True)
        if not last_row:
            row_num = 5
        else:
            row_num = last_row.row_num + 1 if last_row.m == today_str else last_row.row_num + 2

        await db.add_report_row (
            l=[comment],
            m=today_str,
            n=user_info.name,
            b=data.get('b', 0),
            c=data.get('c', 0),
            d=data.get('d', 0),
            e=data.get('e', 0),
            f=data.get('f', 0),
            g=data.get('g', 0),
            h=data.get('h', 0),
            i=data.get('i', 0),
            j=data.get('j', 0),
            k=data.get('k', 0),
            row_num=row_num
        )
        # if user_info.company == CompanyDLV.POST:
        #     edit_post_order_ld (
        #         user_id=user_id,
        #         action=Action.ADD.value,
        #         key_1=KeyWords.REPORT.value
        #     )

        await db.save_user_action (user_id, user_info.name, UserActions.ADD_EXPENSES.value, str(data))

    today = datetime.now().strftime (Config.datetime_form)
    text = (f'Курьер: {user_info.name}\n'
            f'Время: {today}\n'
            f'Сумма: {data["exp_sum"]} ₽\n'
            f'Комментарий: {comment}')

    if data.get('photo_id'):
        await bot.send_photo (work_chats[f'group_expenses'], photo=data['photo_id'], caption=text)
        # await bot.send_photo (work_chats[f'ex_{user_info.company}'], photo=data['photo_id'], caption=text)
    else:
        await bot.send_message (work_chats[f'group_expenses'], text)
        # await bot.send_message (work_chats[f'ex_{user_info.company}'], text)

    await bot.send_message (user_id, '✅Ваша трата учтена')
    await db.save_user_action(user_id, user_info.name, UserActions.ADD_EXPENSES.value, text)


# закрытие заказа
async def done_order(user_id: int, order_id: int, lit: str, msg_id: int = None, node: str = None):
    order_info = await db.get_order (order_id)

    # if order_info.g in [OrderStatus.ACTIVE.value, OrderStatus.SEND.value]:
    order_status = OrderStatus.SUC.value
    # else:
    #     order_status = OrderStatus.SUC_TAKE.value

    await db.update_row_google (
        order_id=order_id,
        letter=lit,
        status=order_status,
        type_update=TypeOrderUpdate.STATE.value,
        take_date=get_today_date_str(),
        note=node
    )
    text = txt.get_order_text (order_info)
    if msg_id:
        await bot.edit_message_text (chat_id=user_id, message_id=msg_id, text=f'{text}\n\n✅ Выполнен')
    else:
        await bot.send_message (chat_id=user_id, text=f'{text}\n\n✅ Выполнен')

    # отправить фото оператору
    order_info = await db.get_order (order_id)
    await send_opr_report_msg (order_info)
    action = UserActions.SUCCESS_ORDER.value

    # журнал действий
    await db.save_user_action (
        user_id=user_id,
        dlv_name=order_info.f,
        action=action,
        comment=str(order_id))


# выводит из статуса
async def stop_state(msg: Message):
    if msg.text == '/start':
        await delivery_start(user_id=msg.from_user.id)
        return True
    elif msg.text == '/main':
        await get_profile_dlv(user_id=msg.from_user.id)
        return True
    else:
        # save_expenses
        return False
