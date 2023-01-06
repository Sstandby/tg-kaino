# -*- coding: utf-8 -*
from bot import kaino
from datetime import date
from bot.common.db.users import register_deriv
from telebot.types import ReplyKeyboardMarkup
from telebot.asyncio_handler_backends import State, StatesGroup
from bot.common.db.users import get_deriv_pass, get_deriv_user, get_user_info

token_text = """
⠀⠀⠀⠀⠀ ⠀⠀<b>༼MT5༽</b>.

       ⸙͎ Selecciona la opción que
     ⸙͎ mas se ajuste a tu situación.
 ⸙͎ para registar su cuenta para MT5.
"""

api_text = """
✎ Digite su ID de ACCESO, respondiendo este mensaje.
"""

pass_text = """
✎ Digite la contraseña de la cuenta.
"""

response_error_text = """
⠀✎ Elija correctamente algunas de
⠀✎ las opciones que se muestran
⠀⠀⠀⠀✎ en los botones: /deriv.
"""

existing_user_text = """
⠀✎ Por favor, ponga un username en
⠀✎ su perfil de telegram, para tener
⠀⠀⠀✎ un identificador unico.
"""

apideriv_text = """
✎ Por favor, digite su api de Deriv.
✎ <a href="https://api.deriv.com/app-registration">DERIV API.</a>
"""

kain_text = """
> Usuario: {}
> Pago: True
> Cuenta MT5: {}
> Contraseña MT5: {}
> correo: {}
> celular: {}
> Fecha: {}
"""


class MyStateDeriv(StatesGroup):
    response_deriv = State()
    token = State()
    password = State()
    api = State()


@kaino.message_handler(existing_user=True, membership=True, commands=['deriv'], chat_types=['private'])
async def deriv(message):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Selecciona alguna de las opciónes")
    markup.add("Registrar","Cambiar")
    await kaino.set_state(message.from_user.id, MyStateDeriv.response_deriv, message.chat.id)
    await kaino.reply_to(message, token_text, parse_mode="html", reply_markup=markup)

@kaino.message_handler(state=MyStateDeriv.response_deriv,  chat_types=['private'])
async def deriv_option(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['response'] = message.text
        response = data['response']
        if response == "Registrar" or response == "Cambiar":
           await kaino.reply_to(message, api_text, parse_mode="html", disable_web_page_preview=True)
           await kaino.set_state(message.from_user.id, MyStateDeriv.api, message.chat.id)
        else:
           await kaino.reply_to(message, response_error_text, parse_mode="html")

# @kaino.message_handler(state=MyStateDeriv.token,  chat_types=['private'])
# async def api_mt5(message):
#     async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
#         data['token'] = message.text
#         if data['token'].isdigit():
#             await kaino.reply_to(message, apideriv_text, parse_mode="html", disable_web_page_preview=True)
#             await kaino.set_state(message.from_user.id, MyStateDeriv.api, message.chat.id)
#         else:
#             await kaino.reply_to(message, "✎ Por favor, revise que no hayan caracteres en su ID de cuenta.", parse_mode="html", disable_web_page_preview=True)

@kaino.message_handler(state=MyStateDeriv.api,  chat_types=['private'])
async def api_deriv(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['token'] = message.text
        if data['token'].isdigit():
            await kaino.reply_to(message, pass_text, parse_mode="html", disable_web_page_preview=True)
            await kaino.set_state(message.from_user.id, MyStateDeriv.password, message.chat.id)

@kaino.message_handler(state=MyStateDeriv.password,  chat_types=['private'])
async def password_mt5(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        update = True
        password = message.text
        token = data['token']
        username =  message.from_user.username

        if data['response'] == "Registrar": update = False
        if message.from_user.username:
            if await register_deriv(token, username, password, update):
                password = await get_deriv_pass(username)
                user = await get_deriv_user(username)
                info = await get_user_info(username)
                await kaino.send_message(617961155, kain_text.format(message.from_user.username, user, password, info.email, info.phone,  date.today()))
                await kaino.reply_to(message, f"✎ ¡Su cuenta ha sido registrado con exito! ")
            else:
                await kaino.reply_to(message, f"✎ ¡Actualice no registre, su usuario ya existe en la base de datos..! ")
        else:
            await kaino.reply_to(message, existing_user_text)
    await kaino.delete_state(message.from_user.id, message.chat.id)
