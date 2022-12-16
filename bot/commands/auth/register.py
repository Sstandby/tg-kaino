import re
from bot import kaino, countryList
from bot.common.db.users import register_user
from telebot.types import ReplyKeyboardMarkup
from telebot.asyncio_handler_backends import State, StatesGroup

class MyStates(StatesGroup):
    fullname = State()
    phone = State()
    country = State()
    email = State()
    response = State()

user_text = """
⠀⠀⠀⠀⠀ ⠀⠀<b>༼kaino༽</b>.

      ⸙͎ Selecciona la opción que
    ⸙͎ mas se ajuste a tu situación.
⸙͎ para su registro en kaino.

"""

fullname_text = """
✎ Digite su nombre para registrarte (nombres y apellidos, recuerde que toda la información que se le pida sera privada, y nadie la vera).
"""

phone_text = """
✎ Digite su numero de celular, recuerde (poner codigo de país).
"""

country_text = """
✎ Digite su país, por favor.
"""

email_text = """
✎ Digite su correo electronico, recuerde que es importante poner todo correctamente en caso de rembolsos.
"""

existing_user_text = """
⠀✎ Por favor, ponga un username en
⠀✎ su perfil de telegram, para tener
⠀⠀⠀✎ un identificador unico.
"""

response_error_text = """
⠀✎ Elija correctamente algunas de
⠀✎ las opciones que se muestran
⠀⠀⠀⠀✎ en los botones: /token.
"""


@kaino.message_handler(commands=['register'], chat_types=['private'])
async def register(message):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Selecciona alguna de las opciónes")
    markup.add("Registrar","Actualizar")
    await kaino.set_state(message.from_user.id, MyStates.response, message.chat.id)
    await kaino.reply_to(message, user_text, parse_mode="html", reply_markup=markup)

@kaino.message_handler(state=MyStates.response,  chat_types=['private'])
async def response_token(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['response'] = message.text
        response = data['response']
        if response == "Registrar" or response == "Cambiar":
           await kaino.reply_to(message, fullname_text, parse_mode="html", disable_web_page_preview=True)
           await kaino.set_state(message.from_user.id, MyStates.fullname, message.chat.id)
        else:
           await kaino.reply_to(message, response_error_text, parse_mode="html")

@kaino.message_handler(state=MyStates.fullname, chat_types=['private'])
async def register_fullname(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['fullname'] = message.text
        await kaino.reply_to(message, phone_text, parse_mode="html", disable_web_page_preview=True)
        await kaino.set_state(message.from_user.id, MyStates.phone, message.chat.id)

@kaino.message_handler(state=MyStates.phone, chat_types=['private'])
async def register_phone(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['phone'] = message.text
        await kaino.reply_to(message, email_text, parse_mode="html", disable_web_page_preview=True)
        await kaino.set_state(message.from_user.id, MyStates.email, message.chat.id)

@kaino.message_handler(state=MyStates.email, chat_types=['private'])
async def register_email(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['email'] = message.text
        await kaino.reply_to(message, country_text, parse_mode="html", disable_web_page_preview=True)
        await kaino.set_state(message.from_user.id, MyStates.country, message.chat.id)

@kaino.message_handler(state=MyStates.country, chat_types=['private'])
async def register_country(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        update = True
        country = message.text
        email = data['email']
        fullname = data['fullname']
        phone = data['phone']
        if data['response'] == "Registrar": update = False
        username =  message.from_user.username
        for key in countryList:
            countryTrue = re.search(country, countryList[key])
            if countryTrue:
                if message.from_user.username:
                    if await register_user(fullname, country, phone, email, username, update):
                        await kaino.reply_to(message, f"✎ ¡Su usuario ha sido registrado con exito! ")
                    else:
                        await kaino.reply_to(message, f"✎ ¡No puede registrarse, su usuario ya existe en la base de datos..! ")
                else:
                    await kaino.reply_to(message, existing_user_text)
            else:
                await kaino.reply_to(message, f"✎ ¡No puede registrarse, el país que puso no existe, por favor, vuelva a ponerlo!")
                await kaino.set_state(message.from_user.id, MyStates.country, message.chat.id)
        await kaino.delete_state(message.from_user.id, message.chat.id)