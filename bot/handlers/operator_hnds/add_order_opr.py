from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.exceptions import TelegramBadRequest
from datetime import datetime

import db
import keyboards as kb
from init import dp, bot, log_error
from config import Config
from handlers.operator_hnds.base_opr import get_profile_opr
from utils import local_data_utils as dt
from utils.base_utils import get_today_date_str
from data.base_data import company_dlv, order_status_data, work_chats
from enums import OperatorCB, OperatorStatus, TypeOrderUpdate, OrderStatus, DataKey, UserActions, UserRole, TypeOrderButton


# взять заказ выбор курьерской
@dp.callback_query(lambda cb: cb.data.startswith(OperatorCB.TAKE_ORDER_0.value))
async def take_order_1(cb: CallbackQuery, state: FSMContext):
    text = f'Оформить забор\n\nВыберите курьерскую'
    await cb.message.edit_text(text, reply_markup=kb.take_order_company_kb())


# кнопка взять заказ
@dp.callback_query(lambda cb: cb.data.startswith(OperatorCB.TAKE_ORDER_1.value))
async def take_order_1(cb: CallbackQuery, state: FSMContext):
    _, comp_id = cb.data.split (':')

    text = f'Чтобы отправить заявку на забор курьерам - подставьте данные в форму \n\n' \
           f'<code>Оператор:\n' \
           f'Партнер:\n' \
           f'ФИО:\n' \
           f'Номер:\n' \
           f'Доп.номер:\n' \
           f'Забрать:\n' \
           f'Цена:\n' \
           f'Доставка:\n' \
           f'Метро:\n' \
           f'Адрес:\n' \
           f'Примечание: </code>'

    await state.set_state (OperatorStatus.TAKE_ORDER)
    sent = await cb.message.answer (text, reply_markup=kb.get_close_kb())
    await state.update_data (data={'msg_id': sent.message_id, 'comp_id': comp_id})


@dp.message (StateFilter(OperatorStatus.TAKE_ORDER))
async def take_order(msg: Message, state: FSMContext):
    if msg.text and msg.text[0] == '/':
        await get_profile_opr(user_id=msg.from_user.id)
        return
    await msg.delete ()
    data = await state.get_data ()
    try:
        await bot.edit_message_text (
            text=msg.text,
            chat_id=msg.chat.id,
            message_id=data ['msg_id'],
            reply_markup=kb.get_take_order_kb(role=UserRole.OPR.value)
        )
    except TelegramBadRequest as ex:
        pass


# добавляет заказ и рассылает его курьерам
@dp.callback_query(lambda cb: cb.data.startswith(OperatorCB.TAKE_ORDER_2.value))
async def take_order_2(cb: CallbackQuery, state: FSMContext):
    sent_wait = await cb.message.answer ('⏳')
    data = await state.get_data ()
    await state.clear ()

    data_dict = {}
    for row in cb.message.text.split ('\n'):
        row_split = row.split(':')
        if len(row_split) == 2:
            v = row_split[1].strip() or None

            if v:
                v = int(v) if v.isdigit() else v.lower()
            data_dict[row_split[0]] = v

    last_row = await db.get_max_row_num ()
    order_id = await db.add_row(
        row_num=last_row + 1,
        g=OrderStatus.NEW.value,
        # h=order_status_data.get(OrderStatus.TAKE.value),
        h='Забор',
        j=get_today_date_str(),
        k=str(data_dict.get('Оператор')),
        l=data_dict.get('Партнер'),
        m=data_dict.get('ФИО'),
        n=str (data_dict.get ('Номер', '')),
        o=str (data_dict.get ('Доп.номер', '')),
        p=data_dict.get ('Забрать'),
        q=data_dict.get ('Цена', 0),
        t=data_dict.get ('Доставка', 0),
        r=0,
        s=0,
        y=0,
        w=data_dict.get ('Метро'),
        x=data_dict.get ('Адрес'),
        ab=data_dict.get ('Примечание'),
        ac=data ['comp_id'],
        type_update=TypeOrderUpdate.ADD_OPR.value
    )
    dlvs = await db.get_users(company=data ['comp_id'])

    sent_list = []
    for dlv in dlvs:
        try:
            sent = await bot.send_message (
                chat_id=dlv.user_id,
                text=cb.message.text,
                reply_markup=kb.get_free_order_kb(order_id=order_id, type_order=TypeOrderButton.TAKE.value)
            )
            sent_list.append ({'user_id': sent.chat.id, 'message_id': sent.message_id})
        except Exception as ex:
            log_error(f'Заказ не отправлен курьеру {dlv.name}', with_traceback=False)
            log_error(ex)

    now_str = datetime.now().replace(microsecond=0).strftime(Config.datetime_form)
    key = f'{DataKey.ADD_OPR_ORDER.value}-{order_id}'
    order_data = {
        'opr': cb.from_user.id,
        'order_id': order_id,
        'created_at': now_str,
        'updated_at': now_str,
        'sent_list': sent_list,
        'text': cb.message.text
    }
    dt.save_opr_msg_data(key, new_data=order_data)
    text = f'✅Заявка добавлена.\n\n{cb.message.text}'
    await sent_wait.edit_text(text)

    # await bot.send_message (f'take_{work_chats [data ["comp_id"]]}', cb.message.text)
    await bot.send_message (work_chats[f'take_{data ["comp_id"]}'], cb.message.text)

    user_info = await db.get_user_info(user_id=cb.from_user.id)
    await db.save_user_action(
        user_id=cb.from_user.id,
        dlv_name=user_info.name,
        action=UserActions.ADD_TAKE_ORDER.value,
        comment=f'Добавлен заказ №{order_id} для {company_dlv.get(data["comp_id"], "н/д")}'
    )
