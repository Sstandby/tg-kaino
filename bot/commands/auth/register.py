import re
import unicodedata
from bot import kaino, countryList
from bot.common.db.users import register_user
from telebot.types import ReplyKeyboardMarkup
from telebot.asyncio_handler_backends import State, StatesGroup

class MyStates(StatesGroup):
    fullname = State()
    phone = State()
    country = State()
    inviteTrader = State()
    trader = State()
    email = State()
    response = State()

user_text = """
⠀⠀⠀⠀⠀ ⠀⠀<b>༼kaino༽</b>.

      ⸙͎ Selecciona la opción que
    ⸙͎ mas se ajuste a tu situación.
      ⸙͎ para su registro en kaino.
"""

fullname_text = """
✎ Digite su nombre para registrarse (nombres y apellidos, recuerde que toda la información que se le pida sera privada, y nadie la vera), por favor.
"""

traderName_text = """
✎ Digite su nombre de Trader, por favor.
"""

inviteTraderName_text = """
✎ Digite el nombre del Trader que lo invito. (Esto puede beneficiar en un futuro aquien lo invito.)
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

notIsValidEmail_text = """
✎ Su email no es valido, por favor, vuelve a ingresar todo correctamente de nuevo. (/register)
"""

existing_user_text = """
⠀✎ Por favor, ponga un username en
⠀✎ su perfil de telegram, para tener
⠀⠀⠀✎ un identificador unico.
"""

response_error_text = """
⠀✎ Elija correctamente algunas de
⠀✎ las opciones que se muestran
⠀⠀ ✎ en los botones de: /register.
"""

async def is_valid_email(email):
  return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is not None

async def remove_tildes(x):
    return unicodedata.normalize("NFD", x).encode("ascii", "ignore").decode("utf-8")

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
        if response == "Registrar" or response == "Actualizar":
           await kaino.reply_to(message, fullname_text, parse_mode="html", disable_web_page_preview=True)
           await kaino.set_state(message.from_user.id, MyStates.fullname, message.chat.id)
        else:
           await kaino.reply_to(message, response_error_text, parse_mode="html")
           await kaino.delete_state(message.from_user.id, message.chat.id)

@kaino.message_handler(state=MyStates.fullname, chat_types=['private'])
async def register_fullname(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['fullname'] = message.text
        await kaino.reply_to(message, traderName_text, parse_mode="html", disable_web_page_preview=True)
        await kaino.set_state(message.from_user.id, MyStates.trader, message.chat.id)

@kaino.message_handler(state=MyStates.trader, chat_types=['private'])
async def register_traderName(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['trader'] = message.text
        await kaino.reply_to(message, inviteTraderName_text, parse_mode="html", disable_web_page_preview=True)
        await kaino.set_state(message.from_user.id, MyStates.inviteTrader, message.chat.id)

@kaino.message_handler(state=MyStates.inviteTrader, chat_types=['private'])
async def register_inviteTrader(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['inviteTrader'] = message.text
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
        if await is_valid_email(message.text):
           await kaino.reply_to(message, country_text, parse_mode="html", disable_web_page_preview=True)
           await kaino.set_state(message.from_user.id, MyStates.country, message.chat.id)
        else:
           await kaino.reply_to(message, notIsValidEmail_text, parse_mode="html", disable_web_page_preview=True)

@kaino.message_handler(state=MyStates.country, chat_types=['private'])
async def register_country(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        update = True
        countryTrue = False
        country = message.text
        email = data['email']
        fullname = data['fullname']
        phone = data['phone']
        invite = data['inviteTrader']
        trader = data['trader']
        if data['response'] == "Registrar": update = False
        username =  message.from_user.username
        for key in countryList:
            countryTrue = re.search(await remove_tildes(country), await remove_tildes(countryList[key]), re.IGNORECASE)
            if countryTrue: break
        if countryTrue:
            if message.from_user.username:
                if await register_user(fullname, country, phone, email, username, invite, trader, update):
                    await kaino.reply_to(message, f"✎ ¡Su usuario ha sido registrado con exito! Para seguir con su registro al 100% reacuerde usar /membership, para pagar su membresia, y /deriv para registrar su cuenta de MT5.")
                    await kaino.delete_state(message.from_user.id, message.chat.id)
                else:
                    await kaino.reply_to(message, f"✎ ¡No puede registrarse, su usuario ya existe en la base de datos..! ")
            else:
                await kaino.reply_to(message, existing_user_text)
        else:
            await kaino.reply_to(message, f"✎ ¡No puede registrarse, el país que puso no existe, por favor, vuelva a ponerlo!")
            await kaino.set_state(message.from_user.id, MyStates.country, message.chat.id)
