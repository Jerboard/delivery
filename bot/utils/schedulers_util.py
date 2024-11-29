from datetime import datetime, timedelta

import db
import keyboards as kb
from init import scheduler, bot, log_error
from config import Config
from google_api import update_google_row
from utils import local_data_utils as dt
from utils.base_utils import get_today_date_str
from enums import TypeOrderButton, TypeOrderUpdate


# Запускает плпнировцики
async def start_scheduler():
    scheduler.add_job(update_google_row, 'interval', seconds=3)
    # scheduler.add_job(check_take_orders, 'interval', minutes=5)
    scheduler.add_job(update_order_date, 'cron', hour=2)
    scheduler.start()


async def resent_take_order(order_id: int, text: str, sent_list: list[dict]):
    for dlv in sent_list:
        try:
            await bot.send_message (
                chat_id=dlv['user_id'],
                text=text,
                reply_markup=kb.get_free_order_kb (order_id=order_id, type_order=TypeOrderButton.TAKE.value))
        except Exception as ex:
            log_error (f'Заказ не отправлен курьеру повторно {dlv["user_id"]}', with_traceback=False)
            log_error (ex)


async def check_take_orders():
    orders = dt.get_opr_msg_data()

    if orders:
        one_hour_ago = datetime.now() - timedelta(hours=2)
        for key, order in orders.items():
            created = Config.tz.localize(datetime.strptime(order['updated_at'], Config.datetime_form))
            # print(created, one_hour_ago, created < one_hour_ago)
            if created < one_hour_ago:
                await resent_take_order(
                    order_id=order['order_id'],
                    text=order['text'],
                    sent_list=order['sent_list'],
                )
                order['updated_at'] = datetime.now().replace(microsecond=0).strftime(Config.datetime_form)
                dt.save_opr_msg_data(key=key, new_data=order)


# обновляет дату у заказов на руках
async def update_order_date():
    await db.update_multi_orders(date_str=get_today_date_str(), type_update=TypeOrderUpdate.UPDATE_ROW.value)
    await db.delete_post_order(flag_del=True)
    # await db.update_multi_orders(type_update=TypeOrderUpdate.NOT_COME.value)
