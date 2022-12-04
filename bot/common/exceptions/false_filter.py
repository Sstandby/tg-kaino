from bot import kaino
from bot import commands_IsBinance, commands_private

isbinance_text = """
✎ No puedes usar este comando, por favor, usa /token para registrarte y usar los comandos de binance.
"""

@kaino.message_handler(binance_user=False, commands=commands_IsBinance)
async def not_is_binance(message):
    """
    Message when the user does not exist in the db registered for binance
    """
    await kaino.reply_to(message, isbinance_text)

@kaino.message_handler(commands=commands_private, chat_types=['group', 'supergroup'])
async def not_isbinance(message):
    """
    commands that do not require public use
    """
    await kaino.reply_to(message, isbinance_text)
