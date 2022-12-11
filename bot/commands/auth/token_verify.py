# -*- coding: utf-8 -*
from bot import kaino
from bot.common.db.users import register
from telebot.types import ReplyKeyboardMarkup
from telebot.asyncio_handler_backends import State, StatesGroup

token_text = """
⠀⠀⠀⠀⠀ ⠀⠀<b>༼TOKEN༽</b>.

      ⸙͎ Selecciona la opción que
    ⸙͎ mas se ajuste a tu situación.
⸙͎ para su token de binance.

"""

change_text = """
✎ Digite su API KEY, respondiendo este mensaje.
✎ <a href="https://www.binance.com/es/support/faq/c%C3%B3mo-crear-una-api-360002502072">BINANCE API.</a>
"""

pass_text = """
✎ Digite su contraseña con la que quiere cifrar su token.
"""

secret_text = """
✎ Digite su API SECRET, respondiendo este mensaje.
✎ <a href="https://www.binance.com/es/support/faq/c%C3%B3mo-crear-una-api-360002502072">BINANCE API.</a>
"""

response_error_text = """
⠀✎ Elija correctamente algunas de
⠀✎ las opciones que se muestran
⠀⠀⠀⠀✎ en los botones: /token.
"""

existing_user_text = """
⠀✎ Por favor, ponga un username en
⠀✎ su perfil de telegram, para tener
⠀⠀⠀✎ un identificador unico.

"""

class MyStates(StatesGroup):
    response = State()
    token = State()
    secret = State()
    password = State()



@kaino.message_handler(commands=['token'], chat_types=['private'])
async def token(message):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Selecciona alguna de las opciónes")
    markup.add("Registrar","Cambiar")
    await kaino.set_state(message.from_user.id, MyStates.response, message.chat.id)
    await kaino.reply_to(message, token_text, parse_mode="html", reply_markup=markup)

@kaino.message_handler(state=MyStates.response,  chat_types=['private'])
async def response_token(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['response'] = message.text
        response = data['response']
        if response == "Registrar" or response == "Cambiar":
           await kaino.reply_to(message, change_text, parse_mode="html", disable_web_page_preview=True)
           await kaino.set_state(message.from_user.id, MyStates.token, message.chat.id)
        else:
           await kaino.reply_to(message, response_error_text, parse_mode="html")

@kaino.message_handler(state=MyStates.token,  chat_types=['private'])
async def change_token(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['token'] = message.text
        await kaino.reply_to(message, secret_text, parse_mode="html", disable_web_page_preview=True)
        await kaino.set_state(message.from_user.id, MyStates.secret, message.chat.id)

@kaino.message_handler(state=MyStates.secret,  chat_types=['private'])
async def change_secret(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['secret'] = message.text
        await kaino.reply_to(message, pass_text)
        await kaino.set_state(message.from_user.id, MyStates.password, message.chat.id)

@kaino.message_handler(state=MyStates.password,  chat_types=['private'])
async def password_token(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        update = True
        password = message.text
        token = data['token']
        secret = data['secret']
        username =  message.from_user.username

        if data['response'] == "Registrar": update = False
        if message.from_user.username:
            if await register(token, secret, username, password, update):
                await kaino.reply_to(message, f"✎ ¡Su token ha sido registrado con exito! ")
            else:
                await kaino.reply_to(message, f"✎ ¡No puede registrarse, su usuario ya existe en la base de datos..! ")
        else:
            await kaino.reply_to(message, existing_user_text)
    await kaino.delete_state(message.from_user.id, message.chat.id)
