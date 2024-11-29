from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from data.base_data import company_dlv
from enums import BaseCB


# # курьерская для забора
# def take_order_company_kb() -> InlineKeyboardMarkup:
#     kb = InlineKeyboardBuilder()
#     for comp_id, name in company.items():
#         kb.button(text=name, callback_data=f'{BaseCB.TAKE_ORDER_1.value}:{comp_id}')
#
#     return kb.adjust(1).as_markup()


# кнопка отмены
def get_close_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='❌ Отмена', callback_data=BaseCB.CLOSE.value)

    return kb.adjust(1).as_markup()
