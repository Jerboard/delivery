from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

import db
import keyboards as kb
from init import bot, dp
from utils import text_utils as txt
from enums import OwnerCB


async def owner_start(user_id: int, msg_id: int = None):
    statistic = await db.get_orders_statistic (own_text=True)
    statistic_text = txt.get_statistic_text (statistic)
    text = f'Заказы\n\n{statistic_text}'

    if msg_id:
        try:
            await bot.edit_message_text (chat_id=user_id, message_id=msg_id, text=text, reply_markup=kb.main_owner_kb ())
        except Exception as ex:
            pass
    else:
        await bot.send_message (user_id, text, reply_markup=kb.main_owner_kb ())


# назад к экрану админа
@dp.callback_query(lambda cb: cb.data.startswith(OwnerCB.BACK.value))
async def back_owner(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await owner_start(cb.from_user.id, msg_id=cb.message.message_id)
