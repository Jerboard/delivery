import re

import db
from utils.base_utils import get_order_cost
from data import base_data as dt
from enums import (OrderStatus, UserRole, ShortText, KeyWords, done_status_list, active_status_list, ref_status_list,
                   CompanyDLV)


# убирает пустые строки
def clearing_text(text: str) -> str:
    clear_text = ''
    for row in text.split ('\n'):
        if row and row[0] == '#':
            clear_text = f'{clear_text}\n{row[1:]}'
        elif not row or not re.search ('None', row):
            clear_text = f'{clear_text}\n{row}'

    return clear_text.replace('None', '').strip()


# текст заказа по строке
def get_order_text(order: db.OrderRow) -> str:
    cost = get_order_cost(order)
    bottom_text = '✖️ Клиент не явился' if order.d == KeyWords.NOT_COME.value else ''
    text = (
        f'Заказ от: {order.j} \n'
        f'Оператор: {order.k}\n'
        f'Клиент: {order.m}\n'
        f'Номер: <code>{order.n}</code> <code>{order.o}</code>\n'
        f'Доставка: {order.w}\n'
        f'Адрес: {order.x}\n'
        f'Цена: {cost} + {order.clmn_t}\n'
        f'Курьеру к оплате: {cost + order.clmn_t}\n'
        f'Примечания: {order.ab}\n\n'
        f'{bottom_text}'
    )
    return clearing_text(text)


# текст заказа для админов
def get_admin_order_text(order: db.OrderRow) -> str:
    prepay = order.u + order.v

    if order.q == 0 and prepay != 0:
        cost = 0
    else:
        # (q + r + s - y) + t
        cost = order.q + order.r + order.s - order.y

    status = dt.order_status_data.get(order.g)
    text = (f'#Заказ от {order.j}, исполнитель {order.h}\n'
            f'#Курьерская: {dt.company_dlv.get(order.ac)} ({order.f})\n'
            f'Номер курьера: {order.phone}\n'
            f'Статус заказа: {order.e} {status}\n\n'
            f'Оператор: {order.k}\n'
            f'ФИО: {order.m}\n'
            f'#Номер: <code>{order.n}</code> <code>{order.o}</code>\n'
            f'Метро: {order.w} \n'
            f'Адрес: {order.x}\n\n'
            f'Цена: {order.q}\n'
            f'Наценка: {order.r}\n'
            f'Доп: {order.s}\n'
            f'Доставка: {order.clmn_t}\n'
            f'Биток: {order.b}\n'
            f'Предоплата: {prepay}\n\n'
            f'Курьеру к оплате: {cost} + {order.clmn_t}\n'
            f'Итого: {cost + order.clmn_t}\n\n'
            f'Примечания: {order.ab}\n')

    return clearing_text(text)


# краткий заказ строка
def get_short_order_row(order: db.OrderRow, for_: str) -> str:
    cost = get_order_cost(order)

    if for_ in [UserRole.OWN.value, UserRole.OPR.value]:
        text = (f'<code>{order.n}</code>, <code>{order.o}</code>  {order.m} {order.x} '
                f'{order.f} {dt.order_status_data.get(order.g)}\n'.replace('None', ''))

    elif for_ == ShortText.ACTIVE.value:
        text = (f'{order.i} | {order.k} | {order.m} | <code>{order.n}</code> <code>{order.o}</code> '
                f'| {cost} + {order.clmn_t}| {order.w}')

    elif for_ == ShortText.FREE.value:
        # [ J ] | [ K ] | [ М ] | [ N ] [ O ] | ([ Q ]+[ R ]+[ S ]) + ([ T ]) | [ W ] | [ X ]
        text = (f'{order.j} | {order.k} | {order.m} | <code>{order.n}</code>  <code>{order.o}</code> |'
                f' {cost} + {order.clmn_t} | {order.w} | {order.x}')

    elif for_ == ShortText.REPORT.value:
        comment = f'({order.ab})' if order.ab else ''
        comment_d = f'({order.d})' if order.d else ''
        text = f'{comment_d} {dt.order_status_data.get (order.g)} (от {order.j}) {order.n} {cost} + {order.clmn_t} {order.w} {comment}\n'

    else:
        node = f'<code>{order.ab}</code>' if order.ac == CompanyDLV.POST else ''
        text = (f'<code>{order.n}</code>  <code>{order.o}</code> {cost} + {order.clmn_t} {order.w} {node}'
                f'\n---------------------------\n')

    return text.replace('None', '')


