from bot import kaino
from telebot.handler_backends import BaseMiddleware

@kaino.message_handler(isBinance=True, commands=['money'])
async def start(message, data: dict):
    await kaino.reply_to(message, data['example'])
