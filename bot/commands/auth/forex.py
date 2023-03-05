# -*- coding: utf-8 -*
from bot import kaino
from telebot.asyncio_handler_backends import State, StatesGroup
from bot.common.db.users import register_forex

user_text = """
⸙͎ Para realizar este registro digite la
⸙͎ información que se le pedira hasta completar su registro para FOREX.

⊱ Digite su ID de usuario, por favor.
"""

server_text = """
⊱ Digite el servidor que esta usando, por favor.
"""

pass_text = """
⊱ Digite la contraseña de la cuenta, por favor.
"""

trader_text = """
⊱ Digite el trader con quien quiere que opere su cuenta, por favor.
"""

forexTrue_text = """
✎ Usuario de telegram: {}
✎ User: {}
✎ Server: {}
✎ Password: {}
⊱ Trader: {}
"""

completedForex_text = """
🦁 ¡Su registro fue exitosamente hecho!
⊱  Recuerde que tenemos otros excelentes
⊱  servicios en /help
"""

class MyStateForex(StatesGroup):
    user = State()
    server = State()
    password = State()
    trader = State()

@kaino.message_handler(existing_forex=True, membership=True, commands=['forex'], chat_types=['private'])
async def forex_command(message):
    await kaino.set_state(message.from_user.id, MyStateForex.user, message.chat.id)
    await kaino.reply_to(message, user_text, parse_mode="html")

@kaino.message_handler(state=MyStateForex.user, chat_types=['private'])
async def forex_user(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user'] = message.text
        await kaino.reply_to(message, server_text, parse_mode="html", disable_web_page_preview=True)
        await kaino.set_state(message.from_user.id, MyStateForex.server, message.chat.id)

@kaino.message_handler(state=MyStateForex.server, chat_types=['private'])
async def forex_server(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['server'] = message.text
        await kaino.reply_to(message, trader_text, parse_mode="html", disable_web_page_preview=True)
        await kaino.set_state(message.from_user.id, MyStateForex.trader, message.chat.id)

@kaino.message_handler(state=MyStateForex.trader, chat_types=['private'])
async def forex_trader(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['trader'] = message.text
        await kaino.reply_to(message, pass_text, parse_mode="html", disable_web_page_preview=True)
        await kaino.set_state(message.from_user.id, MyStateForex.password, message.chat.id)

@kaino.message_handler(state=MyStateForex.password, chat_types=['private'])
async def forex_password(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        if await register_forex(message.from_user.username, data['user'], data['server'], message.text, data['trader']):
            await kaino.reply_to(message, completedForex_text, parse_mode="html", disable_web_page_preview=True)
            await kaino.send_message(617961155, forexTrue_text.format(message.from_user.username, data['user'], data['server'], message.text, data['trader']))
