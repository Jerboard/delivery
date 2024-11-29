import gspread
import logging
import asyncio
import re

from gspread.spreadsheet import Spreadsheet
from datetime import datetime

import db
from config import Config
from utils.local_data_utils import get_table_id
from enums import OrderStatus, active_status_list, CompanyOPR, UserRole


# (a - 0, b - 1, c - 2, d - 3, e - 4, f - 5, g - 6, h - 7, i - 8, j - 9, k - 10,
#  l - 11, m - 12, n - 13, o - 14, p - 15, q - 16, r - 17, s - 18, t - 19, u - 20,
#  v - 21, w - 22, x - 23, y - 24, z - 25.)
test_table = '12Sm-PMgBy_ANC2WuesE8WWo_sawyaqx4QeMlkWTVfmM'


def get_google_connect(table_id: str = None) -> Spreadsheet:
    gc = gspread.service_account (filename=Config.file_google_path)
    if not table_id:
        table_id = get_table_id()
    return gc.open_by_key (table_id)


# проверяет подключение к таблице
def is_table_exist(tab_id: str) -> bool:
    gc = gspread.service_account(filename=Config.file_google_path)
    try:
        gc.open_by_key(tab_id)
        return True
    except:
        return False


async def add_order_in_google_table(sh: Spreadsheet, row_num: int, row: list, order_id: int):
    cell = f'a{row_num}:z{row_num}'
    row[0] = order_id
    sh.sheet1.update(cell, [row[:26]])
    await asyncio.sleep (1)
    cell = f'ab{row_num}'
    sh.sheet1.update (cell, row [27])
    logging.warning (f'Новая строка в таблицу:\n{row [:26]}\nAB: {row [27]}, Z: {row [25]} 24-30: {row [24:30]}')


async def update_order_in_google_table(sh: Spreadsheet, row: list):
    find_row = sh.sheet1.find (query=row[0], in_column=1)
    number_row = find_row.row
    cell = f'a{number_row}:z{number_row}'
    sh.sheet1.update(cell, [row[:26]])

    await asyncio.sleep(1)
    cell = f'ab{number_row}'
    sh.sheet1.update (cell, row [27])


# Очистить таблицу
def clear_new_order_table(sh: Spreadsheet, last_row: int):
    cell = f'a2:al{last_row + 1}'
    col = {"red": 1, "green": 1, "blue": 1}
    empty_list = [''] * 37
    del_list = [empty_list] * last_row
    sh.get_worksheet(1).update(cell, del_list)
    sh.get_worksheet(1).format (cell, {"backgroundColor": col})


#  подбирает цвет
def choice_color(status: str):
    if status in [OrderStatus.SUC.value, OrderStatus.SUC_TAKE.value]:
        color = {"red": 0.39, "green": 0.93, "blue": 0.54}
    elif status == OrderStatus.SEND.value:
        color = {"red": 1, "green": 0.53, "blue": 0}
    elif status in active_status_list:
        color = {"red": 1.0, "green": 1.0, "blue": 0.0}
    elif status in [OrderStatus.REF.value, OrderStatus.REF_TAKE.value]:
        color = {"red": 1.0, "green": 0.0, "blue": 0.0}
    else:
        color = {"red": 1.0, "green": 1.0, "blue": 1.0}
    return color


# создаёт словарь с актуальными операторами
async def get_company_dict(role: str) -> dict:
    users = await db.get_users(role=role)
    comp_dict = {}
    for user in users:
        opr_list = comp_dict.get(user.company, [])
        opr_list.append(user.name)
        comp_dict[user.company] = opr_list

    return comp_dict


# проверяет операторскую заказа
def check_comp_name(name: str, comp_dict: dict) -> str:
    for k, v in comp_dict.items():
        if name in v:
            return k
