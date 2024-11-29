import telebot
import logging
import traceback
import os

from datetime import datetime

from delivery_admin.settings import BASE_DIR, DEBUG, BOT_TOKEN
from bot_admin.models import UserTable, WorkOrders, OrderTable

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='html')


# информирует куру о назначенном заказе
def send_order_dlv(name: str, order_info: OrderTable):
    user = UserTable.objects.filter (name=name).first()
    work_order = WorkOrders.objects.filter(order_id=order_info.id).first()
    if work_order:
        work_order.user_id = user.user_id
    else:
        work_order = WorkOrders(user_id=user.user_id, order_id=order_info.id)
    work_order.save ()

    prepay = order_info.u + order_info.v
    if order_info.q == 0 and prepay != 0:
        cost = 0
    else:
        cost = order_info.q + order_info.r + order_info.clmn_t - order_info.y

    text = (f'❗️ Вам назначен заказ\n\n'
            f'Заказ от: {order_info.j} \n' 
            f'Оператор: {order_info.k}\n' 
            f'Клиент: {order_info.m}\n' 
            f'Номер: <code>{order_info.n}</code>    <code>{order_info.o}</code>\n' 
            f'Доставка: {order_info.w}\n' 
            f'Адрес: {order_info.x}\n' 
            f'Цена: {cost} + {order_info.s}\n' 
            f'Курьеру к оплате: {cost + order_info.s}\n' 
            f'Примечания: {order_info.ab} ')

    bot.send_message(user.user_id, text)


bot_test = telebot.TeleBot('7181274585:AAEPJ_CXjhKFR3CiLhV8W9AS_8KmHej7JmI', parse_mode='html')


def send_message(text: str):
    bot_test.send_message(chat_id=524275902, text=text)

