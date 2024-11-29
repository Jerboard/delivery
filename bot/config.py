import os
from pytz import timezone

from enums import CompanyDLV

DEBUG = bool(int(os.getenv('DEBUG')))


class Config:
    if DEBUG:
        token = os.getenv ("TOKEN_TEST")
        # db_url = os.getenv ('DB_URL')
        # db_url = os.getenv ('DB_URL_WORK')
        bot_name = 'tushchkan_test_3_bot'

    else:
        token = os.getenv ("TOKEN")
        # db_url = os.getenv ('DB_URL')
        bot_name = 'MatrixDeliveryBot'

    tz = timezone('Europe/Moscow')

    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('POSTGRES_DB')
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_url = f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

    report_sheet_num = 6
    day_form = '%d.%m'
    datetime_form = '%d.%m.%Y %H:%M'
    time_form = '%H:%M'

    file_google_path = os.path.join ('data', 'cred.json')
    data_path = 'data'
    table_file_filename = 'google_table.txt'
    opr_send_users_filename = 'opr_send_users_msg.json'
    expenses_log = 'expenses_log.txt'
