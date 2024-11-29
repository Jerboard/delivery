import asyncio
import logging
import sys

from handlers import dp
from config import DEBUG
from init import set_main_menu, bot, log_error
from db.base import init_models, create_trigger
from utils.schedulers_util import start_scheduler, update_order_date
from utils.local_data_utils import create_local_data_files
# from google_api.base_google import save_new_order_table
from utils.local_data_utils import save_table_id, get_table_id


async def main() -> None:
    # await save_new_order_table('12Sm-PMgBy_ANC2WuesE8WWo_sawyaqx4QeMlkWTVfmM')
    # await update_order_date()
    create_local_data_files()
    await init_models()
    await set_main_menu()
    if not DEBUG:
        await start_scheduler()
    else:
        pass
        await start_scheduler ()
    await bot.delete_webhook (drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    if DEBUG:
        # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        logging.basicConfig(level=logging.WARNING, stream=sys.stdout)
        # log_error('start_bot', with_traceback=False)
    else:
        log_error('start_bot', with_traceback=False)
    asyncio.run(main())
