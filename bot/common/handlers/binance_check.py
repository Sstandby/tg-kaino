from bot import commands_IsBinance
from binance import AsyncClient
from bot.common.db.users import get_api_key, get_api_secret
from telebot.handler_backends import BaseMiddleware

class BinanceClient(BaseMiddleware):

    def __init__(self):
        self.update_types = ['message']

    async def pre_process(self, message, data):
        if message.text in commands_IsBinance:
            api_key = await get_api_key(message.from_user.username)
            api_secret = await get_api_secret(message.from_user.username)
            data['client'] = await AsyncClient.create(api_key, api_secret)

    async def post_process(self, message, data, exception=None):
        if exception:
            print(exception)
