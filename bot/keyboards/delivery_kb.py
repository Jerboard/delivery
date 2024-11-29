from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import db
from data.base_data import expensis_dlv, letters
from enums import DeliveryCB, BaseCB, OrderAction, OrderStatus, TypeOrderButton, CompanyDLV


# отправить контакт
def get_send_contact_kb():
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text='📱 Отправить номер', request_contact=True)]
    ])


# клавиатура ЛК курьера
def main_dvl_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.button(text='🖊 Сменить имя', callback_data=f'{DeliveryCB.EDIT_PROFILE.value}:name')
    kb.button(text='📱 Сменить номер телефона', callback_data=f'{DeliveryCB.EDIT_PROFILE.value}:phone')
    kb.button(text='📝 Отчёт', callback_data=DeliveryCB.REPORT_1.value)
    kb.button(text='💸 Траты', callback_data=DeliveryCB.EXPENSES_1.value)
    kb.button(text='💵 Траты сегодня', callback_data=DeliveryCB.EXPENSES_VIEW.value)
    return kb.adjust(2).as_markup()


# клава для курьера свободный заказ
def get_free_order_kb(order_id: int, type_order: str, dlv_name: str = None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if type_order == TypeOrderButton.BASE.value:
        kb.button(text='📦 Взять в работу', callback_data=f'{DeliveryCB.ORDER_1.value}:{order_id}')
    elif type_order == TypeOrderButton.TAKE.value:
        kb.button (text='📦 Взять в работу', callback_data=f'{DeliveryCB.TAKE_ORDER_2.value}:{order_id}')
    else:
        kb.button (text=f'⭕️ Забрать у курьера {dlv_name} ⭕️',
                   callback_data=f'{DeliveryCB.PICKUP_ORDER_1.value}:{order_id}:conf')
    return kb.adjust (1).as_markup ()


# клава для курьера свободное сообщение
def get_dlv_main_order_kb(order_id: int, order_status: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if order_status == OrderStatus.ACTIVE.value:
        kb.button(text='✅ Доставлен', callback_data=f'{DeliveryCB.ORDER_2.value}:{order_id}:{OrderAction.SUC.value}')
    else:
        kb.button(text='✅ Забрал', callback_data=f'{DeliveryCB.ORDER_7.value}:{order_id}:{OrderAction.SUC_TAKE.value}')

    kb.button(text='❌ Отказ', callback_data=f'{DeliveryCB.REF_ORDER_1.value}:{order_id}')
    kb.button(text='❌ Частичный отказ', callback_data=f'{DeliveryCB.ORDER_2.value}:{order_id}:{OrderAction.REF.value}')

    # if order_status == OrderStatus.ACTIVE.value:
    kb.button(
        text='✖️ Клиент не явился',
        callback_data=f'{DeliveryCB.ORDER_4.value}:{order_id}:{OrderAction.NOT_COME.value}:d'
        # callback_data=f'{DeliveryCB.ORDER_7.value}:{order_id}:{OrderAction.NOT_COME.value}'
    )
    kb.button(text='↩️ Передать другому курьеру', callback_data=f'{DeliveryCB.ORDER_3.value}:{order_id}')
    return kb.adjust(1).as_markup()


# основная клавиатура закрытия заказа
def get_close_order_option_kb(order_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='✅ Закрыть заказ',
        callback_data=f'{DeliveryCB.ORDER_7.value}:{order_id}:{OrderAction.SUC.value}')
    kb.button(
        text='🖍 Изменить стоимость',
        callback_data=f'{DeliveryCB.ORDER_6.value}:{OrderAction.COST.value}:{order_id}')
    kb.button(
        text='🖍 Изменить цену доставки',
        callback_data=f'{DeliveryCB.ORDER_6.value}:{OrderAction.DELI.value}:{order_id}')
    kb.button(text='🔙 Назад', callback_data=f'{DeliveryCB.BACK_MAIN_ORDER.value}:{order_id}')
    return kb.adjust(1).as_markup()


# вернуться к закрытию заказа
def get_back_close_order_kb(order_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Назад', callback_data=f'{DeliveryCB.BACK_CLOSE_ORDER.value}:{order_id}')
    return kb.adjust(1).as_markup()


# вернуться в главное меню
def get_main_dlv_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Назад', callback_data=f'{DeliveryCB.BACK_MAIN.value}')
    return kb.adjust(1).as_markup()


# выбрать букву при закрытии заказа
def get_done_order_letters_kb(order_id: int, order_action: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for k, v in letters.items ():
        kb.button (text=v, callback_data=f'{DeliveryCB.ORDER_4.value}:{order_id}:{order_action}:{k}')
    kb.button(text='🔙 Назад', callback_data=f'{DeliveryCB.BACK_CLOSE_ORDER.value}:{order_id}')
    return kb.adjust(1).as_markup()


# кнопка подтвердить Отказа от заказа
def get_pickup_order_kb(order_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='✅ Забрать', callback_data=f'{DeliveryCB.PICKUP_ORDER_2.value}:{order_id}')
    # kb.button(text='✅ Подтвердить', callback_data=f'{DeliveryCB.PICKUP_ORDER_2.value}:{order_id}')
    kb.button(text='❌ Отмена', callback_data=f'{DeliveryCB.PICKUP_ORDER_1.value}:{order_id}:back')
    return kb.adjust(1).as_markup()


# выбрать букву при отправке зп
def get_expensis_let_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for k, v in letters.items():
        kb.button (text=v, callback_data=f'{DeliveryCB.EXPENSES_5.value}:{k}')

    kb.button (text='❌ Отмена', callback_data=BaseCB.CLOSE.value)
    return kb.adjust(1).as_markup()


# кнопка подтвердить Отказа от заказа
def get_close_order_kb(order_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='✅ Подтвердить отказ', callback_data=f'{DeliveryCB.REF_ORDER_2.value}:{order_id}')
    kb.button(text='🔙 Назад', callback_data=f'{DeliveryCB.BACK_MAIN_ORDER.value}:{order_id}')
    return kb.adjust(1).as_markup()


# передать заказ
def get_transfer_order_kb(users: tuple[db.UserRow], order_id) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Назад', callback_data=f'{DeliveryCB.BACK_MAIN_ORDER.value}:{order_id}')
    for user in users:
        kb.button(text=user.name, callback_data=f'{DeliveryCB.TRANS_ORDER.value}:{user.user_id}:{order_id}')

    return kb.adjust(1, 2).as_markup()


# клавиатура трат курьера
def expenses_dvl_kb(comp: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    #  «ЗП» «Почта / СДЭК» «Премия» «Разное» 11, 14, 12
    kb.button (text='🔙 Назад', callback_data=DeliveryCB.BACK_MAIN.value)
    for k, v in expensis_dlv.items():
        if k == 1:
            kb.button(text=f'{v["emoji"]} {v["text"]}', callback_data=f'{DeliveryCB.EXPENSES_5.value}:start')
        else:
            if comp == CompanyDLV.POST:
                if k in [11, 14, 12]:
                    kb.button(text=f'{v["emoji"]} {v["text"]}', callback_data=f'{DeliveryCB.EXPENSES_2.value}:{k}')
            else:
                kb.button(text=f'{v["emoji"]} {v["text"]}', callback_data=f'{DeliveryCB.EXPENSES_2.value}:{k}')
        # kb.button(text=f'💸 {name}', callback_data=f'{DeliveryCB.EXPENSES_2.value}:{column}')

    return kb.adjust(1, 2).as_markup()


# дни просмотра отчёта
def report_view_days_kb(report_rows: tuple[db.ReportRow]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Сегодня', callback_data=f'{DeliveryCB.REPORT_2.value}:today')
    kb.button(text='🔙 Назад', callback_data=f'{DeliveryCB.BACK_MAIN.value}')

    for day_row in report_rows:
        kb.button(text=day_row.m, callback_data=f'{DeliveryCB.REPORT_2.value}:{day_row.m}')
    return kb.adjust(2).as_markup()


# отправить отчёт
def get_day_report_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    kb.button (text='📤 Отправить отчёт', callback_data=f'{DeliveryCB.REPORT_4.value}')
    kb.button (text='💸 Внести трату', callback_data=f'{DeliveryCB.EXPENSES_1.value}')
    return kb.adjust(1).as_markup()


# отправить отчёт
def get_send_day_report_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button (text='🔙 Назад', callback_data=f'{DeliveryCB.BACK_MAIN.value}')
    kb.button(text='📤 Отправить отчёт', callback_data=DeliveryCB.REPORT_3.value)
    return kb.adjust(1).as_markup()


# почтовые заказы
def get_post_order_kb(order_id: int, order_status) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    if order_status == OrderStatus.ACTIVE.value:
        kb.button (text='📯 Отправлен', callback_data=f'{DeliveryCB.POST_1.value}:{order_id}')
    elif order_status == OrderStatus.SEND.value:
        kb.button (
            text='✅ Доставлен',
            callback_data=f'{DeliveryCB.ORDER_4.value}:{order_id}:{OrderAction.SUC.value}:del'
        )
    kb.button (text='❌ Отказ', callback_data=f'{DeliveryCB.POST_2.value}:{order_id}')
    # kb.button(text='❌ Отказ', callback_data=f'{DeliveryCB.REF_ORDER_1.value}:{order_id}')


    return kb.adjust (1).as_markup ()


# отправленные сообщения просмотр
def get_view_send_orders(orders_date: dict) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    for k, v in orders_date.items():
        kb.button(text=f'{k} ({v})', callback_data=f'{DeliveryCB.SEND_ORDERS.value}:{k}')

    return kb.adjust(3).as_markup()
