from bot import kaino
from bot import commands_IsBinance, commands_private, commands_IsMembership

notExistingUser_text = """
✎ No puedes usar este comando, por favor, usa /register para registrar tu usuario en la base de datos y poder usar este comando.
"""

private_text = """
✎ Este comando es privado, por favor no lo uses en un chat publico por seguridad.
"""

membershipCommandTrue_text = """
✎ Si ya pago su membresia no es necesario realizar esta parte, por favor, disfrute de los demas comandos: /start
"""

membershipCommandFalse_text = """
✎ Para usar este comando debe pagar la membresia mediante el comando; /membership
"""


@kaino.message_handler(existing_user=False, commands=commands_IsBinance)
async def not_is_user(message):
    """
    Message when the user does not exist in the db registered for binance
    """
    await kaino.reply_to(message, notExistingUser_text)

@kaino.message_handler(membership=False, commands=commands_IsMembership)
async def membership_desactivated(message):
    """
    Message except if membership is desactivated
    """
    await kaino.reply_to(message, membershipCommandFalse_text)


@kaino.message_handler(membership=True, commands=['membership', 'accepting'])
async def membership_active(message):
    """
    Message except if membership is desactivated
    """
    await kaino.reply_to(message, membershipCommandTrue_text)

@kaino.message_handler(commands=commands_private, chat_types=['group', 'supergroup'])
async def private_chat(message):
    """
    commands that do not require public use
    """
    await kaino.reply_to(message, private_text)