def get_statistic_text(statistic: tuple[db.OrderGroupRow]) -> str:
    text = ''
    total = 0
    for order in statistic:
        status = dt.order_status_data.get(order.status) if order.status != OrderStatus.NEW.value else 'Без курьера'
        if status:
            text += f'{status.capitalize()}: {order.orders_count}\n'
            total += order.orders_count
    return f'Всего заказов: {total}\n{text}'.strip()


# отчёт в группу при отказе от заказа
def get_dlv_refuse_text(order: db.OrderRow, note: str) -> str:
    cost = get_order_cost(order)
    text = (
        f'Курьер: {order.f}\n'
        f'Номер курьера: <code>{order.phone}</code>\n\n'
        f'Оператор: {order.k}\n'
        f'Клиент: {order.m}\n'
        f'Номер: <code>{order.n}</code>, <code>{order.o}</code>\n'
        f'Доставка: {order.w}\n'
        f'Адрес: {order.x}\n'
        f'Цена: {cost} + {order.clmn_t}\n'
        f'Курьеру к оплате: {cost + order.clmn_t}\n'
        f'Примечания: {note}\n'
    )
    return clearing_text(text)


# отчёты для операторов
def get_opr_order_text(order: db.OrderRow) -> str:
    cost = get_order_cost (order)
    mark = dt.order_mark.get (order.g, '')
    status_str = dt.order_status_data.get (order.g, '')
    comp = dt.company_dlv.get (order.ac, 'н/д')
    node = f'Трек номер <code>{order.ab}</code>' if order.g == OrderStatus.SEND else f'Примечание: {order.ab}'
    text = (
        f'{mark} {status_str} {order.e}\n'
        f'Курьер: {order.f} ({comp})\n\n'
        f'Оператор: {order.k}\n'
        f'ФИО: {order.m}\n'
        f'#Номер: <code>{order.n}</code>, <code>{order.o}</code>\n'
        f'Цена: {cost}\n'
        f'Доставка: {order.clmn_t}\n'
        f'Метро: {order.w}\n'
        f'Адрес: {order.x}\n'
        f'{node}\n'
    )
    return clearing_text(text)


def get_opr_report_text(order: db.OrderRow) -> str:
    cost = get_order_cost (order)
    mark = dt.order_mark.get(order.g, '')
    status_str = dt.order_status_data.get(order.g, '')
    comp = dt.company_dlv.get(order.ac, 'н/д')

    if not order.ab:
        node = ''
    elif order.comp_opr == CompanyDLV.POST:
        node = f'Трек номер <code>{order.ab}</code>'
    elif order.g in ref_status_list:
        node = f'Причина отказа: {order.ab}'
    else:
        node = f'Примечание: {order.ab}'

    text = (f'{mark} {status_str} {order.e}\n'
            f'Курьерская: {comp} ({order.f})\n'
            f'Номер курьера: <code>{order.phone}</code>\n\n'
            f'Оператор {order.k}\n'
            f'ФИО {order.m}\n'
            f'#Номер {order.n}  {order.o}\n'
            f'Метро {order.w}\n\n'
            f'Курьеру к оплате: {cost} + {order.clmn_t} \n'
            f'Курьеру к оплате: {cost + order.clmn_t} \n\n'
            f'{node}')
    return clearing_text(text)

'''

🟢 доставлен 14.06
Заказ от 13.06, исполнитель Тринити
Курьерская: Путилин (Твердый)
Номер курьера: +79

Оператор: 18
ФИО: крейдич дмитрий максимович
Номер: 9036695755 
Метро: щелковская 

Курьеру к оплате: 5800 + 300
Итого: 6100

Примечание:



🟠 отправлен 31.05
Заказ от 30.05, исполнитель Кукла
Курьерская: Почта / СДЭК (Николь)

Оператор: 18
ФИО: зызда
Номер: 9229995903 
Метро: почта 
Адрес: емс
адрес: кировская обл., мурашинский р-он, посёлок октябрьский, ул. свободы, д.32, кв.2
получатель: зызда дмитрий иванович

Курьеру к оплате: 0 + 1800
Итого: 1800

Трек номер: ED328833991RU



🟡 на руках 14.06
Заказ от 14.06, исполнитель Настя
Курьерская: Путилин (Димас)
Номер курьера: +79

Оператор: 18
ФИО: бакеев александр михайлович
Номер: 9258488251 
Метро: шоссе энтузиастов 
Адрес: шоссе энтузиастов, д.31д

Курьеру к оплате: 0 + 0
Итого: 0



🔴 отказ 13.06
Заказ от 03.06, исполнитель Тринити
Курьерская: Путилин (Тод)
Номер курьера: +79

Оператор: 18
ФИО: левкович денис михайлович
Номер: 9653365596 9135822746
Метро: пушкинская 

Курьеру к оплате: 5500 + 300
Итого: 5800

Причина отказа:
'''
