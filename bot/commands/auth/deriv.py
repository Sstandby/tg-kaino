# -*- coding: utf-8 -*
from bot import kaino
from bot.common.db.users import register_deriv
from telebot.types import ReplyKeyboardMarkup
from telebot.asyncio_handler_backends import State, StatesGroup

token_text = """
⠀⠀⠀⠀⠀ ⠀⠀<b>༼TOKEN༽</b>.

      ⸙͎ Selecciona la opción que
    ⸙͎ mas se ajuste a tu situación.
   ⸙͎ para registar su cuenta para MT5.
"""

api_text = """
✎ Digite su API_ACCESO, respondiendo este mensaje.
"""

pass_text = """
✎ Digite la contraseña de la cuenta.
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
    password = State()



@kaino.message_handler(existing_user=True, commands=['token'], chat_types=['private'])
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
           await kaino.reply_to(message, api_text, parse_mode="html", disable_web_page_preview=True)
           await kaino.set_state(message.from_user.id, MyStates.token, message.chat.id)
        else:
           await kaino.reply_to(message, response_error_text, parse_mode="html")

@kaino.message_handler(state=MyStates.token,  chat_types=['private'])
async def api_mt5(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['token'] = message.text
        await kaino.reply_to(message, pass_text, parse_mode="html", disable_web_page_preview=True)
        await kaino.set_state(message.from_user.id, MyStates.password, message.chat.id)

@kaino.message_handler(state=MyStates.password,  chat_types=['private'])
async def password_mt5(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        update = True
        password = message.text
        token = data['token']
        username =  message.from_user.username

        if data['response'] == "Registrar": update = False
        if message.from_user.username:
            if await register_deriv(token, username, password, update):
                await kaino.reply_to(message, f"✎ ¡Su token ha sido registrado con exito! ")
            else:
                await kaino.reply_to(message, f"✎ ¡No puede registrarse, su usuario ya existe en la base de datos..! ")
        else:
            await kaino.reply_to(message, existing_user_text)
    await kaino.delete_state(message.from_user.id, message.chat.id)
