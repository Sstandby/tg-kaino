# -*- coding: utf-8 -*
from bot import kaino
from telebot.types import ReplyKeyboardMarkup
from telebot.asyncio_handler_backends import State, StatesGroup

start_text = """
╔══════════════════════╗
    ¡✩ Aqui kaino presentandose ✩!
   ❝ Recuerde seleccionar la opción
            que mas se ajusta a sus
                     necesidades. ❞
╚══════════════════════╝
"""

start_membership_text = """
Para un proceso limpio para su registro y el pago de la membresia, debe realizar los siguientes pasos 👇👇

📥 Registrar su cuenta en nuestra base de datos con /register
✍️ Una vez completado, registrar su cuenta de deriv y MT5 con /deriv
🪙 Como caso opcional, su cuenta de binance registrando sus APIS (Recuerde solamente poner uso de lectura) utilizando el comando /binance
"""

start_help_text = """
🚧  ¡¡En mantenimiento!! 🚧
"""

class MyStateInfo(StatesGroup):
    option = State()

@kaino.message_handler(commands=['start'])
async def start(message):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Selecciona alguna de las opciónes")
    markup.add("Membership","Help")
    await kaino.reply_to(message, start_text, parse_mode="html", reply_markup=markup)
    await kaino.set_state(message.from_user.id, MyStateInfo.option, message.chat.id)

@kaino.message_handler(state=MyStateInfo.option)
async def option_start(message):
    async with kaino.retrieve_data(message.from_user.id, message.chat.id) as data:
        option = message.text
        if option == "Membership":
           await kaino.reply_to(message, start_membership_text, parse_mode="html", disable_web_page_preview=True)
        elif option == "Help":
           await kaino.reply_to(message, start_help_text, parse_mode="html", disable_web_page_preview=True)
        else:
           await kaino.reply_to(message, "✩ Por favor seleccione una opción valida al usar /start ✩", parse_mode="html")
    await kaino.delete_state(message.from_user.id, message.chat.id)
