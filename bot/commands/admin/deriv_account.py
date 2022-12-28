# -*- coding: utf-8 -*
from bot import kaino
from bot.common.db.users import get_deriv_pass, get_deriv_user, existing_user
from telebot.types import ReplyKeyboardMarkup
from telebot.asyncio_handler_backends import State, StatesGroup

search_text = """
✎ Digite el usuario al que quiere tener su cuenta de MT5.
"""

error_text = """
✎ Este usuario no existe en la DB
"""

info_text = """
✎ id de acceso: {user}
✎ pass: {password}
"""

class MyStates(StatesGroup):
    username = State()

@kaino.message_handler(is_admin=True, commands=['searchDeriv'])
async def deriv_account(message):
    await kaino.reply_to(message, search_text, parse_mode="html")
    await kaino.set_state(message.from_user.id, MyStates.username, message.chat.id)

@kaino.message_handler(state=MyStates.username)
async def data_deriv(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        if await existing_user(message.text):
            password = await get_deriv_pass(message.text)
            user = await get_deriv_user(message.text)
            await kaino.reply_to(message, info_text.format(user=user, password=password), parse_mode="html")
        else:
            await kaino.reply_to(message, error_text, parse_mode="html")
