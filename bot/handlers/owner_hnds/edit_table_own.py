from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from datetime import datetime
from asyncio import sleep

import db
import keyboards as kb
from init import dp
from config import Config
from google_api.utils_google import is_table_exist
import google_api as ggl
from utils.base_utils import get_today_date_str, check_active_post_orders
from handlers.owner_hnds.owner_base import owner_start
from utils.local_data_utils import save_table_id
from enums import OwnerCB, OwnerStatus


# меняет рабочую таблицу. Запрашивает номер новой таблицы
@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.CHANGE_TAB.value))
async def change_tab_1(cb: CallbackQuery, state: FSMContext):
    await state.set_state(OwnerStatus.CHANGE_TAB)
    text = f'Отправьте номер новой таблицы.\n\n' \
           f'‼️Важно: рабочая таблица должна располагаться на первом листе. ' \
           f'Не забудьте дать боту доступ к таблице\n\n' \
           f'Служебный аккаунт:\n\n <code>matrix@delivery-443213.iam.gserviceaccount.com</code>'

    await cb.message.answer(text, reply_markup=kb.get_close_kb())


# Меняет рабочую таблицу. Проверяет таблицу
@dp.message(StateFilter(OwnerStatus.CHANGE_TAB))
async def change_tab_2(msg: Message, state: FSMContext):
    await state.clear()
    time_start = datetime.now()
    sent = await msg.answer ('⏳ Таблица обновляется это может занять какое-то время')

    if is_table_exist(msg.text):
        update_table = True
        while update_table:
            wait_orders = await db.get_orders (get_wait_update=True)
            wait_reports = await db.get_reports_all_dlv (get_wait_update=True)

            wait_updates = len(wait_orders) + len(wait_reports)
            if wait_updates == 0:
                update_table = False
            else:
                try:
                    await sent.edit_text (
                        text=f'⏳ Ожидает внесения изменений. Примерно {wait_updates * 3} с.',
                        reply_markup=kb.get_hard_update_kb()
                    )
                except:
                    pass
                await sleep(3)

        # очистить таблицу
        await db.delete_orders ()
        # обновляет таблицу
        error_text = await ggl.save_new_order_table(msg.text)
        # обновляет почтовые заказы
        await check_active_post_orders()
        # очистить таблицу отчётов
        await db.clear_report_table ()
        # обновляет отчёт и траты
        await ggl.save_new_report_table(msg.text)
        # сохраняет новую таблицу
        save_table_id(msg.text)
        # по релизу удалить. обновляет даты
        await db.update_multi_orders (date_str=get_today_date_str (), test=True)

        time_finish = datetime.now() - time_start
        await sent.edit_text(f'✅ Таблица обновлена\nВремя обновления: {time_finish}')
        if error_text:
            await msg.answer(f'{error_text}\n\n‼️ Обратитесь к разработчику')

    else:
        await sent.delete()
        await msg.answer('‼ Произошла ошибка. Неправильный номер таблицы или ошибка доступа')


# ставит все заказы в статус обновлено
@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.HARD_UPDATE.value))
async def hard_update(cb: CallbackQuery):
    await db.hard_order_update()


# обновляет таблицу update_table
@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.UPDATE_TABLE.value))
async def update_google_table(cb: CallbackQuery):
    _, type_table = cb.data.split(':')
    sent = await cb.message.answer ('⏳')
    if type_table == 'order':
        await ggl.update_google_table(cb.from_user.id)
    else:
        # очистить таблицу отчётов
        await db.clear_report_table ()
        # обновляет отчёт и траты
        await ggl.save_new_report_table ()

    await owner_start(user_id=cb.from_user.id, msg_id=cb.message.message_id)
    await sent.delete()



# вернуть клавиатуру передачи заказа
# @dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.UPDATE_USERS_TABLE_1.value))
# async def update_users_1(cb: CallbackQuery):
#     ga.add_users_table()
#     await cb.answer('📤Данные выгружены в таблицу', show_alert=True)


# вернуть клавиатуру передачи заказа
# @dp.callback_query_handler(text_startswith='update_users_table_2')
# async def update_users_2(cb: CallbackQuery):
#     ga.update_users_table()
#     await cb.answer('📥Данные обновлены', show_alert=True)