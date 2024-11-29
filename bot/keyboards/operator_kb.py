from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

import db
from data.base_data import company_dlv, company_dlv_opr_bt
from enums import BaseCB, OperatorCB, UserRole, OwnerCB, OrderStatus


# основная клавиатура оператора
def get_main_opr_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.button (text='⚪️ Без статуса', callback_data=f'{OperatorCB.VIEW_ORDER_1.value}:{OrderStatus.NEW.value}')
    kb.button (text='⚪️ Без статуса', callback_data=f'{OperatorCB.VIEW_ORDER_2.value}:{OrderStatus.NEW.value}:0')
    kb.button (text='🟢 Доставлен', callback_data=f'{OperatorCB.VIEW_ORDER_1.value}:{OrderStatus.SUC.value}')
    kb.button (text='🟠 Отправлен', callback_data=f'{OperatorCB.VIEW_ORDER_1.value}:{OrderStatus.SEND.value}')
    kb.button (text='🟡 На руках', callback_data=f'{OperatorCB.VIEW_ORDER_1.value}:{OrderStatus.ACTIVE.value}')
    kb.button (text='🔴 Отказ', callback_data=f'{OperatorCB.VIEW_ORDER_1.value}:{OrderStatus.REF.value}')
    kb.button (text='🔵 Оформить забор', callback_data=f'{OperatorCB.TAKE_ORDER_0.value}')
    return kb.adjust (2).as_markup ()


# курьерская для забора
def take_order_company_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button (text='🔙 Назад', callback_data=OperatorCB.BACK_MAIN.value)
    for comp_id, name in company_dlv_opr_bt.items():
        kb.button(text=name, callback_data=f'{OperatorCB.TAKE_ORDER_1.value}:{comp_id}')

    return kb.adjust(1).as_markup()


# курьерская для забора
def get_take_order_kb(role: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='❌ Отмена', callback_data=BaseCB.CLOSE.value)
    if role == UserRole.OPR.value:
        kb.button(text='✅ Подтвердить', callback_data=OperatorCB.TAKE_ORDER_2.value)
    elif role == UserRole.OWN.value:
        kb.button(text='✅ Подтвердить', callback_data=OwnerCB.ADD_ORDER.value)
    return kb.as_markup()


# выбрать день отчёта
def get_opr_day_report_kb(orders: tuple[db.OprReportRow], order_status: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button (text='🔙 Назад', callback_data=OperatorCB.BACK_MAIN.value)
    for order in orders:
        date = order.date if order_status != OrderStatus.NEW else 'Без курьера'
        kb.button(
            text=f'{date} ({order.orders_count})',
            callback_data=f'{OperatorCB.VIEW_ORDER_2.value}:{order_status}:{order.date}')

    return kb.adjust(1, 2).as_markup()