from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

import db
from data.base_data import company_dlv, company_opr
from enums import OwnerCB, UserRole


# клавиатура владельца на кнопке старт
def main_owner_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='📄 Добавить/Обновить заказы', callback_data=f'{OwnerCB.UPDATE_TABLE.value}:order')
    kb.button(text='📄 Добавить/Обновить отчеты', callback_data=f'{OwnerCB.UPDATE_TABLE.value}:report')
    kb.button(text='🏃 Добавить Курьера', callback_data=f'{OwnerCB.ADD_USER_1.value}:{UserRole.DLV.value}')
    kb.button(text='🧑‍💻 Добавить Оператора', callback_data=f'{OwnerCB.ADD_USER_1.value}:{UserRole.OPR.value}')
    kb.button(text='🏃‍♂️ Удалить Курьера', callback_data=f'{OwnerCB.DEL_USER_1.value}:{UserRole.DLV.value}')
    kb.button(text='🙅 Удалить Оператора', callback_data=f'{OwnerCB.DEL_USER_1.value}:{UserRole.OPR.value}')
    kb.button(text='🗒 У Курьера', callback_data=f'{OwnerCB.VIEW_ORDERS_1.value}')
    kb.button(text='🗒 Без Курьера', callback_data=f'{OwnerCB.VIEW_FREE_ORDERS.value}:0')
    kb.button (text='📝 Сменить таблицу', callback_data=f'{OwnerCB.CHANGE_TAB.value}')
    # kb.button(text='📤 Выгрузить данные', callback_data=f'{OwnerCB.UPDATE_USERS_TABLE_1.value}')
    # kb.button(text='📥 Загрузить данные', callback_data=f'{OwnerCB.UPDATE_USERS_TABLE_2.value}')
    return kb.adjust(1, 1, 2).as_markup()


# Владелец для заказов на руках
def get_hard_update_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Принудительно обновить', callback_data=f'{OwnerCB.HARD_UPDATE.value}')
    return kb.adjust(1).as_markup()


# список курьерских для добавления курьера
def get_add_dlv_comp_kb(role: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    comp = company_dlv if role == UserRole.DLV else company_opr
    kb.button(text='🔙 Назад', callback_data=OwnerCB.BACK.value)
    for k, v in comp.items():
        kb.button(text=v, callback_data=f'{OwnerCB.ADD_USER_2.value}:{role}:{k}')

    return kb.adjust(1, 2).as_markup()


# Владелец для заказов на руках
def get_busy_order_own_kb(order_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Снять', callback_data=f'{OwnerCB.MAKE_ORDER_FREE.value}:{order_id}')
    kb.button(text='Передать', callback_data=f'{OwnerCB.TRANS_ORDER_1.value}:{order_id}')
    return kb.adjust(2).as_markup()


# кнопка назначить заказ заказа
def get_free_order_own_kb(order_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    kb.button (text='Назначить', callback_data=f'{OwnerCB.TRANS_ORDER_1.value}:{order_id}')
    return kb.as_markup ()


# вернуть заказ курьеру
def get_close_order_own_kb(order_id: int, dlv_name: str, user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    kb.button (
        text=f'↪️ Вернуть курьеру {dlv_name}',
        callback_data=f'{OwnerCB.TRANS_ORDER_2.value}:{user_id}:{order_id}')
    return kb.as_markup ()


# список пользователей на удаление
def get_del_user_kb(users: tuple[db.UserRow], user_role: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    kb.button (text='🔙 Назад', callback_data=OwnerCB.BACK.value)
    for user in users:
        kb.button (text=user.name, callback_data=f'{OwnerCB.DEL_USER_2.value}:{user.user_id}:{user_role}')

    return kb.adjust (1, 2).as_markup ()


# список кур назначитьзаказ
def get_trans_orders_users_kb(users: tuple[db.UserRow], order_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    kb.button (text='🔙 Назад', callback_data=f'{OwnerCB.BACK_FREE.value}:{order_id}')
    for user in users:
        kb.button (text=user.name, callback_data=f'{OwnerCB.TRANS_ORDER_2.value}:{user.user_id}:{order_id}')

    return kb.adjust (1, 2).as_markup ()


# список курьеров и их заказы
def get_orders_users_own_kb(users: tuple[db.OrderGroupRow]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    kb.button (text='🔙 Назад', callback_data=OwnerCB.BACK.value)
    for user in users:
        kb.button (
            text=f'{user.name} ({user.orders_count})',
            callback_data=f'{OwnerCB.VIEW_ORDERS_2.value}:{user.name}')

    return kb.adjust (1, 2).as_markup ()


# просмотр свободных заказов
def get_view_free_order_own_kb(start: int, next_page: bool, order_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    kb.button (text='Назначить', callback_data=f'{OwnerCB.TRANS_ORDER_1.value}:{order_id}')
    start_next = start + 20
    start_back = start - 20
    if start_back >= 0:
        kb.button (text='⬅️️ Назад', callback_data=f'{OwnerCB.VIEW_FREE_ORDERS.value}:{start_back}')
    if next_page:
        kb.button (text='➡️ Вперёд', callback_data=f'{OwnerCB.VIEW_FREE_ORDERS.value}:{start_next}')
    return kb.adjust(1, 2).as_markup ()
